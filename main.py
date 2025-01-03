import cv2

import model

sample_image_path = "nguyen.jpg"

if __name__ == "__main__":
    frame = cv2.imread(sample_image_path)
    image,prediction = model.emotion_detection(frame)
    print("Prediction emotion:",prediction)