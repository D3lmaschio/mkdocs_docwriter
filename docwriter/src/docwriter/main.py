import sys
import os
import shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QFileDialog, QTreeView, QInputDialog
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from docwriter.ui_mainwindow import Ui_MainWindow
from docwriter.core import (
    get_nav, index, unindex, _unmap_folders, _map_folders, _write_config, _read_config, _MKDOCS_CONFIG_PATH, _MKDOCS_DOC_ROOT_PATH, index_folder
)
from docwriter.navtree import nav_get, nav_add, nav_remove, nav_update


if not _MKDOCS_CONFIG_PATH:
    print("MKDOCS_CONFIG_PATH incorreto.")
    quit()
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("MkDocs Editor")

        self.selected_path = None
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Documentação"])
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.clicked.connect(self.on_tree_clicked)

        self.ui.pushButton.clicked.connect(self.create_document)
        self.ui.pushButton_2.clicked.connect(self.remove_document)
        self.ui.pushButton_3.clicked.connect(self.apply_update)
        self.ui.toolButton.clicked.connect(self.browse_file)
        self.ui.pushButton_refresh.clicked.connect(self.refresh_tree)
        self.ui.pushButton_rename.clicked.connect(self.rename_document)
        self.ui.pushButton_create_index.clicked.connect(self.create_index)  # NOVO

        self.refresh_tree()

    def refresh_tree(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Documentação"])
        nav = get_nav()
        if nav:
            self.build_tree(self.model, nav)

    def build_tree(self, parent, nav_data):
        for item in nav_data:
            if isinstance(item, dict):
                for key, value in item.items():
                    node = QStandardItem(str(key))
                    parent.appendRow(node)
                    if isinstance(value, list):
                        self.build_tree(node, value)
                    elif isinstance(value, str):
                        leaf = QStandardItem(str(value))
                        node.appendRow(leaf)
            elif isinstance(item, str):
                leaf = QStandardItem(os.path.basename(item))
                parent.appendRow(leaf)

    def on_tree_clicked(self, index):
        item = self.model.itemFromIndex(index)
        path = []
        while item:
            path.insert(0, item.text())
            item = item.parent()
        tree_path = ".".join(path)
        self.selected_path = tree_path

        nav = get_nav()
        value = nav_get(nav, tree_path) if nav else None

        self.ui.lineEdit_2.setText(tree_path)
        if isinstance(value, str):
            self.ui.lineEdit.setText(value)
        else:
            self.ui.lineEdit.setText("")

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar arquivo Markdown", "", "Markdown Files (*.md);;All Files (*)")
        if file_path:
            self.ui.lineEdit.setText(file_path)

    def create_document(self):
        yaml_path = self.ui.lineEdit_2.text().strip()
        file_path = self.ui.lineEdit.text().strip()
        if not file_path:
            QMessageBox.warning(self, "Aviso", "Informe o caminho do documento antes de adicionar.")
            return
        try:
            if index(yaml_path, file_path):
                self.refresh_tree()
                QMessageBox.information(self, "Sucesso", "Documento adicionado.")
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
                self.selected_path = None
            else:
                QMessageBox.warning(self, "Aviso", "Já existe um documento neste caminho.")
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
                self.selected_path = None
        except Exception as ex:
            QMessageBox.critical(self, "Erro ao adicionar", str(ex))
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            self.selected_path = None

    def remove_document(self):
        yaml_path = self.selected_path or self.ui.lineEdit_2.text().strip()
        file_path = self.ui.lineEdit.text().strip()
        if not yaml_path:
            QMessageBox.warning(self, "Erro", "Selecione um item ou informe o yaml_path.")
            return

        nav = get_nav()
        value = nav_get(nav, yaml_path) if nav else None

        if isinstance(value, list) and value:
            reply = QMessageBox.question(
                self,
                "Confirmação de exclusão",
                "Esta pasta e todos os seus documentos e subpastas serão excluídos do sistema e do mkdocs. Tem certeza?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
            # Remove do nav/yaml
            unindex(yaml_path, "")
            # Remove do diretório físico (recursivo)
            keys = yaml_path.split('.')
            folder_path = os.path.join(_MKDOCS_DOC_ROOT_PATH, *keys)
            if os.path.isdir(folder_path):
                shutil.rmtree(folder_path)
        else:
            # Documento simples
            if unindex(yaml_path, file_path):
                _unmap_folders(yaml_path, file_path)

        self.refresh_tree()
        self.selected_path = None
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit.clear()
        QMessageBox.information(self, "Sucesso", "Item removido.")

    def apply_update(self):
        yaml_path = self.ui.lineEdit_2.text().strip()
        file_path = self.ui.lineEdit.text().strip()
        nav = get_nav()
        try:
            if nav is not None and nav_update(nav, yaml_path, file_path):
                cfg = _read_config(_MKDOCS_CONFIG_PATH)
                if isinstance(cfg, dict):
                    cfg['nav'] = nav
                    _write_config(_MKDOCS_CONFIG_PATH, cfg)
                    self.refresh_tree()
                    QMessageBox.information(self, "Sucesso", "Documento atualizado.")
                    self.ui.lineEdit.clear()
                    self.ui.lineEdit_2.clear()
                    self.selected_path = None
                else:
                    QMessageBox.warning(self, "Erro", "Configuração inválida.")
                    self.ui.lineEdit.clear()
                    self.ui.lineEdit_2.clear()
                    self.selected_path = None
            else:
                QMessageBox.warning(self, "Aviso", "Não foi possível atualizar o documento.")
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
                self.selected_path = None
        except Exception as ex:
            QMessageBox.critical(self, "Erro ao atualizar", str(ex))
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            self.selected_path = None

    def create_index(self):
        yaml_path = self.selected_path or self.ui.lineEdit_2.text().strip()
        if not yaml_path:
            QMessageBox.warning(self, "Erro", "Selecione uma pasta para indexar.")
            return
        try:
            result = index_folder(yaml_path)
            if result:
                self.refresh_tree()
                QMessageBox.information(self, "Sucesso", f"index.md indexado para: {yaml_path}")
            else:
                QMessageBox.warning(self, "Aviso", "Não foi possível indexar o index.md.")
        except Exception as ex:
            QMessageBox.critical(self, "Erro ao indexar", str(ex))
    
    def rename_document(self):
        yaml_path = self.selected_path or self.ui.lineEdit_2.text().strip()
        if not yaml_path:
            QMessageBox.warning(self, "Erro", "Selecione um item para renomear.")
            return

        nav = get_nav()
        value = nav_get(nav, yaml_path) if nav else None

        new_name, ok = QInputDialog.getText(self, "Renomear", "Novo nome:")
        if not ok or not new_name.strip():
            return

        keys = yaml_path.split('.')
        parent_path = ".".join(keys[:-1])
        old_dir = os.path.join(_MKDOCS_DOC_ROOT_PATH, *keys)
        new_keys = keys[:-1] + [new_name.strip()]
        new_yaml_path = ".".join(new_keys)
        new_dir = os.path.join(_MKDOCS_DOC_ROOT_PATH, *new_keys)

        # Renomeia diretório físico
        if os.path.isdir(old_dir):
            os.rename(old_dir, new_dir)

        # Atualiza nav
        if nav and nav_remove(nav, yaml_path):
            nav_add(nav, new_yaml_path, os.path.join(new_dir, "index.md"))
            cfg = _read_config(_MKDOCS_CONFIG_PATH)
            if isinstance(cfg, dict):
                cfg['nav'] = nav
                _write_config(_MKDOCS_CONFIG_PATH, cfg)

        self.refresh_tree()
        self.selected_path = None
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit.clear()
        QMessageBox.information(self, "Sucesso", "Item renomeado.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())