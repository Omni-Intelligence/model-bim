# AnalystHub 2.0

AnalystHub 2.0 is a desktop-based Power BI Analysis Toolkit that uses a custom Tkinter interface to help you upload and analyze Power BI files. The application reads Power BI files, extracts content and data models, and displays analysis results within an interactive GUI.

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

- **Drag and Drop File Support:** Easily upload Power BI files by dragging and dropping them onto the interface.
- **File Analysis:** Separate analysis for report content and data model extraction.
- **Interactive Display:** Analysis results are presented in a nicely formatted HTML view.
- **Gradient Header:** Custom gradient header and branding using custom images.
- **Reset and Reload:** Options to start over the analysis after reviewing results.

---

## Features

- **User Interface:** Built using customTkinter, the interface includes a header, upload section, and separate panels for analysis results.
- **File Handling:** Uses dedicated file handler methods to validate file types and read file contents.
- **AI-Driven Analysis:** Integrates with AI analysis modules to interpret and provide insights from the uploaded Power BI file.
- **Visual Enhancements:** Uses a custom gradient and a modern font for a sleek look.
- **Responsive Design:** Dynamically shows and hides analysis panels when required.

---

## Project Structure

Below is an overview of major components in the project:

- **GUI Module:** Contains the primary GUI class that sets up the interface, registers drag & drop functionality, displays analysis results, and provides file reset options.
- **file_handler Module:** Contains methods for handling file uploads, validations, and reading file contents.
- **ai_analyzer Module:** Contains logic to perform analysis on the given Power BI file content and data models.
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
   pip install customtkinter tkinterdnd2 tkinterweb Pillow markdown
```

3. **Run the Application:**

You can start the application using:

```bash
  python main.py
```

---

## Usage

1. **Launch the App:** Run the main Python script to open the GUI.
2. **Upload a File:** Use the drag and drop functionality or click the \"Upload Power BI File\" button to select your Power BI file.
3. **View Analysis:** After uploading, the app will analyze the file and display the results in an HTML formatted panel.
4. **Model Analysis:** If the file includes a data model, an additional panel is displayed with further analysis.
5. **Reset:** Use the \"Start Over\" button to clear the current analysis and return to the upload screen.

--

## Dependencies

- **Python 3.x**
- **customtkinter**: For enhanced Tkinter UI components.
- **tkinterdnd2**: For drag and drop file support.
- **tkinterweb**: For rendering HTML content within the GUI.
- **Pillow**: For image processing.
- **markdown**: For converting analysis results into HTML.

---

## Customization

- **Colors:** Update the `COLORS` dictionary to change the UI color scheme.
- **Fonts:** Modify the font settings (using Poppins font) to adjust text appearance.
- **Assets:** Replace or update images within the assets folder to customize branding.
- **CSS:** The HTML analysis view pulls styles from an external CSS file located in the assets folder; modify this file to alter the appearance of the analysis results.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

For further contributions or questions, please feel free to open an issue or contact the maintainers. Enjoy using AnalystHub 2.0 for your Power BI analysis!
