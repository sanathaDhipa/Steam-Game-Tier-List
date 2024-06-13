import streamlit as st
import datetime, pickle, datetime
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def load_model():
    with open('best_gb_pipeline.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

data = {
    'Price': [],
    'Year': [],
    'Quarter': [],
    'Month': [],
    'Day': [],
    'PEGI_3': [0],
    'PEGI_7': [0],
    'PEGI_12': [0],
    'PEGI_16': [0],
    'PEGI_18': [0],
    'Sub_concentration_points': [],
    'Dub_concentration_points': [],
    'Platform_concentration_points': [],
    'Genre_concentration_points': [0]
}

@st.experimental_dialog("Your Game rating. . .", width="small")
def show_tier(tier):
    if tier == 'S':
        st.balloons()
        st.image('./asset/S.svg', use_column_width='always')
    elif tier == 'A':
        st.balloons()
        st.image('./asset/A.svg', use_column_width='always')
    elif tier == 'B':
        st.image('./asset/B.svg', use_column_width='always')
    elif tier == 'C':
        st.image('./asset/C.svg', use_column_width='always')

def calculate_true_concentration(item_list):
    if not item_list:
        return 0.0
    counter = Counter(item_list)
    true_count = counter.get(True, 0)
    total = sum(counter.values())
    concentration = true_count / total if total > 0 else 0.0
    return concentration

def show_predict_page():
    # st.title()
    st.header('Game :red[Tier] Prediction:video_game:', divider='rainbow')
    # < -- Content Rating -- >
    content_selectbox = (
        "PEGI 18",
        "PEGI 16",
        "PEGI 12",
        "PEGI 7",
        "PEGI 3",
    )
    content_rating = st.selectbox("Content Rating", content_selectbox)
    
    data['PEGI_18'] = [0]
    data['PEGI_16'] = [0]
    data['PEGI_12'] = [0]
    data['PEGI_7'] = [0]
    data['PEGI_3'] = [0]
    if content_rating == "PEGI 18":
        data['PEGI_18'] = [1]
    elif content_rating == "PEGI 16":
        data['PEGI_16'] = [1]
    elif content_rating == "PEGI 12":
        data['PEGI_12'] = [1]
    elif content_rating == "PEGI 7":
        data['PEGI_7'] = [1]
    elif content_rating == "PEGI 3":
        data['PEGI_3'] = [1]

    # < -- Release Date -- >
    release_date = st.date_input("Release Date", datetime.date(2024, 6, 14), format="MM-DD-YYYY")
    
    data['Year'] = [0]
    data['Quarter'] = [0]
    data['Month'] = [0]
    data['Day'] = [0]
    data['Year'] = [release_date.year]
    data['Quarter'] = [(release_date.month - 1) // 3 + 1]
    data['Month'] = [release_date.month]
    data['Day'] = [(release_date.day)]
    
    
    # < -- Genre -- >
    options_genre = st.multiselect(
    "Genre",
    ["Free to Play", "Early Access", "Action", "Adventure", 'Casual', 'Indie', 'Massively Multiplayer', 'Racing', 'RPG', 'Simulation', 'Sports', 'Strategy'])
    concentration_value = calculate_true_concentration(options_genre)
    data['Genre_concentration_points'] = [concentration_value]
    
    data_genre = {
    'Free to Play': [0],
    'Early Access': [0],
    'Action': [0],
    'Adventure': [0],
    'Casual': [0],
    'Indie': [0],
    'Massively Multiplayer': [0],
    'Racing': [0],
    'RPG' : [0],
    'Simulation': [0],
    'Sports': [0],
    'Strategy': [0],
    }
    
    for option in options_genre:
        if option in data_genre:
            data_genre[option] = [1]
            
    values_list_genre = [data_genre[language][0] for language in data_genre]
    
    genre_concentrated_points = calculate_true_concentration(values_list_genre)
    
    data['Genre_concentration_points'] = [genre_concentrated_points]
    
    # < -- Game language Support -- >
    options_sub = st.multiselect(
    "Language Support",
    ["English", "French", "Italian", "German", 'Spanish-Spain', 'Japanese', 'Portuguese-Brazil', 'Russian', 'SimplifiedChinese', 'Korean', 'Other'])
    
    data_sub = {
    'English': [0],
    'French': [0],
    'Italian': [0],
    'German': [0],
    'Spanish-Spain': [0],
    'Japanese': [0],
    'Portuguese-Brazil': [0],
    'Russian': [0],
    'SimplifiedChinese': [0],
    'Korean': [0],
    'Other': [0],
    }
    
    for option in options_sub:
        if option in data_sub:
            data_sub[option] = [1]
    
    values_list_sub = [data_sub[language][0] for language in data_sub]
    
    sub_concentrated_points = calculate_true_concentration(values_list_sub)
    
    data['Sub_concentration_points'] = [sub_concentrated_points]
    
    # < -- Game Audio Support -- >
    options_dub = st.multiselect(
    "Audio Support",
    ["Text Only", "English", "Japanese", "German", 'French', 'Italian', 'Spanish-Spain', 'Russian', 'TraditionalChinese', 'SimplifiedChinese', 'Other'])
    
    data_dub = {
    "Text Only": [0],
    'English': [0],
    'Japanese': [0],
    'German': [0],
    'French': [0],
    'Italian': [0],
    'Spanish-Spain': [0],
    'Russian': [0],
    'TraditionalChinese': [0],
    'SimplifiedChinese': [0],
    'Other': [0],
    }
    
    for option in options_dub:
        if option in data_dub:
            data_dub[option] = [1]
    
    values_list_dub = [data_dub[language][0] for language in data_dub]
    
    dub_concentrated_points = calculate_true_concentration(values_list_dub)
    
    data['Dub_concentration_points'] = [dub_concentrated_points]
    
    # < -- Game Platform -- >
    options_platform = st.multiselect(
    "Platform",
    ["Windows", "Linux", "Mac"])
    
    data_platform = {
    "Windows": [0],
    'Linux': [0],
    'Mac': [0]
    }
    
    for option in options_platform:
        if option in data_platform:
            data_platform[option] = [1]
    
    values_list_platform = [data_platform[language][0] for language in data_platform]
    
    platform_concentrated_points = calculate_true_concentration(values_list_platform)
    
    data['Platform_concentration_points'] = [platform_concentrated_points]
    
    # < -- Game Price -- >
    slider_price = st.slider("Price", 0.0, 200.0)
    data['Price'] = [slider_price]
    
    # < -- Submit -- >
    ok = st.button("Get Tier")
    if ok:
        df = pd.DataFrame(data) 
        
        classification = load_model()
        tier = classification.predict(df)
        show_tier(tier)
        if tier == 'S':
            st.balloons()
        elif tier == 'A':
            st.balloons()

    
    # < -- Testing -- >
    # st.write('Test :')
    
    # st.write(data_genre)
    # st.write(values_list_genre)
    # st.write(genre_concentrated_points)
    
    # st.write(data_sub)
    # st.write(values_list_sub)
    # st.write(sub_concentrated_points)
    
    # st.write(data_dub)
    # st.write(values_list_dub)
    # st.write(dub_concentrated_points)
    
    # st.write(data_platform)
    # st.write(values_list_platform)
    # st.write(platform_concentrated_points)
    
    # st.write(data)
    
# < -- Lunch the app -- >
show_predict_page()
    
    
