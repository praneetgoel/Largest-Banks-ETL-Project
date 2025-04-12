# 🌍 Largest Banks ETL Project

This project automates the extraction, transformation, and loading (ETL) of market capitalization data for the largest banks in the world. The goal is to create a repeatable ETL pipeline that processes data from Wikipedia, converts the market cap values to multiple currencies, and stores the results in both CSV and SQLite formats for further analysis.

---

## 📖 Project Scenario

A global financial firm requires up-to-date data on the largest banks for strategic decision-making. You, as a junior data engineer, are tasked with:

- Extracting market capitalization data (in USD) for the top global banks from a reliable source (Wikipedia).
- Converting this data to other currencies (GBP, EUR, INR) using exchange rates.
- Storing the cleaned data in multiple formats (CSV, SQLite DB).
- Querying the database for key insights, such as the average market capitalization in GBP and the top 5 banks by name.
- Logging the entire ETL process for transparency and debugging purposes.

---

## ⚙️ Tech Stack

- Python 3
- pandas
- BeautifulSoup (bs4)
- SQLite (`sqlite3`)
- NumPy
- Requests
- datetime

---

## 📂 Project Files

- **banks_project.py**: Main script that performs the ETL process.
- **exchange_rate.csv**: CSV file containing exchange rates for GBP, EUR, INR.
- **Largest_banks_data.csv**: Final output CSV file with market capitalization data in USD, GBP, EUR, and INR.
- **Banks.db**: SQLite database containing the processed data in a table called `Largest_banks`.
- **code_log.txt**: Log file tracking the ETL process with timestamps.

---

## 🔄 ETL Pipeline

### ✅ Extract
Scrapes market capitalization data for the largest banks from this archived Wikipedia page:
[Archived Link](https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks)

### 🔧 Transform
- Converts market capitalization values from string to float.
- Transforms the market cap values from USD to GBP, EUR, and INR using exchange rates.
- Rounds the transformed values to two decimal places for better readability.

### 💾 Load
- Saves the cleaned data to:
  - `Largest_banks_data.csv` (CSV file with market cap in USD, GBP, EUR, INR)
  - SQLite table `Largest_banks` in `Banks.db`.

### 🔍 Query
Queries the database for:
- Average market capitalization in GBP.
- Names of the top 5 largest banks.

Example SQL queries:
- `SELECT * FROM Largest_banks`
- `SELECT AVG(MC_GBP_Billion) FROM Largest_banks`
- `SELECT Name FROM Largest_banks LIMIT 5`

### 🧾 Logging
Every step of the ETL process is logged with timestamps in the `code_log.txt` file for transparency and debugging purposes.

---

## 🚀 How to Run

```bash
# Install dependencies
pip install requests pandas numpy beautifulsoup4

# Run the script
python banks_project.py
