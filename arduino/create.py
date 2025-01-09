import os
import sys
from pathlib import Path



def create_code_content(melody: str, duration: str):
    code = """
#include "pitches.h"

#define BUZZER_PIN 9

int melody[] = melody_placeholder;

int durations[] = duration_placeholder;

void setup()
{
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop()
{
  int size = sizeof(durations) / sizeof(int);

  for (int note = 0; note < size; note++) {
    int duration = 1000 / durations[note];
    tone(BUZZER_PIN, melody[note], duration);

    int pauseBetweenNotes = duration * 1.30;
    delay(pauseBetweenNotes);

    noTone(BUZZER_PIN);
  }
}
"""
    code = code.replace("melody_placeholder", melody).replace("duration_placeholder", duration)
    return code


def create_arduino_file(folder_path ="code", filename= "code", code_content = None, overwrite=True):
    """
    Creates an Arduino (.ino) file in the specified folder with the given code content.
    
    Args:
        folder_path (str): Path to the folder where the file should be created
        filename (str): Name of the Arduino file (without extension)
        code_content (str): The Arduino code to write to the file
        overwrite (bool): If True, overwrites existing file; if False, raises error
    
    Returns:
        tuple: (bool, str) - (Success status, Message)
    """
    try:
        parent_dir = Path(__file__).parent.resolve()

        # Resolve the target folder inside the parent directory
        target_folder = parent_dir / folder_path
        target_folder = target_folder.resolve()
        # Create folder if it doesn't exist
        folder = target_folder
        folder.mkdir(parents=True, exist_ok=True)
        
        # Ensure filename has .ino extension
        if not filename.endswith('.ino'):
            filename = filename + '.ino'
        
        # Create full file path
        file_path = folder / filename
        
        # Check if file already exists and overwrite is False
        if file_path.exists() and not overwrite:
            return False, f"File {filename} already exists in {folder_path} and overwrite is disabled"
        
        # Write or overwrite the code content to the file
        with open(file_path, 'w') as f:
            f.write(code_content)
        
        action = "Updated" if file_path.exists() else "Created"
        return True, f"Successfully {action} {filename} in {folder_path}"
    
    except PermissionError:
        return False, f"Permission denied: Cannot create/modify file in {folder_path}"
    except Exception as e:
        return False, f"Error creating/modifying file: {str(e)}"

# Example usage
if __name__ == "__main__":
    pass
    # Sample Arduino code
    # songs = utils.query_songs("3")
    # song = utils.get_random_song(songs)
    # print(song)

    
    # song_code = create_code_content("melody","duration")
    
    # # Create or overwrite the file
    # success, message = create_arduino_file(
    #     folder_path="code",
    #     filename="code",
    #     code_content=song_code,
    #     overwrite=True  # Set to True to allow overwriting
    # )
    
    # print(message)