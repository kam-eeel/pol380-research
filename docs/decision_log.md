# Eurobarometer Volume Choice

Eurobarometer data sets are provided in a number of volumes (A/AA/AP/AAP/B/BP/C/D), each of which provides a different degree of resolution/type of comparison for the results. For our analysis, volume A is the most relevant as it directly provides country-level results. All other volumes look at either groups of countries, trends over time, and results broken down by socio-demographics. Since country and wave fixed effects absorb time-invariant national traits and demographic composition, only the outcome variable at the country level is needed.

# Exposure — Criterion D (Independence)

Criterion D (criterion A corroborated by two or more independent sources) is computed programmatically rather than hand-logged. A, B, and C are recorded per source in the register; D is derived for each country-window as the presence of at least two distinct authors among the sources that establish A there.
At data entry, every date and country attribution in the register was taken only from the portion of a source reporting its own primary research, never from background sections or passages discussing other investigations. A logged attribution is therefore never a cited, reprinted, or reused one, so the sources establishing A for a given cell are independent evidentiary bases by construction. The cluster of late-September 2022 disclosures surrounding Meta's takedown announcement (EU DisinfoLab, DFRLab, Meta, and the Institute for Strategic Dialogue) accordingly counts as four independent sources, not one: each conducted its own investigation and only its own findings were logged. The single sponsor overlap in the register — the Federal Foreign Office and the Bavarian Office for the Protection of the Constitution, both German state bodies — affects no coded cell, since the former is Germany-only and the latter's attributed countries are each corroborated by other authors.

# Exposure — Tier Assignment Gap (A with partial evidence, no corroboration)

The codebook's tier table does not explicitly cover three combinations in which criterion A is met but the remaining criteria are only partly present: A with B alone, A with C alone, and A with D alone. These satisfy neither tier-2 rule (which requires corroboration paired with at least one content criterion, or both content criteria together) nor the tier-1 rule as literally written ("A met, none of B, C, or D"). Such cells are assigned tier 1.
The rationale derived from the general logic of the table: A gates any positive score, tier 2 ("secondary target") is reserved for a country showing either corroborated content activity or the full B-and-C content pair, and tier 3 for the complete A-B-C-D profile. A single uncorroborated signal — one content criterion without corroboration, or bare corroboration of naming with no documented content — does not clear the tier-2 bar and remains marginal or incidental.

# Exposure — Analysis Window Truncation

The panel is truncated to windows 1 through 7 (Eurobarometer 97.5 through 103.3), despite the collected Eurobarometer data extending through window 9 (105.2). Forensic activity for any country during windows 8 and 9 could not be found during the research – the time period for which was constrained further than initially expected. Per decision rule R10, a 0 in the exposure index means "no documented activity in the frozen register for this window," not "no activity occurred." Coding windows 8 and 9 as zeros would therefore not measure a decline in exposure; it would inject a block of artefactual zeros reflecting reporting lag, misrepresenting the campaign as having ceased and distorting any within-country trajectory ending in those windows.

# DV — Normalization

The two outcome variables, support_aid and support_sanctions, are operationalized as total_agree ("Tout à fait d'accord" plus "Plutôt d'accord") as reported in Volume A, with "don't know" kept in the denominator. The renormalized alternative, support as a share of valid opinion-holders (agree over agree-plus-disagree), is retained only as a robustness specification.

The choice follows from the mechanism under study. Doppelgänger-style influence operations do not act solely by converting agreement into disagreement; a substantial part of their documented effect is the manufacture of doubt and the demobilization of settled opinion, moving respondents from a committed position into "don't know." For the research question — whether campaign activity erodes public support — erosion achieved by demobilization is erosion, and the as-reported measure registers it as such: an agreer who becomes a don't-know lowers total_agree. Renormalization partially removes this channel, because a respondent leaving agreement for don't-know exits both the numerator and the denominator, so the ratio moves less than underlying support actually did.

The standard motivation for renormalizing — netting out cross-national differences in don't-know propensity, whether from political culture, survey translation, or item salience — does not apply strongly here, because the two-way fixed effects design already absorbs it. Country fixed effects remove any time-invariant national tendency toward non-response, and wave fixed effects remove common shocks to it. The confound that renormalization is meant to address is therefore already handled by the estimator, which inverts the trade-off: in this design renormalization mainly sacrifices within-country signal rather than removing bias.

The as-reported measure is also the more interpretable and defensible quantity. It is the
standard Eurobarometer topline, so a coefficient reads directly as the change in
percentage-point support associated with a one-tier change in exposure, matching how these
figures are publicly reported. The renormalized version estimates support conditional on
holding an opinion, which is both more awkward to state and less standard.

The honest limitation is that the as-reported measure conflates persuasion (agree to disagree) with demobilization (agree to don't-know). Because the research question does not require separating these channels, this is acceptable, and two checks guard against the concern: the renormalized DV is run as a robustness column to confirm the result is not an artefact of the denominator choice, and the don't-know share may be modelled as a secondary outcome. A finding that exposure simultaneously raises the don't-know share and lowers support would evidence the demobilization channel directly rather than leaving it asserted.
