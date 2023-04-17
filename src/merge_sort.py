import terminal_UI
from named_list import Item
from globals import *


def compare(first: Item, second: Item) -> bool:
    while True:
        terminal_UI.sendMessage(
            COMPARE_MESSAGE.format(
                first.name, second.name))
        answer = terminal_UI.getMessage()
        if answer not in [FIRST, SECOND]:
            terminal_UI.sendMessage(WRONG_COMPARE)
        else:
            return answer == SECOND


def merge(first_list: list, second_list: list) -> list:
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


def sort(list_for_sorted: list) -> list:
    if len(list_for_sorted) == 1:
        return list_for_sorted
    sort_left = sort(list_for_sorted[:len(list_for_sorted) // 2])
    sort_right = sort(list_for_sorted[len(list_for_sorted) // 2:])
    return merge(sort_left, sort_right)
