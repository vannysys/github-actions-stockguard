import pytest

from src.sobrestock import clasificar_sobrestock


def test_sobrestock():
    assert clasificar_sobrestock(120, 100) == "SOBRESTOCK"


def test_limite_exacto_no_es_sobrestock():
    assert clasificar_sobrestock(100, 100) == "CERCA_DEL_LIMITE"


def test_cerca_del_limite_en_el_borde_del_90():
    assert clasificar_sobrestock(90, 100) == "CERCA_DEL_LIMITE"
    assert clasificar_sobrestock(89, 100) == "OK"


def test_stock_ok():
    assert clasificar_sobrestock(50, 100) == "OK"


@pytest.mark.parametrize("actual, maximo", [(-1, 100), (10, 0)])
def test_valores_invalidos(actual, maximo):
    with pytest.raises(ValueError):
        clasificar_sobrestock(actual, maximo)
