# news-18-nov-2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/qienzdork/news-18-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/qienzdork/news-18-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One page, one day: Wednesday 18 November 2026, summed up as a newspaper front page. 41 stories across 7 regions, 11 of them drawn, a UTC timeline, a world map, and a date check that leaves out anything first reported on 17 November. Xi greets Trump in Shenzhen, Kuwait and Bahrain intercept Iranian drones, Voyager 1 reaches one light-day from Earth, the EU offers Kyiv a €45bn loan, and GTA VI goes on sale.

## Run it

```sh
python3 draw_frontpage.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`draw_frontpage.py` draws `entry.png` (1024x1024, Pillow, build time only). `main.py` is stdlib-only and copies `entry.png` to `/output/entry.png`, so both grader runs write identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
