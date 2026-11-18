"""analiz.py — чистата логика. Не знае нищо за файлове и печатане."""
import datetime

DAYS = ["понеделник", "вторник", "сряда", "четвъртък", "петък", "събота", "неделя"]


def parse_sales(lines: list) -> tuple:
    """Разбира редове от вида 'дата | продукт | брой | цена'.

    Празните редове и редовете, започващи с #, се пропускат. Повреден ред
    (не 4 полета, или брой и цена, които не са числа) не спира обработката,
    а се записва като съобщение в списъка с проблеми.
    Връща двойка (продажби, проблеми).
    """
    sales, problems = [], []
    for number, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [part.strip() for part in line.split("|")]
        if len(parts) != 4:
            problems.append(f"Ред {number}: очаквах 4 полета, а са {len(parts)} — пропускам")
            continue
        date, product, count, price = parts
        try:
            quantity, unit_price = int(count), float(price)
        except ValueError:
            problems.append(f"Ред {number}: '{count}' или '{price}' не е число — пропускам")
        else:
            sales.append({"data": date, "produkt": product, "broy": quantity, "cena": unit_price})
    return sales, problems


def turnover_by_product(sales: list) -> dict:
    """Оборотът (брой × цена) за всеки продукт."""
    result = {}
    for sale in sales:
        amount = sale["broy"] * sale["cena"]
        result[sale["produkt"]] = result.get(sale["produkt"], 0) + amount
    return result


def turnover_by_day(sales: list) -> dict:
    """Оборотът за всеки ден."""
    result = {}
    for sale in sales:
        result[sale["data"]] = result.get(sale["data"], 0) + sale["broy"] * sale["cena"]
    return result


def ranked_products(by_product: dict) -> list:
    """Двойки (продукт, оборот), подредени от най-големия оборот към най-малкия."""
    return sorted(by_product.items(), key=lambda pair: -pair[1])


def weekday_name(date_text: str) -> str:
    """Името на деня от седмицата за дата във вида 2026-10-12."""
    return DAYS[datetime.date.fromisoformat(date_text).weekday()]


def best_day(by_day: dict):
    """Денят с най-голям оборот (при равенство — по-ранният). None, ако няма дни."""
    if not by_day:
        return None
    return max(sorted(by_day), key=by_day.get)


def units_by_product(sales: list) -> dict:
    """Колко броя са продадени от всеки продукт."""
    result = {}
    for sale in sales:
        result[sale["produkt"]] = result.get(sale["produkt"], 0) + sale["broy"]
    return result


def top_selling(units: dict):
    """Двойка (продукт, брой) за най-продавания продукт. None, ако няма продукти."""
    if not units:
        return None
    name = max(units, key=units.get)
    return name, units[name]


def average_units(units: dict) -> float:
    """Средно продадени бройки на продукт. 0.0, ако няма продукти."""
    if not units:
        return 0.0
    return sum(units.values()) / len(units)


def total_turnover(sales: list) -> float:
    """Общият оборот от всички продажби."""
    total = 0
    for sale in sales:
        total = total + sale["broy"] * sale["cena"]
    return total


def build_report(total: float, by_product: dict, by_day: dict) -> list:
    """Редовете на седмичния отчет (без да ги записва никъде)."""
    lines = ["ОТЧЕТ ЗА СЕДМИЦАТА", f"Общ оборот: {total:.2f} лв.", "", "По продукти:"]
    lines += [f"  {product}: {amount:.2f} лв." for product, amount in ranked_products(by_product)]
    lines += ["", "По дни:"]
    lines += [f"  {day}: {by_day[day]:.2f} лв." for day in sorted(by_day)]
    return lines


if __name__ == "__main__":
    # Проверките работят, без на диска да има какъвто и да е файл.
    lines = ["# заглавие", "2026-10-12 | банан | 2 | 1.50", "2026-10-12 | вода | 3 | 1.00",
             "2026-10-13 | банан | 1 | 1.50", "лош ред", "2026-10-13 | вода | пет | 1.00", ""]
    sales, problems = parse_sales(lines)
    assert len(sales) == 3
    assert problems == ["Ред 5: очаквах 4 полета, а са 1 — пропускам",
                        "Ред 6: 'пет' или '1.00' не е число — пропускам"]
    assert parse_sales([]) == ([], [])

    by_product, by_day = turnover_by_product(sales), turnover_by_day(sales)
    assert ranked_products(by_product) == [("банан", 4.5), ("вода", 3.0)]
    assert by_day == {"2026-10-12": 6.0, "2026-10-13": 1.5}
    assert best_day(by_day) == "2026-10-12" and best_day({}) is None
    assert weekday_name("2026-10-12") == "понеделник"

    units = units_by_product(sales)
    assert top_selling(units) == ("банан", 3)       # равенство -> първият
    assert average_units(units) == 3.0 and average_units({}) == 0.0
    assert total_turnover(sales) == 7.5
    assert build_report(7.5, by_product, by_day)[:4] == [
        "ОТЧЕТ ЗА СЕДМИЦАТА", "Общ оборот: 7.50 лв.", "", "По продукти:"]
    print("analiz.py: всички проверки минаха.")
