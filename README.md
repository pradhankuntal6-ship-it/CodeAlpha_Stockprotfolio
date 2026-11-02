# Stock Portfolio Tracker

A simple console application written in Python. Enter stock symbols and the number of shares you own, and the program calculates the value of each holding and your total investment. You can also save the summary as a `.txt` or `.csv` file.

> Prices are **hardcoded and illustrative**. They are not live market data and should not be used for real investment decisions.

## Features

- Choose from 10 built-in stocks with preset USD prices
- Enter as many holdings as you like, then type `done` to finish
- Entering the same stock twice adds to the existing quantity
- Input validation for symbols (case-insensitive) and quantities (positive whole numbers only)
- Formatted summary table with per-stock value and total investment
- Optional export to a timestamped `.txt` or `.csv` file
- Handles `Ctrl+C` / `Ctrl+D` gracefully
- No external dependencies (standard library only)

## Requirements

- **Python 3.10 or newer** (the code uses type hints such as `str | None` and `dict[str, int]`)

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

2. Run the program:

   ```bash
   python "STOCK PROTFOLIO.py"
   ```

   Use `python3` on some systems. The filename contains a space, so keep the quotes, or rename the file to `stock_portfolio_tracker.py` (the name used in the script's own docstring) and run `python stock_portfolio_tracker.py`.

## Available Stocks

| Symbol | Price (USD) |
|--------|------------:|
| AAPL   | $180 |
| TSLA   | $250 |
| GOOGL  | $140 |
| MSFT   | $410 |
| AMZN   | $175 |
| META   | $480 |
| NVDA   | $900 |
| NFLX   | $600 |
| INTC   | $35 |
| AMD    | $160 |

## How to Use

1. Type a stock symbol from the list (for example `AAPL`).
2. Enter how many shares you own.
3. Repeat for more stocks, then type `done` (or `d`) when finished.
4. View the portfolio summary.
5. Choose whether to save it as a text file, a CSV file, or not at all.

### Example Session

```
====================================================
            STOCK PORTFOLIO TRACKER
====================================================

Stock symbol (or 'done' to finish): aapl
Quantity of AAPL: 10
  Added 10 x AAPL.

Stock symbol (or 'done' to finish): tsla
Quantity of TSLA: 5
  Added 5 x TSLA.

Stock symbol (or 'done' to finish): done

Portfolio Summary  (2026-11-03 12:00)
----------------------------------------------------
Stock      Qty         Price               Value
----------------------------------------------------
AAPL        10       $180.00           $1,800.00
TSLA         5       $250.00           $1,250.00
----------------------------------------------------
TOTAL INVESTMENT                       $3,050.00
----------------------------------------------------

Save this summary to a file?
  1) Text file (.txt)
  2) CSV file  (.csv)
  3) No, thanks
Choose 1, 2 or 3:
```

## Saved Files

Files are saved in the same folder as the script with a timestamped name, for example:

```
portfolio_20261103_120000.txt
portfolio_20261103_120000.csv
```

The CSV file has the columns `Stock, Quantity, Price, Value`, followed by a `TOTAL` row.

## Configuration

At the top of the script you can change:

```python
STOCK_PRICES = {"AAPL": 180, "TSLA": 250, ...}  # add or edit stocks and prices
CURRENCY = "$"                                  # currency symbol
```

## Code Overview

| Function | Purpose |
|----------|---------|
| `ask_stock_symbol()` / `ask_quantity()` | Validated user input |
| `collect_portfolio()` | Builds the `{symbol: quantity}` dictionary |
| `calculate_holdings()` / `calculate_total()` | Per-stock values and the total |
| `build_report()` | Creates the formatted summary text |
| `save_as_txt()` / `save_as_csv()` | File export |
| `main()` | Program entry point |

Concepts demonstrated: dictionaries, input/output, basic arithmetic, file handling, and error handling.

## Ideas for Improvement

- Fetch live prices from a market data API
- Support fractional shares
- Load and save portfolios between sessions
- Show each holding's percentage of the total
- Add unit tests for the calculation functions

## Contributing

Suggestions and pull requests are welcome.
