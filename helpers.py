import io
import os
import re
import numpy as np
import pandas as pd
import eurostat

from datetime import date, datetime, timedelta
from multiprocessing import get_context
from scipy import stats
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
    if fw_start > fw_end:  # fieldwork crossing New Year: the start is in the previous year
        fw_start = fw_start.replace(year=fw_start.year - 1)

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
    Parse excel dataset *fn* and extract *eb_number, wave_id, fieldwork_start,
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
    A row with only one date covers that date's whole period (month or year).
    """
    a = _parse_activity_date(row.activity_start, end=False) \
        or _parse_activity_date(row.activity_end, end=False)
    b = _parse_activity_date(row.activity_end, end=True) \
        or _parse_activity_date(row.activity_start, end=True)

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


def write_sheet(path: str, sheet: str, df: pd.DataFrame) -> bool:
    """
    Replace one sheet of an existing workbook, leaving the other sheets intact.
    Skips the write when the sheet's contents are unchanged, so a re-run does not touch the file.
    """
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    try:
        unchanged = pd.read_excel(buf).equals(pd.read_excel(path, sheet_name=sheet))
    except ValueError:  # sheet not in the workbook yet
        unchanged = False
    if unchanged:
        return False
    with pd.ExcelWriter(path, engine="openpyxl", mode="a",
                        if_sheet_exists="replace") as xl:
        df.to_excel(xl, sheet_name=sheet, index=False)
    return True


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


def _fe_design(d, fe, controls=()):
    """
    Nuisance design matrix: one-hot fixed effects plus any controls.
    """
    Z = [pd.get_dummies(d[f], prefix=f).astype(float).values for f in fe]
    if controls:
        Z.append(d[list(controls)].astype(float).values)
    return np.column_stack(Z)


def _annihilator(Z):
    """
    Residual-maker M = I - Z Z^+.
    """
    return np.eye(Z.shape[0]) - Z @ np.linalg.pinv(Z)


def _cluster_meat(xt, E, g, G):
    """
    Sum of squared cluster scores of the partialled-out regressor *xt*, one per
    column of *E*.
    """
    E = E[:, None] if E.ndim == 1 else E
    D = np.zeros((G, len(g))); D[g, np.arange(len(g))] = 1.
    return ((D @ (xt[:, None] * E)) ** 2).sum(0)


def _boot_t(xt, M, e_dgp, g, G, W, wg):
    """
    Bootstrap t-statistics for wild DGP disturbances e_dgp * W[wg], with the
    variance always clustered at *g*. Centred on whatever the DGP imposes, so
    the same expression serves restricted and unrestricted bootstraps.
    """
    xtxt = xt @ xt
    U = e_dgp[:, None] * W[wg]
    db = (xt @ U) / xtxt
    return db * xtxt / np.sqrt(_cluster_meat(xt, M @ U - xt[:, None] * db, g, G))


def _boot_pvals(t_obs, t_b):
    """
    Bootstrap p-values, (1 + #) / (B + 1): symmetric and equal-tailed two-sided,
    and one-sided against H1: beta > beta0 ("up") and H1: beta < beta0 ("lo").
    """
    B = len(t_b)
    up = (1 + np.sum(t_b >= t_obs)) / (B + 1)
    lo = (1 + np.sum(t_b <= t_obs)) / (B + 1)
    return {"p_sym": (1 + np.sum(np.abs(t_b) >= abs(t_obs))) / (B + 1),
            "p_eqt": min(1., 2 * min(up, lo)), "p_up": up, "p_lo": lo}


def wild_boot(panel, dv, test="exposure", controls=(), fe=("iso2", "wave_num"),
              cluster="iso2", beta0=0., restricted=True, level="cluster",
              B=9999, seed=0):
    """
    Wild bootstrap test of H0: coef(test) = beta0 with a cluster-robust t-statistic
    clustered by *cluster* (the CRV1 sandwich without its small-sample factor, which
    cancels in the bootstrap p-values; the returned t omits it too). restricted=True imposes the null in the DGP (WCR/WR);
    False uses unrestricted residuals (WCU/WU). level="cluster" draws one
    Rademacher weight per cluster (wild cluster bootstrap); level="obs" draws one
    per observation, the subcluster wild bootstrap at its finest level (MacKinnon
    and Webb 2018). Defaults reproduce wcr_wildboot exactly.
    Returns {beta, t, p_sym, p_eqt, p_up, p_lo}.
    """
    d = panel
    Z = _fe_design(d, fe, controls); M = _annihilator(Z)
    y = d[dv].to_numpy(float); x = d[test].to_numpy(float)
    g = pd.factorize(d[cluster])[0]; G = g.max() + 1
    xt = M @ x; xtxt = xt @ xt
    beta = (xt @ y) / xtxt
    e = M @ y - xt * beta
    t_obs = (beta - beta0) * xtxt / np.sqrt(_cluster_meat(xt, e, g, G)[0])
    e_dgp = M @ (y - beta0 * x) if restricted else e
    wg = g if level == "cluster" else np.arange(len(y))
    W = np.random.default_rng(seed).choice([-1., 1.], size=(wg.max() + 1, B))
    t_b = _boot_t(xt, M, e_dgp, g, G, W, wg)
    return {"beta": beta, "t": t_obs, **_boot_pvals(t_obs, t_b)}


def cluster_diagnostics(panel, dv, test="exposure", controls=(), fe=("iso2", "wave_num"),
                        cluster="iso2"):
    """
    Analytic inference and cluster heterogeneity for coef(test).
    CRV1 (pyfixest's convention: fixed effects nested in the clusters are not
    counted in k) and jackknife CV3 (MacKinnon, Nielsen and Webb 2023, eq. 18),
    both against t(G-1); each cluster's partial leverage (MNW eq. 39); the
    leave-one-cluster-out estimates; and the effective number of clusters G*(0)
    of Carter, Schnepel and Steigerwald (2017), the only version defined when the
    model has cluster fixed effects.
    """
    d = panel
    Z = _fe_design(d, fe, controls); M = _annihilator(Z)
    y = d[dv].to_numpy(float); x = d[test].to_numpy(float)
    g, names = pd.factorize(d[cluster]); G = len(names); N = len(y)
    xt = M @ x; xtxt = xt @ xt
    beta = (xt @ y) / xtxt
    e = M @ y - xt * beta
    k = np.linalg.matrix_rank(Z) + 1 - (G - 1 if cluster in fe else 0)
    se1 = np.sqrt(G / (G - 1) * (N - 1) / (N - k) * _cluster_meat(xt, e, g, G)[0]) / xtxt

    loo = np.empty(G)
    for h in range(G):
        xh = _annihilator(Z[g != h]) @ x[g != h]
        loo[h] = (xh @ y[g != h]) / (xh @ xh)
    se3 = np.sqrt((G - 1) / G * np.sum((loo - beta) ** 2))

    lev = np.bincount(g, weights=xt ** 2, minlength=G) / xtxt
    p = lambda t: 2 * stats.t.sf(abs(t), G - 1)
    return {"beta": beta, "se_crv1": se1, "p_crv1": p(beta / se1),
            "se_cv3": se3, "p_cv3": p(beta / se3),
            "g_star": G / (1 + np.mean((lev - lev.mean()) ** 2) / lev.mean() ** 2),
            "leverage": pd.Series(lev, index=names), "loo": pd.Series(loo, index=names)}


def exposure_trajectories(panel, test="exposure", exclude=()):
    """
    Exposure paths (one row per country, one column per wave) of the countries whose exposure varies,
    minus any in *exclude*.
    """
    pv = panel.pivot(index="iso2", columns="wave_num", values=test)
    return pv[pv.nunique(axis=1) > 1].drop(index=list(exclude)).to_numpy(float)


def _placebo_prep(d, controls):
    """
    Everything a placebo draw needs that does not depend on the placebo regressor.
    """
    g = pd.factorize(d["cl"])[0]; G = g.max() + 1
    Z = _fe_design(d, ("cl", "wave_num"), controls)
    return {"g": g, "G": G, "M": _annihilator(Z),
            "Mh": [_annihilator(Z[g != h]) for h in range(G)],
            "k": np.linalg.matrix_rank(Z) + 1 - (G - 1)}


def _placebo_tests(y, x, P, Wc, Wo):
    """
    p-values for one placebo regressor under every method.
    """
    g, G, M = P["g"], P["G"], P["M"]; N = len(y)
    xt = M @ x; xtxt = xt @ xt
    beta = (xt @ y) / xtxt
    e = M @ y - xt * beta
    t = beta * xtxt / np.sqrt(_cluster_meat(xt, e, g, G)[0])
    loo = np.empty(G)
    for h in range(G):
        xh = P["Mh"][h] @ x[g != h]
        loo[h] = (xh @ y[g != h]) / (xh @ xh)

    out = {}
    for m, tm in (("CRV1", t / np.sqrt(G / (G - 1) * (N - 1) / (N - P["k"]))),
                  ("CV3", beta / np.sqrt((G - 1) / G * np.sum((loo - beta) ** 2)))):
        out.update({f"{m}_p_sym": 2 * stats.t.sf(abs(tm), G - 1),
                    f"{m}_p_up": stats.t.sf(tm, G - 1), f"{m}_p_lo": stats.t.cdf(tm, G - 1)})
    e_r, obs = M @ y, np.arange(N)
    for m, e_dgp, W, wg in (("WCR", e_r, Wc, g), ("WCU", e, Wc, g),
                            ("WR", e_r, Wo, obs), ("WU", e, Wo, obs)):
        out.update({f"{m}_{k}": v for k, v in
                    _boot_pvals(t, _boot_t(xt, M, e_dgp, g, G, W, wg)).items()})
    return out


def _placebo_chunk(args):
    """
    One worker's share of placebo_sim.
    """
    panel, traj, outcomes, specs, resample, draws, B, seed = args
    rng = np.random.default_rng(seed)
    base = panel.assign(cl=pd.factorize(panel["iso2"])[0])
    fixed = None if resample else {s: _placebo_prep(base, c) for s, c in specs.items()}
    countries = panel["iso2"].unique()
    rows = []
    for r in range(draws):
        if resample:
            pick = rng.integers(0, len(countries), len(countries))
            d = pd.concat([panel[panel["iso2"] == countries[j]].assign(cl=i)
                           for i, j in enumerate(pick)], ignore_index=True)
            P = {s: _placebo_prep(d, c) for s, c in specs.items()}
        else:
            assert fixed is not None  # built above whenever resample is False
            d, P = base, fixed
        G = d["cl"].nunique()
        tab = np.zeros((G, traj.shape[1]))
        tab[rng.choice(G, size=len(traj), replace=False)] = traj[rng.permutation(len(traj))]
        x = tab[pd.factorize(d["cl"])[0], d["wave_num"].to_numpy() - 1]
        Wc = rng.choice([-1., 1.], size=(G, B))
        Wo = rng.choice([-1., 1.], size=(len(d), B))
        for dv in outcomes:
            y = d[dv].to_numpy(float)
            for s in specs:
                rows.append({"draw": r, "outcome": dv, "spec": s,
                             **_placebo_tests(y, x, P[s], Wc, Wo)})
    return rows


_BLAS_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS")


def placebo_sim(panel, traj, outcomes, specs, resample=False, draws=4002, B=999,
                chunks=6, seed=0, workers=None):
    """
    Placebo-treatment rejection-rate simulation (Bertrand, Duflo and Mullainathan
    2004). Each draw hands the rows of *traj* (real exposure paths) to randomly
    chosen countries, gives every other country 0, and tests the placebo
    coefficient with CRV1 and CV3 t(G-1) tests and the WCR, WCU, WR and WU
    bootstraps (B draws each). resample=True first resamples whole country
    histories with replacement, removing the conditioning on one realised
    dataset. Work is split into *chunks* seeded seed + i, so results do not
    depend on the number of worker processes. Each chunk runs ceil(draws / chunks)
    draws, so the total is rounded up to a multiple of *chunks*.
    """
    per = -(-draws // chunks)
    jobs = [(panel, traj, outcomes, specs, resample, per, B, seed + i) for i in range(chunks)]
    saved = {v: os.environ.get(v) for v in _BLAS_VARS}
    os.environ.update({v: "1" for v in _BLAS_VARS})  # one BLAS thread per worker
    try:
        with get_context("spawn").Pool(workers or min(chunks, os.cpu_count() or 1)) as pool:
            out = pool.map(_placebo_chunk, jobs)
    finally:
        for v, val in saved.items():
            if val is None:
                os.environ.pop(v, None)
            else:
                os.environ[v] = val
    return pd.DataFrame([{"chunk": i, **r} for i, rows in enumerate(out) for r in rows])


def rejection_rates(sims, methods=("CRV1", "CV3", "WCR", "WCU", "WR", "WU")):
    """
    Rejection rates (%) of placebo_sim output per outcome, spec and method:
    two-sided at 5% and 10%, equal-tailed at 10% (what a 90% test-inversion CI
    uses; the symmetric test for the analytic methods), and one-sided at 5% in
    each direction (the two halves of TOST).
    """
    rows = []
    for (dv, s), d in sims.groupby(["outcome", "spec"], sort=False):
        for m in methods:
            eqt = d[f"{m}_p_eqt"] if f"{m}_p_eqt" in d else d[f"{m}_p_sym"]
            rows.append({"outcome": dv, "spec": s, "method": m, "draws": len(d),
                         "two-sided 5%": 100 * np.mean(d[f"{m}_p_sym"] <= .05),
                         "two-sided 10%": 100 * np.mean(d[f"{m}_p_sym"] <= .10),
                         "equal-tailed 10%": 100 * np.mean(eqt <= .10),
                         "one-sided up 5%": 100 * np.mean(d[f"{m}_p_up"] <= .05),
                         "one-sided lo 5%": 100 * np.mean(d[f"{m}_p_lo"] <= .05)})
    return pd.DataFrame(rows)

def boot_ci(panel, dv, conf=0.90, test="exposure", controls=(), tol=1e-4, **kw):
    """
    Equal-tailed confidence interval for coef(test) by inverting wild_boot: the
    beta0 at which neither one-sided p-value is at or below (1 - conf) / 2. Every
    beta0 reuses the same draws (same seed). Each endpoint is bracketed by
    stepping outward from the estimate, then bisected to *tol*. Extra keywords
    (B, seed, level, restricted, ...) pass through to wild_boot.
    """
    a = round((1 - conf) / 2, 12)  # exactly 0.05, so p == a rejects
    p = lambda b0, side: wild_boot(panel, dv, test, controls, beta0=b0, **kw)[side]
    beta = wild_boot(panel, dv, test, controls, **{**kw, "B": 1})["beta"]
    step = max(abs(beta), 1.) / 2

    def edge(side, sign):
        inside, out = beta, beta + sign * step
        while p(out, side) > a:
            inside, out = out, out + sign * step
            if abs(out - beta) > 500 * step:
                return sign * np.inf
        while abs(out - inside) > tol:
            mid = (inside + out) / 2
            inside, out = (mid, out) if p(mid, side) > a else (inside, mid)
        return (inside + out) / 2

    return edge("p_up", -1), edge("p_lo", +1)


def tost(panel, dv, delta, test="exposure", controls=(), **kw):
    """
    Two one-sided wild bootstrap tests of H0: beta <= -delta and H0: beta >= +delta,
    each imposing its boundary in the DGP. p_tost <= alpha is equivalent to the
    (1 - 2 alpha) equal-tailed boot_ci lying inside +-delta.
    """
    lo = wild_boot(panel, dv, test, controls, beta0=-delta, **kw)["p_up"]
    hi = wild_boot(panel, dv, test, controls, beta0=+delta, **kw)["p_lo"]
    return {"p_lower": lo, "p_upper": hi, "p_tost": max(lo, hi)}


def mde(ci95, G, power=0.80):
    """
    Minimum detectable effect at *power* from a 95% interval: its half-width
    converted to an implied SE with t(.975, G-1), times t(.975) + t(power).
    """
    t975 = stats.t.ppf(.975, G - 1)
    return (t975 + stats.t.ppf(power, G - 1)) * (ci95[1] - ci95[0]) / (2 * t975)


def twfe_weights(panel, test="exposure", controls=(), fe=("iso2", "wave_num")):
    """
    de Chaisemartin and D'Haultfoeuille (2020) weights of the two-way fixed
    effects coefficient on an ordered treatment: eps * D over the treated cells,
    normalised to sum to 1, where eps is the residual of D on the fixed effects
    (and controls). beta_fe = sum(w * per-unit cell effects). Returns a Series
    indexed like *panel*'s treated rows.
    """
    D = panel[test].to_numpy(float)
    eps = _annihilator(_fe_design(panel, fe, controls)) @ D
    tr = D != 0
    return pd.Series(eps[tr] * D[tr] / np.sum(eps[tr] * D[tr]), index=panel.index[tr])


def dcdh_sigma(beta, w, d):
    """
    The two robustness measures of de Chaisemartin and D'Haultfoeuille (2020,
    Corollary 1) for an ordered treatment (online appendix, Section 3.2): treated
    cells are weighted by their treatment level *d* (N_gt D_gt with one observation
    per cell), and the weights are w / share. Returns the smallest SD of the per-unit
    cell effects compatible with an average effect of zero, |beta| / sigma(w), and,
    if some weights are negative, the smallest SD compatible with every cell effect
    having the opposite sign to beta (nan when all weights are positive).
    """
    w = np.asarray(w, float); d = np.asarray(d, float)
    share = d / d.sum()
    order = np.argsort(-(w / share), kind="stable")  # descending in the weights
    om, share = (w / share)[order], share[order]       # share-weighted mean 1
    sd = np.sqrt(np.sum(share * (om - 1) ** 2))
    P = share[::-1].cumsum()[::-1]                    # P_k = sum_{i>=k} share_i
    S = (share * om)[::-1].cumsum()[::-1]
    T = (share * om ** 2)[::-1].cumsum()[::-1]
    n = len(om)
    k = np.arange(1, n)                               # P_1 = 1: the condition starts at k = 2
    hit = k[om[k] < -S[k] / (1 - P[k])]
    if not len(hit):
        return abs(beta) / sd, np.nan
    s = hit[0]
    return abs(beta) / sd, abs(beta) / np.sqrt(T[s] + S[s] ** 2 / (1 - P[s]))


def did_m(panel, dv, test="exposure", group="iso2", time="wave_num"):
    """
    DID_M of de Chaisemartin and D'Haultfoeuille (2020) per unit of an ordered
    treatment. Each group whose treatment changes between consecutive periods is
    compared with the groups that stayed at its starting level: its outcome change
    minus the stayers' mean change, signed by the direction of the switch, summed
    and divided by the total absolute change. Switches with no stayer at the
    starting level are skipped. Returns the estimate and the joiners' (increase)
    and leavers' (decrease) components, with switch counts.
    """
    Y = panel.pivot(index=group, columns=time, values=dv).to_numpy(float)
    D = panel.pivot(index=group, columns=time, values=test).to_numpy(float)
    num = {1: 0., -1: 0.}; den = {1: 0., -1: 0.}; cnt = {1: 0, -1: 0}; skipped = 0
    for t in range(1, D.shape[1]):
        dD, dY = D[:, t] - D[:, t - 1], Y[:, t] - Y[:, t - 1]
        for g in np.nonzero(dD)[0]:
            stay = (D[:, t - 1] == D[g, t - 1]) & (dD == 0)
            if not stay.any():
                skipped += 1
                continue
            sg = int(np.sign(dD[g]))
            num[sg] += sg * (dY[g] - dY[stay].mean()); den[sg] += abs(dD[g]); cnt[sg] += 1
    tot = den[1] + den[-1]
    return {"beta": (num[1] + num[-1]) / tot if tot else np.nan,
            "joiners": num[1] / den[1] if den[1] else np.nan,
            "leavers": num[-1] / den[-1] if den[-1] else np.nan,
            "n_join": cnt[1], "n_leave": cnt[-1], "n_skipped": skipped}


def did_m_inference(panel, dv, test="exposure", group="iso2", time="wave_num",
                    B=999, perms=4002, conf=0.90, seed=0):
    """
    Indicative inference for did_m: percentile intervals (for the estimate and the
    joiners' and leavers' components) from resampling whole groups with
    replacement, with draws lacking a usable switch dropped and counted, and a
    two-sided permutation p-value for the estimate that reassigns the groups' real
    treatment paths at random, holding the outcomes fixed.
    """
    rng = np.random.default_rng(seed)
    est = did_m(panel, dv, test, group, time)
    gs = np.sort(panel[group].unique())               # row order must not matter
    by = {g: d for g, d in panel.groupby(group)}
    parts = ("beta", "joiners", "leavers")
    boots = {k: [] for k in parts}
    for _ in range(B):
        pick = rng.choice(gs, len(gs))
        d = pd.concat([by[g].assign(**{group: i}) for i, g in enumerate(pick)], ignore_index=True)
        r = did_m(d, dv, test, group, time)
        for k in parts:
            boots[k].append(r[k])
    a = (1 - conf) / 2
    out = {**est}
    for k in parts:
        b = np.array(boots[k]); ok = ~np.isnan(b)
        out.update({f"{k}_lo": np.quantile(b[ok], a), f"{k}_hi": np.quantile(b[ok], 1 - a),
                    f"{k}_dropped": int((~ok).sum())})
    paths = panel.pivot(index=group, columns=time, values=test)
    perm = []
    for _ in range(perms):
        sh = pd.DataFrame(paths.to_numpy()[rng.permutation(len(paths))],
                          index=paths.index, columns=paths.columns)
        d = panel.drop(columns=test).merge(
            sh.reset_index().melt(id_vars=group, var_name=time, value_name=test), on=[group, time])
        perm.append(did_m(d, dv, test, group, time)["beta"])
    perm = np.array(perm); perm = perm[~np.isnan(perm)]
    out["p_perm"] = (1 + np.sum(np.abs(perm) >= abs(est["beta"]))) / (len(perm) + 1)
    return out
