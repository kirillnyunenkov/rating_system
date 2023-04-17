import sql_api
from named_list import NamedList, Item
from globals import *


def saveList(new_list: NamedList) -> None:
    sql_api.insertList(DEFAULT_NAME, new_list.name, new_list)


def saveItem(new_item: Item, name_of_list: str) -> None:
    sql_api.insertItem(DEFAULT_NAME, name_of_list, new_item.name)


def saveSortedList(new_list: NamedList) -> None:
    sql_api.deleteList(DEFAULT_NAME, new_list.name)
    sql_api.insertList(DEFAULT_NAME, new_list.name, new_list, True)


def uploadNamesOfLists(is_sorted: bool = False) -> list:
    return sql_api.getNamesOfLists(DEFAULT_NAME, is_sorted)


def uploadList(name_of_list: str) -> NamedList:
    names = sql_api.getNamesInList(DEFAULT_NAME, name_of_list)
    items = NamedList(name_of_list, list(map(Item, names)))
    return items


def deleteList(list_id: str) -> None:
    sql_api.deleteList(DEFAULT_NAME, list_id)
