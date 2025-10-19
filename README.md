# eCourts Cause List Scraper

## Overview

The eCourts Cause List Scraper automates the extraction of daily district court cause list data from the official [eCourts portal](https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/index).
It allows users to manually select filters (State, District, Court, Date) and fill the captcha, then automatically parses and exports the cause list as a PDF file.

## Features

- Opens eCourts portal automatically in a browser
- Lets users manually select filters and fill captcha
- Extracts structured cause list data (Sr No, Case Info, Party, Advocate)
- Generates a clean, formatted PDF of the results

## Prerequisites
Python Version

- Python 3.8+

Install Required Libraries
```
pip install selenium webdriver-manager reportlab
```
## Setup Instructions

1. Clone or download this script into your working directory.

2. Ensure Google Chrome is installed.

3. Run the script with:
```
python eCourts_Scraper.py
```
## How to Use

1. When the browser opens, manually select:
   - State

   - District

   - Court Complex

   - Date

   - Fill in the captcha

2. Click either:

   - Civil — for Civil Cause List, or

   - Criminal — for Criminal Cause List

3. Wait for the table to fully load.

4. Return to the terminal and press Enter.

The script scrapes the table and generates:
```
Cause_List.pdf
```
