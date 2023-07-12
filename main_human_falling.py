
import cv2                          # This is the OpenCV library for image and video processing.
from ultralytics import YOLO        # This is a YOLO (You Only Look Once) object detection model from the Ultralytics library.
import numpy                        # This library provides support for multi-dimensional arrays and matrices.
import requests                     # This library is used to send HTTP requests in Python.
from pydantic import BaseModel      # This is a base class for creating models

#This code below is the LINE Notificate function.
def send_line_notify(message, image_path):
    url = "https://notify-api.line.me/api/notify"
    token = "PxOmKMhv4eNST4tacpYl1yQ8GqczL1tVQTa04lWBa55"  # Replace with your Line Notify token
    headers = {"Authorization": "Bearer " + token}

    payload = {"message": message}
    r = requests.post(url, headers=headers, data=payload)

    # Send image
    files = {"imageFile": open(image_path, "rb")}
    r = requests.post(url, headers=headers, data=payload, files=files)

#This function help to identify each of keypoints.
class GetKeypoint(BaseModel):
    NOSE:           int = 0
    LEFT_EYE:       int = 1
    RIGHT_EYE:      int = 2
    LEFT_EAR:       int = 3
    RIGHT_EAR:      int = 4
    LEFT_SHOULDER:  int = 5
    RIGHT_SHOULDER: int = 6
    LEFT_ELBOW:     int = 7
    RIGHT_ELBOW:    int = 8
    LEFT_WRIST:     int = 9
    RIGHT_WRIST:    int = 10
    LEFT_HIP:       int = 11
    RIGHT_HIP:      int = 12
    LEFT_KNEE:      int = 13
    RIGHT_KNEE:     int = 14
    LEFT_ANKLE:     int = 15
    RIGHT_ANKLE:    int = 16

# Initializing the YOLO model.
model = YOLO('yolov8n-pose.pt')

# Initialize=ing the camera.
video_path = 0  
cap = cv2.VideoCapture(video_path)

frame_time = 0 
delay_frame = 5 # you can custom delay here

while cap.isOpened():
    success, frame = cap.read()     
    boxes=[]
    annotations_frame = frame
   
    if success:                                              # if camera-read is successfully
        result = model(frame, save=True)                     # process frame with model
        
        annotations_frame = result[0].plot()                 # plot keypoints lines including rectangle around object

        for detection in result:                             # If there are persons in frame
            
            # x,y axis and width,height of object(person)
            boxes = detection.boxes.xywhn.cpu().numpy()

            # fetch amount of persons
            person = detection.boxes.shape                   
            person = int(person[0])

            if boxes.all():                                 # if there are a xywh of person in the frame        
                
                for i in range(person):                     # get value for every persons
    
                   # get array of keypoints
                    get_keypoint = GetKeypoint()
                    result_keypoint = detection.keypoints.xyn.cpu().numpy()
                   
                   # fetch some keypoint for make conditions
                    right_hip_x, right_hip_y = result_keypoint[i][get_keypoint.RIGHT_HIP]
                    right_shd_x, right_shd_y = result_keypoint[i][get_keypoint.RIGHT_SHOULDER]
                    left_hip_x, left_hip_y = result_keypoint[i][get_keypoint.LEFT_HIP]
                    left_shd_x, left_shd_y = result_keypoint[i][get_keypoint.LEFT_SHOULDER]


                    ####   thess code below are conditions ####
                   
                    if (right_hip_y or left_hip_y) != 1:  

                        if abs(right_hip_x - right_shd_x) > abs(right_hip_y - right_shd_y):
                            print("falling............")
                            cv2.putText(annotations_frame, " FALLING FOUND ", (20, 450), cv2.FONT_HERSHEY_PLAIN, 2, (218, 224, 159), 2)
                           
                            frame_time = frame_time +1
                            if frame_time % delay_frame == 0 and frame_time != 0 :
                                print("Notificate to LINE  Successfully......")
                                image_path = "falling_person.jpg"
                                cv2.imwrite(image_path, annotations_frame)
                                
                                
                                # Send Line notification with image
                                message = "Falling person detected!"
                                send_line_notify(message, image_path)
                                frame_time = 0

                        if abs(left_hip_x - left_shd_x) > abs(left_hip_y - left_shd_y):
                            print("falling............")
                            cv2.putText(annotations_frame, " FALLING FOUND ", (20, 450), cv2.FONT_HERSHEY_PLAIN, 2, (218, 224, 159), 2)
                            
                            frame_time = frame_time+1
                            if frame_time % delay_frame == 0 and frame_time != 0 :
                                print("Notificate to LINE  Successfully......")
                                image_path = "falling_person.jpg"
                                cv2.imwrite(image_path, annotations_frame)
                                
                                
                                # Send Line notification with image
                                message = "Falling person detected!"
                                send_line_notify(message, image_path)
                                frame_time = 0

    # Display frame.
    cv2.imshow("pose estimated", annotations_frame)

    # press "q" for stop this program
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
   

cap.release()
cv2.destroyAllWindows()
