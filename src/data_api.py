import sql_api
from named_list import NamedList, Item
from globals import *


def saveList(new_list: NamedList) -> None:
    sql_api.insertList(DEFAULT_NAME, new_list.name, new_list, False, False)

def saveItem(new_item: Item, name_of_list: str) -> None:
    sql_api.insertItem(DEFAULT_NAME, name_of_list, new_item.name)

def deleteItem(name_of_item: str, name_of_list: str) -> None:
    sql_api.deleteItem(DEFAULT_NAME, name_of_list, name_of_item)

def saveSortedList(new_list: NamedList) -> None:
    is_favorite = sql_api.isFavorite(DEFAULT_NAME, new_list.name)
    sql_api.deleteList(DEFAULT_NAME, new_list.name)
    sql_api.insertList(DEFAULT_NAME, new_list.name, new_list, True, is_favorite)

def addToFavorites(name_of_list: str) -> None:
    old_list = uploadList(name_of_list)
    sql_api.deleteList(DEFAULT_NAME, name_of_list)
    sql_api.insertList(DEFAULT_NAME, name_of_list, old_list, True, True)

def removeFromFavorites(name_of_list: str) -> None:
    old_list = uploadList(name_of_list)
    sql_api.deleteList(DEFAULT_NAME, name_of_list)
    sql_api.insertList(DEFAULT_NAME, name_of_list, old_list, True, False)

def uploadNamesOfLists(is_sorted: bool, is_favorite: bool = False) -> list:
    return sql_api.getNamesOfLists(DEFAULT_NAME, is_sorted, is_favorite)


def uploadList(name_of_list: str) -> NamedList:
    names = sql_api.getNamesInList(DEFAULT_NAME, name_of_list)
    items = NamedList(name_of_list, list(map(Item, names)))
    return items


def deleteList(list_id: str) -> None:
    sql_api.deleteList(DEFAULT_NAME, list_id)
