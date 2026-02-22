from typing import Any, Optional

from bson import ObjectId


def build_filters(**kwargs: Optional[Any]) -> dict[str, Any]:
    """
    Dynamically builds the filter dictionary.
    - Ignores keys with a value of None.
    - Builds a range for 'created_at' using 'start_date' and 'end_date'.
    Returns {} if there are no filters.
    """
    filters: dict[str, Any] = {}

    start_date = kwargs.pop("start_date", None)
    end_date = kwargs.pop("end_date", None)
    _id = kwargs.get("_id")

    filters.update({key: value for key, value in kwargs.items() if value is not None})

    if start_date or end_date:
        created_at: dict[str, Any] = {}
        if start_date:
            created_at["$gte"] = start_date
        if end_date:
            created_at["$lte"] = end_date
        filters["created_at"] = created_at

    if _id:
        # if it's a list
        if isinstance(_id, list):
            filters["_id"] = {"$in": [ObjectId(oid) for oid in _id]}
        else:
            # force conversion even if it's already an ObjectId
            filters["_id"] = ObjectId(str(_id))

    return filters
