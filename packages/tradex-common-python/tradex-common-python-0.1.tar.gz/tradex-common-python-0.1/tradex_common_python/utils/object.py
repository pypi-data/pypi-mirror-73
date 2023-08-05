from typing import Union, Dict, List


Cloneable = Union[Dict, List, str, int, float, bool]


def deep_clone(data: Cloneable) -> Cloneable:
    if data is None:
        return None
    if isinstance(data, Dict):
        result: Dict = dict()
        for key in data.keys():
            value = data[key]
            result[key] = deep_clone(value)
        return result
    if isinstance(data, List):
        result: List = list()
        for i in range(len(data)):
            result.append(deep_clone(data[i]))
        return result
    return data



