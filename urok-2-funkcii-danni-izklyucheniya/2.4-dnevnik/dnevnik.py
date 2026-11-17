"""dnevnik.py — среден успех и класация от речник с оценки.

Задача 2.4. Данните имат вида:

    {"име": {"предмет": [оценки], ...}, ...}

Нито една функция не бива да гърми при ученик без оценки
или при празен речник. Функциите връщат резултат и не печатат.
"""

STUDENTS = {
    "Ани":    {"математика": [6, 5, 6], "български": [5, 6], "история": [6]},
    "Борис":  {"математика": [3, 2, 4], "български": [3], "история": [4, 3]},
    "Вера":   {"математика": [5, 5], "български": [6, 6], "история": []},
    "Георги": {},
    "Диана":  {"математика": [2, 3], "български": [3, 4], "история": [3]},
}


def subject_averages(student: dict) -> dict:
    """Среден успех по всеки предмет, в който има оценки. Предметите без оценки се пропускат."""
    return {subject: sum(grades) / len(grades)
            for subject, grades in student.items() if grades}


def subject_average(student: dict, subject: str):
    """Среден успех по предмет. None, ако предметът липсва или няма оценки."""
    grades = student.get(subject)
    if not grades:
        return None
    return sum(grades) / len(grades)


def overall_average(student: dict):
    """Общ успех: средно аритметично на средните успехи по предмети.

    Предмети без оценки не участват. None, ако ученикът няма нито една оценка.
    """
    averages = subject_averages(student)
    if not averages:
        return None
    return sum(averages.values()) / len(averages)


def weakest_subject(student: dict):
    """Предметът с най-нисък среден успех. None, ако няма оценки.

    При равенство — първият по азбучен ред.
    """
    averages = subject_averages(student)
    if not averages:
        return None
    return min(averages, key=lambda subject: (averages[subject], subject))


def class_ranking(students: dict) -> list:
    """Списък от (име, общ успех), подреден от най-високия към най-ниския.

    Учениците без оценки са накрая (с успех None), подредени по азбучен ред.
    При равен успех — по азбучен ред на името.
    """
    ranking = [(name, overall_average(student)) for name, student in students.items()]
    return sorted(ranking, key=lambda item: (item[1] is None, -(item[1] or 0), item[0]))


def at_risk(students: dict, threshold: float = 3.50) -> list:
    """Имената (по азбучен ред) на учениците с общ успех под threshold.

    Ученици без оценки не се включват — за тях няма данни.
    """
    return sorted(name for name, average in class_ranking(students)
                  if average is not None and average < threshold)


if __name__ == "__main__":
    import copy

    ani, vera, georgi = STUDENTS["Ани"], STUDENTS["Вера"], STUDENTS["Георги"]

    # subject_average
    assert subject_average(ani, "история") == 6
    assert subject_average(georgi, "история") is None          # ученик без оценки
    assert subject_average(vera, "история") is None            # празен списък
    assert subject_average({}, "математика") is None           # празен ученик

    # overall_average
    assert overall_average(vera) == 5.5                        # предмет без оценки не участва
    assert overall_average({}) is None
    assert overall_average({"математика": []}) is None         # само предмет без оценки

    # weakest_subject
    assert weakest_subject(STUDENTS["Борис"]) == "български"   # равенство -> по азбучен ред
    assert weakest_subject({}) is None

    # class_ranking
    assert class_ranking(STUDENTS)[0][0] == "Ани"
    assert class_ranking(STUDENTS)[-1] == ("Георги", None)     # без оценки -> накрая
    assert class_ranking({}) == []
    assert class_ranking({"Яна": {}, "Ася": {}}) == [("Ася", None), ("Яна", None)]

    # at_risk
    assert at_risk(STUDENTS) == ["Борис", "Диана"]
    assert at_risk(STUDENTS, threshold=3.0) == []              # „под прага“ е строго по-малко
    assert at_risk({}) == []

    # функциите не променят данните
    before = copy.deepcopy(STUDENTS)
    class_ranking(STUDENTS)
    at_risk(STUDENTS)
    assert STUDENTS == before

    print("Всички проверки минаха.")
