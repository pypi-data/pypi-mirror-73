def find_first(collection, predicate):
    """
    Find first element in collection that match predicate.

    :param collection: Collection to find
    :param predicate: check predicate
    :return: First matched element, or None if not found
    """
    for item in collection:
        if predicate(item):
            return item
    return None


def find_first_by_key(collection, key, value):
    """
    Find first element in collection of dict by key and value
    :param collection: Collection to find. items in collection should be dict-like object
    :param key: dict key
    :param value: dict value
    :return: First matched element, or None if not found
    """
    return find_first(collection, lambda x: x.get(key, None) == value)


def find_first_by_attr(collection, attr: str, value):
    """
    Find first element in collection of objects
    :param collection: Collection to find
    :param attr: attr of object
    :param value: attr value
    :return: First matched element, or None if not found
    """
    return find_first(collection, lambda x: getattr(x, attr, None) == value)
