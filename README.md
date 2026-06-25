# Book Scraper Project

## Overview

This project scrapes book data from https://books.toscrape.com using Selenium and Requests, then processes and analyzes the data using Pandas.

---

## Features

* Scrapes all pages (pagination handled)
* Extracts:

  * Title
  * Star rating
  * Price
  * Availability
  * Product details
* Cleans and processes data using Pandas
* Outputs:

  * JSON (raw data)
  * CSV (cleaned + filtered data)

---

## Tech Stack

* Python
* Selenium
* BeautifulSoup
* Requests
* Pandas

---

## Project Structure

```
book-scraper/
│
├── main.py        # Scraper (raw data collection)
├── to_csv.py     # Data cleaning + analysis
├── data/
│   ├── books.json
│   ├── books.csv
│   └── filtered_books.csv
```

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run scraper

```bash
python main.py
```

### 3. Run analysis file

```bash
python to_csv.py
```

---

## Notes

* Scraper uses Selenium for navigation and Requests for product pages.
* Data cleaning is handled separately using Pandas for flexibility.
