# THE 23rd — Monday 23 November 2026 in one image

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/xszee/news-image-20261123-main/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/xszee/news-image-20261123-main/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-day newspaper front page summing up the world's news of
**Monday 23 November 2026**, built for the
[make.fun news-image-20261123 bounty](https://make.fun/bounty/news-image-20261123).

## The front page

- **Lead — Democrats take the House.** A recount in North Carolina
  confirms Chuck Hubbard's win, giving Democrats at least 258 seats,
  their best House result since 1992.
- **Markets — AI fears sink stocks worldwide.** Tokyo's Nikkei plunges
  5.06% and the S&P 500 falls 3.7% as investors question AI valuations.
- **Mexico — 'El Chapo Isidro' captured.** FBI most-wanted cartel leader
  Fausto Isidro Meza Flores is arrested in Guasave, Sinaloa.
- **Turkey — Thousands march on media takeover.** Crowds rally in Istanbul
  against a government takeover of independent media.
- **The world in brief — 12 more stories:** COP31 ends with no deal,
  Gaza contamination, Italy's ex-police chief inquiry, Belgian airport
  strike, Rwanda deportation centres, Bolsonaro in intensive care,
  Tata Steel's $1.67bn stake, the Nvidia affair, METR's AI-safety warning,
  Márquez's eighth MotoGP title, Denmark's Russia plot claim, and
  US mediators heading to Moscow.

All stories were reported on Monday 23 November 2026
(sources: Reuters, AP, AFP, BBC).

## How it is built

`draw.py` draws the front page with Pillow (no network, no downloaded
assets): masthead, headlines, two drawn panels (a ballot box and a
plunging market chart), and the brief list. It writes `art.png`
(1024×1024, under 1 MiB, deterministic — re-running it gives identical
bytes). `main.ts` validates that image and copies it to
`/output/entry.png`.

```sh
python3 draw.py            # regenerate art.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
