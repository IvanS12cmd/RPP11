"""Проверки за smetka_nova.py.

Пускане:  python -m pytest urok-2-funkcii-danni-izklyucheniya/domashno-smetka -v
"""
import builtins

import pytest

from smetka_nova import InputError, ask, parse_amount, parse_people, split_bill


def test_suma_obiknovena():
    assert parse_amount("12.50") == 12.5


def test_suma_s_zapetaya():
    assert parse_amount("12,50") == 12.5


def test_suma_s_intervali():
    assert parse_amount("  8 ") == 8.0


def test_suma_ne_e_chislo():
    with pytest.raises(InputError):
        parse_amount("abc")


def test_suma_otritsatelna_ili_nula():
    for text in ("-5", "0"):
        with pytest.raises(InputError):
            parse_amount(text)


def test_suma_nan_i_inf_ne_se_priemat():
    for text in ("nan", "inf", "-inf"):
        with pytest.raises(InputError):
            parse_amount(text)


def test_hora_obiknoveno():
    assert parse_people("3") == 3


def test_hora_drobno_chislo():
    with pytest.raises(InputError):
        parse_people("2.5")


def test_hora_nula_ili_otritsatelno():
    for text in ("0", "-4"):
        with pytest.raises(InputError):
            parse_people(text)


def test_izklyuchenieto_nosi_poleto_i_teksta():
    with pytest.raises(InputError) as info:
        parse_people("abc")
    assert info.value.field == "Брой хора"
    assert info.value.text == "abc"


def test_split_bill():
    assert split_bill(100, 4) == 25.0
    assert split_bill(10, 3) == 3.33


def test_split_bill_nevalidni_hora():
    for people in (0, -2):
        with pytest.raises(ValueError):
            split_bill(10, people)


def test_ask_pita_dokato_vhodat_e_validen(monkeypatch, capsys):
    answers = iter(["abc", "-1", "4"])
    monkeypatch.setattr(builtins, "input", lambda prompt: next(answers))
    assert ask("Брой хора: ", parse_people) == 4
    assert capsys.readouterr().out.count("Грешка") == 2
