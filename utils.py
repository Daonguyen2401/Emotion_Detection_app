
import os
import sqlite3
from datetime import datetime,timedelta
from pathlib import Path
import shutil
from PIL import Image
from typing import Optional,TypeVar,List
import random
import arduino



print("Current Working Directory:", os.getcwd())

def save_daily_emotion(timestamp, emotion, song_name, image):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    """
    Save emotion data and image to local storage and SQLite database.
    
    Parameters:
    timestamp (datetime): Timestamp of the emotion entry
    emotion (str): Emotion label
    song_name (str): Name of the associated song
    image: File object or path to the image file
    
    Returns:
    tuple: (success (bool), message (str))
    """
    try:
        # Create images directory if it doesn't exist
        image_dir = Path("image_history")
        image_dir.mkdir(exist_ok=True)

        # Generate unique filename using timestamp
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        image_filename = f"emotion_{timestamp_str}.jpg"
        image_path = image_dir / image_filename

        # Save image to local folder
        image = Image.open(image)
        if isinstance(image, Image.Image):  # If it's a PIL/Pillow Image object
            image.save(str(image_path), 'JPEG')
            print("Image saved")
        else:
            print("Image not saved")

        # Connect to SQLite database
        conn = sqlite3.connect('emotions.db')
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_emotions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                emotion TEXT NOT NULL,
                song_name TEXT NOT NULL,
                image_path TEXT NOT NULL
            )
        ''')
        
        # Insert data into database
        cursor.execute('''
            INSERT INTO daily_emotions (timestamp, emotion, song_name, image_path)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, emotion, song_name, str(image_path)))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        return True, f"Successfully saved emotion data and image to {image_path}"
        
    except Exception as e:
        # If any error occurs, return False with error message
        return False, f"Error saving emotion data: {str(e)}"

def recomend_audio(emotion):
    
    path =  "toy-story-short-happy-audio-logo-short-cartoony-intro-outro-music-125627.mp3"
    song_name = "Toystory"
    return song_name,path




def query_emotions_history(from_date=None, to_date=None):
    """
    Query daily emotions from SQLite database within a date range.
    If no dates are provided, returns all emotions.
    
    Parameters:
    from_date (datetime, optional): Start date of the date range
    to_date (datetime, optional): End date of the date range
    
    Returns:
    list: List of emotion entries (dict) matching the query criteria
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('emotions.db')
        cursor = conn.cursor()
        
        # Build the query based on provided parameters
        if from_date is None and to_date is None:
            # Query all emotions if no dates provided
            cursor.execute('SELECT * FROM daily_emotions ORDER BY timestamp DESC')
        elif from_date is None:
            # Query emotions up to to_date
            cursor.execute('''
                SELECT * FROM daily_emotions
                WHERE timestamp <= ?
                ORDER BY timestamp DESC
            ''', (to_date,))
        elif to_date is None:
            # Query emotions from from_date
            cursor.execute('''
                SELECT * FROM daily_emotions
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
            ''', (from_date,))
        else:
            # Query emotions within date range
            cursor.execute('''
                SELECT * FROM daily_emotions
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp DESC
            ''', (from_date, to_date))
        
        # Fetch all rows from the query result
        rows = cursor.fetchall()
        
        # Close connection
        conn.close()
        
        # Convert rows to list of dictionaries
        columns = ['id', 'timestamp', 'emotion', 'song_name', 'image_path']
        emotions = []
        for row in rows:
            emotion_dict = dict(zip(columns, row))
            # Convert timestamp string to datetime object with microseconds support
            try:
                datetime_object = datetime.strptime(
                    emotion_dict['timestamp'], 
                    '%Y-%m-%d %H:%M:%S.%f'  # Added .%f for microseconds
                )
                emotion_dict['timestamp'] = datetime_object.strftime('%d-%m-%Y')
            except ValueError:
                # If no microseconds in timestamp, try without them
                emotion_dict['timestamp'] = datetime.strptime(
                    emotion_dict['timestamp'], 
                    '%Y-%m-%d %H:%M:%S'
                )
            emotions.append(emotion_dict)
        
        return emotions
        
    except Exception as e:
        print(f"Error querying emotions: {str(e)}")
        return []
    
def query_songs(category: Optional[int] = None) -> list[dict]:
    
    try:
        # Connect to the database
        conn = sqlite3.connect('emotions.db')
        # Create a cursor object using Row factory to get dictionary-like results
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if category is not None:
            # Execute query with category filter
            cursor.execute('''
                SELECT *
                FROM songs
                WHERE category = ?
            ''', (category,))
        else:
            # Execute query without filter
            cursor.execute('''
                SELECT *
                FROM songs
            ''')
        
        # Fetch all matching rows and convert to list of dictionaries
        songs = [dict(row) for row in cursor.fetchall()]
        
        return songs
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
        
    finally:
        if conn:
            conn.close()

T = TypeVar('T')

def get_random_song(items: List[T]) -> Optional[T]:
    """
    Select a random element from a list.
    
    Args:
        items (List[T]): List of items to choose from
        
    Returns:
        Optional[T]: A random element from the list, or None if the list is empty
    """
    if not items:
        return None
    return random.choice(items)

if __name__ == '__main__':
    # image = Image.open('nguyen.jpg')
    # save_daily_emotion(datetime.now()+timedelta(days=1), 'Happy', 'Toystory', image)
    # ressult = query_emotions_history()
    # print(ressult)
    # songs = query_songs("4")
    # song = get_random_song(songs)
    # #print((song['melody']))
    # arduino_code = arduino.create_code_content(song['melody'], song['duration'])
    # success, message = arduino.create_arduino_file(
    #     folder_path="code",
    #     filename="code",
    #     code_content=arduino_code,
    #     overwrite=True  # Set to True to allow overwriting
    # )
    # success, message = arduino.upload_play_song()
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # print("Current Working Directory:", os.getcwd())
    songs = query_songs()
    print(songs)
    
    
    





