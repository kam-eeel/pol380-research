## Tier dummies and linearity test

| outcome           | spec          | term                    |   beta |   p_WCR | WCR 90% CI     |   p_WR | WR 90% CI      |
|:------------------|:--------------|:------------------------|-------:|--------:|:---------------|-------:|:---------------|
| support_aid       | m1 base       | beta1 (tier 1)          | -0.741 |   0.542 | [-3.44, 1.74]  |  0.545 | [-3.00, 1.42]  |
| support_aid       | m1 base       | beta3 (tier 3)          |  0.091 |   0.965 | [-2.92, 8.41]  |  0.973 | [-3.94, 5.58]  |
| support_aid       | m1 base       | gamma = beta3 - 3 beta1 |  2.313 |   0.576 | [-4.10, 10.13] |  0.575 | [-4.38, 9.88]  |
| support_aid       | m2 + controls | beta1 (tier 1)          | -0.197 |   0.914 | [-3.98, 3.88]  |  0.913 | [-3.55, 3.04]  |
| support_aid       | m2 + controls | beta3 (tier 3)          |  0.949 |   0.716 | [-2.42, 9.06]  |  0.719 | [-3.30, 6.62]  |
| support_aid       | m2 + controls | gamma = beta3 - 3 beta1 |  1.539 |   0.77  | [-7.41, 11.87] |  0.764 | [-6.97, 11.12] |
| support_sanctions | m1 base       | beta1 (tier 1)          | -0.687 |   0.511 | [-2.40, 0.97]  |  0.498 | [-2.43, 1.16]  |
| support_sanctions | m1 base       | beta3 (tier 3)          |  0.024 |   0.985 | [-3.01, 3.69]  |  0.987 | [-3.03, 3.10]  |
| support_sanctions | m1 base       | gamma = beta3 - 3 beta1 |  2.085 |   0.506 | [-3.36, 7.75]  |  0.509 | [-3.51, 7.54]  |
| support_sanctions | m2 + controls | beta1 (tier 1)          | -0.519 |   0.622 | [-2.40, 1.79]  |  0.667 | [-2.64, 1.67]  |
| support_sanctions | m2 + controls | beta3 (tier 3)          |  0.497 |   0.754 | [-3.50, 4.83]  |  0.782 | [-3.09, 4.05]  |
| support_sanctions | m2 + controls | gamma = beta3 - 3 beta1 |  2.053 |   0.563 | [-4.58, 8.78]  |  0.578 | [-4.65, 8.52]  |

## Equivalence of the tier-3 coefficient (0 -> 3) at each bound

| outcome           | spec          | bound                  |   delta |   p_TOST WCR |   p_erosion WCR |   p_TOST WR |   p_erosion WR | equivalent (WCR)   | WR agrees   |
|:------------------|:--------------|:-----------------------|--------:|-------------:|----------------:|------------:|---------------:|:-------------------|:------------|
| support_aid       | m1 base       | A1 full EU decline     |  8.4219 |       0.0493 |          0.0014 |      0.0172 |         0.0003 | True               | True        |
| support_aid       | m1 base       | A2 half EU decline     |  4.2109 |       0.147  |          0.0117 |      0.0865 |         0.0391 | False              | True        |
| support_aid       | m1 base       | B poll margin of error |  2.953  |       0.1945 |          0.0467 |      0.1469 |         0.1045 | False              | True        |
| support_aid       | m1 base       | C H&H 0.36 sd          |  1.6202 |       0.2866 |          0.2342 |      0.2649 |         0.2432 | False              | True        |
| support_aid       | m1 base       | D Piccardi-sized       |  2      |       0.2579 |          0.1803 |      0.2251 |         0.198  | False              | True        |
| support_aid       | m2 + controls | A1 full EU decline     |  8.4219 |       0.0618 |          0.0032 |      0.0237 |         0.0009 | False              | False       |
| support_aid       | m2 + controls | A2 half EU decline     |  4.2109 |       0.2156 |          0.0112 |      0.1379 |         0.0219 | False              | True        |
| support_aid       | m2 + controls | B poll margin of error |  2.953  |       0.2832 |          0.0257 |      0.2343 |         0.0681 | False              | True        |
| support_aid       | m2 + controls | C H&H 0.36 sd          |  1.6202 |       0.3977 |          0.1405 |      0.3939 |         0.1677 | False              | True        |
| support_aid       | m2 + controls | D Piccardi-sized       |  2      |       0.3556 |          0.0902 |      0.3396 |         0.1287 | False              | True        |
| support_sanctions | m1 base       | A1 full EU decline     |  4.5379 |       0.0329 |          0.0256 |      0.0157 |         0.0157 | True               | True        |
| support_sanctions | m1 base       | A2 half EU decline     |  2.2689 |       0.0995 |          0.0833 |      0.0986 |         0.0986 | False              | True        |
| support_sanctions | m1 base       | B poll margin of error |  2.8089 |       0.0762 |          0.0561 |      0.0627 |         0.0627 | False              | True        |
| support_sanctions | m1 base       | C H&H 0.36 sd          |  1.3804 |       0.1643 |          0.1463 |      0.2001 |         0.1931 | False              | True        |
| support_sanctions | m1 base       | D Piccardi-sized       |  2      |       0.1149 |          0.097  |      0.1218 |         0.1218 | False              | True        |
| support_sanctions | m2 + controls | A1 full EU decline     |  4.5379 |       0.0567 |          0.0289 |      0.0334 |         0.021  | False              | False       |
| support_sanctions | m2 + controls | A2 half EU decline     |  2.2689 |       0.152  |          0.0782 |      0.1769 |         0.0919 | False              | True        |
| support_sanctions | m2 + controls | B poll margin of error |  2.8089 |       0.1206 |          0.0623 |      0.1212 |         0.0615 | False              | True        |
| support_sanctions | m2 + controls | C H&H 0.36 sd          |  1.3804 |       0.2877 |          0.1232 |      0.3125 |         0.1648 | False              | True        |
| support_sanctions | m2 + controls | D Piccardi-sized       |  2      |       0.1792 |          0.0912 |      0.2125 |         0.1124 | False              | True        |
