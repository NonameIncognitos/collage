import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout,
    QWidget, QHBoxLayout, QListWidget, QMessageBox, QLineEdit, QSpinBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from utils.collage import create_collage
import os


class CollageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Collage Creator")
        self.setGeometry(100, 100, 1000, 700)

        self.image_paths = []
        self.output_path = "output"
        self.output_name = "collage.jpg"
        self.collage_width = 800

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Buttons
        button_layout = QHBoxLayout()
        btn_add_images = QPushButton("Add Images")
        btn_add_images.clicked.connect(self.add_images)
        button_layout.addWidget(btn_add_images)

        btn_add_single = QPushButton("Add Single Image")
        btn_add_single.clicked.connect(self.add_single_image)
        button_layout.addWidget(btn_add_single)

        btn_remove = QPushButton("Remove Selected")
        btn_remove.clicked.connect(self.remove_selected_images)
        button_layout.addWidget(btn_remove)

        btn_clear = QPushButton("Clear All")
        btn_clear.clicked.connect(self.clear_images)
        button_layout.addWidget(btn_clear)

        main_layout.addLayout(button_layout)

        # Image list
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        main_layout.addWidget(self.list_widget)

        # Customization options
        options_layout = QHBoxLayout()
        
        # Output folder
        btn_output_folder = QPushButton("Select Save Folder")
        btn_output_folder.clicked.connect(self.select_output_folder)
        options_layout.addWidget(btn_output_folder)
        
        self.line_output_folder = QLineEdit(self.output_path)
        options_layout.addWidget(self.line_output_folder)

        # Output name
        self.line_output_name = QLineEdit(self.output_name)
        options_layout.addWidget(QLabel("Name:"))
        options_layout.addWidget(self.line_output_name)

        # Collage width
        self.spin_collage_width = QSpinBox()
        self.spin_collage_width.setRange(200, 5000)
        self.spin_collage_width.setValue(self.collage_width)
        options_layout.addWidget(QLabel("Width:"))
        options_layout.addWidget(self.spin_collage_width)

        main_layout.addLayout(options_layout)

        # Create collage button
        btn_create_collage = QPushButton("Create Collage")
        btn_create_collage.clicked.connect(self.create_collage)
        main_layout.addWidget(btn_create_collage)

        # Collage preview
        self.label_collage = QLabel("Your collage will appear here.")
        self.label_collage.setAlignment(Qt.AlignCenter)
        self.label_collage.setMinimumHeight(400)
        main_layout.addWidget(self.label_collage)

        # Set main widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def add_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "",
                                                "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)")
        if files:
            self.image_paths.extend(files)
            self.update_list_widget()

    def add_single_image(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Single Image", "",
                                              "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)")
        if file:
            self.image_paths.append(file)
            self.update_list_widget()

    def update_list_widget(self):
        self.list_widget.clear()
        for path in self.image_paths:
            self.list_widget.addItem(os.path.basename(path))

    def remove_selected_images(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return

        selected_names = [item.text() for item in selected_items]
        self.image_paths = [path for path in self.image_paths if os.path.basename(path) not in selected_names]
        self.update_list_widget()

    def clear_images(self):
        self.image_paths = []
        self.list_widget.clear()

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_path = folder
            self.line_output_folder.setText(folder)

    def create_collage(self):
        if not self.image_paths:
            QMessageBox.warning(self, "Warning", "Please select images first.")
            return

        self.output_path = self.line_output_folder.text()
        self.output_name = self.line_output_name.text()
        self.collage_width = self.spin_collage_width.value()

        full_output_path = os.path.join(self.output_path, self.output_name)

        try:
            create_collage(self.image_paths, full_output_path, collage_width=self.collage_width)

            pixmap = QPixmap(full_output_path)
            scaled_pixmap = pixmap.scaled(
                self.label_collage.width(),
                self.label_collage.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label_collage.setPixmap(scaled_pixmap)
            QMessageBox.information(self, "Success", f"Collage saved to: {full_output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error creating collage: {str(e)}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.label_collage.pixmap():
            scaled_pixmap = self.label_collage.pixmap().scaled(
                self.label_collage.width(),
                self.label_collage.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label_collage.setPixmap(scaled_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CollageApp()
    window.show()
    sys.exit(app.exec_())
