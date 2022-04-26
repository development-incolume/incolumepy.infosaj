"""Tests for incolumepy.infosaj.infosaj Module."""
import os
import shutil
from datetime import datetime
from inspect import stack
from pathlib import Path
from tempfile import gettempdir
from bs4 import BeautifulSoup
import pytest
import yaml

from incolumepy.infosaj.infosaj import (
    HTMLSKEL,
    datamodel,
    gen_model_conf,
    set_entrance,
    meses,
    stylecss,
    section_decisoes,
    section_aniver,
)

__author__ = "@britodfbr"


@pytest.mark.parametrize(
    "entrance",
    [
        datamodel,
        HTMLSKEL,
    ],
)
def test_has_element(entrance):
    """Test if has elements."""
    assert entrance


@pytest.mark.parametrize(
    "entrance expected".split(),
    [(datamodel, dict), (HTMLSKEL, str)],
)
def test_element_type(entrance, expected):
    """Test if type is correct."""
    assert isinstance(entrance, expected)


def test_gen_model_conf():
    """Test if create model."""
    file = gen_model_conf()
    assert file.is_file()
    shutil.rmtree(file.parent, ignore_errors=True)


def test_load_model():
    """Test if load model.yaml."""
    # file = Path.home().joinpath('model.yaml')
    file = gen_model_conf()
    data = yaml.full_load(file.read_text(encoding="iso8859-1"))
    assert isinstance(data, dict)
    shutil.rmtree(file.parent, ignore_errors=True)


def test_load_model_byte():
    """Test if load model.yaml."""
    file = gen_model_conf()
    data = yaml.full_load(file.read_bytes().decode("iso8859-1"))
    assert isinstance(data, dict)
    shutil.rmtree(file.parent, ignore_errors=True)


def test_load_model_envvar():
    """Test if load model.yaml from envvar."""
    expected = Path(gettempdir()).joinpath(stack()[0][3], "a.html")
    os.environ["INCOLUMEPY_INFOSAJ"] = expected.as_posix()
    file = gen_model_conf()
    assert file.parent.as_posix() == expected.parent.as_posix()
    del os.environ["INCOLUMEPY_INFOSAJ"]


def test_set_entrance_envvar():
    """Test if load model.yaml from envvar."""
    expected = Path(gettempdir()).joinpath(stack()[0][3], "model.yaml")
    os.environ["INCOLUMEPY_INFOSAJ"] = expected.with_name('a.html').as_posix()
    with pytest.raises(AssertionError):
        assert set_entrance() == Path.home().joinpath('infosaj', 'model.yaml')
    expected.write_text('')
    assert set_entrance() == expected
    expected.unlink(missing_ok=True)


@pytest.mark.parametrize(
    "entrance expected".split(),
    [
        (0, None),
        (1, "Jan"),
        (5, "Mai"),
        (6, "Jun"),
        (8, "Ago"),
        (12, "Dez"),
        (13, None),
        (23, None),
    ],
)
def test_meses(entrance, expected):
    if entrance in range(1, 13):
        assert meses(entrance) == expected
    else:
        with pytest.raises(ValueError, match="Invalid month"):
            assert meses(entrance) == expected


def test_stylecss():
    soup = BeautifulSoup(
        '<html><head><style></style></head><body></body></html>',
        'html5lib'
    )
    content = {'stylecss': ['css/fake.css']}
    assert stylecss(soup, content) == BeautifulSoup(
        '<html><head><style>@import url("css/fake.css");'
        '</style></head><body></body></html>', 'html.parser')


def test_section_decisoes():
    soup = BeautifulSoup('<div class="decisoes">', 'html5lib')
    content = {
        'decisões': [
            {
                "title": "ADI 999 Medida Cautelar",
                "relator": "Zé das Colves",
                "resumo": "Fake",
                "message": 'Tá aí: ',
                "linkaddress": "#",
                "linktext": "http://xpto.br"
            }
        ]
    }
    result = section_decisoes(soup, content)
    assert result.select_one('.decisoes')
    assert result.select_one('.decisao')
    assert result.find('h3').text == content['decisões'][0]['title']
    assert result.select_one('#relator')\
               .text.split(': ')[-1] == content['decisões'][0]['relator']


def test_section_aniver():
    expected = '<html><head></head><body><div class="aniversariantes">' \
               '<h2>Aniversariantes do Mês</h2><table><thead><tr><th></th>' \
               '<th></th></tr></thead>' \
               '<caption>Aniversariantes SAJ — Jun/2022</caption>' \
               '<tbody><tr><td>05/07</td><td>Ana Brito</td></tr><tr>' \
               '<td>20/06</td><td>Pedro Silva</td></tr></tbody><tfoot>' \
               '</tfoot></table></div></body></html>'
    entrance = '<div class="aniversariantes"></div>'
    content = {
        'infodate': datetime(2022, 6, 20),
        'aniversariantes': [
            (datetime(2012, 6, 20), 'Pedro Silva'),
            (datetime(2009, 7, 5), 'Ana Brito'),
        ]
    }
    soup = BeautifulSoup(entrance, 'html5lib')
    assert str(section_aniver(soup, content)) == expected
