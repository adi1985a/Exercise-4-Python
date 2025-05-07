# Currency Exchange Rate Visualizer

## Overview
Currency Exchange Rate Visualizer is a Flask web application that displays historical EUR and USD buy/sell rates from a CSV file. Users can select a date range to filter data, and the app generates charts using processed data returned as JSON. Built with Flask and Pandas.

## Features
- **Data Visualization**: Displays EUR and USD buy/sell rates in interactive charts.
- **Date Range Filtering**: Allows users to select custom date ranges for data analysis.
- **Data Processing**: Uses Pandas to filter and format data from a CSV file.
- **JSON API**: Returns chart data in JSON format for frontend rendering.
- **Simple Interface**: Serves a webpage with a form for date range selection.

## Requirements
- Python 3.6+
- Libraries:
  - `Flask`
  - `pandas`
- Data file: `history.csv` with columns `date_time`, `EURbuy`, `EURsell`, `USDbuy`, `USDsell`.

Install dependencies using:
```bash
pip install Flask pandas
```

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install the required libraries (see Requirements).
3. Place `history.csv` in the project directory with the required columns.
4. Run the application:
   ```bash
   python app.py
   ```

## Usage
1. Launch the app and navigate to `http://localhost:5000` in a browser.
2. **Interface**:
   - Use the form on the homepage (`index.html`) to select a start and end date.
   - Submit the form to fetch filtered data.
   - View charts displaying EUR and USD buy/sell rates for the selected period.
3. The `/charts` endpoint processes POST requests and returns JSON data for chart rendering.

## File Structure
- `app.py`: Main Flask application script handling routes and data processing.
- `templates/index.html`: (Assumed) HTML template for the homepage with date range form and chart display.
- `history.csv`: CSV file containing historical exchange rate data.
- `README.md`: This file, providing project documentation.

## Notes
- Ensure `history.csv` is formatted correctly with `date_time` in a parseable datetime format and numeric columns for rates.
- The `index.html` template is not provided but assumed to include a form for date range input and JavaScript for chart rendering (e.g., using Chart.js).
- The app runs in debug mode by default; disable it in production (`debug=False`).

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make changes and commit (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or feedback, open an issue on GitHub or contact the repository owner.