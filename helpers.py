import os
import pandas as pd

from datetime import date
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
        season = f"Spring {fw_start.year}"

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
            q_col[COUNTRY_CODES[country]] = CountryScores(
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