from typing import Type

from foxdemo.common.persistence_models import BaseDocument

LIMIT = "limit"
ORDER_BY = "order_by"
SKIP = "skip"
VALID_MODIFIERS = {LIMIT, ORDER_BY, SKIP}
DEFAULT_MODIFIERS = {"limit": 1000}


def extract_query_modifiers(query_parameters: dict):
    modifiers = {}
    modifiers.update(DEFAULT_MODIFIERS)
    modifiers.update({modifier: query_parameters.pop(modifier) for modifier
                      in VALID_MODIFIERS.intersection(set(query_parameters.keys()))})
    return modifiers, query_parameters


def build_queryset(model_class: Type[BaseDocument], model_filter_properties: dict = None, skip: int = None,
                   limit: int = 1000, order_by: str = None):
    if model_filter_properties is None:
        model_filter_properties = {}

    query_set = model_class.objects(**model_filter_properties)
    if skip is not None and limit is not None:
        query_set = query_set[int(skip):int(skip) + int(limit)]
    elif skip is not None:
        query_set = query_set[int(skip):]
    elif limit is not None:
        query_set = query_set[:int(limit)]

    if order_by is not None:
        query_set = query_set.order_by(order_by)

    return query_set
