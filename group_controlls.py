import pymel.core as pm
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

def mayaWindow():

    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr),QtWidgets.QWidget)


def get_selection(list, elements):
    
    index = get_index(list)
    selection = elements[index]
    
    return selection

def get_index(list):

    index =list.currentIndex()
    return index



class group_controllers(QtWidgets.QDialog):
        
    #Konstruktor
    def __init__(self,parent=mayaWindow()):
            
        # Definiert Standardwerte jeder benötigten 
        # Variablen in der Klasse.
        self.winName = "Group Controllers"
        self.geo_name = ""
        self.selection = 0
        self.every_other_variable = 0
        self.selected_variable = 0
        self.not_selected_variable = 0
        self.list_of_elements = []
        
        
        super(group_controllers,self).__init__(parent)
              
        self.setWindowTitle(self.winName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, 1)
        self.resize(400, 250)
        self.layout()
    
    # Diese Funktion definiert den Aufbau der Bedienfläche.
    def layout(self):

        # Teilt die Bedienfläche in zwei Hauptgruppen ein.
        self.groups_group = QtWidgets.QGroupBox("Groups")
        self.edit_group = QtWidgets.QGroupBox()

        self.groups_layout = QtWidgets.QHBoxLayout()
        self.groups_list = QtWidgets.QComboBox()
        self.groups_list.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.groups_layout.addWidget(self.groups_list)
        self.groups_group.setLayout(self.groups_layout)

        
        #self.edit_layout = QtWidgets.QVBoxLayout()
        self.edit_layout = QtWidgets.QVBoxLayout()

        self.select_group_layout = QtWidgets.QHBoxLayout()
        self.selection_button = QtWidgets.QPushButton("Select", self)
        self.select_group_layout.addWidget(self.selection_button)

        self.text_layout = QtWidgets.QHBoxLayout()
        self.add_groups_label = QtWidgets.QLabel("Name of added group")
        self.add_groups_text = QtWidgets.QLineEdit(self)
        #self.add_groups_text.setText()
        self.text_layout.addWidget(self.add_groups_text)
        
        self.add_delete_group_layout = QtWidgets.QHBoxLayout()
        self.add_group_button = QtWidgets.QPushButton("Add",self)
        self.delete_group_button = QtWidgets.QPushButton("Delete", self)
        self.add_delete_group_layout.addWidget(self.add_group_button)
        self.add_delete_group_layout.addWidget(self.delete_group_button)

        self.add_remove_element_layout = QtWidgets.QHBoxLayout()
        self.add_element_to_group_button = QtWidgets.QPushButton("Add Element", self)
        self.remove_element_from_group_button = QtWidgets.QPushButton("Remove Element", self)
        self.add_remove_element_layout.addWidget(self.add_element_to_group_button)
        self.add_remove_element_layout.addWidget(self.remove_element_from_group_button)

        self.edit_layout.addLayout(self.select_group_layout)
        self.edit_layout.addLayout(self.text_layout)
        self.edit_layout.addLayout(self.add_delete_group_layout)
        self.edit_layout.addLayout(self.add_remove_element_layout)
        self.edit_group.setLayout(self.edit_layout)

        # Verbindet die beiden Hauptgruppen mit dem Hauptlayout und
        # setzt dieses.
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.addWidget(self.groups_group)
        main_layout.addWidget(self.edit_group)
        self.setLayout(main_layout)
		
        # Fügt Aktionen zu den Buttons und dem Zahlenregler hinzu.
        # Diese werden ausgeführt, sobald der Button betätigt
        # oder der Wert des Zahlenreglers verändert wird.
        self.selection_button.clicked.connect(self.select_group)
        self.add_group_button.clicked.connect(self.add_selection_to_list)
        self.delete_group_button.clicked.connect(self.delete_selected_group)
        self.add_element_to_group_button.clicked.connect(self.add_selection_to_group)
        self.remove_element_from_group_button.clicked.connect(self.remove_element_from_group)


    def add_selection_to_list(self):
        temp_selection = pm.ls(selection= True, fl = True)
        self.list_of_elements.append(temp_selection)

        self.groups_list.addItem(self.add_groups_text.text())
        self.add_groups_text.clear()
        pm.select(clear = True)

    def select_group(self):

        selection = get_selection(self.groups_list, self.list_of_elements)
        pm.select(selection)

    def delete_selected_group(self):

        #selection = get_selection(self.groups_list, self.list_of_elements)
        index = get_index(self.groups_list)

        self.list_of_elements.pop(index)
        self.groups_list.removeItem(index)

    def add_selection_to_group(self):
        selection = get_selection(self.groups_list, self.list_of_elements)
        index = get_index(self.groups_list)
        pm.select(selection, add=True)
        temp_selection = pm.ls(selection=True, fl=True)
        self.list_of_elements[index]= temp_selection
        pm.select(clear = True)


    def remove_element_from_group(self):
        selection = get_selection(self.groups_list, self.list_of_elements)
        index = get_index(self.groups_list)
        removeable_object = pm.ls(selection=True, fl=True)

        pm.select(selection)
        pm.select(removeable_object, deselect=True)
        temp_selection = pm.ls(selection=True, fl=True)
        self.list_of_elements[index]= temp_selection
        pm.select(clear = True)
    




    

# Dies sorgt für die Ausführung des Tools.                                 
if __name__=="__main__":
    myWin = group_controllers()
    myWin.show()
