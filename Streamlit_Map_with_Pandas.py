import streamlit as st
import pydeck as pdk
import pandas as pd


path = "/Users/zacharykourakis/Downloads/OneDrive_1_12-11-2023/"

df_bos = pd.read_csv(path + "boston_universities.csv")
#Map data must contain a column named "latitude" or "lat"
st.write(df_bos)
df_bos.rename(columns={"lat":"lat", "lon": "lon"}, inplace= True)

selected_map = st.sidebar.radio("Please select the map", ["", "Simple", "Scatter", "Custom Icon"])
zoom_level = st.sidebar.slider("Please select the zoom level", 0.0, 15.0, 10.0)
# python -m streamlit run ""

if selected_map == "Simple":
    st.title('Simple Map')
    # The most basic map, st.map(df)
    st.map(df_bos)

elif selected_map == "Scatter":

    st.title("Scatterplot map")

    # Create a view of the map: https://pydeck.gl/view.html
    view_state = pdk.ViewState(
        latitude=df_bos["lat"].mean(), # The latitude of the view center
        longitude=df_bos["lon"].mean(), # The longitude of the view center
        #latitude= 0,
        #longitude= 0,
        zoom=zoom_level, # View zoom level
        pitch=0) # Tilt level

    # Create a map layer with the given coordinates
    layer1 = pdk.Layer(type = 'ScatterplotLayer', # layer type
                      data=df_bos, # data source
                      get_position='[lon, lat]', # coordinates
                      get_radius=500, # scatter radius
                      get_color=[0,200,0],   # scatter color
                      pickable=True # work with tooltip
                      )

    # Can create multiple layers in a map
    # For more layer information
    # https://deckgl.readthedocs.io/en/latest/layer.html
    # Line layer https://pydeck.gl/gallery/line_layer.html
    layer2 = pdk.Layer('ScatterplotLayer',
                      data=df_bos,
                      get_position='[lon, lat]',
                      get_radius=100,
                      get_color=[0,0,255],
                      pickable=True
                      )


   # stylish tool tip: https://pydeck.gl/tooltip.html?highlight=tooltip
    tool_tip = {"html": "University Short Name:<br/> <b>{URL}</b>",
                "style": { "backgroundColor": "orange",
                            "color": "white"}
              }

    # Create a map based on the view, layers, and tool tip
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v12', # Go to https://docs.mapbox.com/api/maps/styles/ for more map styles
        initial_view_state=view_state,
        layers=[ layer1, layer2], # The following layer would be on top of the previous layers
        tooltip= tool_tip
    )

    st.pydeck_chart(map) # Show the map in your app

elif selected_map == "Custom Icon":

    st.title("Icon Map")

    # Create custom icons
    ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/b/b3/Icon_Information.svg" # Get the custom icon online
    #Icon or picture finder: https://commons.wikimedia.org/

    # Format your icon
    icon_data = {
        "url": ICON_URL,
        "width": 100,
        "height": 100,
        "anchorY": 1
        }

    # Add icons to your dataframe
    df_bos["icon_data"]= None
    for i in df_bos.index:
        #df_bos["icon_data"][i] = icon_data
        df_bos.at[i, "icon_data"] = icon_data

    st.write(df_bos)
    # Create a layer with your custom icon
    icon_layer = pdk.Layer(type="IconLayer",
                           data = df_bos,
                           get_icon="icon_data",
                           get_position='[lon,lat]',
                           get_size=4,
                           size_scale=10,
                           pickable=True)

    # Create a view of the map: https://pydeck.gl/view.html
    view_state = pdk.ViewState(
        latitude=df_bos["lat"].mean(),
        longitude=df_bos["lon"].mean(),
        zoom=11,
        pitch=0
        )

    # stylish tool tip: https://pydeck.gl/tooltip.html?highlight=tooltip
    tool_tip = {"html": "University Name:<br/> <b>{Name}</b>",
                "style": { "backgroundColor": "orange",
                            "color": "white"}
              }


    icon_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/navigation-day-v1',
        layers=[icon_layer],
        initial_view_state= view_state,
        tooltip = tool_tip
        )
    st.pydeck_chart(icon_map)

