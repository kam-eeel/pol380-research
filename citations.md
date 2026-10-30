# Methodology sources

The analysis draws on the following methodological sources. The papers themselves are not distributed in this repository for copyright reasons.

## References

Bertrand, M., Duflo, E., & Mullainathan, S. (2004). How much should we trust differences-in-differences estimates? *The Quarterly Journal of Economics*, *119*(1), 249–275. https://doi.org/10.1162/003355304772839588

Bloom, H. S. (1995). Minimum detectable effects: A simple way to report the statistical power of experimental designs. *Evaluation Review*, *19*(5), 547–556. https://doi.org/10.1177/0193841X9501900504

Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2008). Bootstrap-based improvements for inference with clustered errors. *The Review of Economics and Statistics*, *90*(3), 414–427. https://doi.org/10.1162/rest.90.3.414

Carter, A. V., Schnepel, K. T., & Steigerwald, D. G. (2017). Asymptotic behavior of a *t*-test robust to cluster heterogeneity. *The Review of Economics and Statistics*, *99*(4), 698–709. https://doi.org/10.1162/REST_a_00639

de Chaisemartin, C., & D'Haultfœuille, X. (2020). Two-way fixed effects estimators with heterogeneous treatment effects. *American Economic Review*, *110*(9), 2964–2996. https://doi.org/10.1257/aer.20181169

Donald, S. G., & Lang, K. (2007). Inference with difference-in-differences and other panel data. *The Review of Economics and Statistics*, *89*(2), 221–233. https://doi.org/10.1162/rest.89.2.221

Hartman, E., & Hidalgo, F. D. (2018). An equivalence approach to balance and placebo tests. *American Journal of Political Science*, *62*(4), 1000–1013. https://doi.org/10.1111/ajps.12387

Lakens, D. (2017). Equivalence tests: A practical primer for *t* tests, correlations, and meta-analyses. *Social Psychological and Personality Science*, *8*(4), 355–362. https://doi.org/10.1177/1948550617697177

Lakens, D., Scheel, A. M., & Isager, P. M. (2018). Equivalence testing for psychological research: A tutorial. *Advances in Methods and Practices in Psychological Science*, *1*(2), 259–269. https://doi.org/10.1177/2515245918770963

MacKinnon, J. G., Nielsen, M. Ø., & Webb, M. D. (2023). Cluster-robust inference: A guide to empirical practice. *Journal of Econometrics*, *232*(2), 272–299. https://doi.org/10.1016/j.jeconom.2022.04.001

MacKinnon, J. G., & Webb, M. D. (2018). The wild bootstrap for few (treated) clusters. *The Econometrics Journal*, *21*(2), 114–135. https://doi.org/10.1111/ectj.12107

Piccardi, T., Saveski, M., Jia, C., Hancock, J., Tsai, J. L., & Bernstein, M. S. (2025). Reranking partisan animosity in algorithmic social media feeds alters affective polarization. *Science*, *390*(6776), Article eadu5584. https://doi.org/10.1126/science.adu5584

Rainey, C. (2014). Arguing for a negligible effect. *American Journal of Political Science*, *58*(4), 1083–1091. https://doi.org/10.1111/ajps.12102

Roodman, D., MacKinnon, J. G., Nielsen, M. Ø., & Webb, M. D. (2019). Fast and wild: Bootstrap inference in Stata using boottest. *The Stata Journal*, *19*(1), 4–60. https://doi.org/10.1177/1536867X19830877

Roth, J. (2022). Pretest with caution: Event-study estimates after testing for parallel trends. *American Economic Review: Insights*, *4*(3), 305–322. https://doi.org/10.1257/aeri.20210236

## Where each source is used

| Source | Use in the analysis |
|---|---|
| Bertrand et al. (2004) | Placebo-treatment simulation in the inference diagnostic |
| Bloom (1995) | Minimum detectable effect |
| Cameron et al. (2008) | Wild cluster bootstrap |
| Carter et al. (2017) | Effective number of clusters, G\*(0) |
| de Chaisemartin and D'Haultfœuille (2020) | TWFE weights, robustness measures (ordered-treatment version, online appendix Section 3.2), and DID_M |
| Donald and Lang (2007) | Inference with few groups |
| Hartman and Hidalgo (2018) | Equivalence framing of the placebo test and the 0.36σ bound |
| Lakens (2017); Lakens et al. (2018) | TOST procedure and the justification of equivalence bounds |
| MacKinnon et al. (2023) | CV3, G\*(0), partial leverage, and leave-one-out estimates |
| MacKinnon and Webb (2018) | Restricted and subcluster wild bootstrap (WCR, WR) with few treated clusters |
| Piccardi et al. (2025) | Benchmark for the Piccardi-sized equivalence bound |
| Rainey (2014) | Equivalence argument and 90% confidence intervals |
| Roodman et al. (2019) | Test-inversion confidence intervals for the wild bootstrap |
| Roth (2022) | Pre-trend testing and the lead placebo |
