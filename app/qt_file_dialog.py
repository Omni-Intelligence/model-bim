import os
import sys
from PyQt6.QtWidgets import QApplication, QFileDialog


class QtFileDialog:
    _app = None

    @staticmethod
    def get_file():
        """
        Show file dialog and return selected file path.
        Can be called multiple times in the same program.
        """
        # Get or create QApplication instance only once
        if QtFileDialog._app is None:
            QtFileDialog._app = QApplication.instance() or QApplication(sys.argv)

        try:
            # Create dialog as a temporary object
            file_path, _ = QFileDialog.getOpenFileName(
                parent=None,
                caption="Select a BIM file",
                directory=os.path.expanduser("~"),
                filter="Power BI model files (*.bim)",
                options=QFileDialog.Option.DontUseNativeDialog,
            )

            # Process any pending events
            QtFileDialog._app.processEvents()

            return file_path if file_path else None

        except Exception as e:
            print(f"Error in file dialog: {e}", file=sys.stderr)
            return None


def select_file():
    file_path = QtFileDialog.get_file()
    print(file_path)


if __name__ == "__main__":
    select_file()
