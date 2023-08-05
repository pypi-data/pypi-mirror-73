from typing import Dict, Optional, Any, List, Callable

from tradex_common_python.utils.string_utils import to_camel_case


def create_key_map_from_array(inp: List[str]) -> Dict[str, str]:
    result = dict()
    for key in inp:
        if '_' in key:
            json_key: str = to_camel_case(key)
            result[key] = json_key
    return result


# must use slots to save mem
class Base:
    __slots__ = ()

    def get_slots(self, current_type):
        parent_type = current_type.__bases__[0]
        current_slots = current_type.__slots__
        if isinstance(current_slots, str):
            current_slots = (current_slots,)

        if parent_type == Base:
            return current_slots
        return current_slots + self.get_slots(parent_type)

    def get_keys(self):
        return self.get_slots(type(self))

    # map from object key -> json key
    def key_mapping(self) -> Dict[str, str]:
        return {}

    def to_dict(self) -> Dict:
        data = {}
        special_keys = self.key_mapping()
        for key in self.get_keys():
            field = getattr(self, key)
            if field is not None:
                if key in special_keys:
                    data[special_keys[key]] = self.to_dict_item(field)
                else:
                    data[key] = self.to_dict_item(field)
        return data

    def to_dict_item(self, field):
        if field is None:
            return None
        if isinstance(field, Base):
            return field.to_dict()
        elif isinstance(field, list):
            res = []
            for item in field:
                res.append(self.to_dict_item(item))
            return res
        return field

    # map from object key -> method
    def get_from_dict_mapping(self) -> Dict:
        return {}

    def from_dict(self, dic: Dict) -> Any:
        special_keys = self.key_mapping()
        special_fields: Dict = self.get_from_dict_mapping()
        for key in self.get_keys():
            if key in dic:
                item = dic[key]
                if key in special_keys:
                    item = dic[special_keys[key]]
                if key in special_fields:
                    setattr(self, key, special_fields[key](item, dic, self))
                else:
                    try:
                        field = getattr(self, key)
                        if isinstance(field, Base):
                            field.from_dict(dic[key])
                        else:
                            setattr(self, key, dic[key])
                    except Exception as err:
                        setattr(self, key, dic[key])
        return self


def from_dict_list(producer: Callable[[], Base], item: List[Dict]) -> List:
    result = []
    for i in item:
        result.append(producer().from_dict(i))

    return result
