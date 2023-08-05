import os
from unittest.mock import patch, MagicMock

import pytest

from query_factory import SQLQueryFactory
from query_factory import exceptions


@pytest.fixture()
def template_path():
    return os.path.join(os.path.dirname(__file__), "data", "sql_template.yaml")


def test_init(template_path):
    _ = SQLQueryFactory(template_path)


def test_get_query_with(template_path):
    templator = SQLQueryFactory(template_path)
    templator._query = MagicMock()
    templator.get_query_with(start_date="1", end_date="2")
    templator._query.format.assert_called_with(start_date="1", end_date="2")


def test_get_query_with_raises(template_path):
    templator = SQLQueryFactory(template_path)
    with pytest.raises(exceptions.MissingOrExtraVariableException):
        templator.get_query_with(wrong_arg="1")


@patch("yaml.load", return_value={"wrong_key": "value"})
def test_malformed_raise(load_mock, template_path):
    with pytest.raises(exceptions.MalformedTemplate):
        _ = SQLQueryFactory(template_path)


@patch("yaml.load", return_value={"query_template": "", "variables": []})
def test_raise_on_empty_query(template_path):
    with pytest.raises(exceptions.NoOrEmptyQueryException):
        _ = SQLQueryFactory(template_path)
