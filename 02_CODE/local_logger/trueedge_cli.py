import sys

import logger
import simulate_trades
import metrics_demo
import metrics_by_strategy
import generate_html_report


def print_menu() -> None:
    print()
    print("=== TRUEEDGE Local CLI ===")
    print("1) Log a single demo trade (logger.py)")
    print("2) Simulate multiple trades (simulate_trades.py)")
    print("3) Show basic metrics (metrics_demo.py)")
    print("4) Show metrics by strategy/account (metrics_by_strategy.py)")
    print("5) Generate HTML report (generate_html_report.py)")
    print("0) Exit")
    print()


def main() -> None:
    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            print("\n[RUN] logger.py → single demo trade")
            logger.main()
        elif choice == "2":
            print("\n[RUN] simulate_trades.py → multiple simulated trades")
            simulate_trades.main()
        elif choice == "3":
            print("\n[RUN] metrics_demo.py → basic metrics")
            metrics_demo.main()
        elif choice == "4":
            print("\n[RUN] metrics_by_strategy.py → grouped metrics")
            metrics_by_strategy.main()
        elif choice == "5":
            print("\n[RUN] generate_html_report.py → HTML report")
            generate_html_report.main()
            print("\n[INFO] Open reports/index.html in your browser to view the report.")
        elif choice == "0":
            print("Exiting TRUEEDGE CLI.")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted, exiting.")
        sys.exit(0)
