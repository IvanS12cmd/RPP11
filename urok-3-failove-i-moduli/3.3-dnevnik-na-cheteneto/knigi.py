"""knigi.py — дневник на прочетените книги в текстов файл.

Задача 3.3. Един ред във файла е една книга:

    заглавие | автор | година на прочитане | оценка от 1 до 6

Правила: файлът се отваря само с with и само с явно кодиране;
повреден ред не спира програмата.
"""
from pathlib import Path

HERE = Path(__file__).parent
KNIGI = HERE / "knigi.txt"

MIN_RATING, MAX_RATING = 1, 6


def validate_book(title: str, author: str, year: int, rating: int) -> None:
    """Проверява данните за една книга. Вдига ValueError, ако нещо не е наред.

    Заглавието и авторът не са празни и не съдържат '|' или нов ред (иначе
    редът във файла ще се чете като повреден), годината е цяло число,
    а оценката е цяло число от 1 до 6.
    """
    for name, text in (("заглавие", title), ("автор", author)):
        if not text.strip():
            raise ValueError(f"Празно {name}")
        if "|" in text or "\n" in text:
            raise ValueError(f"В полето '{name}' не може да има '|' или нов ред")
    if not isinstance(year, int):
        raise ValueError(f"Годината трябва да е цяло число, а не {year!r}")
    if not isinstance(rating, int) or not MIN_RATING <= rating <= MAX_RATING:
        raise ValueError(f"Оценката трябва да е цяло число от {MIN_RATING} до {MAX_RATING}, а не {rating!r}")


def parse_line(line: str):
    """Разбира един ред от файла. Връща речник с книгата или None при повреден ред.

    Повреден е ред с друг брой полета, с година или оценка, която не е число,
    или с оценка извън 1..6. Функцията не чете файлове и не печата.
    """
    parts = [part.strip() for part in line.split("|")]
    if len(parts) != 4:
        return None
    title, author, year_text, rating_text = parts
    try:
        year, rating = int(year_text), int(rating_text)
    except ValueError:
        return None
    if not MIN_RATING <= rating <= MAX_RATING:
        return None
    return {"zaglavie": title, "avtor": author, "godina": year, "otsenka": rating}


def add_book(path, title: str, author: str, year: int, rating: int) -> None:
    """Добавя ред в края на файла, без да презаписва старите.

    При неправилни данни (например оценка извън 1..6) вдига ValueError
    и не пише нищо. Ако последният ред във файла няма нов ред накрая,
    добавя го, за да не се слеят две книги в един ред.
    """
    validate_book(title, author, year, rating)
    with open(path, "a+", encoding="utf-8") as f:
        f.seek(0)
        content = f.read()
        prefix = "\n" if content and not content.endswith("\n") else ""
        f.write(f"{prefix}{title} | {author} | {year} | {rating}\n")


def load_books(path) -> tuple:
    """Чете файла. Връща (книги, брой_пропуснати_редове).

    Всяка книга е речник с ключове "zaglavie", "avtor",
    "godina" (int) и "otsenka" (int).
    Пропуска повредените редове: с друг брой полета, с година
    или оценка, която не е число, или с оценка извън 1..6.
    Празните редове не се броят за повредени.
    Ако файлът липсва, дневникът е празен: връща ([], 0).
    Файлът се чете като UTF-8 (с или без BOM).
    """
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return [], 0
    books, skipped = [], 0
    for line in lines:
        if not line.strip():
            continue
        book = parse_line(line)
        if book is None:
            skipped += 1
        else:
            books.append(book)
    return books, skipped


def stats(books: list) -> dict:
    """Връща речник с ключове:

    "sredna_otsenka" — средната оценка (None при празен списък),
    "nay_dobra"      — заглавието с най-висока оценка
                       (при равенство — първото във файла; None при празен списък),
    "po_godini"      — речник {година: брой книги}.
    """
    if not books:
        return {"sredna_otsenka": None, "nay_dobra": None, "po_godini": {}}
    per_year = {}
    for book in books:
        per_year[book["godina"]] = per_year.get(book["godina"], 0) + 1
    return {
        "sredna_otsenka": sum(book["otsenka"] for book in books) / len(books),
        "nay_dobra": max(books, key=lambda book: book["otsenka"])["zaglavie"],
        "po_godini": dict(sorted(per_year.items())),
    }


def build_report(books: list) -> list:
    """Редовете на отчета (без да ги записва никъде).

    Книгите са подредени по оценка (от най-високата), а при равенство по заглавие.
    """
    summary = stats(books)
    average = summary["sredna_otsenka"]
    lines = [
        "ДНЕВНИК НА ЧЕТЕНЕТО",
        f"Прочетени книги: {len(books)}",
        f"Средна оценка: {'няма данни' if average is None else f'{average:.2f}'}",
        f"Най-добра книга: {summary['nay_dobra'] or 'няма данни'}",
        "",
        "По години:",
    ]
    lines += [f"  {year}: {count} бр." for year, count in summary["po_godini"].items()]
    lines += ["", "Книги (по оценка):"]
    ranked = sorted(books, key=lambda book: (-book["otsenka"], book["zaglavie"]))
    lines += [f"  {book['otsenka']}  {book['zaglavie']} — {book['avtor']} ({book['godina']})"
              for book in ranked]
    return lines


def export_report(path, books: list) -> None:
    """Записва подреден текстов отчет в UTF-8."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(build_report(books)) + "\n")


if __name__ == "__main__":
    books, skipped = load_books(KNIGI)
    print(f"Заредени {len(books)} книги, пропуснати {skipped} повредени реда.")
