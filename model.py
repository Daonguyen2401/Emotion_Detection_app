import numpy as np
import argparse
import matplotlib.pyplot as plt
from PIL import Image
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# command line argument
ap = argparse.ArgumentParser()
ap.add_argument("--mode",help="train/display")
mode = ap.parse_args().mode

# Create the model
model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

model.load_weights('model/Emotion-detection/src/model.h5')

emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}


def emotion_detection(frame):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        emotion = None
        maxindex = None
        if frame is None:
            print("Could not read input file")
            return
        else:
            facecasc = cv2.CascadeClassifier('model/Emotion-detection/src/haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
                prediction = model.predict(cropped_img)
            
                if np.max(prediction)>0:
                    maxindex = int(np.argmax(prediction))
                    emotion = emotion_dict[maxindex]
                    cv2.putText(frame, emotion, (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                else:
                    maxindex = None
                    emotion = None
                    cv2.putText(frame, 'Cannot Detect', (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    
            return frame,emotion,maxindex

def predict_image(upload_image):
        image = Image.open(upload_image)
        imagarray  = np.array(image)
        detected_image,prediction,maxindex = emotion_detection(imagarray)
        detected_image = Image.fromarray(detected_image)
        return detected_image,prediction,maxindex

    

if __name__ == '__main__':
        frame = cv2.imread('R.jpg')
        image,prediction,maxindex = emotion_detection(frame)
        # cv2.imshow('Emotion Detection', prediction)
        # cv2.waitKey(0)  # Wait indefinitely for a key press
        # cv2.destroyAllWindows()         
        print(maxindex)  
             
             


