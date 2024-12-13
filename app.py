import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from PIL import Image
st.set_page_config(layout="wide")  

# Function to establish database connection
@st.cache_resource
def connect_to_database():
    try:
        #
        engine = create_engine("mysql+mysqlconnector://root:root@127.0.0.1:3307/redbus")
        return engine
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        st.stop()

# Function to fetch unique values for dropdowns
def get_unique_values(column_name, engine):
    try:
        query = f"SELECT DISTINCT {column_name} FROM busdetails"
        df = pd.read_sql(query, engine)
        return df[column_name].tolist()
    except Exception as e:
        st.error(f"Error fetching unique values for {column_name}: {e}")
        return []

# Function to fetch min and max values for a column
def get_min_max_values(column_name, engine):
    try:
        query = f"SELECT MIN({column_name}) AS min_val, MAX({column_name}) AS max_val FROM busdetails"
        result = pd.read_sql(query, engine)
        return result['min_val'][0], result['max_val'][0]
    except Exception as e:
        st.error(f"Error fetching min/max values for {column_name}: {e}")
        return None, None

# Main Streamlit App
def main():
    # sidebar  
    st.sidebar.title("🚍 FindBus Menu")
    
    menu = st.sidebar.radio("Go to", 
                            ["🏠 Home", "🚌 Select the Bus"])

    # Connect to the database
    engine = connect_to_database()

    if menu == "🏠 Home":
        st.title("Welcome to FindBus!")
        
        # Showing an image of a bus
        bus_image = Image.open("bus.jpg")  
        st.image(bus_image, caption="Find Your Perfect Bus!", use_container_width=True)

        st.write(""" 
        **FindBus** is your one-stop platform to discover the best buses for your travel needs. 
        Whether you're looking for the fastest, most comfortable, or budget-friendly bus, we've got it all!  
        Please note that **FindBus** does not allow direct bookings, but it helps you find the best buses and make informed decisions for your journey.

        ### Key Features:
        - **Easy Search**: Filter buses by route, type, price, star rating, and more!
        - **Real-time Availability**: Check live seat availability and duration for each bus.
        - **User Ratings**: Make informed decisions with star ratings from fellow travelers.
        - **Budget-Friendly**: Find buses that suit your budget, with price filters ranging from low to high.
        
        ### How it works:
        1. Choose your desired route and bus type.
        2. Adjust the filters for price, rating, and seat availability.
        3. View the buses available according to your preferences.
        
        Let's get started by selecting a bus route and filtering options in the next section. Happy travels!
        """)

    elif menu == "🚌 Select the Bus":
        st.title("Filter and Select the Bus")

        # Fetch filtering options
        route_names = get_unique_values("route_name", engine)
        bus_types = get_unique_values("bustype", engine)

        # Sidebar Filters
        selected_route = st.sidebar.selectbox("Select Route:", ["All"] + route_names)
        selected_bustypes = st.sidebar.multiselect("Select Bus Type:", bus_types)

        # Fetch dynamic slider ranges
        min_price, max_price = get_min_max_values("price", engine)
        selected_min_price, selected_max_price = st.sidebar.slider(
            "Price Range (INR):", min_price, max_price, (min_price, max_price)
        )

        min_rating, max_rating = get_min_max_values("star_rating", engine)
        selected_min_rating, selected_max_rating = st.sidebar.slider(
            "Star Rating:", min_rating, max_rating, (min_rating, max_rating)
        )

        min_seats, max_seats = get_min_max_values("seats_available", engine)
        selected_min_seats, selected_max_seats = st.sidebar.slider(
            "Seats Availability:", min_seats, max_seats, (min_seats, max_seats)
        )

        max_duration = st.sidebar.slider("Maximum Duration (hours):", 0, 24, 10)

        # Builds SQL Query
        query = f"""
            SELECT 
                route_name,  
                busname, 
                bustype, 
                DATE_FORMAT(departing_time, '%H:%i') AS departing_time, 
                duration, 
                DATE_FORMAT(reaching_time, '%H:%i') AS reaching_time, 
                star_rating, 
                price, 
                seats_available
            FROM busdetails 
            WHERE 1=1
        """

        # Apply filters dynamically
        if selected_route != "All":
            query += f" AND route_name = '{selected_route}'"
        if selected_bustypes:
            bustypes = "', '".join(selected_bustypes)
            query += f" AND bustype IN ('{bustypes}')"
        query += f" AND price BETWEEN {selected_min_price} AND {selected_max_price}"
        query += f" AND star_rating BETWEEN {selected_min_rating} AND {selected_max_rating}"
        query += f" AND seats_available BETWEEN {selected_min_seats} AND {selected_max_seats}"
        query += f" AND TIME_TO_SEC(duration) <= {max_duration * 3600}"

        try:
            # Fetch and display data
            bus_data = pd.read_sql(query, engine)
            if not bus_data.empty:
                # Reset index and start it from 1 (not adding a column, just changing index)
                bus_data.index = bus_data.index + 1  # This will make the index start from 1

                # Preprocess column names
                bus_data.columns = [col.replace("_", " ").title() for col in bus_data.columns]

                st.write(f"Showing buses for **{selected_route}**:")

                # Sets a maximum height for the table and allow horizontal scrolling
                st.dataframe(bus_data, use_container_width=True)  # Makes the table span the full width

            else:
                st.write("No buses found for the selected filters.")
        except Exception as e:
            st.error(f"Error fetching bus data: {e}")

if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from PIL import Image
st.set_page_config(layout="wide")  

# Function to establish database connection
@st.cache_resource
def connect_to_database():
    try:
        #
        engine = create_engine("mysql+mysqlconnector://root:root@127.0.0.1:3307/redbus")
        return engine
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        st.stop()

# Function to fetch unique values for dropdowns
def get_unique_values(column_name, engine):
    try:
        query = f"SELECT DISTINCT {column_name} FROM busdetails"
        df = pd.read_sql(query, engine)
        return df[column_name].tolist()
    except Exception as e:
        st.error(f"Error fetching unique values for {column_name}: {e}")
        return []

# Function to fetch min and max values for a column
def get_min_max_values(column_name, engine):
    try:
        query = f"SELECT MIN({column_name}) AS min_val, MAX({column_name}) AS max_val FROM busdetails"
        result = pd.read_sql(query, engine)
        return result['min_val'][0], result['max_val'][0]
    except Exception as e:
        st.error(f"Error fetching min/max values for {column_name}: {e}")
        return None, None

# Main Streamlit App
def main():
    # sidebar  
    st.sidebar.title("🚍 FindBus Menu")
    
    menu = st.sidebar.radio("Go to", 
                            ["🏠 Home", "🚌 Select the Bus"])

    # Connect to the database
    engine = connect_to_database()

    if menu == "🏠 Home":
        st.title("Welcome to FindBus!")
        
        # Showing an image of a bus
        bus_image = Image.open("bus.jpg")  
        st.image(bus_image, caption="Find Your Perfect Bus!", use_container_width=True)

        st.write(""" 
        **FindBus** is your one-stop platform to discover the best buses for your travel needs. 
        Whether you're looking for the fastest, most comfortable, or budget-friendly bus, we've got it all!  
        Please note that **FindBus** does not allow direct bookings, but it helps you find the best buses and make informed decisions for your journey.

        ### Key Features:
        - **Easy Search**: Filter buses by route, type, price, star rating, and more!
        - **Real-time Availability**: Check live seat availability and duration for each bus.
        - **User Ratings**: Make informed decisions with star ratings from fellow travelers.
        - **Budget-Friendly**: Find buses that suit your budget, with price filters ranging from low to high.
        
        ### How it works:
        1. Choose your desired route and bus type.
        2. Adjust the filters for price, rating, and seat availability.
        3. View the buses available according to your preferences.
        
        Let's get started by selecting a bus route and filtering options in the next section. Happy travels!
        """)

    elif menu == "🚌 Select the Bus":
        st.title("Filter and Select the Bus")

        # Fetch filtering options
        route_names = get_unique_values("route_name", engine)
        bus_types = get_unique_values("bustype", engine)

        # Sidebar Filters
        selected_route = st.sidebar.selectbox("Select Route:", ["All"] + route_names)
        selected_bustypes = st.sidebar.multiselect("Select Bus Type:", bus_types)

        # Fetch dynamic slider ranges
        min_price, max_price = get_min_max_values("price", engine)
        selected_min_price, selected_max_price = st.sidebar.slider(
            "Price Range (INR):", min_price, max_price, (min_price, max_price)
        )

        min_rating, max_rating = get_min_max_values("star_rating", engine)
        selected_min_rating, selected_max_rating = st.sidebar.slider(
            "Star Rating:", min_rating, max_rating, (min_rating, max_rating)
        )

        min_seats, max_seats = get_min_max_values("seats_available", engine)
        selected_min_seats, selected_max_seats = st.sidebar.slider(
            "Seats Availability:", min_seats, max_seats, (min_seats, max_seats)
        )

        max_duration = st.sidebar.slider("Maximum Duration (hours):", 0, 24, 10)

        # Builds SQL Query
        query = f"""
            SELECT 
                route_name,  
                busname, 
                bustype, 
                DATE_FORMAT(departing_time, '%H:%i') AS departing_time, 
                duration, 
                DATE_FORMAT(reaching_time, '%H:%i') AS reaching_time, 
                star_rating, 
                price, 
                seats_available
            FROM busdetails 
            WHERE 1=1
        """

        # Apply filters dynamically
        if selected_route != "All":
            query += f" AND route_name = '{selected_route}'"
        if selected_bustypes:
            bustypes = "', '".join(selected_bustypes)
            query += f" AND bustype IN ('{bustypes}')"
        query += f" AND price BETWEEN {selected_min_price} AND {selected_max_price}"
        query += f" AND star_rating BETWEEN {selected_min_rating} AND {selected_max_rating}"
        query += f" AND seats_available BETWEEN {selected_min_seats} AND {selected_max_seats}"
        query += f" AND TIME_TO_SEC(duration) <= {max_duration * 3600}"

        try:
            # Fetch and display data
            bus_data = pd.read_sql(query, engine)
            if not bus_data.empty:
                # Reset index and start it from 1 (not adding a column, just changing index)
                bus_data.index = bus_data.index + 1  # This will make the index start from 1

                # Preprocess column names
                bus_data.columns = [col.replace("_", " ").title() for col in bus_data.columns]

                st.write(f"Showing buses for **{selected_route}**:")

                # Sets a maximum height for the table and allow horizontal scrolling
                st.dataframe(bus_data, use_container_width=True)  # Makes the table span the full width

            else:
                st.write("No buses found for the selected filters.")
        except Exception as e:
            st.error(f"Error fetching bus data: {e}")

if __name__ == "__main__":
    main()
