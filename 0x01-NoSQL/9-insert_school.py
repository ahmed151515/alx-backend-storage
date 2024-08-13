#!/usr/bin/env python3
"""_summary_
    """


def insert_school(mongo_collection, **kwargs):
    """_summary_

    Args:
        mongo_collection (_type_): _description_

    Returns:
        _type_: _description_
    """
    res = mongo_collection.insert_one(kwargs)

    return res.inserted_id
