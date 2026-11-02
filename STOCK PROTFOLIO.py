#!/usr/bin/env python3
"""Stock Portfolio Tracker: a simple console application.

The user enters stock symbols and quantities. The program looks up each price
in a hardcoded dictionary, calculates the value of every holding and the total
investment, displays a summary table and can optionally save it to a .txt or
.csv file.

Concepts used: dictionary, input/output, basic arithmetic, file handling.

Run:
    python stock_portfolio_tracker.py
"""

import csv
from datetime import datetime
from pathlib import Path

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
# Hardcoded, illustrative prices in USD (not live market data).
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "MSFT": 410,
    "AMZN": 175,
    "META": 480,
    "NVDA": 900,
    "NFLX": 600,
    "INTC": 35,
    "AMD": 160,
}

CURRENCY = "$"
OUTPUT_DIR = Path(__file__).resolve().parent
DONE_COMMANDS = ("done", "d")


# --------------------------------------------------------------------------- #
# Formatting helpers
# --------------------------------------------------------------------------- #
def money(amount: float) -> str:
    """Format a number as currency, e.g. 1234.5 -> '$1,234.50'."""
    return f"{CURRENCY}{amount:,.2f}"


def print_banner() -> None:
    """Print the program title."""
    print("=" * 52)
    print("            STOCK PORTFOLIO TRACKER")
    print("=" * 52)


def print_available_stocks() -> None:
    """Show every stock the user can choose, with its price."""
    print("\nAvailable stocks:")
    for symbol, price in STOCK_PRICES.items():
        print(f"  {symbol:<6} {money(price):>10}")
    print()


# --------------------------------------------------------------------------- #
# User input
# --------------------------------------------------------------------------- #
def ask_stock_symbol() -> str | None:
    """Ask for a stock symbol. Return None when the user is finished."""
    while True:
        answer = input("Stock symbol (or 'done' to finish): ").strip().upper()

        if answer.lower() in DONE_COMMANDS:
            return None
        if answer in STOCK_PRICES:
            return answer
        if answer == "":
            print("  Please enter a stock symbol.")
        else:
            print(f"  '{answer}' is not in the price list. "
                  f"Choose from: {', '.join(STOCK_PRICES)}")


def ask_quantity(symbol: str) -> int:
    """Ask for a positive whole number of shares."""
    while True:
        answer = input(f"Quantity of {symbol}: ").strip()

        if not answer.isdigit():
            print("  Please enter a whole number (e.g. 10).")
        elif int(answer) <= 0:
            print("  Quantity must be greater than zero.")
        else:
            return int(answer)


def collect_portfolio() -> dict[str, int]:
    """Collect {symbol: quantity} from the user until they type 'done'.

    Entering the same stock twice adds to the existing quantity.
    """
    portfolio: dict[str, int] = {}

    while True:
        symbol = ask_stock_symbol()
        if symbol is None:
            break

        quantity = ask_quantity(symbol)
        portfolio[symbol] = portfolio.get(symbol, 0) + quantity
        print(f"  Added {quantity} x {symbol}.\n")

    return portfolio


# --------------------------------------------------------------------------- #
# Calculations
# --------------------------------------------------------------------------- #
def calculate_holdings(portfolio: dict[str, int]) -> list[dict]:
    """Return one record per stock: symbol, quantity, price and total value."""
    holdings = []
    for symbol, quantity in portfolio.items():
        price = STOCK_PRICES[symbol]
        holdings.append({
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "value": quantity * price,
        })
    return holdings


def calculate_total(holdings: list[dict]) -> float:
    """Return the total investment value of all holdings."""
    total = 0
    for holding in holdings:
        total += holding["value"]
    return total


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
def build_report(holdings: list[dict], total: float) -> str:
    """Build the portfolio summary as a printable / saveable text report."""
    line = "-" * 52
    lines = [
        f"Portfolio Summary  ({datetime.now():%Y-%m-%d %H:%M})",
        line,
        f"{'Stock':<8}{'Qty':>6}{'Price':>14}{'Value':>20}",
        line,
    ]
    for h in holdings:
        lines.append(
            f"{h['symbol']:<8}{h['quantity']:>6}"
            f"{money(h['price']):>14}{money(h['value']):>20}"
        )
    lines += [line, f"{'TOTAL INVESTMENT':<28}{money(total):>24}", line]
    return "\n".join(lines)


def save_as_txt(path: Path, report: str) -> None:
    """Save the text report to a .txt file."""
    path.write_text(report + "\n", encoding="utf-8")


def save_as_csv(path: Path, holdings: list[dict], total: float) -> None:
    """Save the holdings and total to a .csv file."""
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Stock", "Quantity", "Price", "Value"])
        for h in holdings:
            writer.writerow([h["symbol"], h["quantity"], h["price"], h["value"]])
        writer.writerow(["TOTAL", "", "", total])


def ask_save_format() -> str | None:
    """Ask whether to save the result. Return 'txt', 'csv' or None."""
    print("\nSave this summary to a file?")
    print("  1) Text file (.txt)")
    print("  2) CSV file  (.csv)")
    print("  3) No, thanks")

    while True:
        choice = input("Choose 1, 2 or 3: ").strip()
        if choice == "1":
            return "txt"
        if choice == "2":
            return "csv"
        if choice == "3":
            return None
        print("  Please enter 1, 2 or 3.")


def save_results(holdings: list[dict], total: float, report: str) -> None:
    """Save the results in the format chosen by the user (if any)."""
    file_format = ask_save_format()
    if file_format is None:
        return

    filename = f"portfolio_{datetime.now():%Y%m%d_%H%M%S}.{file_format}"
    path = OUTPUT_DIR / filename

    try:
        if file_format == "txt":
            save_as_txt(path, report)
        else:
            save_as_csv(path, holdings, total)
    except OSError as error:
        print(f"\nSorry, the file could not be saved: {error}")
    else:
        print(f"\nSaved to: {path}")


# --------------------------------------------------------------------------- #
# Program entry point
# --------------------------------------------------------------------------- #
def main() -> None:
    """Run the stock portfolio tracker."""
    print_banner()
    print_available_stocks()

    try:
        portfolio = collect_portfolio()

        if not portfolio:
            print("\nNo stocks were entered. Nothing to calculate.")
        else:
            holdings = calculate_holdings(portfolio)
            total = calculate_total(holdings)
            report = build_report(holdings, total)

            print("\n" + report)
            save_results(holdings, total, report)
    except (KeyboardInterrupt, EOFError):
        print()  # Move to a clean line after Ctrl+C / Ctrl+D.

    print("\nThank you for using the Stock Portfolio Tracker. Goodbye!")


if __name__ == "__main__":
    main()