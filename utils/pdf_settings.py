import os
from fpdf import FPDF


class PDFSettings(FPDF):
    first_page = True

    def header(self):
        if self.first_page:
            logo_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "assets",
                "images",
                "ah_logo.png",
            )
            if os.path.exists(logo_path):
                self.image(logo_path, 10, 8, 50)
            self.ln(20)
            self.first_page = False

    def footer(self):
        pass

    @staticmethod
    def setup_pdf():
        pdf = PDFSettings()
        fonts_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets",
            "fonts",
        )
        pdf.add_font(
            "Poppins", "", os.path.join(fonts_dir, "Poppins-Regular.ttf"), uni=True
        )
        pdf.add_font(
            "Poppins", "B", os.path.join(fonts_dir, "Poppins-Bold.ttf"), uni=True
        )
        pdf.add_font(
            "Poppins", "I", os.path.join(fonts_dir, "Poppins-Italic.ttf"), uni=True
        )
        pdf.set_font("Poppins", size=12)
        pdf.add_page()
        return pdf

    @staticmethod
    def get_styling_config():
        return {
            "line_height": 6,
            "paragraph_spacing": 4,
            "colors": {
                "heading1": (202, 90, 139),
                "heading2": (102, 84, 245),
                "heading3": (102, 84, 245),
                "default_text": (11, 12, 24),
                "table_header_bg": (242, 179, 71),
                "table_header_text": (255, 255, 255),
                "table_row_bg": (245, 245, 245),
                "code_block_bg": (235, 235, 235),
            },
            "fonts": {
                "heading1": {"name": "Poppins", "style": "B", "size": 28},
                "heading2": {"name": "Poppins", "style": "B", "size": 22},
                "heading3": {"name": "Poppins", "style": "B", "size": 18},
                "normal": {"name": "Poppins", "style": "", "size": 12},
                "bold": {"name": "Poppins", "style": "B", "size": 12},
                "code": {"name": "Courier", "style": "", "size": 10},
                "table_header": {"name": "Poppins", "style": "B", "size": 11},
                "table_cell": {"name": "Poppins", "style": "", "size": 11},
            },
            "spacing": {
                "before_h1": 10,
                "after_h1": 16,
                "before_h2": 8,
                "after_h2": 12,
                "before_h3": 6,
                "after_h3": 10,
            },
            "list_indent": 10,
            "bullet_spacing": 3,
        }

    @staticmethod
    def process_markdown(content):
        import re
        import markdown2

        content = re.sub(r"\n{3,}", "\n\n", content)
        html_content = markdown2.markdown(
            content,
            extras=[
                "fenced-code-blocks",
                "tables",
                "code-friendly",
                "numbering",
                "cuddled-lists",
            ],
        )
        return html_content

    @staticmethod
    def render_section(pdf, section, style):
        import re

        if not section.strip():
            return

        if section.startswith("<h1"):
            text = re.sub(r"<h1.*?>(.*?)</h1>", r"\1", section)
            pdf.ln(style["spacing"]["before_h1"])
            pdf.set_text_color(*style["colors"]["heading1"])
            font_config = style["fonts"]["heading1"]
            pdf.set_font(font_config["name"], font_config["style"], font_config["size"])
            pdf.write(10, text)
            pdf.ln(style["spacing"]["after_h1"])
            pdf.set_text_color(*style["colors"]["default_text"])

        elif section.startswith("<h2"):
            text = re.sub(r"<h2.*?>(.*?)</h2>", r"\1", section)
            pdf.ln(style["spacing"]["before_h2"])
            pdf.set_text_color(*style["colors"]["heading2"])
            font_config = style["fonts"]["heading2"]
            pdf.set_font(font_config["name"], font_config["style"], font_config["size"])
            pdf.write(10, text)
            pdf.ln(style["spacing"]["after_h2"])
            pdf.set_text_color(*style["colors"]["default_text"])

        elif section.startswith("<h3"):
            text = re.sub(r"<h3.*?>(.*?)</h3>", r"\1", section)
            pdf.ln(style["spacing"]["before_h3"])
            pdf.set_text_color(*style["colors"]["heading3"])
            font_config = style["fonts"]["heading3"]
            pdf.set_font(font_config["name"], font_config["style"], font_config["size"])
            pdf.write(10, text)
            pdf.ln(style["spacing"]["after_h3"])
            pdf.set_text_color(*style["colors"]["default_text"])

        elif section.startswith("<pre><code>"):
            code = section.replace("<pre><code>", "").replace("</code></pre>", "")
            pdf.set_fill_color(*style["colors"]["code_block_bg"])
            font_config = style["fonts"]["code"]
            pdf.set_font(font_config["name"], font_config["style"], font_config["size"])
            for line in code.split("\n"):
                pdf.set_x(15)
                pdf.cell(0, 5, line, 0, 1, fill=True)
            font_config = style["fonts"]["normal"]
            pdf.set_font(font_config["name"], font_config["style"], font_config["size"])
            pdf.ln(style["paragraph_spacing"])

        elif section.startswith("<ul>") or section.startswith("<ol>"):
            PDFSettings.render_list(pdf, section, style)

        elif section.startswith("<p>"):
            text = re.sub(r"<p>(.*?)</p>", r"\1", section)
            text = re.sub(r"<[^>]+>", "", text)
            if text.strip():
                normal_font = style["fonts"]["normal"]
                bold_font = style["fonts"]["bold"]
                pdf.set_font(
                    normal_font["name"], normal_font["style"], normal_font["size"]
                )
                parts = re.split(r"(\*\*.*?\*\*)", text)
                for i, part in enumerate(parts):
                    if i % 2 == 1:
                        pdf.set_font(
                            bold_font["name"], bold_font["style"], bold_font["size"]
                        )
                        pdf.write(style["line_height"], part.replace("**", ""))
                        pdf.set_font(
                            normal_font["name"],
                            normal_font["style"],
                            normal_font["size"],
                        )
                    else:
                        pdf.write(style["line_height"], part)
                pdf.ln(style["paragraph_spacing"])

        elif section.startswith("<table>"):
            rows = re.findall(r"<tr>(.*?)</tr>", section, re.DOTALL)
            is_header = True
            for row in rows:
                cells = re.findall(r"<t[hd]>(.*?)</t[hd]>", row)
                cell_width = 190 / max(len(cells), 1)
                if is_header:
                    pdf.set_fill_color(*style["colors"]["table_header_bg"])
                    pdf.set_text_color(*style["colors"]["table_header_text"])
                    header_font = style["fonts"]["table_header"]
                    pdf.set_font(
                        header_font["name"], header_font["style"], header_font["size"]
                    )
                else:
                    pdf.set_fill_color(*style["colors"]["table_row_bg"])
                    pdf.set_text_color(*style["colors"]["default_text"])
                    cell_font = style["fonts"]["table_cell"]
                    pdf.set_font(
                        cell_font["name"], cell_font["style"], cell_font["size"]
                    )
                for cell in cells:
                    text = re.sub(r"<[^>]+>", "", cell)
                    pdf.cell(cell_width, 8, text, 1, 0, fill=True)
                pdf.ln()
                is_header = False
            pdf.ln(style["paragraph_spacing"])
            pdf.set_text_color(*style["colors"]["default_text"])

        else:
            text = re.sub(r"<[^>]+>", "", section)
            if text.strip():
                normal_font = style["fonts"]["normal"]
                pdf.set_font(
                    normal_font["name"], normal_font["style"], normal_font["size"]
                )
                pdf.write(style["line_height"], text)
                pdf.ln(style["paragraph_spacing"])

    @staticmethod
    def render_list(pdf, section, style):
        import re

        list_type = "ul" if section.startswith("<ul>") else "ol"
        items = re.findall(r"<li>(.*?)</li>", section, re.DOTALL)

        normal_font = style["fonts"]["normal"]
        bold_font = style["fonts"]["bold"]
        indent = style["list_indent"]

        for i, item_text in enumerate(items):
            pdf.set_x(pdf.get_x() + indent)
            item_text = re.sub(r"<[^>]+>", "", item_text).strip()

            # Create bullet point or number
            if list_type == "ul":
                bullet = "•"
                pdf.set_font(
                    normal_font["name"], normal_font["style"], normal_font["size"]
                )
                pdf.write(style["line_height"], f"{bullet} ")
            else:
                number = f"{i + 1}."
                pdf.set_font(
                    normal_font["name"], normal_font["style"], normal_font["size"]
                )
                pdf.write(style["line_height"], f"{number} ")

            # Handle text with potential bold sections
            parts = re.split(r"(\*\*.*?\*\*)", item_text)
            for j, part in enumerate(parts):
                if j % 2 == 1:  # Bold text
                    pdf.set_font(
                        bold_font["name"], bold_font["style"], bold_font["size"]
                    )
                    pdf.write(style["line_height"], part.replace("**", ""))
                    pdf.set_font(
                        normal_font["name"], normal_font["style"], normal_font["size"]
                    )
                else:  # Regular text
                    pdf.write(style["line_height"], part)

            pdf.ln(style["bullet_spacing"] + 3)
            pdf.set_x(pdf.get_x() - indent)  # Reset x position

        pdf.ln(style["paragraph_spacing"])
