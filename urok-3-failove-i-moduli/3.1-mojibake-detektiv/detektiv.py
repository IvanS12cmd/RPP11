"""detektiv.py — в какво кодиране е записан файлът?

Задача 3.1. Четирите файла tekst_a.txt … tekst_d.txt съдържат един
и същ текст, но са записани в различни кодирания.
"""
from pathlib import Path

HERE = Path(__file__).parent
FILES = ["tekst_a.txt", "tekst_b.txt", "tekst_c.txt", "tekst_d.txt"]
ENCODINGS = ["utf-8", "cp1251", "utf-16", "latin-1"]

# Знаци, които почти никога не се срещат в български текст,
# но са типични за mojibake. Допълнете списъка, ако е нужно.
SUSPICIOUS = "ÃÐÑñÿÇäðàâåé"

BULGARIAN_LETTERS = "абвгдежзийклмнопрстуфхцчшщъьюя"
MIN_BULGARIAN_SHARE = 0.8  # поне толкова от буквите трябва да са български


def read_text(path, encoding: str) -> str:
    """Целият текст на файла, прочетен с даденото кодиране.

    UnicodeDecodeError не се прехваща тук — нека реши викащият.
    (С "utf-16" и файл без BOM open() вдига UnicodeError, родителя на UnicodeDecodeError.)
    """
    with open(path, "r", encoding=encoding) as f:
        return f.read()


def preview(path, encoding: str, n: int = 40) -> str:
    """Първите n символа от файла, прочетен с даденото кодиране.

    Файлът се чете целия, а не само първите n символа, за да се види
    грешното кодиране дори когато повреденият байт е по-нататък.
    Ако файлът не може да се прочете с това кодиране,
    UnicodeDecodeError не се прехваща тук — нека реши викащият.
    """
    return read_text(path, encoding)[:n]


def looks_bulgarian(text: str) -> bool:
    """Прилича ли текстът на български?

    Да, ако повечето от буквите му са български, няма знаци от SUSPICIOUS
    и няма управляващи знаци (като NUL), които не са нов ред или табулация.
    """
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return False
    if any(ch in SUSPICIOUS for ch in text):
        return False
    if any(ord(ch) < 32 and ch not in "\n\r\t" for ch in text):
        return False
    bulgarian = sum(ch.lower() in BULGARIAN_LETTERS for ch in letters)
    return bulgarian / len(letters) >= MIN_BULGARIAN_SHARE


def guess_encoding(path):
    """Името на първото кодиране от ENCODINGS, при което текстът
    съдържа български букви и няма знаци от SUSPICIOUS.
    None, ако нито едно не пасва.
    """
    for encoding in ENCODINGS:
        try:
            text = read_text(path, encoding)
        except UnicodeError:  # хваща UnicodeDecodeError и "utf-16 без BOM"
            continue
        if looks_bulgarian(text):
            return encoding
    return None


def main() -> None:
    for name in FILES:
        print(f"\n=== {name} ===")
        for enc in ENCODINGS:
            try:
                print(f"  {enc:8s} -> {preview(HERE / name, enc)!r}")
            except UnicodeDecodeError as err:
                print(f"  {enc:8s} -> не става ({err.reason})")
            except UnicodeError as err:  # utf-16 за файл без BOM
                print(f"  {enc:8s} -> не става ({err})")
        print(f"  ДОГАДКА: {guess_encoding(HERE / name)}")


if __name__ == "__main__":
    main()

# СТЪПКА 4: кога методът ви би сгрешил? Отговорете тук в коментар.
#
# 1. Файл с BOM (tekst_d.txt). Методът връща "utf-8", но невидимият знак
#    \ufeff остава в началото на текста. Правилното кодиране е "utf-8-sig".
#
# 2. Кодирания, които не гърмят. latin-1 пасва на всеки байт, затова никога
#    не вдига грешка и дава безсмислица. cp1251 също пасва почти на всичко.
#    Методът ги различава от правилното само по това, че излиза текст без
#    български букви, а други кирилски кодирания (cp866, koi8-r, MIK) дават
#    кирилица и могат да минат като верни.
#
# 3. Текст, който не прилича на български: само цифри, само латиница или
#    много чужди думи (под 80% български букви). Методът връща None, макар
#    кодирането да е правилно. Същото става, ако в български текст има
#    име със знак от SUSPICIOUS, например "café".
#
# 4. Много кратки файлове. С няколко байта данни е лесно грешно кодиране
#    случайно да даде валиден текст, а правилното да не мине проверката.
#
# 5. "utf-16" без BOM. open() вдига UnicodeError (не UnicodeDecodeError), затова
#    except UnicodeDecodeError би пропуснал този случай. Хващам UnicodeError,
#    който включва и двата.
#
# 6. Редът в ENCODINGS има значение: първото кодиране, което мине
#    проверката, печели. Затова utf-8 е първо: то почти никога не пасва
#    на чужд файл по случайност, а cp1251 би приело повечето UTF-8 файлове.
