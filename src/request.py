import terminal_UI
import data_processor
import merge_sort
from named_list import NamedList, Item
from globals import *


def printList(print_list: list, is_sorted: bool = False) -> None:
    for i, item in enumerate(print_list):
        line = str(item.name)
        if is_sorted:
            line = str(i + 1) + ': ' + line
        terminal_UI.sendMessage(line)


def printAllLists(is_sorted: bool = False) -> None:
    names = data_processor.uploadNamesOfLists(is_sorted)
    if not len(names):
        terminal_UI.sendMessage(NO_RATINGS if is_sorted else NO_LISTS)
    else:
        terminal_UI.sendMessage('\n'.join(names))


def choose(is_sorted: bool) -> str:
    names = data_processor.uploadNamesOfLists(is_sorted)
    if not len(names):
        terminal_UI.sendMessage(NO_RATINGS if is_sorted else NO_LISTS)
        raise Exception
    terminal_UI.sendMessage(CHOOSE_MESSAGE)
    terminal_UI.sendMessage('\n'.join(names))
    name = terminal_UI.getMessage()
    if name == STOP_COMMAND:
        raise Exception
    if name not in names:
        terminal_UI.sendMessage(WRONG_MESSAGE)
        raise Exception
    return name


def printOneList(is_sorted: bool = False) -> None:
    try:
        name = choose(is_sorted)
        printList(data_processor.uploadList(name), is_sorted)
    except Exception:
        pass


def buildRating() -> None:
    try:
        name = choose(False)
        current_list = data_processor.uploadList(name)
        sorted_list = NamedList(name, merge_sort.sort(current_list))
        terminal_UI.sendMessage(NEW_RATING)
        printList(sorted_list, True)
        data_processor.saveSortedList(sorted_list)
        terminal_UI.sendMessage(RATING_SAVED)
    except Exception:
        pass


def addNewList() -> None:
    terminal_UI.sendMessage(NEW_LIST)
    name = terminal_UI.getMessage()
    if name == STOP_COMMAND:
        return
    new_item = ''
    items = NamedList(name)
    while True:
        terminal_UI.sendMessage(NEXT_ITEM)
        new_item = terminal_UI.getMessage()
        if new_item == STOP_COMMAND:
            break
        items.append(Item(new_item))
    data_processor.saveList(items)
    terminal_UI.sendMessage(LIST_SAVED)


def addItemToList() -> None:
    try:
        name_of_list = choose(False)
        terminal_UI.sendMessage(ADD_ITEM)
        new_item = terminal_UI.getMessage()
        data_processor.saveItem(Item(new_item), name_of_list)
        terminal_UI.sendMessage(ITEM_SAVED)
    except Exception:
        pass


def deleteList() -> None:
    try:
        name = choose(False)
        data_processor.deleteList(name)
    except Exception:
        pass
