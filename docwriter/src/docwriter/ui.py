import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLineEdit, QLabel, QHBoxLayout, QMessageBox, QFileDialog
)

from core import *
from yaml_io import read_config as _read_config
from config import MKDOCS_CONFIG_PATH as _MKDOCS_CONFIG_PATH

if not _MKDOCS_CONFIG_PATH:
    print("config file not found")
    quit()

cfg = get_nav()

class NavManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DocWriter – Indexação MkDocs")
        self.resize(600, 500)

        self.selected_path = None  # armazena o item clicado
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self.on_item_clicked)  # novo

        self.refresh_tree()

        # Inputs
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("yaml_path (ex: Aplicações.Teste)")
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("file_path (ex: C:/docs/teste.md)")

        add_btn = QPushButton("Adicionar / Atualizar")
        remove_btn = QPushButton("Remover")

        add_btn.clicked.connect(self.add_item)
        remove_btn.clicked.connect(self.remove_item)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Estrutura atual"))
        layout.addWidget(self.tree)
        layout.addWidget(QLabel("YAML Path"))
        layout.addWidget(self.path_input)

        hbox = QHBoxLayout()
        layout.addLayout(hbox)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("file_path (ex: C:/docs/teste.md)")

        browse_btn = QPushButton("...")
        browse_btn.setMaximumWidth(30)
        browse_btn.clicked.connect(self.browse_file)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
       
        hbox.addWidget(add_btn)
        hbox.addWidget(remove_btn)

    # === CAPTURA DO ITEM CLICADO ===
    def on_item_clicked(self, item):
        parts = []
        node = item
        while node is not None:
            parts.insert(0, node.text(0))
            node = node.parent()
        self.selected_path = ".".join(parts)
        self.path_input.setText(self.selected_path)

    # === RENDERIZAÇÃO ===
    def refresh_tree(self):
        self.tree.clear()
        self.build_tree(self.tree, cfg)

    def build_tree(self, widget, nav_data):
        for item in nav_data:
            if isinstance(item, dict):
                for key, value in item.items():
                    node = QTreeWidgetItem([key])
                    widget.addTopLevelItem(node)
                    if isinstance(value, list):
                        self.build_subtree(node, value)
                    elif isinstance(value, str):
                        node.addChild(QTreeWidgetItem([value]))

    def build_subtree(self, parent, data):
        for item in data:
            if isinstance(item, dict):
                for key, value in item.items():
                    node = QTreeWidgetItem([key])
                    parent.addChild(node)
                    if isinstance(value, list):
                        self.build_subtree(node, value)
                    elif isinstance(value, str):
                        node.addChild(QTreeWidgetItem([value]))

    # === AÇÕES ===
    def add_item(self):
        yaml_path = self.path_input.text().strip()
        file_path = self.file_input.text().strip()
        try:
            if index(yaml_path, file_path):
                self.refresh_config()
                self.refresh_tree()
        except Exception as ex:
            QMessageBox.critical(self, "Erro ao indexar", str(ex))

    def refresh_config(self):
        """Recarrega o estado atual do mkdocs.yml"""
        global cfg
        cfg = _read_config(_MKDOCS_CONFIG_PATH)

    def remove_item(self):
        yaml_path = self.selected_path or self.path_input.text().strip()
        if not yaml_path:
            QMessageBox.warning(self, "Erro", "Selecione um item ou informe o yaml_path.")
            return
        try:
            if unindex(yaml_path):
                self.refresh_tree()
                self.selected_path = None
                self.path_input.clear()
        except Exception as ex:
            QMessageBox.critical(self, "Erro ao desindexar", str(ex))

    # --- função ---
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar arquivo Markdown", "", "Markdown Files (*.md);;All Files (*)")
        if file_path:
            self.file_input.setText(file_path)