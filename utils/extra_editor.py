def delete_extra(need_types: list, update_dict: dict) -> dict:
    need_dict = {}
    for key, element in update_dict.items():
        if key in need_types:
            need_dict[key] = element
    return need_dict


def add_to_dict(old_dict, **kwargs):
    old_dict.update(**kwargs)
    return old_dict
