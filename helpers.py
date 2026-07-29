import os
import re
import numpy as np
import pandas as pd
import eurostat

from datetime import date, datetime, timedelta
from typing import TypedDict

class DocOutput(TypedDict):
    eb_n: str
    wave_id: float
    fw_start: date
    fw_end: date
    season: str
    questions: list[str]
    q_ids: list[str]

class CountryScores(TypedDict):
    total: int
    total_agree: int
    total_disagree: int
    totally_agree: int
    tend_to_agree: int
    dont_know: int
    tend_to_disagree: int
    totally_disagree: int

class SourceRecord(TypedDict):
    s_id: str
    author: str
    window: tuple[date | None, date | None]
    countries: dict[str, set[str]]

class CellCode(TypedDict):
    exposure: int
    criteria_met: str
    n_sources_A: int
    n_indep_A: int
    evidence_sources: str
    notes: str

EB_BASE_PATH = "data/raw/"

COUNTRY_CODES = {
    "BE": "Belgium",
    "BG": "Bulgaria",
    "CZ": "Czechia",
    "DK": "Denmark",
    "DE": "Germany",
    "EE": "Estonia",
    "IE": "Ireland",
    "EL": "Greece",
    "ES": "Spain",
    "FR": "France",
    "HR": "Croatia",
    "IT": "Italy",
    "CY": "Cyprus",
    "LV": "Latvia",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "HU": "Hungary",
    "MT": "Malta",
    "NL": "Netherlands",
    "AT": "Austria",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "SI": "Slovenia",
    "SK": "Slovakia",
    "FI": "Finland",
    "SE": "Sweden"
}

CRITERIA = ("A", "B", "C", "D")


def check_q(q: str) -> bool:
    """
    Return true iff *q* is a relevant question to the research project.
    A question is relevant if it asks about providing military aid to Ukraine
    or imposing economic sanctions on Russia.
    """
    q = q.lower()

    return (
        ("ukraine" in q and "military" in q)
        or
        ("russia" in q and "sanction" in q)
    )


def _parse_dates(ds: str) -> tuple[date, date, str]:
    """
    Convert Eurobarometer date strings to separate start/end date objects.
    Assumes date strings are formatted as "DD/MM - DD/MM/YYYY".
    Returns a tuple: (*fw_start, fw_end, season*).
    """
    start = ds.split("-")[0].strip() + ds[-5:]
    end = ds.split("-")[-1].strip()
    fw_start = date(*[int(v) for v in start.split("/")[::-1]])
    fw_end = date(*[int(v) for v in end.split("/")[::-1]])

    if any(m == fw_start.month for m in [3, 4, 5]):
        season = f"Spring {fw_start.year}"
    elif any(m == fw_start.month for m in [6, 7, 8]):
        season = f"Summer {fw_start.year}"
    elif any(m == fw_start.month for m in [9, 10, 11]):
        season = f"Fall {fw_start.year}"
    elif any(m == fw_start.month for m in [12, 1, 2]):
        season = f"Winter {fw_start.year}"

    return (fw_start, fw_end, season)


def parse_doc(fn: str) -> DocOutput:
    """
    Parse excel dataset *fp* and extract *eb_number, wave_id, fieldwork_start,
    fieldwork_end, season*, and all questions relevant to the research project.
    """
    df = pd.read_excel(f"{EB_BASE_PATH}{fn}")
    eb_n = fn.split("_")[0]
    wave_id = float(df.iat[0, 1])  # type: ignore[arg-type]
    fw_start, fw_end, season = _parse_dates(str(df.iat[1, 1]))
    col_qs, col_ids = [], []

    for question in df["Unnamed: 2"][4:].dropna():
        q_n: str = question.split(". ", 1)[0]
        if check_q(question):
            col_qs.append(question)
            col_ids.append(q_n.replace(".", "_"))

    return DocOutput(
        eb_n=eb_n,
        wave_id=wave_id,
        fw_start=fw_start,
        fw_end=fw_end,
        season=season,
        questions=col_qs,
        q_ids=col_ids
    )


def collect_scores(wave: str, q_ids: list[str]) -> dict[str, dict[str, int]]:
    """
    Collect per-country responses to questions with question numbers *q_ids*
    in Eurobarometer wave *wave*.
    """
    collected = {}

    df = pd.read_excel(
        f"{EB_BASE_PATH}{wave}_volume_A.xlsx",
        sheet_name=None,
        header=7,
    )

    for q in q_ids:
        q_col = {}

        sdf = df[q].dropna(how="all")
        sdf = sdf.drop(sdf.columns[0], axis=1)
        countries = sdf.iloc[0][2:].to_list()
        sdf.columns = ["Score", "EU27"] + countries

        for country in countries:
            if country not in COUNTRY_CODES:
                # Skip surveyed countries that are not EU member states and
                # regional divisions absorbed by fixed effects.
                continue
            cdf = sdf.set_index("Score")[country]
            q_col[country] = CountryScores(
                total=cdf.at["Total"],
                total_agree=cdf.at["Total 'D'accord'"],
                total_disagree=cdf.at["Total 'Pas d'accord'"],
                totally_agree=cdf.at["Tout à fait d'accord"],
                tend_to_agree=cdf.at["Plutôt d'accord"],
                dont_know=cdf.at["Ne sait pas"],
                tend_to_disagree=cdf.at["Plutôt pas d'accord"],
                totally_disagree=cdf.at["Pas du tout d'accord"]
            )

        collected[q] = q_col

    return collected


def parse_country_codes(raw: str) -> dict[str, set[str]]:
    """
    Parse the register's 'countries' field into {iso2: {criteria letters}}.
    """
    out: dict[str, set[str]] = {}

    for tok in str(raw).split(";"):
        tok = tok.strip().replace(":", "")
        m = re.match(r"^([A-Z]{2})\s+([A-C]+)$", tok)

        if m:
            out[m.group(1)] = set(m.group(2))

    return out


def _parse_activity_date(s: str, *, end: bool) -> date | None:
    """
    Parse a register activity date given as YYYY, YYYY-MM, or YYYY-MM-DD.
    Activity windows are treated as inclusive of the whole period reported.
    """
    s = str(s).strip()

    for fmt, has_month, has_day in (("%Y-%m-%d", True, True),
                                    ("%Y-%m", True, False),
                                    ("%Y", False, False)):
        try:
            d = datetime.strptime(s, fmt).date()
        except ValueError:
            continue

        if end:
            if not has_month:
                return date(d.year, 12, 31)
            if not has_day:
                nxt = date(d.year + (d.month == 12), (d.month % 12) + 1, 1)
                return nxt - timedelta(days=1)

        return d

    return None


def source_window(row) -> tuple[date | None, date | None]:
    """
    Return (start, end) dates for a register row, or (None, None) if undated.
    """
    a = _parse_activity_date(row.activity_start, end=False) \
        or _parse_activity_date(row.activity_end, end=True)
    b = _parse_activity_date(row.activity_end, end=True) \
        or _parse_activity_date(row.activity_start, end=False)

    return (a, b) if (a and b) else (None, None)


def load_sources(register: pd.DataFrame) -> list[SourceRecord]:
    """
    Pre-parse the source register.
    """
    return [SourceRecord(s_id=r.source_id,  # type: ignore[arg-type]
                         author=r.author,  # type: ignore[arg-type]
                         window=source_window(r),
                         countries=parse_country_codes(r.countries))  # type: ignore[arg-type]
            for r in register.itertuples()]


def assign_tier(A: bool, B: bool, C: bool, D: bool) -> int:
    """
    Codebook Tier Assignment.

    Tier 3: A, B, C, and D all met.
    Tier 2: A and D and (B or C);  or A and B and C without D.
    Tier 1: A met but no tier-2/3 combination.
    Tier 0: A not met.
    """
    if not A:
        return 0
    if A and B and C and D:
        return 3
    if A and D and (B or C):
        return 2
    if A and B and C and not D:
        return 2
    return 1


def code_country_window(iso2: str, w_start: date, w_end: date,
                        sources: list[SourceRecord]) -> CellCode:
    """
    Assign the exposure tier for one country-window from the register.
    """
    a_sids: list[str] = []
    a_authors: set[str] = set()
    b_sids: list[str] = []
    c_sids: list[str] = []
    for s in sources:
        a, b = s["window"]
        if not (a and b and a <= w_end and b >= w_start):     # R1 overlap
            continue
        letters = s["countries"].get(iso2)
        if not letters:
            continue
        if "A" in letters:
            a_sids.append(s["s_id"]); a_authors.add(s["author"])
        if "B" in letters:
            b_sids.append(s["s_id"])
        if "C" in letters:
            c_sids.append(s["s_id"])

    A, B, C = bool(a_sids), bool(b_sids), bool(c_sids)
    D = len(a_authors) >= 2
    tier = assign_tier(A, B, C, D)

    note = " | ".join(f"{lbl}:{','.join(sorted(set(sids)))}"
                      for lbl, sids in (("A", a_sids), ("B", b_sids), ("C", c_sids))
                      if sids)

    return CellCode(exposure=tier,
                    criteria_met="".join(k for k, v in zip(CRITERIA, (A, B, C, D)) if v),
                    n_sources_A=len(a_sids),
                    n_indep_A=len(a_authors),
                    evidence_sources=";".join(sorted(a_sids)),
                    notes=note)


def eurostat_long(code, geos=None, dims=None, since=None):
    """
    Fetch a Eurostat dataset and return it tidy-long (dimension cols + geo, period,
    value).
    """
    df = eurostat.get_data_df(code)

    if df is None or df.empty:
        raise ValueError(f"No data for {code}")

    geo_col = next(c for c in df.columns if "geo" in c.lower())

    if geos is not None:
        df = df[df[geo_col].isin(geos)]

    if dims:
        for k, val in dims.items():
            if k in df.columns:
                df = df[df[k] == val]

    time_cols = [c for c in df.columns if str(c)[:4].isdigit()]
    id_cols   = [c for c in df.columns if c not in time_cols]
    long = (df.melt(id_vars=id_cols, value_vars=time_cols,
                    var_name="period", value_name="value")
              .rename(columns={geo_col: "geo"})
              .dropna(subset=["value"]))
    long["period"] = long["period"].astype(str)

    if since is not None:
        long = long[long["period"] >= since]

    return long


def wcr_wildboot(panel, dv, test="exposure", controls=(), fe=("iso2", "wave_num"),
                 cluster="iso2", B=9999, seed=0):
    """
    Wild cluster restricted bootstrap (Rademacher weights, Cameron-Gelbach-Miller 2008;
    Roodman et al. 2019) p-value for H0: coef(test) = 0.
    Imposes the null in the DGP and returns (beta, p_value).
    """
    d = panel
    Zparts = [pd.get_dummies(d[f], prefix=f).astype(float).values for f in fe]
    if controls:
        Zparts.append(d[list(controls)].astype(float).values)
    Z = np.column_stack(Zparts)
    y = d[dv].to_numpy(float); x = d[test].to_numpy(float)
    g = pd.factorize(d[cluster])[0]; G = g.max() + 1
    pinvZ = np.linalg.pinv(Z)
    resid = lambda V: V - Z @ (pinvZ @ V)
    xt = resid(x); xtxt = xt @ xt
    beta = (xt @ y) / xtxt
    e = resid(y) - xt * beta

    def meat(E):
        E = E[:, None] if E.ndim == 1 else E
        s = np.zeros((G, E.shape[1])); np.add.at(s, g, xt[:, None] * E)
        return (s ** 2).sum(0)

    t_obs = abs(beta) * xtxt / np.sqrt(meat(e)[0])
    u_r = y - Z @ (pinvZ @ y)
    W = np.random.default_rng(seed).choice([-1., 1.], size=(G, B))
    Ustar = u_r[:, None] * W[g]
    beta_b = (xt @ Ustar) / xtxt
    e_b = resid(Ustar) - xt[:, None] * beta_b
    t_b = np.abs(beta_b) * xtxt / np.sqrt(meat(e_b))
    return beta, (1 + np.sum(t_b >= t_obs)) / (B + 1)