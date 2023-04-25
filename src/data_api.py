import sql_api
from item import Item
from globals import *


def saveList(name_of_list: str, new_list: list) -> None:
    sql_api.insertList(DEFAULT_NAME, name_of_list, new_list, False, False)


def saveItem(name_of_item: str, name_of_list: str) -> None:
    sql_api.insertItem(DEFAULT_NAME, name_of_list, name_of_item)


def deleteItem(name_of_item: str, name_of_list: str) -> None:
    sql_api.deleteItem(DEFAULT_NAME, name_of_list, name_of_item)


def saveSortedList(name_of_list: str, new_list: list) -> None:
    is_favorite = sql_api.isFavorite(DEFAULT_NAME, name_of_list)
    sql_api.deleteList(DEFAULT_NAME, name_of_list)
    sql_api.insertList(DEFAULT_NAME, name_of_list, new_list, True, is_favorite)


def addToFavorites(name_of_list: str, is_sorted: bool) -> None:
    old_list = uploadList(name_of_list)
    sql_api.deleteList(DEFAULT_NAME, name_of_list)
    sql_api.insertList(DEFAULT_NAME, name_of_list, old_list, is_sorted, True)


def removeFromFavorites(name_of_list: str) -> None:
    old_list = uploadList(name_of_list)
    sql_api.deleteList(DEFAULT_NAME, name_of_list)
    sql_api.insertList(DEFAULT_NAME, name_of_list, old_list, True, False)


def uploadNamesOfLists(is_sorted: bool, is_favorite: bool = False) -> list:
    return sql_api.getNamesOfLists(DEFAULT_NAME, is_sorted, is_favorite)


def uploadList(name_of_list: str) -> list:
    names = sql_api.getNamesInList(DEFAULT_NAME, name_of_list)
    return list(map(Item, names))

def isSorted(name_of_list: str) -> bool:
    return sql_api.isSorted(DEFAULT_NAME, name_of_list)

def deleteList(list_id: str) -> None:
    sql_api.deleteList(DEFAULT_NAME, list_id)


def sort(list_for_sorted: list, compare) -> list:
    def merge(first_list: list, second_list: list, compare) -> list:
        ans = []
        index_in_first = 0
        index_in_second = 0
        while index_in_first < len(first_list) and \
                index_in_second < len(second_list):
            if not compare(first_list[index_in_first],
                           second_list[index_in_second]):
                ans.append(first_list[index_in_first])
                index_in_first += 1
            else:
                ans.append(second_list[index_in_second])
                index_in_second += 1
        while index_in_first < len(first_list):
            ans.append(first_list[index_in_first])
            index_in_first += 1
        while index_in_second < len(second_list):
            ans.append(second_list[index_in_second])
            index_in_second += 1
        return ans

    if len(list_for_sorted) == 1:
        return list_for_sorted
    sort_left = sort(list_for_sorted[:len(list_for_sorted) // 2], compare)
    sort_right = sort(list_for_sorted[len(list_for_sorted) // 2:], compare)
    return merge(sort_left, sort_right, compare)
