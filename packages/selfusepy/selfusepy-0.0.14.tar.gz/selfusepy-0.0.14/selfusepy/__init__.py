#    Copyright 2018-2020 LuomingXu
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#   Author : Luoming Xu
#   File Name : __init__.py
#   Repo: https://github.com/LuomingXu/selfusepy

import json
from datetime import datetime, timezone, timedelta
from typing import TypeVar, List

import selfusepy.jsonparse

__version__ = '0.0.14'

T = TypeVar('T')


def fromtimestamp(timestamp: float, offset: int) -> datetime:
    return datetime.fromtimestamp(timestamp, timezone(timedelta(hours = offset)))


def now(offset: int):
    return datetime.now(timezone(timedelta(hours = offset)))


def parse_json(j: str, obj: T) -> T:
    """
    Json to Python Object
    >>>import selfusepy
    >>>obj: T = selfusepy.parse_json(jsonStr, Obj())
    :param j: json string
    :param obj: Py Object
    :return: obj
    """

    jsonparse.generate_class_dict(obj)
    json_dict: dict = json.loads(j)
    j_modified: str = json.dumps(jsonparse.add_classname(json_dict, type(obj).__name__))
    res = json.loads(j_modified, object_hook = jsonparse.deserialize_object)

    jsonparse.class_dict.clear()
    return res


def parse_json_array(j: str, obj: T) -> List[T]:
    """
    Json array to List
    """
    jsonparse.generate_class_dict(obj)
    json_list: list = json.loads(j)
    j_modified: str = json.dumps(jsonparse.add_classname_list(json_list, type(obj).__name__))
    res = json.loads(j_modified, object_hook = jsonparse.deserialize_object)

    jsonparse.class_dict.clear()
    return res
