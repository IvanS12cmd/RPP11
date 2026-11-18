"""main.py — само сглобява: чете, вика анализа и печата."""
from pathlib import Path

from analiz import (average_units, best_day, build_report, parse_sales, ranked_products,
                    top_selling, total_turnover, turnover_by_day, turnover_by_product,
                    units_by_product, weekday_name)
from chetene import read_lines, save_report

# Пътищата се смятат спрямо папката на main.py, затова програмата
# работи, откъдето и да я стартирате.
HERE = Path(__file__).parent
DATA_FILE = HERE / "data" / "prodazhbi.txt"
REPORT_FILE = HERE / "otchet.txt"


def show_products(by_product: dict) -> None:
    print("\nОБОРОТ ПО ПРОДУКТИ")
    for product, amount in ranked_products(by_product):
        print(f"  {product:10s} {amount:8.2f} лв.")


def show_days(by_day: dict) -> None:
    print("\nОБОРОТ ПО ДНИ")
    for day in sorted(by_day):
        print(f"  {day}  {weekday_name(day):11s}{by_day[day]:8.2f} лв.")
    print(f"  Най-добър ден: {best_day(by_day)}")


def show_best_seller(units: dict) -> None:
    name, count = top_selling(units)
    print(f"\nНАЙ-ПРОДАВАН ПРОДУКТ: {name} ({count} бр.)")
    print(f"Средно продадени бройки на продукт: {average_units(units):.1f}")


def main() -> None:
    print("АНАЛИЗ НА ПРОДАЖБИТЕ В БЮФЕТА")
    sales, problems = parse_sales(read_lines(DATA_FILE))
    for problem in problems:
        print(f"  {problem}")
    print(f"Заредени {len(sales)} продажби, пропуснати {len(problems)} реда.")
    if not sales:
        return

    by_product, by_day = turnover_by_product(sales), turnover_by_day(sales)
    show_products(by_product)
    show_days(by_day)
    show_best_seller(units_by_product(sales))

    total = total_turnover(sales)
    print(f"\nОБЩ ОБОРОТ: {total:.2f} лв.")
    save_report(REPORT_FILE, build_report(total, by_product, by_day))
    print(f"Отчетът е записан в {REPORT_FILE.name}")


if __name__ == "__main__":
    main()
