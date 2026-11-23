# The World in One Day — Monday 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/c/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/BGBug22/news-image-20261123-entry/rank.svg)](https://make.fun/c/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/BGBug22/news-image-20261123-entry/reward.svg)](https://make.fun/c/news-image-20261123)

Entry for the make.fun bounty **news-image-20261123**: https://make.fun/c/news-image-20261123

One newspaper front page, 1024×1024, for the news of Monday 23 November 2026.
A light world map carries nine numbered pins; each number matches a story.

| # | Where | Story |
|---|-------|-------|
| 1 | Antalya, Türkiye | COP31 climate summit ends with no deal (lead) |
| 2 | Benghazi, Libya | Russian warship sinks after sea-drone strike; UN urges probe |
| 3 | Washington, USA | Democrats win 258 House seats, the most since 1992 |
| 4 | Strait of Hormuz | Tankers struck as attacks on shipping surge |
| 5 | Ituri, DR Congo | Ebola team trapped by fighting; WHO pleads for peace |
| 6 | New Delhi, India | Nepal PM Balendra Shah holds talks with Modi |
| 7 | Wellington, NZ | India hunt final-day Test win after record 720-9 |
| 8 | Italy | Jeweller Paolo Bulgari dies aged 89 |
| 9 | Seoul, South Korea | Education minister quits over AI exam cheating |

## Run

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` uses only the Node standard library and no network. It checks the
drawn page (`entry.png`) and writes it to `/output/entry.png`, byte for byte
the same on every run.

The page itself is drawn by `tools/render_front_page.py` (Pillow, Noto fonts):

```
python3 tools/render_front_page.py
```

MIT licensed — see `LICENSE`.
