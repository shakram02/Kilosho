def get_nested_dict_values(d):
    for v in d.values():
        if isinstance(v, dict):
            yield from get_nested_dict_values(v)
        else:
            yield v
