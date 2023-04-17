class NamedList(list):
    def __init__(self, name='', common_list=[]):
        super().__init__(common_list)
        self.name = name


class Item:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name
