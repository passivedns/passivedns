from time import time

from fastapi import APIRouter, Depends, HTTPException, Response

import pandas
from apiv2.auth import get_current_user
from models.domain_name import (
    DomainNameFilterNotFound,
    DomainNameSortNotFound,
    DomainName,
    EXPORT_CSV,
    EXPORT_JSON,
)
from models.user import User

alert_router = APIRouter()


@alert_router.get("/alert")
def get_alert(
    filter: str,
    filter_by: str,
    sort_by: str,
    limit: str,
    days: str,
    user: User = Depends(get_current_user),
):
    username = user.username

    input_filter = filter
    input_filter_by = filter_by
    sort_by = sort_by
    limit_str = limit
    days_str = days

    if not limit_str.isdigit():
        raise HTTPException(status_code=400, detail="invalid limit")

    if not days_str.isdigit():
        raise HTTPException(status_code=400, detail="invalid days count")

    limit = int(limit_str)
    days = int(days_str)

    try:
        t1 = time()
        dn_list = DomainName.list_recent_changes(
            username, days, input_filter, input_filter_by, sort_by, limit
        )
        t2 = time()
    except DomainNameFilterNotFound:
        raise HTTPException(status_code=400, detail="invalid filter field")

    except DomainNameSortNotFound:
        raise HTTPException(status_code=400, detail="invalid sort field")

    transaction_time = round(t2 - t1, 2)

    return {
        "msg": "domain name list retrieved",
        "stats": {
            "transaction_time": transaction_time,
            "count": len(dn_list),
        },
        "dn_list": dn_list,
    }


# Export in csv or json
@alert_router.get("/alert/export")
def export_alert(
    filter: str,
    filter_by: str,
    sort_by: str,
    limit: str,
    days: str,
    export: str,
    user: User = Depends(get_current_user),
):
    username = user.username

    input_filter = filter
    input_filter_by = filter_by
    sort_by = sort_by
    limit_str = limit
    days_str = days

    export = export

    if not limit_str.isdigit():
        raise HTTPException(status_code=400, detail="invalid limit")

    if not days_str.isdigit():
        raise HTTPException(status_code=400, detail="invalid days count")

    limit = int(limit_str)
    days = int(days_str)

    try:
        dn_list = DomainName.list_recent_changes(
            username, days, input_filter, input_filter_by, sort_by, limit
        )
    except DomainNameFilterNotFound:
        raise HTTPException(status_code=400, detail="invalid filter field")

    except DomainNameSortNotFound:
        raise HTTPException(status_code=400, detail="invalid sort field")

    data = []
    for dn in dn_list:
        data.append(
            [
                dn["domain_name"],
                dn["domain_name_tags"],
                dn["last_ip_address"],
                dn["last_ip_tags"],
                dn["current_ip_address"],
                dn["current_ip_tags"],
            ]
        )

    columns = [
        "Domain name",
        "Domain name tags",
        "Last IP address",
        "Last IP tags",
        "Current IP address",
        "Current IP tags",
    ]
    df = pandas.DataFrame(data=data, columns=columns)
    if export == EXPORT_CSV:
        exported_data = df.to_csv(index=False)
        mimetype = "text/csv"

    elif export == EXPORT_JSON:
        exported_data = df.to_json(orient="split", index=False)
        mimetype = "application/json"

    else:
        raise HTTPException(status_code=400, detail="invalid export field")

    return Response(exported_data, headers={"Content-Type": mimetype})
