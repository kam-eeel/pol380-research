## TWFE weights and robustness measures

| outcome           | spec          |   beta TWFE |   treated cells |   negative cells |   negative weight |   sigma: zero average |   sigma: all opposite sign |
|:------------------|:--------------|------------:|----------------:|-----------------:|------------------:|----------------------:|---------------------------:|
| support_aid       | m1 base       |       0.068 |              49 |               14 |            -0.234 |                 0.035 |                      0.107 |
| support_sanctions | m1 base       |       0.042 |              49 |               14 |            -0.234 |                 0.022 |                      0.066 |
| support_aid       | m2 + controls |       0.336 |              49 |               12 |            -0.23  |                 0.179 |                      0.525 |
| support_sanctions | m2 + controls |       0.192 |              49 |               12 |            -0.23  |                 0.103 |                      0.3   |

## DID_M per unit of exposure (no controls)

| outcome           | estimate   |   per unit | 90% CI        |   draws dropped |   switches |   skipped (no stayer) |   p_perm |
|:------------------|:-----------|-----------:|:--------------|----------------:|-----------:|----------------------:|---------:|
| support_aid       | DID_M      |      1.049 | [-0.94, 2.71] |               0 |         12 |                     2 |    0.365 |
| support_aid       | joiners    |      0.062 | [-1.15, 2.28] |              13 |          4 |                   nan |  nan     |
| support_aid       | leavers    |      1.472 | [-4.16, 3.32] |              46 |          8 |                   nan |  nan     |
| support_sanctions | DID_M      |      0.917 | [-1.45, 1.93] |               0 |         12 |                     2 |    0.305 |
| support_sanctions | joiners    |     -0.28  | [-1.96, 1.13] |              13 |          4 |                   nan |  nan     |
| support_sanctions | leavers    |      1.431 | [-5.24, 2.64] |              46 |          8 |                   nan |  nan     |
