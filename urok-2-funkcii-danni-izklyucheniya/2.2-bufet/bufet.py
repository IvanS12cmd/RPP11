"""bufet.py — училищният бюфет: речници, функции и йерархия от изключения.

Задача 2.2: разширете модула с функциите от README.md на урока.
"""
import copy

TEACHER_DISCOUNT = 0.10

STOCK = {
    "банан":   {"cena": 1.20, "kolichestvo": 10},
    "кроасан": {"cena": 2.50, "kolichestvo": 4},
    "вода":    {"cena": 0.90, "kolichestvo": 25},
    "сандвич": {"cena": 3.80, "kolichestvo": 0},
}


class BufetError(Exception):
    """Базово изключение на бюфета — всички останали наследяват него."""


class UnknownProduct(BufetError):
    pass


class NotEnoughStock(BufetError):
    def __init__(self, name, wanted, available):
        super().__init__(f"Искаш {wanted} бр. '{name}', а има само {available} бр.")
        self.name, self.wanted, self.available = name, wanted, available


def sell(stock: dict, name: str, quantity: int) -> float:
    """Продава quantity броя от name. Връща сумата."""
    if name not in stock:
        raise UnknownProduct(f"Няма продукт '{name}' в бюфета")
    if quantity <= 0:
        raise ValueError("Количеството трябва да е положително цяло число")
    item = stock[name]
    if item["kolichestvo"] < quantity:
        raise NotEnoughStock(name, quantity, item["kolichestvo"])
    item["kolichestvo"] -= quantity
    return round(item["cena"] * quantity, 2)


def receipt(stock: dict, order: list) -> tuple:
    """Обработва поръчка. Връща (сума, редове на бележката, проблеми)."""
    total, lines, problems = 0.0, [], []
    for name, quantity in order:
        try:
            price = sell(stock, name, quantity)
        except BufetError as err:
            problems.append(str(err))
        except ValueError as err:
            problems.append(f"Невалидно количество за '{name}': {err}")
        else:
            total += price
            lines.append(f"{name:10s} x{quantity:2d} = {price:6.2f} лв.")
    return round(total, 2), lines, problems


def low_stock(stock: dict, threshold: int = 5) -> list:
    """Имена на продуктите, които трябва да се доставят."""
    return sorted(name for name, item in stock.items()
                  if item["kolichestvo"] <= threshold)


class PriceError(BufetError):
    """Цената трябва да е по-голяма от нула. Носи името на продукта и цената."""

    def __init__(self, name, cena):
        super().__init__(f"Невалидна цена {cena} за '{name}': трябва да е по-голяма от 0")
        self.name, self.cena = name, cena


def deliver(stock: dict, name: str, quantity: int, cena: float = None) -> int:
    """Добавя quantity броя от name и връща новата наличност.

    За нов продукт цената е задължителна. Ако продуктът вече има запис и е
    дадена цена, тя става новата му цена. Ако се вдигне изключение, наличността
    не се променя. Вдига ValueError при quantity <= 0, UnknownProduct за нов
    продукт без цена и PriceError при цена <= 0.
    """
    if quantity <= 0:
        raise ValueError("Количеството трябва да е положително цяло число")
    if name not in stock and cena is None:
        raise UnknownProduct(f"'{name}' е нов продукт: трябва да се зададе цена")
    if cena is not None and cena <= 0:
        raise PriceError(name, cena)
    item = stock.setdefault(name, {"cena": cena, "kolichestvo": 0})
    if cena is not None:
        item["cena"] = cena
    item["kolichestvo"] += quantity
    return item["kolichestvo"]


def apply_discount(total: float, is_teacher: bool) -> float:
    """Връща сумата за плащане: 10% отстъпка за учители, закръглена до стотинка."""
    if is_teacher:
        total *= 1 - TEACHER_DISCOUNT
    return round(total, 2)


def daily_report(stock: dict) -> dict:
    """Връща справка за наличността: обща стойност, най-скъп продукт, изчерпани."""
    return {
        "obshta_stoynost": round(sum(i["cena"] * i["kolichestvo"] for i in stock.values()), 2),
        "nay_skap": max(stock, key=lambda name: stock[name]["cena"], default=None),
        "izcherpani": sum(1 for item in stock.values() if item["kolichestvo"] == 0),
    }


def run_scenario(title: str, action) -> str:
    """Изпълнява един сценарий и връща едно изречение за резултата или за грешката."""
    try:
        result = action()
    except (BufetError, ValueError) as err:
        return f"{title}: {type(err).__name__} — {err}"
    return f"{title}: {result}"


if __name__ == "__main__":
    original = copy.deepcopy(STOCK)  # чисто копие за сценариите, преди бележката да промени STOCK
    order = [("банан", 2), ("кроасан", 1), ("сандвич", 1),
             ("пица", 1), ("вода", -3), ("вода", 2)]
    total, lines, problems = receipt(STOCK, order)

    print("КАСОВА БЕЛЕЖКА")
    for line in lines:
        print("  " + line)
    print(f"  ОБЩО: {total:.2f} лв.")

    if problems:
        print("\nНЕИЗПЪЛНЕНИ ПОЗИЦИИ:")
        for problem in problems:
            print(f"  - {problem}")

    print(f"\nЗА ДОСТАВКА: {', '.join(low_stock(STOCK))}")

    scenarios = [
        ("1. Доставка на кроасан (4 + 6)",
         lambda: deliver(copy.deepcopy(original), "кроасан", 6)),
        ("2. Нов продукт йогурт с цена",
         lambda: deliver(copy.deepcopy(original), "йогурт", 12, cena=1.60)),
        ("3. Нов продукт без цена",
         lambda: deliver(copy.deepcopy(original), "йогурт", 12)),
        ("4. Нов продукт с цена 0",
         lambda: deliver(copy.deepcopy(original), "йогурт", 12, cena=0)),
        ("5. Доставка на 0 броя",
         lambda: deliver(copy.deepcopy(original), "банан", 0)),
        ("6. Сметка 6.70 лв. за учител",
         lambda: apply_discount(6.70, True)),
        ("7. Сметка 6.70 лв. за ученик",
         lambda: apply_discount(6.70, False)),
        ("8. Справка за деня",
         lambda: daily_report(copy.deepcopy(original))),
        ("9. Справка за празен бюфет",
         lambda: daily_report({})),
    ]
    print("\nСЦЕНАРИИ")
    for title, action in scenarios:
        print("  " + run_scenario(title, action))
