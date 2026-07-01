# catalog/admin/witgets.py:1
import re

from django.forms import Textarea


class JSONSelectMultipleWidget(Textarea):
    def value_from_datadict(self, data, files, name):
        f"""
        :param {str} attributes_additional:  Your data (I mean it is properties if item) you can insert/write
        of three types.
        Example: Note: Don't forget that ',' and strictly from the beginning of line,
            (Стекло, универсальное),(память, 3ПИ) or (glass, universal), (RAM, 3ПИ) or ("glass", "universal")
            or
            glass=universal, RAM=3ПИ
            or
            {"test_key1":"tesst_value1", "test_key2":"tesst_value2"}
        This data be saving to the database under a dictionary format.
        """
        try:
            d = data.__getitem__("attributes_additional")
            if type(d) == str and d.startswith("(") or d.startswith("{"):
                d_list = d.split("), ")
                d_list = [
                    re.sub(
                        r"[):{=}(]",
                        ", ",
                        re.sub(r"(\r\n|\r|\n)", ", ", d_str, count=0),
                        count=0,
                    )
                    for d_str in d_list
                ]
                d_list = [
                    item
                    for item_str in d_list
                    for item in item_str.strip().split(",")
                    if len(item) > 0
                ]
                d_list = [
                    re.sub(r"['\"]", "", item, count=0)
                    for item in d_list
                    if len(item) > 1
                ]
                k_list = [
                    ((item.strip()).split(","))
                    for i, item in enumerate(d_list)
                    if i % 2 == 0
                ]
                v_list = [
                    ((item.strip()).split(","))
                    for i, item in enumerate(d_list)
                    if i % 2 != 0
                ]
                d_json = {}
                for k, v in zip(k_list, v_list):
                    d_json[k[0].strip()] = v[0].strip()
                if len(d_json) > 0:
                    data_copy = data.copy()
                    data_copy.__setitem__("attributes_additional", d_json)
                    return super().value_from_datadict(data_copy, files, name)
        except AttributeError:
            pass
        except TypeError:
            pass
        return super().value_from_datadict(data, files, name)
