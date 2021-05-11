DOMAIN_NAME_LIST_QUERY = """
FOR d IN DomainName
    LET user_dn = (
        FOR u IN UsersDn
            FILTER u.domain_name == d._key AND u.username == @username
            RETURN u
    )
    LET owned = LENGTH(user_dn) == 1 AND user_dn[0].owned
    LET followed = LENGTH(user_dn) == 1 AND NOT user_dn[0].owned

    LET resolution = (
        FOR r IN DomainNameResolution
            FILTER r.domain_name == d._key
            SORT r.last_updated_at desc
            RETURN r
    )[0]
    LET dn_tags = (
        FOR t IN TagDnIp
            FILTER t.object == d._key
            RETURN t.tag
    )
    LET ip_tags = (
        FOR t IN TagDnIp
            FILTER t.object == resolution.ip_address
            RETURN t.tag
    )
    """

DOMAIN_NAME_LIST_RETURN = """
    LIMIT @limit
    RETURN {
        domain_name: d._key,
        domain_name_tags: dn_tags,
        ip_address: resolution.ip_address,
        ip_address_tags: ip_tags,
        last_ip_change: resolution.first_updated_at,
        owned: owned,
        followed: followed
    }
"""

DOMAIN_NAME_LIST_FILTER_DN = """
    FILTER CONTAINS(d._key, @filter)
"""

DOMAIN_NAME_LIST_FILTER_DN_TAG = """
    FILTER POSITION(dn_tags, @filter)
"""

DOMAIN_NAME_LIST_FILTER_IP_TAG = """
    FILTER POSITION(ip_tags, @filter)
"""

DOMAIN_NAME_LIST_FILTER_OWNED = """
    FILTER owned
"""

DOMAIN_NAME_LIST_FILTER_FOLLOWED = """
    FILTER followed
"""

DOMAIN_NAME_LIST_FILTER_FOLLOWED_OWNED = """
    FILTER followed OR owned
"""

DOMAIN_NAME_LIST_SORT_DN = """
    SORT d._key
"""

DOMAIN_NAME_LIST_SORT_IP = """
    SORT resolution.ip_address
"""

DOMAIN_NAME_LIST_SORT_CHANGE = """
    SORT resolution.first_updated_at desc
"""
