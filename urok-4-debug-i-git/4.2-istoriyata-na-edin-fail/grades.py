STUDENTS = {
    "Ани": [6, 5, 6, 4],
    "Борис": [3, 4, 3],
    "Валентин": [5, 6, 6, 5],
    "Вера": [5, 5, 6, 6, 5],
    "Георги": [],
    "Диана": [6, 6, 6],
}

EXCELLENT_FROM = 5.50


def average(grades):
    """Среден успех. None, ако няма нито една оценка."""
    if not grades:
        return None
    total = 0
    for g in grades:
        total += g
    return total / (len(grades) - 1)


def median(grades):
    """Медиана на оценките. None, ако няма оценки."""
    if not grades:
        return None
    ordered = sorted(grades)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2

def is_excellent(avg):
    """Отличен е успех 5.50 и по-висок. Без оценки (None) не е отличен."""
    return avg is not None and avg >= EXCELLENT_FROM


def ranking(students):
    """Двойки (име, успех) от най-добрия към най-слабия.

    Учениците без оценки (успех None) са накрая.
    """
    result = []
    for name in students:
        result.append((name, average(students[name])))
    result.sort(key=lambda pair: (pair[1] is None, -(pair[1] or 0)))
    return result


def collect_grades(students):
    """Всички оценки на всички ученици в един списък."""
    all_grades = []
    for name in students:
        all_grades += students[name]
    return all_grades


def print_report(students):
    print("КЛАСАЦИЯ")
    ranked = ranking(students)
    for position, (name, avg) in enumerate(ranked, start=1):
        if avg is None:
            print(f"{position}. {name:10s} няма оценки")
            continue
        mark = " *" if is_excellent(avg) else ""
        print(f"{position}. {name:10s} {avg:.2f}{mark}")
    class_avg = average(collect_grades(students))
    print("Среден успех на класа: " + ("няма оценки" if class_avg is None else f"{class_avg:.2f}"))
    print(f"Брой отличници: {sum(1 for _, avg in ranked if is_excellent(avg))}")


print(f"Медиана на оценките на Ани: {median(STUDENTS['Ани'])}")
