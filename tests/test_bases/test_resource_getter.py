# -*- coding: utf-8 -*-
"""Tests for the resource_getter module."""

from py_client.bases import resource_getter, base_entity

import pytest


@pytest.fixture
def mock_entity_class(mocker):
    m_entity = mocker.Mock()
    m_entity.entity_path = "entity/{bcid}"
    m_entity.request_one_path = "extended"
    m_entity.request_many_path = "entity/all/extended"
    return m_entity


@pytest.fixture
def resource_parent():
    parent = resource_getter.ResourceGetter()
    parent._path = "parent_path"
    return parent


@pytest.mark.parametrize(
    "request_list, expected_req_path",
    [(False, "memorybase/entity/extended"), (True, "memorybase/extended")],
)
def test_generate_path(request_list, expected_req_path):
    mb_path = "memorybase"
    entity_path = "entity"
    pre_request_path = "extended"
    expected_entity_path = "memorybase/entity"
    returned_req_path, returned_entity_path = resource_getter.generate_path(
        mb_path, entity_path, pre_request_path, request_list
    )
    assert expected_entity_path == returned_entity_path
    assert expected_req_path == returned_req_path


def test_get_resource(mock_entity_class, resource_parent):
    resource_parent._get_resource(mock_entity_class, bcid="1")
    mock_entity_class.create_singleton_from_path.assert_called_once_with(
        "parent_path/entity/1/extended", "parent_path/entity/1"
    )


def test_get_resource_list(mock_entity_class, resource_parent):
    resource_parent._get_resource_list(mock_entity_class)
    mock_entity_class.create_collection_from_path.assert_called_once_with(
        "parent_path/entity/all/extended", "parent_path/entity/{bcid}"
    )
