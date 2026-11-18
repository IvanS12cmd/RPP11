"""chetene.py — всичко, свързано с файлове. Само функции, които докосват диска."""


def read_lines(path) -> list:
    """Чете текстов файл в UTF-8 и връща редовете му.

    Ако файлът липсва или не е в UTF-8, програмата спира със ясно съобщение.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        raise SystemExit(f"Няма такъв файл: {path}")
    except UnicodeDecodeError:
        raise SystemExit(f"Файлът {path} не е в UTF-8. Опитай cp1251.")


def save_report(path, lines: list) -> None:
    """Записва редовете във файл в UTF-8, по един на ред."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
