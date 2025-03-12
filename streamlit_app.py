# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Establish Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch data from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()

# Extract fruit names
fruit_names = [row['FRUIT_NAME'] for row in my_dataframe]

# Display the app title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in a custom smoothie!")

# Get smoothie name
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie:", name_on_order)

# Multi-select for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_names,
    max_selections=5
)

# Handle order submission
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    st.write("Ingredients:", ingredients_string)

    # Insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Display SQL for debugging
    st.write("SQL Query:", my_insert_stmt)

    # Submit order button
    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
