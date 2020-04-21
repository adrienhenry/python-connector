# -*- coding: utf-8 -*-

"""Tests for the data module."""

from py_client import parameters
from py_client.data import data

import pytest
import datetime
import json

DATASET = {
    "datadefs": [
        {"id": "mb1/d1", "type": "NUMERIC", "data": ["1", "2", "3", "4"]},
        {"id": "mb1/d2", "type": "NUMERIC", "data": ["1", "NaN", "3", "4"]},
        {"id": "mb1/d3", "type": "NUMERIC", "data": ["1.1", "2.1", "3.1", "4.1"]},
        {
            "id": "mb1/d4",
            "type": "DATETIME",
            "data": ["20200331_17010" + str(i) for i in range(4)],
        },
        {"id": "mb1/d5", "type": "DISCRET", "data": ["A", "B", "C", "D"]},
    ]
}


@pytest.fixture
def body_data():
    data = {
        "order": "mb1/d4",
        "definitions": ["mb1/d{}".format(i) for i in range(1, 6)],
        "context": {"dataSource": "mb1"},
    }
    return data


@pytest.mark.parametrize(
    "filter_list, combined_filters",
    [
        (["condA"], "condA"),
        (["condA", "condB"], {"AND": ["condA", "condB"]}),
        (
            ["condA", "condB", "condC", "condD"],
            {"AND": [{"AND": [{"AND": ["condA", "condB"]}, "condC"]}, "condD"]},
        ),
    ],
)
def test_combine_filtes(filter_list, combined_filters):
    assert data._combine_filters(filter_list) == combined_filters


def test_to_datetime():
    date = datetime.datetime(2020, 3, 31, 17, 1, 10)
    date_str = "20200331_170110"
    assert data._to_datetime(date_str) == date


def test_extract_format_data():
    parameters.set_parameter({"parse_date": True})
    formated_dataset = data._extract_format_data(DATASET)
    assert sorted(formated_dataset.keys()) == ["1", "2", "3", "4", "5"]
    assert formated_dataset["1"] == [1, 2, 3, 4]
    assert type(formated_dataset["1"][0]) is int
    assert type(formated_dataset["2"][0]) is float  # No NaN for int...
    assert type(formated_dataset["3"][0]) is float
    assert type(formated_dataset["4"][0]) is datetime.datetime
    assert type(formated_dataset["5"][0]) is str


def test_extract_format_data_no_parse():
    parameters.set_parameter({"parse_date": False})
    formated_dataset = data._extract_format_data(DATASET)
    assert type(formated_dataset["4"][0]) is str


@pytest.mark.parametrize("filters", [None, [{"AND": ["A", "B"]}]])
def test_collect_data(mocker, filters, body_data):
    rpatch = mocker.patch("py_client.client.request_ws", return_value=DATASET)
    received_data = data.collect_data(
        ["1", "2", "3", "4", "5"], "braincube/bcname", {"bcId": "1", "referenceDate": "4"}, filters
    )
    if filters:
        body_data["context"]["filter"] = filters[0]
    rpatch.assert_called_with(
        "braincube/bcname/braindata/mb1/LF", body_data=json.dumps(body_data), rtype="POST"
    )