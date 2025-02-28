import subprocess
import sys
import time
from tkinter import Tk, filedialog, messagebox
import os
import zipfile


class FileHandler:
    @staticmethod
    def is_valid_file_type(file_path):
        valid_extensions = ".bim"
        return file_path.lower().endswith(valid_extensions)

    @staticmethod
    def select_file():
        file_path = filedialog.askopenfilename(
            title="Select a Power BI Model file",
            initialdir=os.path.expanduser("~"),
            filetypes=[("Power BI Model files", "*.bim")],
        )

        return file_path if file_path else ""

    @staticmethod
    def read_file(file_path):
        try:
            with open(file_path, "r") as file:
                return file.read()
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

    @staticmethod
    def save_as_txt(content, filename=None, file_prefix=None):
        """Save content as a text file."""
        if not filename:
            prefix = file_prefix if file_prefix else "analysis"
            filename = os.path.join(
                os.path.expanduser("~"), f"{prefix}_{int(time.time())}.txt"
            )

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("Success", f"File saved to {filename}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save text file: {str(e)}")
            return False

    @staticmethod
    def save_as_doc(content, filename=None, file_prefix=None):
        """Save content as a Word document."""
        try:
            from docx import Document
            from docx.shared import Pt, RGBColor, Inches
            from docx.enum.text import WD_ALIGN_PARAGRAPH
        except ImportError:
            messagebox.showerror(
                "Error",
                "Python-docx package is required to save as DOC. Please install it with 'pip install python-docx'",
            )
            return False

        if not filename:
            prefix = file_prefix if file_prefix else "analysis"
            filename = os.path.join(
                os.path.expanduser("~"), f"{prefix}_{int(time.time())}.docx"
            )

        try:
            doc = Document()
            style = doc.styles["Normal"]
            style.font.name = "Calibri"
            style.font.size = Pt(12)

            # Add logo at the top
            logo_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "assets",
                "images",
                "ah_logo.png",
            )

            # Add logo to the document
            logo_paragraph = doc.add_paragraph()
            logo_paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            logo_run = logo_paragraph.add_run()
            logo_run.add_picture(logo_path, width=Inches(2.0))

            # Add a space after the logo
            doc.add_paragraph()

            # Define custom heading styles to match our CSS
            h1_style = doc.styles["Heading 1"]
            h1_style.font.name = "Calibri"
            h1_style.font.size = Pt(28)
            h1_style.font.bold = True
            h1_style.font.color.rgb = RGBColor(202, 90, 139)  # #ca5a8b

            h2_style = doc.styles["Heading 2"]
            h2_style.font.name = "Calibri"
            h2_style.font.size = Pt(22)
            h2_style.font.bold = True
            h2_style.font.color.rgb = RGBColor(102, 84, 245)  # #6654f5

            h3_style = doc.styles["Heading 3"]
            h3_style.font.name = "Calibri"
            h3_style.font.size = Pt(18)
            h3_style.font.bold = True
            h3_style.font.color.rgb = RGBColor(102, 84, 245)  # #6654f5

            # Split content by lines and add to document
            for line in content.split("\n"):
                if line.startswith("# "):
                    doc.add_heading(line[2:], level=1)
                elif line.startswith("## "):
                    doc.add_heading(line[3:], level=2)
                elif line.startswith("### "):
                    doc.add_heading(line[4:], level=3)
                elif line.startswith("- "):
                    doc.add_paragraph(line[2:], style="List Bullet")
                elif line.startswith("1. "):
                    doc.add_paragraph(line[3:], style="List Number")
                elif line.strip() == "":
                    doc.add_paragraph()
                else:
                    doc.add_paragraph(line)

            doc.save(filename)
            messagebox.showinfo("Success", f"File saved to {filename}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save Word document: {str(e)}")
            return False

    @staticmethod
    def save_as_pdf(content, filename=None, file_prefix=None):
        """Save content as a PDF file."""
        try:
            import weasyprint
            import base64
        except ImportError:
            messagebox.showerror(
                "Error",
                "WeasyPrint package is required to save as PDF. Please install it with 'pip install weasyprint'",
            )
            return False

        if not filename:
            prefix = file_prefix if file_prefix else "analysis"
            filename = os.path.join(
                os.path.expanduser("~"), f"{prefix}_{int(time.time())}.pdf"
            )

        try:
            import markdown2

            html_body = markdown2.markdown(
                content,
                extras=[
                    "fenced-code-blocks",
                    "tables",
                    "break-on-newline",
                    "code-friendly",
                    "numbering",
                    "cuddled-lists",
                    "code-color",
                ],
            )

            # Get the CSS file path - same approach as in ui.py
            css_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "assets",
                "css",
                "analysis.css",
            )

            # Get the logo path
            logo_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "assets",
                "images",
                "ah_logo.png",
            )

            # Convert logo path to data URI for embedding in HTML
            with open(logo_path, "rb") as img_file:
                logo_data = base64.b64encode(img_file.read()).decode("utf-8")

            # Read the CSS file
            with open(css_path, "r", encoding="utf-8") as css_file:
                custom_css = css_file.read()

            styled_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
                <style>
                    {custom_css}

                    body {{
                        background-color: white !important;
                    }}

                    .logo-container {{
                        text-align: left;
                        margin-bottom: 20px;
                    }}

                    .logo {{
                        max-width: 180px;
                    }}

                    @page {{
                        margin: 1cm;
                    }}

                </style>
            </head>
            <body>
                <div class="logo-container">
                    <img src="data:image/png;base64,{logo_data}" class="logo" alt="AnalystHub Logo">
                </div>
                {html_body}
            </body>
            </html>
            """

            # Generate PDF
            weasyprint.HTML(string=styled_html).write_pdf(filename)
            messagebox.showinfo("Success", f"File saved to {filename}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {str(e)}")
            return False

    @staticmethod
    def save_analysis(content, file_format, file_prefix=None):
        """Save analysis content in the specified format."""
        if file_format == "txt":
            return FileHandler.save_as_txt(content, file_prefix=file_prefix)
        elif file_format == "doc":
            return FileHandler.save_as_doc(content, file_prefix=file_prefix)
        elif file_format == "pdf":
            return FileHandler.save_as_pdf(content, file_prefix=file_prefix)
        else:
            messagebox.showerror("Error", f"Unsupported file format: {file_format}")
            return False
