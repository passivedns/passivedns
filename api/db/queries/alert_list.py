ALERT_LIST_QUERY = """
FOR d IN DomainName
    LET user_dn = (
        FOR u IN UsersDn
            FILTER u.domain_name == d._key AND u.username == @username
            RETURN u
    )
    LET owned = LENGTH(user_dn) == 1 AND user_dn[0].owned
    LET followed = LENGTH(user_dn) == 1 AND NOT user_dn[0].owned
    
    FILTER owned OR followed
    
    LET dn_tags = (
        FOR t IN TagDnIp
            FILTER t.object == d._key
            RETURN t.tag
    )

    // getting two last res
    LET resolution_list = (
        FOR r IN DomainNameResolution
            FILTER r.domain_name == d._key
            SORT r.last_updated_at desc
            RETURN r
    )
    LET current_res = resolution_list[0]
    LET current_ip_tags = (
        FOR t IN TagDnIp
            FILTER t.object == current_res.ip_address
            RETURN t.tag
    )
    
    LET last_res = resolution_list[1]
    LET last_ip_tags = (
        FOR t IN TagDnIp
            FILTER t.object == last_res.ip_address
            RETURN t.tag
    )
"""

ALERT_LIST_RETURN = """
    LET dNow = DATE_NOW()
    LET dYesterday = DATE_SUBTRACT(DATE_NOW(), @days, "day")
    LET cDate = d.created_at
    // filtering recently created DN
    FILTER DATE_DIFF(cDate, dYesterday, "i") > 0
    LET uDate = current_res.first_updated_at
    FILTER DATE_DIFF(dYesterday, uDate, "i") > 0

    LIMIT @limit
    RETURN {
        domain_name: d._key,
        domain_name_tags: dn_tags,
        last_ip_address: last_res.ip_address,
        last_ip_tags: last_ip_tags,
        current_ip_address: current_res.ip_address,
        current_ip_tags: current_ip_tags
    }
"""

ALERT_LIST_FILTER_DN = """
    FILTER CONTAINS(d._key, @filter)
"""

ALERT_LIST_FILTER_DN_TAGS = """
    FILTER POSITION(dn_tags, @filter)
"""

ALERT_LIST_FILTER_IP_TAG = """
    FILTER POSITION(current_ip_tags, @filter) OR POSITION(last_ip_tags, @filter) 
"""

ALERT_LIST_SORT_DN = """
    SORT d._key
"""

ALERT_LIST_SORT_LAST_IP = """
    SORT last_res.ip_address
"""

ALERT_LIST_SORT_CURRENT_IP = """
    SORT current_res.ip_address
"""
