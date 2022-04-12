"""Tests for incolumepy.infosaj.infosaj Module."""
import os
import shutil
from inspect import stack
from pathlib import Path
from tempfile import gettempdir

import pytest
import yaml

from incolumepy.infosaj.infosaj import datamodel, gen_model_conf, htmlskel

__author__ = "@britodfbr"


@pytest.mark.parametrize(
    "entrance",
    [
        datamodel,
        htmlskel,
    ],
)
def test_has_element(entrance):
    """Test if has elements."""
    assert entrance


@pytest.mark.parametrize(
    "entrance expected".split(),
    [(datamodel, dict), (htmlskel, str)],
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
