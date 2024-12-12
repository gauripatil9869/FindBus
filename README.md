
# FindBus - Bus Information Finder

**FindBus** is a comprehensive platform designed to help users find buses based on different criteria. It involves a multi-step process where we scrape bus details from various state transport websites, store them in a MySQL database, and then develop a Streamlit web application to display and filter this data.

## Project Flow

1. **Scraping Bus Data**
2. **Storing Data in MySQL Database**
3. **Developing Streamlit Application**

---

## 1. Scraping Bus Data

The first step in the project is scraping bus information from several state transport corporation websites. We use Selenium and WebDriver to navigate through the websites and collect relevant details about buses. The key steps in this process are:

- **State Routes Extraction**: We fetch the list of routes for each state transport corporation.
- **Bus Details Extraction**: For each route, we collect information such as bus name, type, departure time, duration, reaching time, price, seats available, and star rating.
- **Pagination and Infinite Scroll Handling**: We handle pagination and scrolling to load all available buses.

We scrape data for multiple states, including Himachal Pradesh, Rajasthan, Punjab, Chandigarh, Jammu & Kashmir, and others.

**Key Libraries Used**:
- `selenium`: For automating the web scraping.
- `concurrent.futures`: For parallel processing of multiple states to speed up the scraping process.

---

## 2. Storing Data in MySQL Database

After scraping the data, we sanitize the data (e.g., convert prices to integers, handle missing values) and store it in a MySQL database for efficient querying.

### Database Structure:
- **Table Name**: `busdetails`
- **Columns**:
  - `route_name`: Name of the route.
  - `route_link`: URL link for the route.
  - `busname`: Name of the bus.
  - `bustype`: Type of bus (e.g., sleeper, semi-sleeper).
  - `departing_time`: Departure time of the bus.
  - `duration`: Duration of the bus journey.
  - `reaching_time`: Reaching time of the bus.
  - `star_rating`: Rating of the bus (out of 5).
  - `price`: Price of the bus ticket.
  - `seats_available`: Number of available seats on the bus.

### MySQL Setup:
- The data is inserted into a MySQL database using the `mysql-connector-python` library.
- We sanitize and clean the data to ensure it can be used effectively in our application.

---

## 3. Developing Streamlit Application

After storing the data in MySQL, we develop a **Streamlit** web application that allows users to:

- **Filter buses** based on multiple criteria:
  - Route name
  - Bus type
  - Price range
  - Star rating
  - Seats available
  - Duration
  
- **View bus details** such as:
  - Bus name
  - Departure time
  - Duration
  - Price
  - Available seats

The Streamlit app connects to the MySQL database, retrieves the bus data, and displays it in a user-friendly format.

### Key Features:
- **User Interface**: The app has an easy-to-use interface with a sidebar for filtering options.
- **Data Visualization**: Users can view the buses in a table with the option to scroll horizontally for more details.
- **Dynamic Filtering**: The filters update the displayed results based on user input.

---

## Requirements

- Python 3.x
- MySQL Database
- Required Python Libraries:
  - `selenium`
  - `mysql-connector-python`
  - `pandas`
  - `streamlit`
  - `Pillow` (for image handling)
  
You can install the required libraries using `pip`:
```bash
pip install selenium mysql-connector-python pandas streamlit pillow
```

---

## How to Run the Project

1. **Run the Scraper**:
   - Ensure you have the correct state URLs and WebDriver set up for Selenium.
   - Run the Python script for scraping to collect the bus data and store it in the MySQL database.

2. **Run the Streamlit App**:
   - Ensure your MySQL server is running and the data is stored in the `redbus` database.
   - Run the Streamlit app using the following command:
   
   ```bash
   streamlit run app.py
   ```

3. **Access the Application**:
   - Open the app in your browser, and you'll be able to filter and view bus details.

---

## Conclusion

This project provides an easy-to-use platform for users to search and filter bus details from different state transport corporations. The combination of web scraping, MySQL storage, and Streamlit for frontend development creates an efficient and scalable solution for users to find buses based on their preferences.
