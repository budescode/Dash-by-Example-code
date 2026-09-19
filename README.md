# Dash by Example: the code

Companion code for the free book **Dash by Example: Build Real-World Dashboards with Python** by Osakpolor Emmanuel Omonbude.

Get the book, free, at [leanpub.com/dashbyexample](https://leanpub.com/dashbyexample).

Every project in the book is a folder in this repository. Each folder is self-contained: its own `app.py`, its own dependencies, and nothing shared with the others, so you can run any one of them without touching the rest.

## Projects

| Chapter | Folder | What it builds | Data | Status |
|---|---|---|---|---|
| 2 to 4 | `my-dashboard/` | The learning app: smoke test, icons, Bootstrap layout, first callbacks | Built-in Plotly sample data | Available |
| 5 | `superstore-dashboard/` | Sales KPI tracker, multi-page, with AG Grid order detail | Superstore Sales (Kaggle) | Coming soon |
| 6 | `market-monitor-dashboard/` | Financial market monitor: candlesticks, volume, moving averages | Yahoo Finance via `yfinance` | Coming soon |
| 7 | `ecommerce-hub-dashboard/` | E-commerce analytics hub, multi-page: funnel, monthly orders, revenue by state | Olist Brazilian E-Commerce (Kaggle) | Coming soon |
| 8 | `binance-live-dashboard/` | Live crypto dashboard on Dash 4 WebSocket callbacks | Binance public streams | Coming soon |
| 9 | `auth-dashboard/` | Login, registration, password reset and Google/GitHub sign-in | SQLite users table | Coming soon |

Chapter 3 (Plotly Express) uses a scratch file, `charts.py`, inside `my-dashboard/`. Chapters 1, 10 and 11 have no project of their own: they cover choosing Dash, performance, and deployment of the projects above.

A standalone version of the Chapter 9 login system lives at [github.com/budescode/dash-authentication](https://github.com/budescode/dash-authentication), and the social sign-in library it uses is at [github.com/budescode/dash-social-signin](https://github.com/budescode/dash-social-signin).

## Running a project

Clone the repository, then move into the project you want:

```bash
git clone https://github.com/budescode/Dash-by-Example-code.git
cd Dash-by-Example-code/my-dashboard
```

### With uv (recommended)

Each folder has a `pyproject.toml` and a `uv.lock`, so one command installs the exact versions the book was tested with and runs the app:

```bash
uv run python app.py
```

### With pip

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 app.py
```

Then open [http://localhost:8050](http://localhost:8050) in your browser.

Two exceptions, both explained in their chapters:

- **Chapter 8** runs on Dash's FastAPI backend, so in production it is served with `uvicorn app:server` rather than gunicorn. `python app.py` still works for development.
- **Chapter 9** needs its database created once before the first run: `uv run flask db upgrade` (or `flask db upgrade` with pip).

## Datasets

Datasets are not stored in this repository. Two projects need a download, placed in that project's `data/` folder:

| Project | Dataset | Where to get it |
|---|---|---|
| `superstore-dashboard/` | Superstore Sales, saved as `data/superstore.csv` | [kaggle.com/datasets/vivek468/superstore-dataset-final](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) |
| `ecommerce-hub-dashboard/` | Olist Brazilian E-Commerce, all CSV files into `data/` | [kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) |

The other projects fetch their data at run time. The market monitor downloads prices through `yfinance`, with no account or API key. The Binance dashboard connects to the public streams at `stream.binance.com:9443`; if that host is not reachable from your region, `stream.binance.us:9443` serves the same streams.

## Secrets

The Chapter 9 project reads its settings from a `.env` file that is never committed. Copy the keys listed in section 9.10 of the book (`SECRET_KEY`, `DATABASE_URL`, `BASE_URL`, `RESEND_API_KEY`, and the Google and GitHub OAuth pairs) into your own `.env`. For OAuth testing, open the app at `http://localhost:8050`, not `127.0.0.1`, so the session cookie matches `BASE_URL`.

## Versions

The code was written and tested on Python 3.13 with:

| Package | Version |
|---|---|
| dash | 4.4.1 |
| plotly | 7.0.0 |
| dash-bootstrap-components | 2.0.4 |
| dash-ag-grid | 35.3.0 |
| pandas | 3.0.5 |
| yfinance (Chapter 6) | 1.7.0 |
| websockets, fastapi, uvicorn (Chapter 8) | 17.1, 0.141.1, 0.52.4 |

If an example does not behave as printed in the book, check your versions first. The `uv.lock` in each folder pins the exact set.

## Found a problem?

Open an issue on this repository, or email omonbude.emma@gmail.com. Corrections to the code and to the book are both welcome, and so are screenshots of what you built.

## License

The code in this repository is released under the MIT License. The text of the book is licensed separately under CC BY-NC-SA 4.0.
