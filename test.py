import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.file_handler import FileHandler


def test_pdf_generation():
    print("Starting PDF generation test...")

    md_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "assets",
        "examples",
        "chat_response.md",
    )

    if not os.path.exists(md_file_path):
        print(f"Error: Example file not found at {md_file_path}")
        return False

    try:
        with open(md_file_path, "r", encoding="utf-8") as file:
            content = file.read()
        print(f"Successfully read markdown file: {md_file_path}")
    except Exception as e:
        print(f"Error reading markdown file: {str(e)}")
        return False

    output_file = os.path.join(os.path.expanduser("~"), "test_pdf_output.pdf")

    print(f"Generating PDF at: {output_file}")
    success = FileHandler.save_as_pdf(content, output_file)

    if success:
        print(f"PDF successfully generated at: {output_file}")
    else:
        print("PDF generation failed")

    return success


if __name__ == "__main__":
    test_result = test_pdf_generation()
    sys.exit(0 if test_result else 1)
