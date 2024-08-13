# Web-Scraper-MyNeta

## Overview

This project involves scraping data from [MyNeta.info](https://myneta.info/LokSabha2024/). Myneta.info is an open data repository platform of Association for Democratic Reforms (ADR). The data is extracted from multiple pages and saved into CSV files, organized by state and constituency.

## Requirements

To run this project, you need to have Python installed. The following packages are required:

- `beautifulsoup4`: For parsing HTML content.
- `pandas`: For handling data and saving it to CSV files.
- `selenium`: For web automation.
- `webdriver-manager`: For managing ChromeDriver binaries.

You can install these dependencies by running:

```sh
pip install -r requirements.txt
```
Files description:

- `new_scrape.py`: main file for scraping data of all constituencies of states.
- `const.py`: to create `constituencies.csv` of all states with their State_ID and respective links
