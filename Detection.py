import streamlit as st

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import model
from datetime import datetime
import utils
import arduino

st.set_page_config(page_title='Emotion Detection', page_icon=':smiley:', layout='wide', initial_sidebar_state='expanded')


#Set up initial state
if "image" not in st.session_state:
    st.session_state.image = None
if "image_changed" not in st.session_state:
    st.session_state.image_changed = False
if "detected" not in st.session_state:
    st.session_state.detected = False
if "prediction" not in st.session_state:
    st.session_state.prediction = False
if "song" not in st.session_state:
    st.session_state.song = None



st.title('Face Detection Application')
st.write('This app detects faces and predicts the emotion of the detected face. Then Recommends a song based on the detected emotion.')

st.divider()
st.subheader('Upload an image')


col1, col2 = st.columns(2)
with col1:
    
    picture = st.camera_input('Capture a picture')
with col2:
    
    uploaded_file = st.file_uploader("Upload your face image", type="jpg")




button = st.button('Upload Your Face')
if button:
    if picture :
        #st.image(picture, caption='Uploaded Image', use_column_width=True)
        image = picture
        st.session_state.image = image
        st.session_state.image_changed = True
        st.session_state.detected = False
    elif uploaded_file:
        #st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        image = uploaded_file
        st.session_state.image = image
        st.session_state.image_changed = True
        st.session_state.detected = False
    else: 
        st.warning('Please upload an image or capture a picture')

def call_back_detected():
    st.session_state.detected = True

if st.session_state.image: #Cached
    image = st.session_state.image
    st.image(image, caption='Uploaded Image',width=700)
    detect_button = st.button("Detect Emotion",on_click=call_back_detected)

    if detect_button or st.session_state.detected:
        col1_result, col2_result = st.columns(2)
        with col1_result:
            if st.session_state.image_changed:
                arduino.upload_empty_code()

                prediction_image,prediction,prediction_int = model.predict_image(image)
                st.image(prediction_image ,caption='Emotion Detection',width=700)
                if prediction:
                    st.write('Emotion detected successfully')
                    songs = utils.query_songs(prediction_int)
                    song = utils.get_random_song(songs)
                    arduino_code = arduino.create_code_content(song['melody'], song['duration'])
                    success, message = arduino.create_arduino_file(
                        folder_path="code",
                        filename="code",
                        code_content=arduino_code,
                        overwrite=True  # Set to True to allow overwriting
                    )
                    st.balloons()
                else:
                    song = None
                    
                    st.write("Cannot detect emotion")

                

                ### Caching Image
                st.session_state.image_changed = False
                st.session_state.predict_image = prediction_image
                st.session_state.prediction = prediction
                st.session_state.song = song

            else:
                prediction_image = st.session_state.predict_image
                prediction = st.session_state.prediction 
                song = st.session_state.song
                st.image(prediction_image, caption='Emotion Detection',width=700)
                if st.session_state.prediction:
                    st.write('Emotion detected successfully')
                    st.balloons()
                else:
                    st.write("Cannot detect emotion")
        
        with col2_result:
            st.header("Song Recommendation")
            if song is None:
                song_name = None
                st.write(f"Song name: Cannot Recomenend a song because Cannot Detect your Emotion")
            else:
                song_name = song['name']
                st.write(f"Song name: {song_name}")
                st.button("Play Song",on_click=arduino.upload_play_song)
                st.button("Pause Song",on_click=arduino.upload_empty_code)

            st.subheader("Save your Emotion")
            with st.form("example_form",clear_on_submit=False):
                # Datetime input
                current_time = datetime.now()   
                datetime_input = st.date_input("Select a date:", value=current_time)

                
                mood = st.text_input("Mood:", value=prediction)

                # Text input for song name
                song_name = st.text_input("Song Name:", value=song_name)

                # Submit button
                submit_button = st.form_submit_button("Submit",disabled=False)
                if submit_button:
                    utils.save_daily_emotion(current_time, mood, song_name, image)
                    st.write("Emotion saved successfully")
                    
                



        

#     if detect_button:
#         print("Detecting Emotion")
#         prediction = model.predict_image(image)
#         print(prediction)
#         st.image(prediction, caption='Emotion Detection',width=700)
#         st.write('Emotion detected successfully')
#         st.balloons()