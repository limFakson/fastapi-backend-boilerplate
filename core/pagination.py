import math
from typing import Any


def normalize_pagination(page: int, limit: int, all_records: bool) -> tuple[int, int]:
    page = max(1, int(page or 1))
    limit = max(1, int(limit or 10))

    if all_records:
        page = 1

    return page, limit


def build_paginated_payload(data: list[Any], total: int, page: int, limit: int, all_records: bool) -> dict:
    effective_limit = total if all_records else limit
    total_pages = 1 if all_records else max(1, math.ceil(total / limit))

    return {
        "total": total,
        "page": page,
        "limit": effective_limit,
        "totalPages": total_pages,
        "data": data,
    }
