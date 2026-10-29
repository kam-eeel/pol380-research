## TOST and one-sided tests at each bound (WCR, B = 9,999, seed 0)

| outcome           | spec          | bound                  |   delta |   p_TOST | equivalent   |   p_erosion | erosion ruled out   |
|:------------------|:--------------|:-----------------------|--------:|---------:|:-------------|------------:|:--------------------|
| support_aid       | m1 base       | A1 full EU decline     |  8.4219 |   0.0523 | False        |      0.0023 | True                |
| support_aid       | m1 base       | A2 half EU decline     |  4.2109 |   0.1457 | False        |      0.0031 | True                |
| support_aid       | m1 base       | B poll margin of error |  2.953  |   0.1999 | False        |      0.0262 | True                |
| support_aid       | m1 base       | C H&H 0.36 sd          |  1.6202 |   0.2981 | False        |      0.2352 | False               |
| support_aid       | m1 base       | D Piccardi-sized       |  2      |   0.2709 | False        |      0.1715 | False               |
| support_aid       | m2 + controls | A1 full EU decline     |  8.4219 |   0.0635 | False        |      0.0029 | True                |
| support_aid       | m2 + controls | A2 half EU decline     |  4.2109 |   0.2168 | False        |      0.0084 | True                |
| support_aid       | m2 + controls | B poll margin of error |  2.953  |   0.2823 | False        |      0.018  | True                |
| support_aid       | m2 + controls | C H&H 0.36 sd          |  1.6202 |   0.4028 | False        |      0.1329 | False               |
| support_aid       | m2 + controls | D Piccardi-sized       |  2      |   0.3551 | False        |      0.0826 | False               |
| support_sanctions | m1 base       | A1 full EU decline     |  4.5379 |   0.036  | True         |      0.0296 | True                |
| support_sanctions | m1 base       | A2 half EU decline     |  2.2689 |   0.1112 | False        |      0.0748 | False               |
| support_sanctions | m1 base       | B poll margin of error |  2.8089 |   0.0834 | False        |      0.0529 | False               |
| support_sanctions | m1 base       | C H&H 0.36 sd          |  1.3804 |   0.1882 | False        |      0.1343 | False               |
| support_sanctions | m1 base       | D Piccardi-sized       |  2      |   0.1258 | False        |      0.0864 | False               |
| support_sanctions | m2 + controls | A1 full EU decline     |  4.5379 |   0.063  | False        |      0.0294 | True                |
| support_sanctions | m2 + controls | A2 half EU decline     |  2.2689 |   0.16   | False        |      0.0728 | False               |
| support_sanctions | m2 + controls | B poll margin of error |  2.8089 |   0.1243 | False        |      0.0591 | False               |
| support_sanctions | m2 + controls | C H&H 0.36 sd          |  1.3804 |   0.3091 | False        |      0.1136 | False               |
| support_sanctions | m2 + controls | D Piccardi-sized       |  2      |   0.1927 | False        |      0.0827 | False               |

## 90% intervals for the 0 -> 3 change

| outcome           | spec          |   beta 0-3 | WCR 90% 0-3   |   ECI 0-3 | ECI seeds 0-4   |   erosion ruled out beyond | WR 90% 0-3 (comparison)   | CRV1 90% 0-3 (comparison)   |
|:------------------|:--------------|-----------:|:--------------|----------:|:----------------|---------------------------:|:--------------------------|:----------------------------|
| support_aid       | m1 base       |       0.2  | [-2.70, 8.57] |      8.57 | 8.26–8.57       |                      -2.7  | [-3.75, 5.65]             | [-3.58, 3.99]               |
| support_aid       | m2 + controls |       1.01 | [-2.30, 9.16] |      9.16 | 8.96–9.16       |                      -2.3  | [-3.21, 6.63]             | [-3.09, 5.10]               |
| support_sanctions | m1 base       |       0.13 | [-2.90, 3.73] |      3.73 | 3.54–3.73       |                      -2.9  | [-3.01, 3.27]             | [-2.24, 2.49]               |
| support_sanctions | m2 + controls |       0.58 | [-3.31, 5.12] |      5.12 | 4.90–5.22       |                      -3.31 | [-3.05, 4.15]             | [-2.12, 3.27]               |
