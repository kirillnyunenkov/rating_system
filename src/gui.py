from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QLineEdit
from functools import partial
import data_api


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setFixedSize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.lists = QtWidgets.QWidget()
        self.lists.setObjectName("lists")

        self.tabWidget.addTab(self.lists, "")
        self.ratings = QtWidgets.QWidget()
        self.ratings.setObjectName("ratings")
        self.tabWidget.addTab(self.ratings, "")
        self.favorites = QtWidgets.QWidget()
        self.favorites.setObjectName("favorites")
        self.tabWidget.addTab(self.favorites, "")

        MainWindow.setCentralWidget(self.centralwidget)
        self.listNames = data_api.uploadNamesOfLists(False)
        self.ratingNames = data_api.uploadNamesOfLists(True)
        self.favoritesNames = data_api.uploadNamesOfLists(True, True)
        self.listButtons = []
        self.ratingButtons = []
        self.favoritesButtons = []
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.MainWindow = MainWindow
        self.updateUI()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.lists), _translate("MainWindow", "Lists"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.ratings), _translate("MainWindow", "Ratings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.favorites), _translate("MainWindow", "Favorites"))

    def updateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setListButtons(_translate)
        self.setAddListButton(_translate)
        self.setRatingButtons(_translate)
        self.setFavoritesButtons(_translate)

    def setListButtons(self, _translate):
        for button in self.listButtons:
            button.deleteLater()
        self.listButtons = []
        topShift = 20
        for i in range(len(self.listNames)):
            name = self.listNames[i]
            self.listButtons.append(QtWidgets.QPushButton(self.lists))
            self.listButtons[-1].setGeometry(QtCore.QRect(20,
                                             topShift, 100, 30))
            self.listButtons[-1].setObjectName('list-' + name)
            self.listButtons[-1].setText(_translate("MainWindow", name))
            self.listButtons[-1].clicked.connect(partial(self.printList, name))
            topShift += 40

    def setAddListButton(self, _translate):
        self.addButton = QtWidgets.QPushButton(self.lists)
        self.addButton.setGeometry(QtCore.QRect(680, 20, 100, 30))
        self.addButton.setObjectName('addButton')
        self.addButton.setText(_translate("MainWindow", 'Add new list'))
        self.addButton.clicked.connect(self.addList)

    def setRatingButtons(self, _translate):
        for button in self.ratingButtons:
            button.deleteLater()
        self.ratingButtons = []
        topShift = 20
        for i in range(len(self.ratingNames)):
            name = self.ratingNames[i]
            self.ratingButtons.append(QtWidgets.QPushButton(self.ratings))
            self.ratingButtons[-1].setGeometry(
                QtCore.QRect(20, topShift, 100, 30))
            self.ratingButtons[-1].setObjectName('rating-' + name)
            self.ratingButtons[-1].setText(_translate("MainWindow", name))
            self.ratingButtons[-1].clicked.connect(
                partial(self.printRating, name))
            topShift += 40

    def setFavoritesButtons(self, _translate):
        for button in self.favoritesButtons:
            button.deleteLater()
        self.favoritesButtons = []
        topShift = 20
        for i in range(len(self.favoritesNames)):
            name = self.favoritesNames[i]
            self.favoritesButtons.append(QtWidgets.QPushButton(self.favorites))
            self.favoritesButtons[-1].setGeometry(
                QtCore.QRect(20, topShift, 100, 30))
            self.favoritesButtons[-1].setObjectName('favorite-' + name)
            self.favoritesButtons[-1].setText(_translate("MainWindow", name))
            self.favoritesButtons[-1].clicked.connect(
                partial(self.printFavorite, name))
            topShift += 40

    def addList(self):
        newListWindow = QDialog()
        newListWindow.setWindowTitle('New list')

        newListWindow.layout = QVBoxLayout()
        newListWindow.layout.addWidget(QLabel('Write name of list'))
        textbox = QLineEdit()
        newListWindow.layout.addWidget(textbox)
        box = QDialogButtonBox()
        self.newListName = ''
        box.addButton(
            "Save name",
            QDialogButtonBox.ActionRole).clicked.connect(
            partial(
                self.saveName,
                newListWindow,
                textbox))
        self.goFurther = True
        box.addButton(
            QDialogButtonBox.Close).clicked.connect(
            partial(
                self.closeWindow,
                newListWindow))
        newListWindow.layout.addWidget(box)
        newListWindow.setLayout(newListWindow.layout)
        newListWindow.setWindowFlags(QtCore.Qt.Window |
                                     QtCore.Qt.CustomizeWindowHint |
                                     QtCore.Qt.WindowTitleHint |
                                     QtCore.Qt.WindowMinimizeButtonHint
                                     )
        newListWindow.exec_()
        if self.goFurther:
            data_api.saveList(self.newListName, [])
            while self.addItem(self.newListName, None):
                pass
        self.setupUi(self.MainWindow)

    def saveName(self, newListWindow, textbox):
        text = textbox.text()
        newListWindow.accept()
        self.newListName = text

    def printList(self, name):
        list_to_print = data_api.uploadList(name)
        names_of_items = [item.name for item in list_to_print]
        listWindow = QDialog()
        listWindow.setWindowTitle(name)
        listWindow.layout = QVBoxLayout()
        listWindow.layout.addWidget(QLabel('\n'.join(names_of_items)))
        box = QDialogButtonBox()
        box.addButton("Add item", QDialogButtonBox.ActionRole).clicked.connect(
            partial(self.addItem, name, listWindow))
        box.addButton(
            "Build rating",
            QDialogButtonBox.ActionRole).clicked.connect(
            partial(
                self.buildRating,
                name,
                listWindow))

        box.addButton(
            "Delete list",
            QDialogButtonBox.ActionRole).clicked.connect(
            partial(
                self.deleteList,
                name,
                listWindow))
        box.addButton(
            "Delete item",
            QDialogButtonBox.ActionRole).clicked.connect(
            partial(
                self.chooseItemToDelete,
                name,
                names_of_items,
                listWindow))
        listWindow.layout.addWidget(box)
        listWindow.setLayout(listWindow.layout)
        listWindow.exec_()

    def addToFavorites(self, name, ratingWindow):
        ratingWindow.accept()
        data_api.addToFavorites(name)
        self.setupUi(self.MainWindow)

    def printRating(self, name):
        rating_to_print = data_api.uploadList(name)
        names_of_items = [item.name for item in rating_to_print]
        text = ''
        for i, item in enumerate(names_of_items):
            text += str(i + 1) + ': ' + item + '\n'
        ratingWindow = QDialog()
        ratingWindow.setWindowTitle(name)
        ratingWindow.layout = QVBoxLayout()
        ratingWindow.layout.addWidget(QLabel(text))
        box = QDialogButtonBox()
        box.addButton(
            "Add to favorites",
            QDialogButtonBox.ActionRole).clicked.connect(
            partial(
                self.addToFavorites,
                name,
                ratingWindow))
        ratingWindow.layout.addWidget(box)
        ratingWindow.setLayout(ratingWindow.layout)
        ratingWindow.exec_()

    def printFavorite(self, name):
        favorite_to_print = data_api.uploadList(name)
        names_of_items = [item.name for item in favorite_to_print]
        text = ''
        for i, item in enumerate(names_of_items):
            text += str(i + 1) + ': ' + item + '\n'
        favoriteWindow = QDialog()
        favoriteWindow.layout = QVBoxLayout()
        favoriteWindow.setWindowTitle(name)
        favoriteWindow.layout.addWidget(QLabel(text))
        box = QDialogButtonBox()
        box.addButton(
            "Remove from favorites",
            QDialogButtonBox.ActionRole).clicked.connect(
            partial(
                self.removeFromFavorites,
                name,
                favoriteWindow))
        favoriteWindow.layout.addWidget(box)
        favoriteWindow.setLayout(favoriteWindow.layout)
        favoriteWindow.exec_()

    def removeFromFavorites(self, name, favoriteWindow):
        favoriteWindow.accept()
        data_api.removeFromFavorites(name)
        self.setupUi(self.MainWindow)

    def deleteList(self, name, listWindow):
        listWindow.accept()
        data_api.deleteList(name)
        self.setupUi(self.MainWindow)

    def chooseItemToDelete(self, name, names_of_items, listWindow):
        listWindow.accept()
        deleteWindow = QDialog()
        deleteWindow.setWindowTitle('Delete item')

        deleteWindow.layout = QVBoxLayout()
        deleteWindow.layout.addWidget(
            QLabel('\n'.join(names_of_items) + '\n\n'))
        deleteWindow.layout.addWidget(QLabel('Write name'))
        textbox = QLineEdit()
        deleteWindow.layout.addWidget(textbox)
        box = QDialogButtonBox()
        box.addButton(
            "Delete this item",
            QDialogButtonBox.ActionRole).clicked.connect(
            partial(
                self.deleteItem,
                name,
                names_of_items,
                deleteWindow,
                textbox))
        box.addButton(
            QDialogButtonBox.Close).clicked.connect(
            partial(
                self.closeWindow,
                deleteWindow))
        deleteWindow.layout.addWidget(box)
        deleteWindow.setLayout(deleteWindow.layout)
        deleteWindow.exec_()

    def deleteItem(self, name, names_of_items, deleteWindow, textbox):
        deleteWindow.accept()
        text = textbox.text()
        if text in names_of_items:
            data_api.deleteItem(text, name)
        else:
            errorWindow = QDialog()
            errorWindow.setWindowTitle('Error')
            errorWindow.layout = QVBoxLayout()
            errorWindow.layout.addWidget(QLabel("Item doesn't consist"))
            box = QDialogButtonBox()
            box.addButton(
                QDialogButtonBox.Close).clicked.connect(
                partial(
                    self.closeWindow,
                    errorWindow))
            errorWindow.layout.addWidget(box)
            errorWindow.setLayout(errorWindow.layout)
            errorWindow.exec_()
        self.setupUi(self.MainWindow)

    def buildRating(self, name, listWindow):
        listWindow.accept()
        current_list = data_api.uploadList(name)
        sorted_list = data_api.sort(
            current_list, lambda x, y: self.compare(x, y))
        data_api.saveSortedList(name, sorted_list)
        self.setupUi(self.MainWindow)

    def compare(self, first, second):
        compareWindow = QDialog()
        compareWindow.setWindowTitle('Choose one')
        compareWindow.layout = QVBoxLayout()
        self.first_answer = False
        self.second_answer = False
        box = QDialogButtonBox()
        box.addButton(first.name, QDialogButtonBox.ActionRole).clicked.connect(
            partial(self.choose_first, compareWindow))
        box.addButton(
            second.name,
            QDialogButtonBox.ActionRole).clicked.connect(
            partial(
                self.choose_second,
                compareWindow))
        compareWindow.layout.addWidget(box)
        compareWindow.setLayout(compareWindow.layout)
        compareWindow.setWindowFlags(QtCore.Qt.Window |
                                     QtCore.Qt.CustomizeWindowHint |
                                     QtCore.Qt.WindowTitleHint |
                                     QtCore.Qt.WindowMinimizeButtonHint
                                     )
        compareWindow.exec_()
        return self.second_answer

    def choose_first(self, compareWindow):
        compareWindow.accept()
        self.first_answer = True

    def choose_second(self, compareWindow):
        compareWindow.accept()
        self.second_answer = True

    def addItem(self, name, listWindow):
        if listWindow:
            listWindow.accept()
        itemWindow = QDialog()
        itemWindow.setWindowTitle('New item')

        itemWindow.layout = QVBoxLayout()
        itemWindow.layout.addWidget(QLabel('Write name'))
        textbox = QLineEdit()
        itemWindow.layout.addWidget(textbox)
        box = QDialogButtonBox()
        box.addButton(
            "Save item",
            QDialogButtonBox.ActionRole).clicked.connect(
            partial(
                self.saveItem,
                name,
                itemWindow,
                textbox))
        box.addButton(
            QDialogButtonBox.Close).clicked.connect(
            partial(
                self.closeWindow,
                itemWindow))
        itemWindow.layout.addWidget(box)
        itemWindow.setLayout(itemWindow.layout)
        return itemWindow.exec_()

    def closeWindow(self, window):
        self.goFurther = False
        window.reject()

    def saveItem(self, name, itemWindow, textbox):
        text = textbox.text()
        itemWindow.accept()
        data_api.saveItem(text, name)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
