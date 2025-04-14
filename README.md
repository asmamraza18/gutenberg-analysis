# Gutenberg Text Analyzer

This Python application retrieves text data directly from Project Gutenberg, analyzes the frequency of proper nouns in books, and generates detailed reports. It is designed to process multiple books and is equipped with robust features like performance tracking and report generation.

## Features

1. **Data Retrieval**:
   - Fetches text data directly from Project Gutenberg URLs.
   - Handles multiple book formats and includes error handling for invalid URLs.

2. **Proper Noun Extraction**:
   - Uses the NLTK library for named entity recognition (NER) to identify proper nouns.
   - Supports extraction of individuals, organizations, places, and other entities.

3. **Frequency Analysis**:
   - Calculates the frequency of each proper noun in individual books.
   - Aggregates proper noun frequencies across all analyzed books.

4. **Performance Tracking**:
   - Tracks the total runtime of the program.
   - Calculates average processing time per book.
   - Includes success and failure rates with detailed error messages.

5. **Report Generation**:
   - Creates individual JSON reports for each book.
   - Generates a combined JSON report with overall statistics and performance metrics.

## Directory Structure

```
project-directory/
├── gutenberg_analyzer.py       # Main analyzer class
├── main.py                     # Entry point of the program
├── requirements.txt            # Dependencies
├── reports/                    # Generated reports (JSON files)
├── gutenberg_analysis.log      # Log file with program execution details
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/gutenberg-analyzer.git
   cd gutenberg-analyzer
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Adding Books to Analyze
Edit the `BOOKS_TO_ANALYZE` list in the `main.py` file. Add the URLs and titles of the books you want to process. Example:
```python
BOOKS_TO_ANALYZE = [
    {
        'url': 'https://www.gutenberg.org/files/1342/1342-0.txt',
        'title': 'Pride and Prejudice'
    },
    {
        'url': 'https://www.gutenberg.org/files/84/84-0.txt',
        'title': 'Frankenstein'
    }
]
```

### 2. Running the Program
Run the program using:
```bash
python main.py
```

### 3. Outputs
- **Reports**: JSON reports are generated in the `reports/` directory. Individual reports are created for each book, along with a combined report (`combined_report.json`) containing aggregated statistics.
- **Log File**: Execution details, including errors, are logged in `gutenberg_analysis.log`.

## Example Output Files

### Individual Book Report (`reports/Pride_and_Prejudice_report.json`)
```json
{
  "title": "Pride and Prejudice",
  "url": "https://www.gutenberg.org/files/1342/1342-0.txt",
  "statistics": {
    "total_proper_nouns": 2500,
    "unique_proper_nouns": 900
  },
  "frequencies": {
    "Elizabeth": 120,
    "Darcy": 95,
    "Bingley": 85,
    "Jane": 80,
    ...
  }
}
```

### Combined Report (`reports/combined_report.json`)
```json
{
  "total_books_analyzed": 2,
  "total_frequencies": {
    "Elizabeth": 120,
    "Darcy": 95,
    "Frankenstein": 50,
    ...
  },
  "books_analyzed": [
    "Pride and Prejudice",
    "Frankenstein"
  ],
  "performance_metrics": {
    "timestamp": "2025-04-10 05:03:06",
    "total_runtime_seconds": 45.2,
    "total_books_attempted": 2,
    "successful_books": 2,
    "success_rate": "100.00%",
    "average_time_per_book": 22.6,
    "performance_metrics": {
      "fastest_book": 20.1,
      "slowest_book": 25.3
    }
  }
}
```

## Troubleshooting

1. **NumPy Errors**:
   If you encounter issues with NumPy compatibility:
   - Ensure you're using `numpy==1.24.3` as specified in `requirements.txt`.

2. **Missing Dependencies**:
   - Run `pip install -r requirements.txt` to ensure all dependencies are installed.

3. **Invalid URLs**:
   - Verify that the URLs in `BOOKS_TO_ANALYZE` point to valid Project Gutenberg text files.

4. **Performance Issues**:
   - For large books, processing may take longer due to intensive text analysis. Reduce the number of books if necessary.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue if you encounter any problems or have suggestions for enhancements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
