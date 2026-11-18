"""detektiv_chardet.py — разширение към задача 3.1: моята догадка срещу chardet.

Изисква пакета chardet:  python -m pip install -r requirements.txt
Пуска се така (в същата папка е и detektiv.py):  python detektiv_chardet.py
"""
import codecs

from detektiv import FILES, HERE, guess_encoding

try:
    import chardet
    HAS_CHARDET = True
except ImportError:
    HAS_CHARDET = False


def guess_with_chardet(path) -> dict:
    """Какво мисли chardet за файла: речник с ключове 'encoding' и 'confidence'.

    chardet работи с байтове, затова файлът се отваря в двоичен режим ("rb"),
    без encoding.
    """
    with open(path, "rb") as f:
        return chardet.detect(f.read())


def canonical(name):
    """Каноничното име на кодирането в Python ("Windows-1251" -> "cp1251").

    None, ако няма име. Непознато за Python име се връща с малки букви.
    """
    if not name:
        return None
    try:
        return codecs.lookup(name).name
    except LookupError:
        return name.lower()


def main() -> None:
    if not HAS_CHARDET:
        print("Пакетът 'chardet' не е инсталиран в тази среда.")
        print("Направи:  python -m pip install -r requirements.txt")
        return
    print(f"chardet {chardet.__version__}\n")
    print(f"{'файл':14s}{'моя догадка':14s}{'chardet':14s}{'увереност':11s}съвпада")
    for name in FILES:
        mine = guess_encoding(HERE / name)
        found = guess_with_chardet(HERE / name)
        theirs = canonical(found["encoding"])
        same = "да" if mine == theirs else "не"
        print(f"{name:14s}{str(mine):14s}{str(theirs):14s}{found['confidence']:<11.2f}{same}")


if __name__ == "__main__":
    main()

# РАЗЛИКАТА МЕЖДУ МОЯ МЕТОД И chardet
#
# 1. Как работят. Моят метод пробва фиксиран списък от четири кодирания по ред
#    и проверява дали прочетеният текст прилича на български. chardet не чете
#    файла като текст, а анализира байтовете: проверява за BOM и после смята
#    колко типични за различните кодирания и езици са комбинациите от байтове.
#    Връща най-вероятното кодиране и число за увереност от 0 до 1.
#
# 2. Къде се различават резултатите. За tekst_d chardet казва utf-8-sig, защото
#    познава BOM, а моят метод казва utf-8 и невидимият знак \ufeff остава в
#    началото на текста. За другите три файла имената съвпадат, но за tekst_a
#    chardet е по-малко сигурен (увереност около 0.6 при cp1251, а за останалите
#    е 0.99 или 1.0). Вероятно защото файлът е кратък, а cp1251 няма ясни
#    „подписи“ като UTF-8, UTF-16 или BOM.
#
# 3. Обхват. Моят метод познава четири кодирания и разпознава само български.
#    chardet познава много повече кодирания и езици.
#
# 4. Цена. chardet е външен пакет: трябва да е във requirements.txt със закачена
#    версия и аз му се доверявам (урок 1). Резултатите могат да се различават
#    между версиите му, затова записвам версията. Моят метод не зависи от нищо.
#
# 5. И двата метода са догадка. chardet връща вероятност, а не истина, затова
#    при ниска увереност не бива да му се вярва сляпо.
