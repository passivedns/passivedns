
def tag_created_view(tag):
    return {
        "msg": f"tag {tag.name} created",
    }, 201


def tag_deleted_view(tag):
    return {
        "msg": f"tag {tag.name} deleted",
    }, 200


def tag_list_view(tag_list):
    return {
        "msg": f"tag list retrieved",
        "tag_list": [
            t.json()['_key'] for t in tag_list
        ]
    }, 200
