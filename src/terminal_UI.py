import request
from globals import *


def main() -> None:
    sendMessage(HELLO_MESSAGE)
    sendMessage(COMMANDS)
    sendMessage(SEPARATOR)
    while True:
        command = getMessage().strip()
        if command == HELP_COMMAND:
            sendMessage(COMMANDS)
        elif command == LISTS_COMMAND:
            request.printAllLists()
        elif command == PRINT_LIST_COMMAND:
            request.printOneList()
        elif command == PRINT_RATING_COMMAND:
            request.printOneList(True)
        elif command == RATINGS_COMMAND:
            request.printAllLists(True)
        elif command == BUILD_COMMAND:
            request.buildRating()
        elif command == ADD_LIST_COMMAND:
            request.addNewList()
        elif command == DELETE_COMMAND:
            request.deleteList()
        elif command == ADD_ITEM_COMMAND:
            request.addItemToList()
        elif command == EXIT_COMMAND:
            break
        else:
            sendMessage(WRONG_COMMAND.format(command))
        sendMessage(SEPARATOR)


def sendMessage(message: str) -> None:
    print(message)


def getMessage() -> str:
    return input()
