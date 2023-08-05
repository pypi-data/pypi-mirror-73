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
