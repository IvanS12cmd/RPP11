"""load_config.py — чете настройки от вида ключ=число.

Задача 2.3: в тази функция има четири проблема. Намерете ги,
опишете ги в otgovori.md и напишете поправена версия тук.
"""
from pathlib import Path

HERE = Path(__file__).parent  # папката на този файл, откъдето и да го стартирате


def parse_line(line: str, number: int) -> tuple:
    """Разбира един ред 'ключ=число' и връща двойката (ключ, число).

    Вдига ValueError с номера на реда, ако редът няма '=' или ключът е празен,
    или ако стойността не е цяло число.
    """
    key, sep, value = line.partition("=")
    key, value = key.strip(), value.strip()
    if not sep or not key:
        raise ValueError(f"Ред {number}: очаква се 'ключ=число', а има {line!r}")
    try:
        return key, int(value)
    except ValueError:
        raise ValueError(f"Ред {number}: '{value}' не е цяло число") from None


def load_config(path) -> dict:
    """Чете файл с настройки 'ключ=число' и връща речник.

    Пропуска празните редове и редовете, започващи с #. Вдига ValueError
    при повреден ред. FileNotFoundError не се прехваща: какво да се прави
    при липсващ файл, решава викащият код.
    """
    config = {}
    with open(path, encoding="utf-8") as f:
        for number, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = parse_line(line, number)
            config[key] = value
    return config


if __name__ == "__main__":
    for name in ("nastroyki.txt", "nastroyki_povredeni.txt", "nyama_takav_fail.txt"):
        try:
            result = load_config(HERE / name)
        except (FileNotFoundError, ValueError) as err:
            result = f"{type(err).__name__}: {err}"
        print(f"{name:28s} -> {result}")
