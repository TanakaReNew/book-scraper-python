"""
Book Scraper - CSV Export Module

Description:
This module processes scraped book data and exports it into a structured
CSV format. It cleans and formats the data to ensure consistency and
readability for analysis or external use.

Features:

* Converts raw book data into a tabular format
* Cleans fields (e.g., price formatting, availability text)
* Handles missing or inconsistent data
* Exports data to CSV files

Output:

* books.csv (complete dataset)
* filtered_books.csv (optional, based on criteria)

Dependencies:

* pandas

Usage:
Run this script after data scraping to generate CSV files:
python to_csv.py

Author:
Tanaka Tsodzo
"""
import pandas as pd
import re

df = pd.read_json("books.json")
print(df.head())

#------------------------------
# Clean price
#------------------------------
df['price'] = df['Price (incl. tax)'].str.replace(r'[^\d.]', '', regex=True).astype(float)

#------------------------------
# Clean availability
#------------------------------
df['in_stock'] = df['Availability'].str.contains('In stock')

#------------------------------
# Extract stock count
#------------------------------
df['stock_count'] = df['Availability'].str.extract(r'(\d+)').fillna(0).astype(int)

#------------------------------
# Drop unnecessary fields
#------------------------------
df = df[[
    'title',
    'UPC',
    'star_rating', 
    'price',
    'in_stock',
    'stock_count',
    'link'
    ]]
#------------------------------
# Filtering
#------------------------------
filtered = df[
    (df['star_rating']>=4)&
    (df['price']>20)&
    (df['in_stock'])
    ]

print(filtered.head())
df.to_csv('my_books.csv', index=False)
filtered.to_csv('filtered_books.csv', index=False)
