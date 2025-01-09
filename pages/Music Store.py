import streamlit as st
import pandas as pd
from datetime import datetime

import utils

# Define the emotion dictionary
emotion_dict = {
    0: "Angry",
    1: "Disgusted",
    2: "Fearful",
    3: "Happy",
    4: "Neutral",
    5: "Sad",
    6: "Surprised"
}

# Sample data


def main():
    st.title("🎵 Song Database")
    
    # Convert the data to a DataFrame
    songs_data = utils.query_songs()
    df = pd.DataFrame(songs_data)
    
    # Map the category numbers to emotion names
    df['emotion'] = df['category'].astype(int).map(emotion_dict)
    
    # Format the created_at date
    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Create a clean display DataFrame with only the required columns
    display_df = df[['name', 'emotion', 'created_at']].rename(columns={
        'name': 'Song Name',
        'emotion': 'Emotion',
        'created_at': 'Created Date'
    })
    
    # Add some styling
    st.markdown("""
    <style>
    .stDataFrame {
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the DataFrame
    st.dataframe(
        display_df,
        hide_index=True,
        width=800
    )
    

if __name__ == "__main__":
    main()