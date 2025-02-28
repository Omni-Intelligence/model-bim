import os
import sys
from PyQt6.QtWidgets import QApplication, QFileDialog


class QtFileDialog:
    @staticmethod
    def get_file():
        app = QApplication.instance() or QApplication(sys.argv)
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Select a file",
            os.path.expanduser("~"),
            "Power BI model files (*.bim)",
        )
        return file_path


def select_file():
    file_path = QtFileDialog.get_file()
    print(file_path)


if __name__ == "__main__":
    select_file()
