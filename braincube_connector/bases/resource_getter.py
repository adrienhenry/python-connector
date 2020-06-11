# -*- coding: utf-8 -*-

from typing import Any, Tuple, Union

from braincube_connector import tools


class ResourceGetter(object):
    """Class that handles getting child resources."""

    def __init__(self):
        """Initialize ResourceGetter."""
        self._path = ""

    def _get_resource(
        self, resource_class: Any, bcid: Union[str, int], singleton_path: str = "", **kwargs,
    ):
        """Get a resource from its bcId.

        Args:
            resource_class: Class of the resource to get.
            bcid: Event bcid.
            singleton_path: Path to request. Default: resource_class.request_one_path.
            **kwargs: Optional parent (e.g. memory_base).

        Returns:
            A resource description.
        """
        return resource_class.create_singleton_from_path(
            *generate_path(
                self._path,
                resource_class.entity_path.replace("{bcid}", str(bcid)),
                resource_class.request_one_path if not singleton_path else singleton_path,
            ),
            **kwargs,
        )

    def _get_resource_list(self, resource_class: Any, collection_path: str = "", **kwargs):
        """Get a list a of resources from a list of ids.

        Args:
            resource_class: Class of the resources to get.
            collection_path: Path to request. Default: resource_class.request_many_path.
            **kwargs: Optional page and page_size or parent (memory_base).

        Returns:
            A list of resources.
        """
        return resource_class.create_collection_from_path(
            *generate_path(
                self._path,
                resource_class.entity_path,
                resource_class.request_many_path if not collection_path else collection_path,
                request_list=True,
            ),
            **kwargs,
        )


def generate_path(
    parent_path: str, entity_path: str, request_path: str, request_list: bool = False
) -> Tuple[str, str]:
    """Factorize the generation of path required by create_*_from_path.

    Args:
        parent_path: Path of the parent object.
        entity_path: Path complement to go to the entity.
        request_path: Path complement to request.
        request_list: Is the request for a list or one element?

    Returns:
        The complete path to request and to bind to the created entity.
    """
    entity_path = tools.join_path([parent_path, entity_path])
    pre_request_path = parent_path if request_list else entity_path
    request_path = tools.join_path([pre_request_path, request_path])
    return (request_path, entity_path)
