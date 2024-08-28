# Web Scraper Pro

Written in python and utilizing Tkinter for the GUI. 
Web Scraper Pro is a feature rich tool that offers BeautifulSoup and Selenium as the scraping methods.
 
BeautifulSoup is suitable for users who only need to scrape static HTML content from websites.

Selenium is the better choice for Scraping Dynamically Loaded Content from websites that load content using JavaScript. 

# Prerequisites

Web Scraper Pro should run on most Windows machines with very few dependencies. 

## Easy Installation

* Download the Web Scraper Pro code and execute on your favorite IDE.

* Paste or type in the URL.
* Select the Scraping Method.
* Select the Output Format.
* Optional - choose nested tags - OR
* Find Elements AND enetering an expression manually.
* Click on the "Scrape Data" button to start the Web Scraper Pro process.
* Web Scraper Pro will perform scraping based on the criteria you select.
* An Explorer Window will open, select a directory and name your file to save.
* A prompt will indicate 'Data Saved Successfully.'

## Key Features:
* Custom Expression Input: The GUI includes a drop-down menu, and text box that allows users to manually input a Selenium expression.
* Custom Scraping Logic: If the user inputs a custom expression, the application will use it for scraping via the selected method.
* Unique Functionality: The code supports scraping using predefined tags with BeautifulSoup and Selenium, along with the ability to save the scraped data in various formats.

# Example Selenium Expression:
# By ID
* element = driver.find_element_by_id('element_id')

* Nested Tags Selection: Checkboxes for common HTML tags (<p>, <h1>, <h2>, <div>, <a>) to enable or disable scraping of these nested tags.
* Dynamic Data Extraction: The application dynamically extracts text from only the tags selected by the user.
* Selection of Nested Tags allows users to customize their scraping to include or exclude specific types of content, making the tool more flexible and user-friendly.

## Exporting Data:
 - CSV: Using Python's built-in csv module.
 - Excel: Using openpyxl or pandas.
 - SQL: Using sqlite3 or any other SQL database libraries.
 - JSON: Using Python's built-in json module.

## Source Modules & Packages

* tkinter
* BeautifulSoup
* selenium
* requests
* csv
* json
* pandas
* sqlite3

## Dependencies

* Python 3.10
* Beautiful Soup
    - requests
    - urllib
* Selenium
    - Install Chrome.
    - Download and install the chromedriver.

* Update the paths in the code to point to chrome.exe and chromedriver.exe
* NOTE - these paths may differ on your machine and OS.

  - chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
  - service = Service(executable_path="C:\\webdrivers\\chromedriver.exe")

Built with python and Tkinter GUI library.

Authors

    David Spies
