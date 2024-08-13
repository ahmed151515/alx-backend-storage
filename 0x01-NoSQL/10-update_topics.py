#!/usr/bin/env python3
"""_summary_
    """


def update_topics(mongo_collection, name, topics):
    """_summary_

    Args:
        mongo_collection (_type_): _description_
        name (_type_): _description_
        topics (_type_): _description_
    """
    filter = {"name": name}
    update = {"$set": {"topics": topics}}
    mongo_collection.update_one(filter, update)
