"""ariane.py — полетът, който можеше да не завърши така.

Опростен модел на това, което се случва на борда на Ariane 5.
Задача 2.1: следвайте стъпките в README.md на урока.

Пускане:  python ariane.py [bez-prehvashtane | ogranichavane | int32]
"""
import sys

INT16_MIN = -32_768
INT16_MAX = 32_767
INT32_MIN = -2_147_483_648
INT32_MAX = 2_147_483_647

# Трите поведения при препълване.
MODE_NONE = "bez-prehvashtane"
MODE_CLAMP = "ogranichavane"
MODE_INT32 = "int32"
MODES = (MODE_NONE, MODE_CLAMP, MODE_INT32)


class OverflowAlarm(Exception):
    """Собствено изключение: стойността не се побира в 16 бита."""

    def __init__(self, value):
        super().__init__(f"Стойност {value:.1f} не се побира в 16-битово цяло")
        self.value = value


def to_int16(value: float) -> int:
    """Преобразува 64-битово дробно число към 16-битово цяло със знак.

    Ако стойността е извън диапазона INT16_MIN..INT16_MAX,
    вдига OverflowAlarm.
    """
    if not INT16_MIN <= value <= INT16_MAX:
        raise OverflowAlarm(value)
    return int(value)


def to_int32(value: float) -> int:
    """Преобразува дробно число към 32-битово цяло със знак.

    Ако стойността е извън диапазона INT32_MIN..INT32_MAX,
    вдига OverflowError.
    """
    if not INT32_MIN <= value <= INT32_MAX:
        raise OverflowError(f"Стойност {value:.1f} не се побира в 32-битово цяло")
    return int(value)


def horizontal_bias(t: float, acceleration: float) -> float:
    """Опростен модел на хоризонталното отклонение BH след t секунди."""
    return 0.5 * acceleration * t * t


def convert(bh: float, mode: str) -> tuple:
    """Подава BH към автопилота според избрания режим.

    Връща двойка (стойност, предупреждение). Предупреждението е None,
    когато няма препълване. При режим MODE_NONE препълването не се
    прехваща и OverflowAlarm продължава нагоре.
    """
    try:
        return to_int16(bh), None
    except OverflowAlarm as alarm:
        if mode == MODE_CLAMP:
            return INT16_MAX, f"{alarm}; ограничавам до {INT16_MAX}"
        if mode == MODE_INT32:
            return to_int32(bh), f"{alarm}; превключвам към 32 бита"
        raise


def flight(rocket: str, acceleration: float, duration: int, mode: str = MODE_NONE) -> None:
    """Симулира полет от duration секунди и печата какво стига до автопилота."""
    if mode not in MODES:
        raise ValueError(f"Непознат режим: {mode!r}. Възможни: {', '.join(MODES)}")
    print(f"\n--- Полет на {rocket} (режим: {mode}) ---")
    for t in range(1, duration + 1):
        bh = horizontal_bias(t, acceleration)
        value, warning = convert(bh, mode)
        if warning:
            print(f"  ВНИМАНИЕ: {warning}")
        print(f"  t={t:2d}s  BH={bh:10.1f}  -> към автопилота: {value}")
    print("  Полетът завърши успешно.")


if __name__ == "__main__":
    selected = sys.argv[1] if len(sys.argv) > 1 else MODE_NONE
    flight("Ariane 4", acceleration=45.0, duration=10, mode=selected)
    flight("Ariane 5", acceleration=900.0, duration=10, mode=selected)
