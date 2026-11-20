# THE WORLD TODAY — Friday, 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/akbarrrputraa/news-image-20261120-v2/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/akbarrrputraa/news-image-20261120-v2/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Entry for the [make.fun bounty **news-image-20261120**](https://make.fun/bounty/news-image-20261120):
*Sum up 20 November's world news in one image.*

## What it does

`main.py` draws a one-page broadsheet — **THE WORLD TODAY** — entirely in
code (Pillow, no network, no external images) and writes it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (1024 x 1024 PNG).

- **Lead story:** Trump, Xi and Putin sign a peace declaration at their
  first trilateral summit in Shenzhen.
- **Markets strip:** Dow 49,097 (-2.2%), S&P 500 7,176 (-2.0%),
  Nasdaq 23,879 (-2.3%), Nikkei -4.8%, Brent $90.05 (+0.7%),
  Anthropic $97.17 (+17%).
- **The Day in Full:** 12 verified stories — the ICJ's Myanmar genocide
  ruling, Anthropic's record $81bn IPO, the Wall Street sell-off,
  GTA VI's $1.84bn launch, Kyiv hit again, Houthi missiles over Riyadh,
  the Pete Rose pardon, Fiona the hippo, COP31, Europe's cost-of-living
  protests, Estonia's Russia border closure, and Texans 26–3 Colts.
- **In Brief:** 9 more verified items, from AMD's short-seller dive to
  Genoa airport's drone halt.
- Every pictogram (skyline, flags, market bars) is drawn in code.

All 22 stories were verified against reporting published 19–20 November
2026 (Reuters, The Times, Wall Street Journal, AP, BBC, USA Today,
Le Monde, Investor's Business Daily). No invented facts.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (1024 x 1024, deterministic: two runs are byte-identical)
```

Requires Python 3.12+ and Pillow (`pip install pillow`).

## License

MIT — see [LICENSE](LICENSE).
