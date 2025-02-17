import subprocess
import sys
from tkinter import messagebox
import os
import zipfile
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD


class DnDTk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


class FileHandler:
    @staticmethod
    def is_valid_file_type(file_path):
        valid_extensions = (".pbix", ".txt", ".csv", ".json")
        return file_path.lower().endswith(valid_extensions)

    @staticmethod
    def select_file():
        result = subprocess.run(
            [
                sys.executable,
                os.path.join(os.path.dirname(__file__), "qt_file_dialog.py"),
            ],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    @staticmethod
    def read_file(file_path):
        if file_path.lower().endswith(".pbix"):
            return FileHandler.read_pbix_report(file_path)
        try:
            with open(file_path, "r") as file:
                return {"content": file.read()}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {str(e)}")
            return None

    @staticmethod
    def read_pbix_report(pbix_path):
        MAX_CHARS = 1048546
        MAX_BYTES = 502857

        try:
            with zipfile.ZipFile(pbix_path, "r") as zip_ref:
                contents = {}

                if "Report/Layout" in zip_ref.namelist():
                    with zip_ref.open("Report/Layout", "r") as report_file:
                        content = report_file.read().decode("utf-8", errors="replace")

                        if len(content) > MAX_CHARS:
                            contents["content"] = (
                                content[:MAX_CHARS] + "\n... (content truncated)"
                            )
                        else:
                            contents["content"] = content

                if "DataModel" in zip_ref.namelist():
                    with zip_ref.open("DataModel", "r") as model_file:
                        model_content = model_file.read().decode(
                            "utf-8", errors="replace"
                        )

                        if len(model_content) > MAX_BYTES:
                            contents["modelContent"] = model_content[:MAX_BYTES]
                        else:
                            contents["modelContent"] = model_content

                if not contents:
                    messagebox.showerror(
                        "Error", "No report file found in the PBIX file."
                    )
                    return None

                return contents
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read PBIX file: {str(e)}")
            return None
