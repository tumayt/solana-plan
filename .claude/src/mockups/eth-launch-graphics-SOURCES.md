# eth-launch-graphics.html: every number and the command that produced it

Verified 2026-08-17, ~18:40 UTC, against production `api.cambrian.org`.
Re-run these before publishing. The pool metrics move hourly.

## G1, Ethereum lending

One call, one counting rule:

```
GET /beta/evm/lending/overview?chain_id=1&limit=5000
```

Aggregate the returned rows by `protocolId`, summing `tvlUsd`:

| protocolId | rows | tvlUsd |
|---|---|---|
| aave-v3 | 67 | $17.809B |
| morpho-v1 | 439 | $0.531B |
| morpho-v2 | 626 | $2.111B |
| euler-lend | 869 | $0.327B |
| **total** | **2,001** | **$20.777B** |

The graphic shows Morpho as one bar: 439 + 626 = 1,065 vaults, $2.642B.

**Counting rule: all indexed rows.** The alternative rule, rows with `tvlUsd > 0`,
gives Aave 35, Morpho 628, Euler 202, total 865, at the same $20.777B. Both are
defensible. Mixing them is not, which is what the first version did.

**Do not add Morpho markets to this total.** `/beta/evm/lending/morpho/markets?chain_id=1`
returns 1,366 rows at $6.314B. Morpho vaults deposit into those markets, so vault
TVL and market TVL overlap. The $20.78B figure is vault-level and stands alone.

## G2, one pool

```
GET /evm/uniswap/v3/pool?chain_id=1&pool_address=0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640
```

That address is the USDC/WETH 0.05% pool on mainnet, created 2021-05-05. The other
three USDC/WETH pools: 0.01% `0xe0554a476a092703abdb3ef35c80e0d76d32939f`,
0.3% `0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8`, 1% `0x7bea39867e4169dbe237d55c8242a8f2fcdcc387`.

| Graphic label | Response field | Value at capture |
|---|---|---|
| TVL | `poolTvlUsd` | 98,973,662.89 |
| 24h swap volume | `swapVolumeUsd["1 day"]` | 76,198,458 |
| Fee APR, 30d | `feeApr["1 month"]` | 0.13843 |
| Fee APR, 24h | `feeApr["1 day"]` | 0.14050 |
| 30d volatility | `priceVolatilityPct["1 month"]` | 0.08027 |
| 30d volume | `swapVolumeUsd["1 month"]` | 2,283,454,397 |

`feeApr` and `priceVolatilityPct` are fractions, not percentages. Multiply by 100.

**Six windows applies to most metrics, not all.** `swapVolumeUsd`, `feeApr`,
`priceVolatilityPct` and `swapCount` carry 6 windows (5 minute, 1 hour, 1 day,
1 week, 1 month, 1 year). `uniqueUserCount` carries 3. The caption names the
metrics that actually have six.

## What was wrong in the first version

| Claim | Reality |
|---|---|
| Euler 305 vaults | No query yields 305. 869 rows, 202 with TVL above zero. |
| Morpho $2.7B | $2.64B, rounds to $2.6B. |
| 628 vaults and markets | The 628 were vaults only, and only under a TVL-above-zero filter. |
| 1,000+ markets | Was the sum of the three bar labels. Real count is 2,001. |
| Mixed counting rules | Aave's 67 counted empty markets; Morpho's 628 excluded them. |
| 24h volume $74.9M, fee APRs | Live values that had already moved by the time of checking. |
| Every metric, six windows | `uniqueUserCount` has three. |
