"""citat.py — цитат на деня.

Цитатите се четат от файла data/citati.txt (формат: текст | автор),
а не са записани в кода. Програмата работи и без инсталиран пакет rich,
но тогава сама казва какво липсва.
"""
import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

# Пътят е спрямо самия файл citat.py, за да работи от всяка работна папка.
QUOTES_FILE = Path(__file__).parent / "data" / "citati.txt"


def load_quotes(path: Path) -> list:
    """Чете файла и връща списък от двойки (текст, автор)."""
    quotes = []
    with open(path, encoding="utf-8") as file:
        for number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue  # празните редове се пропускат
            if "|" not in line:
                raise ValueError(f"Ред {number} в {path.name} няма разделител '|': {line!r}")
            text, author = line.rsplit("|", 1)  # разделяме по последния '|'
            quotes.append((text.strip(), author.strip()))
    if not quotes:
        raise ValueError(f"Файлът {path.name} не съдържа цитати.")
    return quotes


def quote_of_the_day(quotes: list, day: datetime.date) -> tuple:
    """Един и същ цитат за целия ден, различен за всеки ден."""
    return quotes[day.toordinal() % len(quotes)]


def main() -> None:
    try:
        quotes = load_quotes(QUOTES_FILE)
    except (OSError, ValueError) as error:
        print(f"Грешка при четене на цитатите: {error}")
        return

    today = datetime.date.today()
    text, author = quote_of_the_day(quotes, today)
    if HAS_RICH:
        Console().print(Panel(f"[italic]{text}[/italic]\n\n[bold]— {author}[/bold]",
                              title=f"Цитат за {today:%d.%m.%Y}", border_style="cyan"))
    else:
        print("Пакетът 'rich' не е инсталиран в тази среда.")
        print("Направи:  python -m pip install -r requirements.txt")
        print(f"\n{text}\n— {author}")


if __name__ == "__main__":
    main()
