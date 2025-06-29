🏘️ Hawthorn Village Apartments Web Scraper

📖 Table of Contents

✨ Project Objective
🚀 Setup & Dependencies
🎯 Target Website
⚙️ Technical Choices Explained
📊 Scraping Strategy & Workflow
📤 Output
⚠️ Limitations & Assumptions



✨ Project Objective
This project delivers a robust web scraper designed to collect structured data on apartment listings from a real estate website. The scraper is engineered to extract key features, including unit names, square footage, bedroom/bathroom counts, pricing, availability, and a list of amenities. The data is then organized into a clean, easy-to-use CSV file for further analysis.

🚀 Setup & Dependencies
To run this scraper, you need to have Python 3.8+ installed on your system. Follow these steps to set up the project environment and install all necessary dependencies.

Step 1: Clone the Repository
First, clone this repository to your local machine using Git:



git clone https://github.com/OltShala/WebScrapingSelenium
cd WebScraperSelenium


Step 2: Install Required Libraries
It is highly recommended to use a virtual environment to manage project dependencies.

Create a virtual environment (e.g., using venv):



python3 -m venv venv
Activate the virtual environment:

On macOS/Linux:

Bash

source venv/bin/activate
On Windows:

Bash

.\venv\Scripts\activate

Install the dependencies from the requirements.txt file:
Bash
pip install -r requirements.txt
This will install selenium, pandas, and webdriver-manager.

Step 3: Install a Web Browser
The scraper uses Selenium, which requires a web browser to run. Google Chrome is recommended as the default browser for this project. Ensure you have a recent version of Chrome installed on your system.

Note: The webdriver-manager library will automatically download and manage the correct chromedriver executable for your installed Chrome version, so you don't need to do it manually!

Step 4: Run the Scraper
Once the dependencies are installed and your virtual environment is active, you can run the main script from your terminal:

Bash

python hawthon_scraper.py
After the script completes, a new file named hawthorn_apartments.csv will be generated in the project's root directory, containing all the scraped data.

🎯 Target Website
The scraper is specifically built to target and extract data from the Hawthorn Village Apartments website.

🔗 Website URL: https://www.hawthornvillageapts.com

⚙️ Technical Choices Explained
Why Selenium over BeautifulSoup?

My initial approach used requests and BeautifulSoup to fetch and parse the HTML. However, I quickly discovered the apartment listings were not in the raw HTML; they were loaded dynamically with JavaScript. This is a common hurdle with modern websites.

Selenium was the perfect solution. It launches a real browser in the background, executes all the JavaScript, and lets the script interact with the page just like a human would. This allowed me to "see" and scrape the dynamically loaded content that requests couldn't access. The scraper simulates scrolling and clicking a button, ensuring all data is fully rendered before extraction.

Why WebDriver Manager?

Using webdriver-manager was a key convenience choice. It automatically handles the chromedriver executable, which is required by Selenium. This means you don't need to manually download, update, or manage the driver file—the tool does it for you, saving a lot of setup time and preventing compatibility issues.

📊 Scraping Strategy & Workflow
The web scraper navigates and extracts data from two key pages on the target website in a sequential, step-by-step process.

Step 1: Navigate to the Floor Plans Page
The script directs the browser to the main floor plans URL: https://www.hawthornvillageapts.com/apartments/ca/napa/floor-plans#/. It then waits for the page to load.

Step 2: Handle Dynamic Content Loading
A crucial part of the process is to simulate user interaction. The script performs the following actions to ensure all listings are visible:

It scrolls to the bottom of the page repeatedly to trigger lazy-loading of all content.

It clicks the "View All Floor Plans" button to reveal all available units.

It waits for the dynamic content to be fully rendered in the browser's DOM.

Step 3: Scrape Apartment Listing Data
Once the listings are loaded, the scraper iterates through each unit's element on the page and extracts:

✅ Unit Name

✅ Bedrooms

✅ Bathrooms

✅ Square Footage

✅ Price

✅ Static Address (3663 Solano Ave, Napa, CA 94558)

Step 4: Scrape Amenities Data
The scraper then navigates to the amenities page (https://www.hawthornvillageapts.com/apartments/ca/napa/amenities) to collect a comprehensive list of community features.

Step 5: Data Consolidation & Export
All collected data is consolidated. The list of amenities is added as a new column for every apartment unit entry. Finally, the structured data is saved to hawthorn_apartments.csv using the pandas library.

📤 Output
All extracted data is stored in a single CSV file using pandas. A sample output file is provided in this repository.

📁 Filename: hawthorn_apartments.csv

Export to Sheets
⚠️ Limitations & Assumptions
Limitations
Website Structure Dependency: The scraper is highly dependent on the website's HTML structure and CSS selectors. Any change to the website's code by the developers could break the scraper and require maintenance.

Browser Requirement: The script requires a compatible version of the Chrome browser to run.

No CAPTCHA Handling: The scraper does not include logic for bypassing CAPTCHAs or advanced bot detection measures.

Assumptions
Static Address: It is assumed that all apartment units share the same property address, which is hardcoded in the script.

Single Page: The scraper assumes all floor plans are accessible from a single page after lazy loading and button clicks. It is not designed to handle pagination.
