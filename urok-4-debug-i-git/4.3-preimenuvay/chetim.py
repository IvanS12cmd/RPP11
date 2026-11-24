"""chetim.py — същата логика като nechetim.py, но с ясни имена.

Намира учениците, чийто среден успех е най-малко равен на даден праг.
"""


def average(grades):
    """Среден успех. None, ако няма оценки."""
    if not grades:
        return None
    return sum(grades) / len(grades)


def students_at_or_above(grades_by_student, threshold):
    """Двойки (име, среден успех) за учениците със среден успех >= threshold.

    Учениците без оценки се пропускат. Редът е като в речника.
    """
    result = []
    for name, grades in grades_by_student.items():
        student_average = average(grades)
        if student_average is None:
            continue
        if student_average >= threshold:
            result.append((name, student_average))
    return result


if __name__ == "__main__":
    grades_by_student = {
        "Ани": [6, 5, 6, 4],
        "Борис": [3, 4, 3],
        "Валентин": [5, 6, 6, 5],
        "Георги": [],
        "Диана": [6, 6, 6],
    }
    print(students_at_or_above(grades_by_student, 5.0))
    print(students_at_or_above(grades_by_student, 5.5))
    print(students_at_or_above({}, 4.0))
