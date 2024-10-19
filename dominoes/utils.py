def sort_dictionary_by_values(dictionary: dict, des: bool = True) -> dict:
    return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=des))


def concat_lists(a: list, b: list):
    concat_list = []

    for element in a:
        concat_list.append(element)

    for element in b:
        concat_list.append(element)

    return concat_list
