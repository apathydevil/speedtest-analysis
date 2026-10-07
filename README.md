# speedtest-analysis

Analysis of 5,003 speed tests from a home internet connection, February to
October 2026. Data source: a self-hosted
[Speedtest Tracker](https://github.com/alexjustesen/speedtest-tracker),
one test per hour. Live view of the same data:
[speedtest-dashboard](https://github.com/apathydevil/speedtest-dashboard).

**Questions:**

1. Is the connection getting better or worse over time?
2. When during the week is it slow?

## Findings

- **Median** download 938 Mbit/s on a 1 Gbit/s line. **Mean** 839 Mbit/s, pulled
  down by a minority of slow tests (lowest: 1.6 Mbit/s).
- 7-day rolling average: 830 Mbit/s in March, low of 740 Mbit/s at the end of
  May, 850 to 920 Mbit/s since July.
- No evening slowdown. Most hours average 800 to 900 Mbit/s. At 2:00 the
  average drops to 694 to 767 Mbit/s on five of seven weekdays.

![7-day rolling average of download speed](images/trend.png)

![Average download speed by weekday and hour](images/heatmap.png)

## Structure

- `src/speedtest_analysis/fetcher.py`: fetches all results from
  `/api/v1/results`, follows pagination, drops failed and incomplete tests,
  converts to Mbit/s.
- `src/speedtest_analysis/storage.py`: writes `data/results.csv`.
- `notebooks/explore.ipynb`: scatter of all tests, daily and 7-day rolling
  average, weekday-by-hour heatmap.

The API documentation names the page size parameter `per.page`. The server
reads `page[size]` (`ResultsController` in the Speedtest Tracker source).
With `page[size]=500`, a full fetch takes 11 requests instead of 209.

## Stack

- requests, python-dotenv: API access
- pandas: grouping, rolling averages, pivot tables
- matplotlib, seaborn: charts
- Jupyter: analysis
- uv: dependency management

## Setup

Requires a Speedtest Tracker instance and an API token.

```bash
uv sync
cp .env.example .env
```

Set `SPEEDTEST_URL` and `SPEEDTEST_TOKEN` in `.env`.

## Run

From the project root:

```bash
uv run python -m speedtest_analysis.fetcher
```

Open `notebooks/explore.ipynb`, select the `.venv` kernel, run all cells.

`data/` is not committed. The notebook is committed without outputs. The
charts are in `images/`.
