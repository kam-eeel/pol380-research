## Tier dummies and linearity test

| outcome           | spec          | term                    |   beta |   p_WCR | WCR 90% CI     |   p_WR | WR 90% CI      |
|:------------------|:--------------|:------------------------|-------:|--------:|:---------------|-------:|:---------------|
| support_aid       | m1 base       | beta1 (tier 1)          | -0.741 |   0.542 | [-3.44, 1.74]  |  0.545 | [-3.00, 1.42]  |
| support_aid       | m1 base       | beta3 (tier 3)          |  0.091 |   0.965 | [-2.92, 8.41]  |  0.973 | [-3.94, 5.58]  |
| support_aid       | m1 base       | gamma = beta3 - 3 beta1 |  2.313 |   0.576 | [-4.10, 10.13] |  0.575 | [-4.38, 9.88]  |
| support_aid       | m2 + controls | beta1 (tier 1)          | -0.189 |   0.916 | [-3.98, 3.90]  |  0.916 | [-3.52, 3.05]  |
| support_aid       | m2 + controls | beta3 (tier 3)          |  0.946 |   0.717 | [-2.44, 9.07]  |  0.72  | [-3.31, 6.63]  |
| support_aid       | m2 + controls | gamma = beta3 - 3 beta1 |  1.512 |   0.77  | [-7.43, 11.88] |  0.767 | [-6.96, 11.00] |
| support_sanctions | m1 base       | beta1 (tier 1)          | -0.687 |   0.511 | [-2.40, 0.97]  |  0.498 | [-2.43, 1.16]  |
| support_sanctions | m1 base       | beta3 (tier 3)          |  0.024 |   0.985 | [-3.01, 3.69]  |  0.987 | [-3.03, 3.10]  |
| support_sanctions | m1 base       | gamma = beta3 - 3 beta1 |  2.085 |   0.506 | [-3.36, 7.75]  |  0.509 | [-3.51, 7.54]  |
| support_sanctions | m2 + controls | beta1 (tier 1)          | -0.467 |   0.65  | [-2.30, 1.81]  |  0.696 | [-2.54, 1.69]  |
| support_sanctions | m2 + controls | beta3 (tier 3)          |  0.499 |   0.751 | [-3.44, 4.84]  |  0.78  | [-3.06, 4.04]  |
| support_sanctions | m2 + controls | gamma = beta3 - 3 beta1 |  1.9   |   0.589 | [-4.63, 8.57]  |  0.603 | [-4.75, 8.31]  |

## Equivalence of the tier-3 coefficient (0 -> 3) at each bound

| outcome           | spec          | bound                  |   delta |   p_TOST WCR |   p_erosion WCR |   p_TOST WR |   p_erosion WR | equivalent (WCR)   | WR agrees   |
|:------------------|:--------------|:-----------------------|--------:|-------------:|----------------:|------------:|---------------:|:-------------------|:------------|
| support_aid       | m1 base       | A1 full EU decline     |  8.4219 |       0.0493 |          0.0014 |      0.0172 |         0.0003 | True               | True        |
| support_aid       | m1 base       | A2 half EU decline     |  4.2109 |       0.147  |          0.0117 |      0.0865 |         0.0391 | False              | True        |
| support_aid       | m1 base       | B poll margin of error |  2.953  |       0.1945 |          0.0467 |      0.1469 |         0.1045 | False              | True        |
| support_aid       | m1 base       | C H&H 0.36 sd          |  1.6202 |       0.2866 |          0.2342 |      0.2649 |         0.2432 | False              | True        |
| support_aid       | m1 base       | D Piccardi-sized       |  2      |       0.2579 |          0.1803 |      0.2251 |         0.198  | False              | True        |
| support_aid       | m2 + controls | A1 full EU decline     |  8.4219 |       0.0622 |          0.0032 |      0.024  |         0.0009 | False              | False       |
| support_aid       | m2 + controls | A2 half EU decline     |  4.2109 |       0.2162 |          0.0112 |      0.1387 |         0.0226 | False              | True        |
| support_aid       | m2 + controls | B poll margin of error |  2.953  |       0.2844 |          0.0257 |      0.2343 |         0.0688 | False              | True        |
| support_aid       | m2 + controls | C H&H 0.36 sd          |  1.6202 |       0.3982 |          0.1422 |      0.3937 |         0.1683 | False              | True        |
| support_aid       | m2 + controls | D Piccardi-sized       |  2      |       0.3557 |          0.0913 |      0.3397 |         0.1299 | False              | True        |
| support_sanctions | m1 base       | A1 full EU decline     |  4.5379 |       0.0329 |          0.0256 |      0.0157 |         0.0157 | True               | True        |
| support_sanctions | m1 base       | A2 half EU decline     |  2.2689 |       0.0995 |          0.0833 |      0.0986 |         0.0986 | False              | True        |
| support_sanctions | m1 base       | B poll margin of error |  2.8089 |       0.0762 |          0.0561 |      0.0627 |         0.0627 | False              | True        |
| support_sanctions | m1 base       | C H&H 0.36 sd          |  1.3804 |       0.1643 |          0.1463 |      0.2001 |         0.1931 | False              | True        |
| support_sanctions | m1 base       | D Piccardi-sized       |  2      |       0.1149 |          0.097  |      0.1218 |         0.1218 | False              | True        |
| support_sanctions | m2 + controls | A1 full EU decline     |  4.5379 |       0.0572 |          0.0284 |      0.0331 |         0.0206 | False              | False       |
| support_sanctions | m2 + controls | A2 half EU decline     |  2.2689 |       0.1526 |          0.0783 |      0.1771 |         0.0914 | False              | True        |
| support_sanctions | m2 + controls | B poll margin of error |  2.8089 |       0.1213 |          0.0615 |      0.1209 |         0.0609 | False              | True        |
| support_sanctions | m2 + controls | C H&H 0.36 sd          |  1.3804 |       0.2874 |          0.122  |      0.313  |         0.1649 | False              | True        |
| support_sanctions | m2 + controls | D Piccardi-sized       |  2      |       0.1794 |          0.0907 |      0.212  |         0.1121 | False              | True        |
