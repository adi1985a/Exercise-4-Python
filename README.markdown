# 📈💹 FlaskFX Visualizer: Currency Exchange Rate Charting 🌐
_A Flask web application that displays historical EUR and USD buy/sell exchange rates from a CSV file, featuring date range filtering and a JSON API for chart data, powered by Pandas._

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg?logo=pandas)](https://pandas.pydata.org/)
<!-- Add badges for HTML/CSS/JS and Charting Library if known -->
<!-- [![Chart.js](https://img.shields.io/badge/Charts-Chart.js-FF6384.svg?logo=chart.js)]() -->

## 📋 Table of Contents
1.  [Overview](#-overview)
2.  [Key Features](#-key-features)
3.  [Screenshots (Conceptual)](#-screenshots-conceptual)
4.  [System Requirements & Dependencies](#-system-requirements--dependencies)
5.  [Data Requirements (`history.csv`)](#-data-requirements-historycsv)
6.  [Installation and Setup](#️-installation-and-setup)
7.  [Usage Guide](#️-usage-guide)
8.  [Project File Structure (Expected)](#-project-file-structure-expected)
9.  [Technical Notes & Considerations](#-technical-notes--considerations)
10. [Contributing](#-contributing)
11. [License](#-license)
12. [Contact](#-contact)

## 📄 Overview

**FlaskFX Visualizer** is a web application built with the **Flask** Python microframework, designed for visualizing historical currency exchange rates. Developed by Adrian Lesniak, it reads EUR and USD buy/sell rate data from a local CSV file (`history.csv`). Users can interact with a simple web interface to select a specific date range to filter the data. The application then processes this data using the **Pandas** library and serves the filtered, formatted data as a JSON response via an API endpoint. This JSON data is intended to be consumed by a frontend charting library (e.g., Chart.js, Plotly.js, D3.js, assumed to be implemented in `templates/index.html`) to render interactive charts of the exchange rates over the selected period.

<br> 
<p align="center">
  <img src="screenshots/1.gif" width="90%">
</p>
<br>

## ✨ Key Features

*   📊 **Historical Data Visualization**:
    *   Displays charts (implementation assumed in frontend) for EUR and USD buy/sell rates.
*   📅 **Date Range Filtering**:
    *   Provides a web form on the homepage (`index.html`) allowing users to select a custom start and end date to filter the historical exchange rate data.
*   ⚙️ **Data Processing with Pandas**:
    *   Utilizes the Pandas library to efficiently load, filter (by date range), and format the exchange rate data from `history.csv`.
*   <0xF0><0x9F><0xA7><0xAE> **JSON API for Chart Data**:
    *   An endpoint (e.g., `/charts`) processes POST requests containing the selected date range.
    *   Returns the filtered and processed exchange rate data in JSON format, ready for consumption by a frontend charting library.
*   🖥️ **Simple Web Interface**:
    *   Serves a basic HTML page (`templates/index.html`) which includes the date range selection form and the area where charts will be rendered.
*   ✔️ **Input Validation (Basic)**:
    *   The Flask backend likely includes checks for the presence of date range inputs.

## 🖼️ Screenshots (Conceptual)

_Screenshots of: the homepage with the date range selection form, and an example of the interactive charts displaying EUR/USD buy/sell rates after data is filtered and rendered by a frontend charting library._

<p align="center">
  <img src="screenshots\1.jpg" width="300"/>
  <img src="screenshots\2.jpg" width="300"/>
  <img src="screenshots\3.jpg" width="300"/>
  <img src="screenshots\4.jpg" width="300"/>
  <img src="screenshots\5.jpg" width="300"/>
</p>

## ⚙️ System Requirements & Dependencies

### Software:
*   **Python**: Version 3.6 or higher.
*   **Libraries**:
    *   `Flask`: The core web framework.
    *   `pandas`: For loading, manipulating, and processing the CSV data.
    *   (Frontend charting library like Chart.js, Plotly.js, or D3.js would be included in `templates/index.html` via CDN or local files - not a Python dependency).

### Installation:
*   Dependencies are installed using `pip`.

### Data File:
*   `history.csv`: A CSV file located in the project's root directory.

## 💾 Data Requirements (`history.csv`)

The application expects a CSV file named `history.csv` in the project root with the following structure and data types:

*   **Columns**:
    *   `date_time`: The date and time of the rate recording. Must be in a format that Pandas can parse into datetime objects (e.g., `YYYY-MM-DD HH:MM:SS`, `YYYY-MM-DD`).
    *   `EURbuy`: Numeric value representing the Euro buy rate.
    *   `EURsell`: Numeric value representing the Euro sell rate.
    *   `USDbuy`: Numeric value representing the US Dollar buy rate.
    *   `USDsell`: Numeric value representing the US Dollar sell rate.
*   **Example Row**:
    `2023-10-26 10:00:00,4.4560,4.4780,4.1230,4.1450`

*The correct formatting and presence of these columns in `history.csv` are crucial for the application to function.*

## 🛠️ Installation and Setup

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
    *(Replace `<repository-url>` and `<repository-directory>` with your specific details).*

2.  **Set Up a Virtual Environment (Recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Required Libraries**:
    ```bash
    pip install Flask pandas
    # If a requirements.txt file is provided:
    # pip install -r requirements.txt
    ```

4.  **Prepare `history.csv`**:
    *   Ensure the `history.csv` file (with the correct columns and data format as described above) is placed in the root directory of the project.

5.  **Prepare `templates/index.html` (Frontend)**:
    *   Create a `templates` subfolder in your project root.
    *   Inside `templates`, create `index.html`. This file will contain:
        *   An HTML form for submitting the start and end dates (likely to POST to the `/charts` endpoint).
        *   A canvas element or div where the charts will be rendered.
        *   JavaScript code (or a linked JS file) to:
            *   Handle form submission (e.g., using `fetch` API or jQuery AJAX).
            *   Receive the JSON data from the `/charts` API endpoint.
            *   Use a charting library (e.g., Chart.js) to render the charts with the received data.
    *   *(The specific implementation of `index.html` is assumed and not provided in the backend overview).*

6.  **Run the Flask Application**:
    Open a terminal in the project's root directory and execute:
    ```bash
    python app.py
    ```
    *   The application will typically start a development server (often on `http://localhost:5000`).
    *   The terminal will indicate the address where the application is running.

## 💡 Usage Guide

1.  Launch the Flask application by running `python app.py`.
2.  Open your web browser and navigate to `http://localhost:5000` (or the address shown in your terminal).
3.  **Interface (`index.html`)**:
    *   You will see a web page with a form for selecting a **start date** and an **end date**.
    *   There will be a submit button to fetch and display the data.
    *   An area on the page will be designated for displaying the generated charts.
4.  **Actions**:
    *   Select a desired start date and end date using the form's date pickers or input fields.
    *   Click the "Submit" (or similarly labeled) button.
    *   This action will send a POST request (likely via JavaScript `fetch` or AJAX) to the `/charts` endpoint in `app.py`.
    *   The Flask backend (`app.py`) will process the `history.csv` data, filter it by the selected date range, and return a JSON response.
    *   The JavaScript in `index.html` will receive this JSON data and use a charting library (e.g., Chart.js) to render interactive charts displaying the EUR and USD buy/sell rates for the specified period.

## 🗂️ Project File Structure (Expected)

*   `app.py`: The main Flask Python script. Contains route definitions (e.g., for `/` to serve `index.html`, and `/charts` for the API), data processing logic using Pandas, and JSON response generation.
*   `templates/` (directory):
    *   `index.html`: (User-provided/Assumed) The HTML template for the homepage, containing the date range selection form and the canvas/div for chart rendering. It will also include JavaScript for API calls and chart generation.
*   `history.csv`: The CSV file containing the historical exchange rate data, located in the project root.
*   `README.md`: This documentation file.
*   (Potentially a `static/` directory for local CSS or JS files if not using CDNs exclusively for the frontend).

## 📝 Technical Notes & Considerations

*   **`history.csv` Format**: Strict adherence to the CSV format (column names, date parseability, numeric rates) is vital. Errors in this file will likely cause Pandas processing to fail.
*   **Frontend Implementation (`index.html`)**: The entire visualization aspect (chart rendering) is dependent on the JavaScript and charting library (e.g., Chart.js, Plotly.js, D3.js) implemented within `templates/index.html`. This frontend code is not part of `app.py` itself but consumes its API.
*   **Debug Mode**: The Flask application runs in `debug=True` mode by default during development. **This must be set to `debug=False` in a production environment** for security and performance.
*   **Error Handling**: The Flask app should include error handling for scenarios like `history.csv` not being found, incorrect date formats from the user, or empty data for the selected range.
*   **Date Parsing**: Pandas `to_datetime()` is likely used for parsing the `date_time` column. The format of dates in the CSV must be consistent and parsable by Pandas.
*   **Large Datasets**: If `history.csv` becomes very large, loading and processing the entire file on each request might become inefficient. Consider database storage or more optimized data querying techniques for larger scale applications.

## 🤝 Contributing

Contributions to **FlaskFX Visualizer** are highly encouraged! If you have ideas for:

*   Integrating different charting libraries or enhancing chart interactivity.
*   Adding support for more currencies or different data sources.
*   Improving the date range selection UI.
*   Implementing more robust error handling and user feedback.
*   Adding backend data storage (e.g., SQLite, PostgreSQL) instead of CSV.
*   Developing more API endpoints for different types of data analysis.

1.  Fork the repository.
2.  Create a new branch for your feature (`git checkout -b feature/NewCurrencySupport`).
3.  Make your changes to `app.py`, `templates/index.html`, and any other relevant files.
4.  Commit your changes (`git commit -m 'Feature: Add support for GBP exchange rates'`).
5.  Push to the branch (`git push origin feature/NewCurrencySupport`).
6.  Open a Pull Request.

Please ensure your code is well-commented and follows Python (PEP 8) and Flask best practices.

## 📃 License

This project is licensed under the **MIT License**.
(If you have a `LICENSE` file in your repository, refer to it: `See the LICENSE file for details.`)

## 📧 Contact

Project concept by **Adrian Lesniak**.
For questions, feedback, or issues, please open an issue on the GitHub repository or contact the repository owner.

---
💹 _Visualizing currency trends with the power of Flask and Pandas!_
