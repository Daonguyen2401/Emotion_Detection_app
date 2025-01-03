import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime,timedelta
from utils import query_emotions_history

def load_image(image_path):
    try:
        return Image.open(image_path)
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None

def main():
    

    # Add title
    st.markdown("""
        <h1 style='text-align: center; color: #1E88E5;'>Daily Emotion Tracker</h1>
        <hr>
    """, unsafe_allow_html=True)

    # Filter Section
    st.subheader("🔍 Filter Section")
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        from_date = st.date_input("From Date",value=None)
    with col2:
        to_date = st.date_input("To Date",value=None)
    with col3:
        search_clicked = st.button("Search", type="primary")

    # Convert dates to datetime if search is clicked
    if search_clicked:
        from_datetime = datetime.combine(from_date, datetime.min.time())
        to_datetime = datetime.combine(to_date, datetime.max.time())
        emotions_data = query_emotions_history(from_datetime, to_datetime)
    else:
        emotions_data = query_emotions_history()

    # Display records
    st.subheader("📝 Emotion Records")
    
    # Create custom CSS for the image display
    st.markdown("""
        <style>
        .emotion-image {
            width: 150px;
            height: 150px;
            object-fit: cover;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display each record as a row
    for emotion_entry in emotions_data:
        with st.container():
            cols = st.columns([1, 2, 2, 2, 3])
            
            # Load and display image
            image = load_image(emotion_entry['image_path'])
            if image:
                cols[0].image(image, width=150)
            
            # Display emotion with emoji
            emoji_map = {
                "Happy": "😊",
                "Sad": "😢",
                "Angry": "😠",
                "Excited": "🤩",
                "Neutral": "😐",
                "Disgusted": "🤮",
                "Fearful": "😨",
                "Surprised": "😲"
            }
            emoji = emoji_map.get(emotion_entry['emotion'], "❓")
            
            # Display information in columns
            cols[1].write("**Date:**")
            cols[1].write(emotion_entry['timestamp'])
            
            cols[2].write("**Emotion:**")
            cols[2].write(f"{emoji} {emotion_entry['emotion']}")
            
            cols[3].write("**Song:**")
            cols[3].write(f"🎵 {emotion_entry['song_name']}")
            
            cols[4].write("**Image Path:**")
            cols[4].write(emotion_entry['image_path'])
            
            # Add a separator between records
            st.markdown("<hr>", unsafe_allow_html=True)

    # Add basic statistics at the bottom
    # if emotions_data:
    #     st.subheader("📊 Quick Statistics")
    #     df = pd.DataFrame(emotions_data)
        
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         st.write("Emotion Distribution")
    #         emotion_counts = df['emotion'].value_counts()
    #         st.bar_chart(emotion_counts)
            
    #     with col2:
    #         st.write("Most Common Songs")
    #         song_counts = df['song_name'].value_counts().head(5)
    #         st.table(song_counts)

if __name__ == "__main__":
    main()