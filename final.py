"""
Name:       Zachary Kourakis
CS230:      Section 6
Data:       CRIME INCIDENT REPORTS 2023/2020
URL:        Link to your web application on Streamlit Cloud (if posted)

Description:

This program will take a look into Boston Crime rates in 2020 and 2023. I will compare the crime rate
by using a bar chart, line chart, pie chart and a map. An analysis will be provided at the end of the page.

"""

#Importing packages
import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt
#Displaying this message so it doesnt show on streamlit
st.set_option('deprecation.showPyplotGlobalUse', False)

#Creating pages on the app to interact with
page = st.sidebar.selectbox("Choose a page", ["Home", "Scatterplot Map",
                                              "Incidents by Day of Week","Incidents by Night vs Day","Shootings in 2020 compared to 2023","Code","Conclusion"])

#Creating a dictionary to set months to a value
month_names = {
    1: 'Jan',
    2: 'Feb',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'Aug',
    9: 'Sept',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec' }

#Creating the home page
if page == "Home":
    st.title("Boston Crime")

    #Writing a description
    st.markdown("""
        Welcome to the Boston Crime Analysis application. This website provides an
         overview of crime data from the years 2020 and 2023. Key insights include:

        - **Hotspots of Crime**: Identifying areas in Boston with the highest frequency of criminal incidents.
        - **Safest Days**: Analysis of crime trends across different days of the week to suggest safer times.
        - **Yearly Comparison**: A direct comparison of the shooting incidents between 2023 and 2020, highlighting any significant changes or trends.

        Click around the website to explore these aspects and gain a deeper understanding of crime patterns in Boston.
        """)

    #Displaying an image on the page
    image_path = '/Users/zacharykourakis/Downloads/OneDrive_1_12-11-2023/boston.jpeg'
    st.image(image_path, caption='Boston, Massachusetts')

#Reading the data frames from folder
df = pd.read_csv('/Users/zacharykourakis/Downloads/OneDrive_1_12-11-2023/boston_crime_2023.csv', low_memory=False)
df_2020 = pd.read_csv('/Users/zacharykourakis/Downloads/OneDrive_1_12-11-2023/boston_crime_2020.csv', low_memory=False)


#Cleaing up the csv file:
#Removing columns
remove_columns = ['INCIDENT_NUMBER', 'OFFENSE_CODE', 'OFFENSE_CODE_GROUP', 'REPORTING_AREA',
                   'UCR_PART']
df = df.drop(columns=remove_columns)

#Renaming map data to build map
df.rename(columns={'Lat': 'lat', 'Long': 'lon'}, inplace=True)

#Dropping NA lines
df = df.dropna(subset=['lat', 'lon'])


#Creating scatter plot map
if page == "Scatterplot Map":
    st.title("Scatterplot map of Shootings")

    st.markdown("This page represents an interactive map that "
                "visualizes shooting incidents in Boston in 2023. "
                "It highlights locations where shootings have occurred."
                " You can customize your view by using the zoom level. "
                "The areas with a greater influx of red dots are the areas with higher shootings. ")

    #Defining df_shooting as shooting is = 1
    df_shooting = df[df['SHOOTING'] == 1]

    #Creating a zoom bar
    zoom_level = st.sidebar.slider("Please select the zoom level", 0.0, 15.0, 10.0)

    #Creating a view of the map
    view_state = pdk.ViewState(
        latitude=df_shooting["lat"].mean(),
        longitude=df_shooting["lon"].mean(),
        zoom=zoom_level,
        pitch=0
    )

    #Creating a map layer for shootings
    shooting_layer = pdk.Layer(
        type='ScatterplotLayer',
        data=df_shooting,
        get_position='[lon, lat]',
        get_radius=100,
        get_color=[255, 0, 0],  # Red color for shootings
        pickable=True
    )


    tool_tip = {
        "html": "Street:<br/> <b>{STREET}</b>",
        "style": {
            "backgroundColor": "blue",
            "color": "yellow"
        }
    }

    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v12',
        initial_view_state=view_state,
        layers=[shooting_layer],
        tooltip=tool_tip
    )

    st.pydeck_chart(map)

#Creating pie chart page
if page == "Incidents by Night vs Day":
    st.header("Incidents by Night vs Day")
    st.markdown("This page shows the comparison on incidents occured at night vs incidents occured in the day time."
                "I considered 'Day' as any time after 6am and 'Night' as any time after 6pm. You can use the widjet "
                "to adjust the sample size which will produce different results. Incidents occur more during the day time"
                "than the night time.")

    #Adding a number input widget for selecting the number of samples
    sample_count = st.number_input("Enter the number of samples per month", min_value=1, max_value=1000, value=100)

    #Defining a function to classify incidents as Day or Night
    def classify_time(hour):
        return 'Day' if 6 <= hour < 18 else 'Night'

    #Applying the function to the 'HOUR' column to know which is day or night
    df['Time_Type'] = df['HOUR'].apply(classify_time)

    #Sample the data based on the user's input
    sampled_df = df.groupby('MONTH').sample(n=min(sample_count, len(df)), random_state=1)

    #Counting each occurrences in the sampled data
    day_night_counts = sampled_df['Time_Type'].value_counts()

    if not day_night_counts.empty:
        #Creating a pie chart, adjusting size and adding axis labels
        fig, ax = plt.subplots(figsize = (4,4))
        ax.pie(day_night_counts, labels=day_night_counts.index, autopct='%1.1f%%', startangle=90)
        ax.set_title('Incidents by Day and Night (Sampled Data)')

        #Display the pie chart in app
        st.pyplot(fig)
    else:
        st.write("No data available to display.")


#Creating bar chart
if page == "Incidents by Day of Week":
    st.header("Incidents by Day of Week")

    st.markdown("This page shows incidents that occurred in Boston based on the day of the week. "
                " You can change the frequency of the sample size below. "
                " A bar graph was created to demonstrate the data." 
        " Below the bar chart, I have create a list to show an example of what these incidents might look like.")

    #Adding a number input widget for selecting the number of samples
    sample_count = st.number_input("Enter the number of samples", min_value=1, max_value=1000, value=100)

    df_sample_bar = df.groupby('MONTH').sample(n=sample_count, random_state=1)

    day_of_week_counts = df_sample_bar['DAY_OF_WEEK'].value_counts()

    #Plotting the bar chart, axis, and titles
    plt.bar(day_of_week_counts.index, day_of_week_counts.values, color="plum")
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Incidents')
    plt.title('Incidents by Day of the Week')

    plt.grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot()

    #Creating a list of incidents
    df_sample_list = df.groupby('MONTH').sample(n=2, random_state=1)

    #Adding select incidents to list
    incident_types = df_sample_list["OFFENSE_DESCRIPTION"].tolist()

    #Sorting list by alphabetical order
    incident_types = sorted(incident_types)

    incident_type_list = []
    for incident_type in incident_types:
        incident_type_list.append(incident_type)
    incident_type_dict = {incident_type: None for incident_type in incident_type_list}

    #Printing incident type at the bottom of bar chart
    st.write("Examples of Incident Types:")
    for incident_type in incident_type_dict.keys():
        st.write(f"- {incident_type}")


#Creating line chart
if page == "Shootings in 2020 compared to 2023":
    #Making a widget for choosing which year
    st.title("Shootings in 2020 compared to 2023")
    st.markdown("This page shows a comparison between the number of shootings in 2020 and 2023. You can use the widget"
                "on the side to select the year you would like to compare with the other. There are more shootings in"
                " 2020 which signifies a decrease in shootings over the last 3 years.")
    selected_years = st.sidebar.multiselect('Select Year(s)', ['2020', '2023'], default=['2020', '2023'])

    #Creating a line chart
    fig, ax = plt.subplots()

    #Plotting data for 2020
    if '2020' in selected_years:
        data_2020 = df_2020[df_2020['SHOOTING'] == 1].groupby('MONTH').size()
        ax.plot(data_2020.index, data_2020.values, label='2020 Shootings', marker='o')

    #Plotting data for 2023
    if '2023' in selected_years:
        data_2023 = df[df['SHOOTING'] == 1].groupby('MONTH').size()
        ax.plot(data_2023.index, data_2023.values, label='2023 Shootings', marker='o')

    #Adding labels and title to the chart
    if selected_years:
        ax.set_ylabel('Number of Shootings')
        ax.set_title('Monthly Shootings Comparison')
        ax.legend()

        #Setting x-axis labels with the month names in the dictionairy
        ax.set_xticks(list(month_names.keys()))
        ax.set_xticklabels(list(month_names.values()), rotation=45)
        ax.grid(True)


        st.pyplot(fig)
        #Error handling
    else:
        st.write("Select one or more years to display data.")

#Creating page to display a proud code
if page == "Code":
    st.title('Code Display')
    st.write("")

    code_1 = """
    
    df_sample_list = df.groupby('MONTH').sample(n=2, random_state=1)

    incident_types = df_sample_list["OFFENSE_DESCRIPTION"].tolist()
    incident_types = sorted(incident_types)

    incident_type_list = []
    for incident_type in incident_types:
        incident_type_list.append(incident_type)
    incident_type_dict = {incident_type: None for incident_type in incident_type_list}

    for incident_type in incident_type_dict.keys():
        print(f"- {incident_type}")
        """

    st.code(code_1, language='python')



#Creating a conclusion page
if page == "Conclusion":
    st.title("Conclusion and Analysis")
    st.markdown("In conclusion, the areas with the most shootings are around Roxbury and Dorchester. You should "
                "look to avoid these areas when possible if you are new to Boston. If you do happen to go to these areas to visit,"
                " you should go on a Sunday as this is the day with the least amount of incidents per week. During the night time preferably"
                " as crime occurs 60% through the day time and 40% through the night time as show in the bar chart."
                " Lastly, the shooting rates have dropped drastically in 2023 compared to 2020 with a peak difference of"
                " 140 shootings in June of 2020 to 60 shootings in June 2023. Summer times are usually the peak times for crime. ")

    #Spacing for organization
    for _ in range(5):
        st.write("")

    #Inputting second image
    image_path2 = '/Users/zacharykourakis/Downloads/OneDrive_1_12-11-2023/thank_you.jpeg'
    st.image(image_path2)

    for _ in range(2):
        st.write("")



    st.markdown("-App made by Zachary Kourakis")




#Referenced https://docs.streamlit.io/library/api-reference/widgets to learn how to use various widgets
#Referenced https://stackoverflow.com/questions/7818811/error-import-error-no-module-named-numpy-on-windows to fix an error
#Referenced boston image: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.travelandleisure.com%2Ftravel-guide%2Fboston&psig=AOvVaw3uNBbktHE_lbm6jGO-g1os&ust=1702931884946000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCICqxcS3l4MDFQAAAAAdAAAAABAD
#Referenced thank you image: https://www.thankyoudiva.com/images/thank-you-for-visiting-my-website.jpg
