"""env_check.py — „Кой Python работи в момента?“

Изпълнете програмата два пъти: веднъж с глобалния Python и веднъж
от активирана виртуална среда. Сравнете реда „Текущ префикс“.
"""
import importlib.metadata
import os
import platform
import site
import sys


def in_virtualenv() -> bool:
    """Връща True, ако програмата се изпълнява във виртуална среда."""
    return sys.prefix != sys.base_prefix


def site_packages_paths() -> list:
    """Връща папките, в които живеят инсталираните пакети."""
    return site.getsitepackages()


def count_installed_packages() -> int:
    """Брои инсталираните пакети (всеки пакет по веднъж, по име)."""
    names = set()
    for dist in importlib.metadata.distributions():
        name = dist.metadata["Name"]
        if name:  # пропускаме повредени записи без име
            names.add(name.lower())
    return len(names)


def report() -> None:
    print("=" * 52)
    print("ДОКЛАД ЗА СРЕДАТА")
    print("=" * 52)
    print(f"Версия на Python : {platform.python_version()}")
    print(f"Изпълним файл    : {sys.executable}")
    print(f"Базов префикс    : {sys.base_prefix}")
    print(f"Текущ префикс    : {sys.prefix}")
    print(f"Работна папка    : {os.getcwd()}")
    for path in site_packages_paths():
        print(f"Папка с пакети   : {path}")
    print(f"Брой пакети      : {count_installed_packages()}")
    print("-" * 52)
    if in_virtualenv():
        print("СТАТУС: РАБОТИШ ВЪВ ВИРТУАЛНА СРЕДА.")
    else:
        print("СТАТУС: ГЛОБАЛЕН PYTHON — внимавай какво инсталираш!")
        print("ВНИМАНИЕ: НЕ СИ ВЪВ ВИРТУАЛНА СРЕДА!")
    print("=" * 52)


if __name__ == "__main__":
    report()
