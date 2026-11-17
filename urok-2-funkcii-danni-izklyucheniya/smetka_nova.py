"""smetka_nova.py — разделя сметката поравно между приятели (поправената версия).

Какво е различно от smetka_stara.py:
  * невалидният вход се проверява във функции, които вдигат собствено
    изключение InputError с ясно съобщение;
  * потребителят се пита отново, вместо програмата да гръмне;
  * отрицателна сума, нула хора, "nan" и "inf" не дават мълчаливо грешен резултат.
"""
import math


class InputError(Exception):
    """Невалиден вход от потребителя. Носи името на полето и въведения текст."""

    def __init__(self, field: str, text: str, reason: str):
        super().__init__(f"{field}: '{text}' {reason}")
        self.field, self.text = field, text


def parse_amount(text: str) -> float:
    """Превръща текст в положителна сума. Приема и запетая за десетичен знак."""
    try:
        value = float(text.strip().replace(",", "."))
    except ValueError:
        raise InputError("Сума", text, "не е число") from None
    if not math.isfinite(value) or value <= 0:
        raise InputError("Сума", text, "трябва да е положително число")
    return value


def parse_people(text: str) -> int:
    """Превръща текст в брой хора (цяло число, поне 1)."""
    try:
        count = int(text.strip())
    except ValueError:
        raise InputError("Брой хора", text, "не е цяло число") from None
    if count < 1:
        raise InputError("Брой хора", text, "трябва да е поне 1")
    return count


def split_bill(total: float, people: int) -> float:
    """Връща колко плаща всеки, закръглено до стотинка. Вдига ValueError при people < 1."""
    if people < 1:
        raise ValueError("Хората трябва да са поне 1")
    return round(total / people, 2)


def ask(prompt: str, parser):
    """Пита, докато потребителят въведе валидна стойност, и я връща."""
    while True:
        try:
            return parser(input(prompt))
        except InputError as err:
            print(f"  Грешка: {err}. Опитай пак.")


def main() -> None:
    total = ask("Обща сметка (лв.): ", parse_amount)
    people = ask("Брой хора: ", parse_people)
    print(f"Всеки плаща {split_bill(total, people):.2f} лв.")


if __name__ == "__main__":
    main()
