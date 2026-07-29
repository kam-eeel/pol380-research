# Definitions

- **Exposure**: measures the documented intensity of Operation Doppelgänger activity directed at a given country's public during a given observation window, as established by forensic and legal sources.
- **It is not**: audience reach, impressions, engagement, or individual-level exposure. It is a measure of campaign activity aimed at a country, not consumption of that activity by that country's residents.
- **Unit of Observation**: country × wave
- **Sample**: EU-27 only.
- **Scale**: Ordinal 0-3.

---

# Observation Window

For wave _w_, the observation window runs from the fieldwork end date of wave _w-1_ to the fieldwork end date of wave _w_.
Outcome is an attitude measured during wave _w_ fieldwork and would represent the result of all exposure accumulated since the end of wave _w-1_ fieldwork.
Fieldwork windows are 3-4 weeks long and forensic reporting is rarely dated to that resolution. Coding on these windows alone would produce near-uniform zeros and eliminate the within-country variation the design is identified from.
_Special case for Wave 1_: As no prior wave exists, the window will run from February 24, 2022 (start of invasion and campaign's onset) to the end of wave 1's fieldwork. This is a slightly shorter window than the others.

| wave_num | wave_id | Window Start | Window End |
| -------- | ------- | ------------ | ---------- |
| 1        | 97.5    | 2022-02-24   | 2022-07-17 |
| 2        | 98.2    | 2022-07-17   | 2023-02-06 |
| 3        | 99.4    | 2023-02-06   | 2023-06-25 |
| 4        | 100.2   | 2023-06-25   | 2023-11-17 |
| 5        | 101.3   | 2023-11-17   | 2024-05-09 |
| 6        | 102.2   | 2024-05-09   | 2024-11-05 |
| 7        | 103.3   | 2024-11-05   | 2025-04-22 |
| 8        | 104.1   | 2025-04-22   | 2025-11-05 |
| 9        | 105.2   | 2025-11-05   | 2026-04-05 |

---

# Criteria

## A – Named country-level targeting

The country is identified by name as a target of Doppelgänger (or its documented aliases: *RRN / Recent Reliable News*, *Ruza Flood*, *Storm-1099*) for a period overlapping the observation window.
Not met by: appearance in an aggregate EU-wide count with no country attribution; appearance solely as the registrar/host/infrastructure location rather than the target audience.

## B – Dedicated cloned infrastructure

At least one spoofed domain, cloned site, or impersonated brand belonging to that country's media outlets, government bodies, or institutions is documented as registered or active during the window.
Not met by: generic pseudo-outlets with no national referent; domains impersonating a different country's brands even if hosted or promoted in this one.

## C – Language localization

Campaign content in the country's national language(s) is documented: articles, cartoons, memes, sock-puppet posts, or paid amplification.
Not met by: English-language content unless English is a national language of the country.

## D – Independent corroboration

Criterion A is met by ≥2 independent sources.

---

# Source Independence

Two sources are independent only if they rest on separate evidentiary bases. They are not independent if one:

- cites the other as the origin of the country attribution;
- reprints, translates, or summarizes the other's findings;
- shares an author, sponsoring body, or dataset with the other.

---

# Tier Assignment

| Tier | Label                    | Rule                                                           |
| ---- | ------------------------ | -------------------------------------------------------------- |
| 3    | Primary Sustained Target | A, B, C all met and D met                                      |
| 2    | Secondary target         | A met, plus ≥ 1 of B or C, and D; <br>or A, B, and C but not D |
| 1    | Marginal / incidental    | A met, none of B, C, or D                                      |
| 0    | No documented activity   | A not met                                                      |

---

# Register Scope

The primary register contains only sources whose own primary research attributes activity to Operation Doppelgänger or a documented alias (RRN/Recent Reliable News, Ruza Flood, Storm-1099). Sources documenting allied but forensically distinct pro-Kremlin operations (Portal Kombat/Pravda; Matryoshka/Operation Overload) form an extended register, used only in robustness check R5.

---

# Decision Rules

- **R1 — Date-range spanning.** A source documenting activity across a range crossing multiple windows generates a code in _every_ window the range overlaps. Overlap of any length counts.
- **R2 — No carry-forward by default.** Infrastructure documented as active in window _t_ does **not** carry into _t_+1 unless a source affirmatively states it remained active, or a source in _t_+1 re-documents it. Absent that, code _t_+1 on its own evidence and set `ambiguous = 1`.
- **R3 — Documented takedown.** If a platform, registrar, or sanctions action removing infrastructure is documented, do not code that infrastructure as active in subsequent windows.
- **R4 — Undated documentation.** A country documented as targeted with no usable time information receives **0** in every specific window and `ambiguous = 1`.
- **R5 — Aggregate-only evidence.** Counts or claims stated at EU or multi-country level without country attribution do not satisfy criterion A and do not raise any country's tier. Record in notes.
- **R6 — Source conflict.** If two sources imply different tiers for the same country-window, take the **higher** and set `ambiguous = 1`.
- **R7 — Criteria met by different sources.** Criteria A, B, and C may each be satisfied by different sources within the same window; they need not co-occur in one document.
- **R8 — Out-of-sample targets.** Documented targeting of non-EU-27 states does not generate rows and does not raise any EU-27 country's tier, even where the campaign infrastructure is shared.
- **R9 — Closed source register.** Only sources listed in the frozen source register may be used. If a genuinely new and important source surfaces mid-coding, amend the register, log it, and **re-check every previously coded cell that source could speak to**.
- **R10 — Absence of evidence.** A 0 means _no documented activity in the frozen source register for this window_. It does not mean no activity occurred.
- **R11 — Ceiling / no-variation flag.** If a country would receive an identical tier in all eight windows, flag it. Under country fixed effects it contributes nothing to identification.
- **R12 — Evidence recording.** Every non-zero cell records its establishing sources mechanically from the register (evidence\_\*\_source, criteria_met, notes). Page-level locators are maintained at the register level (one row per source), not per cell.
