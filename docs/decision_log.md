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

The limitation is that the as-reported measure conflates persuasion (agree to disagree) with demobilization (agree to don't-know). Because the research question does not require separating these channels, this is acceptable, and two checks guard against the concern: the renormalized DV is run as a robustness column to confirm the result is not an artefact of the denominator choice, and the don't-know share may be modelled as a secondary outcome. A finding that exposure simultaneously raises the don't-know share and lowers support would evidence the demobilization channel directly rather than leaving it asserted.

# Control — GDP per Capita (real)

Real GDP per capita controls for prosperity, which plausibly shapes both a country's attractiveness as a disinformation target and its public's willingness to bear the cost of aid and sanctions. Source: Eurostat nama_10_pc, item B1GQ, unit CLV20_EUR_HAB (chain-linked volumes, constant prices), matched by wave year — constant prices are used to avoid double-counting inflation.

# Control — Inflation (HICP)

Inflation is a live confounder in this window: cost-of-living pressure may turn publics against sanctions as self-harming, independently of disinformation exposure. Source: Eurostat prc_hicp_manr (annual rate of change).

# Control — Ukrainian Displaced-Population Share

The most direct confounder: hosting a large Ukrainian population raises war salience and solidarity while plausibly shifting exposure and receptivity to Russian narratives, so without it exposure could proxy involvement in the war. Constructed as temporary-protection beneficiaries (Eurostat migr_asytpsm, citizen UA) over population (demo_pjan) at the fieldwork-midpoint month.
Two caveats: it counts registered grants, not all Ukrainians present, and is structurally zero before March 2022 (so wave 1 reads ~0 by construction).

# Control — Population Denominator (shared)

Eurostat demo_pjan (1 January, sex T, age TOTAL) is the denominator for both the displaced share and the PSM per-capita moderator (2021). Using one population source keeps the two figures internally consistent.

# Controls — Set Composition and Two Deliberate Omissions

The set (real GDP per capita, inflation, displaced share) is the conventional prosperity/inflation/war-exposure trio, each with a confounding path to both exposure and the outcome.
Two omissions are deliberate: the coalition Russia-friendliness control was dropped as effectively time-invariant (absorbed by country fixed effects) and disproportionately costly, though a Moscow-sympathetic government is a substantive omission to defend; and no direct media-trust control is included, that dimension being addressed through the PSM moderator instead. All controls are justified only by within-country variation, since fixed effects absorb time-invariant traits.

# Moderator — PSM Funding (source and construction)

The moderator is public service media funding strength, operationalized as per-capita public revenues of public service media in euros. Values are for 2021 and cover all EU-27. The figures are transcribed from Figure 4 of the European Parliament study "Public financing of news media in the EU," which reports total public revenues of public service broadcasters by member state drawn from the European Audiovisual Observatory database; per-capita values are obtained by dividing each total by 2021 population (Eurostat, demo_pjan, 1 January 2021). The construction reproduces the report's own published per-capita figures exactly — Germany 103.0, Romania 7.6, the EU mean 49.7, and the identical top-five (Germany, Denmark, Sweden, Finland, Austria) and bottom-five (Poland, Bulgaria, Luxembourg, Malta, Romania) — which serves as the validation check on both the transcribed totals and the population denominators.

The measure is a single-year (2021) snapshot. This is not an assumption that funding levels are constant over 2022–2025; it follows from the moderator's specification as a time-invariant country characteristic. Under two-way fixed effects, any time-invariant national traits are absorbed, so PSM cannot enter as a main effect and appears only through its interaction with exposure. What the interaction requires is not that funding levels stay constant, but only that each country's relative standing in the funding distribution hold across the window. This is a weaker requirement — level constancy would imply stable rankings, but not the reverse. It is also one the evidence supports, since cross-national funding rankings are set by institutional arrangements rather than annual budgets.

# Primary vs Extended source register

Upon further assessment of the source content, restricted the primary exposure register to sources documenting Operation Doppelgänger or its documented aliases (RRN, Ruza Flood, Storm-1099). Four sources documenting allied but forensically distinct pro-Kremlin operations – VIG24 (Portal Kombat), VIG24-2 (Matryoshka), CHK24 (Operation Overload), EDM24 (Pravda) – move to an extended register used only in robustness check R5.

This was done to ensure that the analysis adheres closely to the research question and criterion A.

# Robustness battery expansion

Add R5 (extended register), R6 (drop W1), R7 (binary exposure), R8 (leave-one-country-out) to the pre-committed R1–R4. Soften codebook R12: evidence sources are recorded per cell mechanically; page-level locators live at the register level, not per cell as per-cell locators were never populated so the codebook would have overstated the audit trail as written.

# Inference — Equivalence Bounds (pre-committed)

The null result is tested for equivalence, not only for difference: a non-significant coefficient shows only that an effect was not detected, while an equivalence test asks whether effects of a stated, substantively meaningful size can be ruled out. The bounds below were fixed on 29 October 2026, after the point estimates and analytic standard errors had been reported but before any equivalence test, bootstrap confidence interval, or bootstrap minimum detectable effect was computed. They are derived only from the outcome data and survey sample sizes, never from the exposure coefficient.

Bounds are stated on the change in support when a state moves from no documented exposure to the top tier of the index (0 to 3), the substantively meaningful contrast; Spain makes exactly this switch within the window. The bound on the per-index-point coefficient is that change divided by three, which relies on the linear coding of the index; the tier-dummy specification checks that assumption.

The primary bound is the full EU-wide decline in support over the window: the unweighted mean across the 27 states fell from 67.98 to 59.56 percent for military aid and from 74.84 to 70.31 percent for sanctions between W1 and W7, so Δ = 8.42 points for aid and 4.54 for sanctions (differences taken before rounding; 2.81 and 1.51 per index point). Unweighted means are used because the two-way fixed effects estimator weights each state equally, and the window endpoints rather than the lowest wave are used to avoid selecting the largest drop. An effect of this size would mean that top-tier exposure alone moves a state's support by as much as everything that happened across the Union in two years; ruling it out answers whether documented Doppelgänger activity could account for the decline.

Four stricter bounds are reported as sensitivity checks, with a verdict at each. Half the EU-wide decline (4.21 aid, 2.27 sanctions) is closer to a smallest effect of interest, with the fraction a judgement call. The median 95 percent margin of error of a single country's topline (2.95 aid, 2.81 sanctions), computed from the actual Volume A sample sizes (500 to 1,559 respondents, median 1,011) under simple random sampling, marks an effect too small to register in a national poll. Hartman and Hidalgo's default of 0.36 standard deviations of the residualised untreated outcome (1.62 aid, 1.38 sanctions; σ is the residual standard deviation of the 140 unexposed country-waves after two-way fixed effects, 4.50 and 3.83) has published precedent but was designed for balance and placebo tests with a binary treatment. A Piccardi-sized effect (2.00 for both outcomes) takes the two-degree effect their field experiment was powered to detect on a 0–100 feeling thermometer; it is on a different scale and measured at the individual level under an intensive manipulation, so it serves as context, not as a substantive threshold.

The headline test is two one-sided tests (TOST) at α = 0.05, declaring equivalence when both H0: 3β ≤ −Δ and H0: 3β ≥ +Δ are rejected, equivalently when the 90 percent equal-tailed confidence interval for 3β lies inside ±Δ. A backlash, with exposure raising support, is substantively possible, so the two-sided version carries the claim; the one-sided result against erosion alone is reported alongside. Inference follows the bootstrap diagnostic: each one-sided test is a restricted wild cluster bootstrap (WCR) with the null β = ±Δ/3 imposed, 9,999 Rademacher draws, clustered by country, and the 90 and 95 percent intervals are obtained by inverting the same test over a grid of β. The equivalence confidence interval, the smallest symmetric bound at which equivalence would be declared, is reported so that readers can apply their own bound. Primary specification is the controlled model (m2), with the uncontrolled model (m1) alongside, on the full W1–W7 panel. The minimum detectable effect at 80 percent power is computed from the bootstrap interval as (t.975,26 + t.80,26) × SE*, where SE* is the bootstrap 95 percent interval's half-width divided by t.975,26.

# Inference — Timing and Placebo Specifications (pre-committed)

The lag, joint, and lead specifications below were fixed on 29 October 2026, before any of them was estimated. Only design quantities that do not involve the outcomes had been computed: which states vary, the effective number of clusters, and leverage.

The lag regresses opinion at wave t on exposure at t−1 and is estimated on W2–W7. W1 is dropped rather than assigned a lagged value, because no observation window precedes it. Six states (EE, ES, HU, LT, LV, SK) identify it. France, Italy, and Poland drop out because their only change in exposure falls in W7. As a labelled sensitivity check, the lag is also estimated on W1–W7 with pre-invasion exposure set to zero; the campaign did not exist before 24 February 2022, so that value is true. This version is not primary, because most of its added identification comes from that assumed starting value. It brings in Germany, France, Italy, Poland, and Latvia through a jump between W1 and W2.

The joint model enters contemporaneous and lagged exposure together on W2–W7. It reports both coefficients and their sum, the cumulative effect, which is estimated directly as the coefficient on exposure after reparameterising the lag as the difference between lagged and current exposure.

The placebo regresses opinion at wave t on exposure at t+1, conditional on contemporaneous exposure, on W1–W6. Because exposure is persistent, the lead entered alone would also absorb any contemporaneous effect. The conditional form asks the placebo question directly: does future documented activity predict current opinion? The lead alone is reported alongside. France, Italy, and Poland identify the lead only through the W7 coding: their lead switches at W6 only because W7 is coded 1, and if that drop reflects reporting lag their lead values are artefacts. The conditional lead is therefore also reported without those three states.

Inference follows the bootstrap diagnostic. Every specification here is identified by six states or relies on single-wave changes, so WR is reported alongside WCR throughout, with B = 9,999, seed 0, and intervals obtained by test inversion. Verdicts use WCR, which the diagnostic shows is conservative in six-state designs. Where WR would give a different verdict, the text says so.

The lag and the cumulative effect are tested for equivalence exactly as the contemporaneous effect is. The bounds are the pre-committed ones above, on the 0 to 3 change: the full EU-wide decline as primary, and half the decline, the poll margin of error, 0.36σ, and a Piccardi-sized effect as sensitivity bounds. The headline is TOST, with the one-sided test against erosion alongside. The bounds concern the size of an effect, not its timing, so they apply unchanged to a delayed or accumulated effect.

The placebo is framed as an equivalence test (Hartman and Hidalgo 2018), so a non-significant lead is not treated as evidence of no pre-trend (Roth 2022). The verdict is TOST at the primary bound (8.42 for aid, 4.54 for sanctions). Hartman and Hidalgo's 0.36σ default (1.62, 1.38) is reported as a sensitivity bound, although at the interval widths seen in the main specification it cannot pass whatever the data show. The equivalence confidence interval is reported as the smallest pre-trend, in either direction, that the data rule out. If that magnitude is too large to be informative, the placebo is described as uninformative rather than as passed.

# Inference — Functional Form, Jackknife, and Heterogeneity-Robust Checks (pre-committed)

The specifications below were fixed on 29 October 2026, before any of them was estimated. Only design quantities that do not involve the outcomes had been computed: which states identify each term, and the two-way fixed effects weights.

The index realises only the values 0, 1, and 3, so the linear coding is tested by replacing it with separate dummies for tier 1 and tier 3. The tier-1 dummy varies in eight states. The tier-3 dummy varies in five (Spain, Latvia, France, Italy, and Poland), the last three only through their W7 change. Linearity is tested as γ = β₃ − 3β₁, estimated as the coefficient on the tier-3 dummy when it is added to the linear model. β₃ is the 0-to-3 contrast without any linearity assumption. It is tested for equivalence at the pre-committed bounds directly, without dividing by three: TOST as the headline and the one-sided erosion test alongside. The tier-3 dummy is identified by five states, so WR is reported alongside WCR and verdicts use WCR.

The leave-one-country-out jackknife drops each of the nine states whose exposure varies, and two groups: the Baltic states (Estonia, Latvia, and Lithuania) together, and France, Italy, and Poland together, whose only change falls in W7. For each sample it reports the coefficient, the WCR and WR p-values, the 90 percent interval, the equivalence confidence interval, and TOST and the erosion test at the primary bound. This is done for both outcomes, with and without controls.

The robustness table's remaining analytic p-values are replaced with bootstrap ones. R4 (country-specific linear trends) uses WCR with the trends entered as controls. R8 (leave-one-country-out over all 27 states) uses WCR for every dropped country. A WR p-value is added to every row.

Following de Chaisemartin and D'Haultfœuille (2020), the two-way fixed effects weights are reported for the ordered treatment: the exposure residual from the fixed effects, and the controls where present, times exposure, normalised over the treated cells. Both robustness measures are reported. The first is the smallest dispersion of cell-level effects compatible with the true average effect being zero. The second, which exists because some weights are negative, is the smallest dispersion compatible with every cell-level effect having the opposite sign to the estimate.

Their heterogeneity-robust estimator DID_M is also estimated, generalised to the ordered index per unit of exposure. Each state whose tier changes between consecutive waves is compared with the states that stayed at its starting tier over the same two waves. Its change in support minus the stayers' mean change is signed by the direction of the switch, summed, and divided by the total absolute change in tier. With a binary treatment this is exactly their DID_M. Switches with no stayer at the starting tier are left out. Joiners (increases) and leavers (decreases) are also reported separately. DID_M is estimated without controls. Inference is a percentile 90 percent interval from a bootstrap that resamples countries (999 draws), together with a permutation p-value that reassigns the real exposure paths to random countries, as in the bootstrap diagnostic (4,002 draws). Few states switch, so DID_M is reported as an indicative check on whether effect heterogeneity could hide erosion, without an equivalence verdict.
