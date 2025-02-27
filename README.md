# AnalystHub 2.0 - BIM Model Insight

AnalystHub 2.0 is a desktop application designed to provide comprehensive analysis of Power BI BIM model files. The application uses AI to extract insights from your BIM files and presents them in an interactive, user-friendly interface with multiple analysis tabs.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Customization](#customization)
- [License](#license)

---

## Overview

This application provides:

- **Drag and Drop File Support:** Easily upload BIM files by dragging and dropping them onto the interface.
- **Comprehensive Analysis:** Multiple analysis tabs covering general overview, model structure, DAX measures, data dictionary, performance optimization, missing data analysis, report ideas, and analysis ideas.
- **Interactive Display:** Analysis results are presented in a nicely formatted HTML view with tabbed navigation.
- **Download Options:** Download individual analysis tabs or all analyses combined in multiple formats (PDF, Text, Word Document).
- **Reset and Reload:** Options to start over the analysis after reviewing results.

---

## Features

- **User Interface:** Built using customTkinter, the interface includes a header, upload section, and tabbed panels for different types of analysis.
- **File Handling:** Uses dedicated file handler methods to validate file types and read file contents.
- **AI-Driven Analysis:** Integrates with OpenAI's GPT models to interpret and provide insights from the uploaded BIM file.
- **Download Functionality:** 
  - Download individual tab content in PDF, Text, or Word Document format
  - Download all tabs combined into a single file with the same format options
  - Consistent styling across all download formats
- **Visual Enhancements:** Uses a modern UI with consistent branding and styling.
- **Responsive Design:** Dynamically shows and hides analysis panels when required.

---

## Project Structure

Below is an overview of major components in the project:

- **GUI Module (`ui.py`):** Contains the primary GUI class that sets up the interface, registers drag & drop functionality, displays analysis results in tabs, and provides download options.
- **File Handler Module (`file_handler.py`):** Contains methods for handling file uploads, validations, reading file contents, and exporting analysis in different formats.
- **AI Analyzer Module (`ai_analyzer.py`):** Contains logic to perform AI-powered analysis on the given BIM file content.
- **Controller Module (`controller.py`):** Manages the interaction between different components and defines the analysis tasks.
- **Assets:** Includes external images (e.g., logo) and CSS files for styling the HTML output.

---

## Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/your_username/analysthub-2.0.git
cd analysthub-2.0
```

2. **Install Dependencies:**

Ensure you have Python 3 installed, then install required packages using pip:

```bash
pip install -r requirements.txt
```

3. **Run the Application:**

You can start the application using:

```bash
python -m app.main
```

---

## Usage

1. **Launch the App:** Run the main Python script to open the GUI.
2. **Upload a File:** Use the drag and drop functionality or click the "Upload BIM File" button to select your Power BI BIM file.
3. **View Analysis:** After uploading, the app will analyze the file and display the results in multiple tabs:
   - General Analysis
   - Model Analysis
   - DAX Analysis
   - Data Documentation & Dictionary
   - Performance Analysis
   - Missing Data Analysis
   - Report Ideas
   - Analysis Ideas
4. **Download Options:**
   - Use the "Download" button to save the current tab's content in your preferred format (PDF, Text, Word Document)
   - Use the "Download All" button to combine all tabs into a single file in your preferred format
5. **Reset:** Use the "Start Over" button to clear the current analysis and return to the upload screen.

---

## Dependencies

- **Python 3.x**
- **customtkinter**: For enhanced Tkinter UI components
- **tkinterdnd2**: For drag and drop file support
- **tkinterweb**: For rendering HTML content within the GUI
- **Pillow**: For image processing
- **markdown**: For converting analysis results into HTML
- **python-docx**: For exporting to Word Document format
- **weasyprint**: For exporting to PDF format
- **openai**: For AI-powered analysis

---

## Customization

- **Colors:** Update the `COLORS` dictionary in `ui.py` to change the UI color scheme.
- **Fonts:** Modify the font settings to adjust text appearance.
- **Assets:** Replace or update images within the assets folder to customize branding.
- **CSS:** The HTML analysis view and PDF exports use styles from an external CSS file; modify this file to alter the appearance of the analysis results.
- **Analysis Tasks:** Modify the analysis tasks in `controller.py` to customize the types of analysis performed.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

For further contributions or questions, please feel free to open an issue or contact the maintainers. Enjoy using AnalystHub 2.0 for your Power BI BIM model analysis!
