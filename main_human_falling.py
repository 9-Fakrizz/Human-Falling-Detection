
import os
import cv2                          # This is the OpenCV library for image and video processing.
from ultralytics import YOLO        # This is a YOLO (You Only Look Once) object detection model from the Ultralytics library.
import numpy                        # This library provides support for multi-dimensional arrays and matrices.
import requests                     # This library is used to send HTTP requests in Python.
from pydantic import BaseModel      # This is a base class for creating models
import math
import pandas as pd
import datetime
import time
import pytz
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


desired_timezone = pytz.timezone('Asia/Bangkok')
current_time = datetime.datetime.now(desired_timezone)
excel_file = ("data_{}.xlsx".format(current_time.date()))

def send_email_with_attachment(xlsx_path):
    # Set up email parameters
    smtp_server = 'smtp.gmail.com'  # Replace with your email server
    smtp_port = 587  # Replace with the appropriate port number for your server

    subject = "Almshouse Project"
    body = "Hello, please find the attached .xlsx file."
    from_email = "forproject0858@gmail.com"
    from_password = "kdrkckkofjapeddm"
    to_email = "supakritgongkam@gmail.com"
    
    # Create the message container
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the file
    attachment = open(xlsx_path, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {xlsx_path}')
    msg.attach(part)

    # Add email body
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the email server and send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()


def endofday(current_time):
    return (current_time.hour == 23 and current_time.minute == 58) and current_time.weekday()==6

def remove_excel_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        print(f"Error: {e}")

def save_exel(message):

    data ={"Event":[message],"Date":[str(current_time.date())], "Time":[str(current_time.strftime("%H:%M:%S"))]}
    df = pd.DataFrame(data)
    excel_file = ("data_{}.xlsx".format(current_time.date()))

    if os.path.exists(excel_file):
    
        df_existing = pd.read_excel(excel_file,engine='openpyxl')
        df_appended = df_existing._append(df, ignore_index=True)
        df_appended.to_excel(excel_file, index=False, engine='openpyxl')

    
    else :
        writer = pd.ExcelWriter(excel_file, engine='openpyxl')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer._save()


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


width = 640
height = 480
compression_quality = 90


frame_time = 0   # use for count frames
frame_time2 = 1  # use for calculate the delta theta/frame2
delay_frame = 40 # you can custom delay here
delay_frame_stg = 3 # use for count stg frames
scale = []  #use for calculate the delta thetha
speed = 0

status = True
status_delay = 0
status_count = 0

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

while cap.isOpened():
    success, frame = cap.read()   
    frame = cv2.resize(frame, (width, height))  
    boxes=[]
    #annotations_frame = frame
    annotations_frame0 = frame
    jpeg_params = [cv2.IMWRITE_JPEG_QUALITY, compression_quality]
    _, compressed_frame = cv2.imencode('.jpg', annotations_frame0, jpeg_params)
    annotations_frame= cv2.imdecode(compressed_frame, cv2.IMREAD_COLOR)

    if success:                                              # if camera-read is successfully
        result = model(annotations_frame, save=True)                     # process frame with model
        annotations_frame = result[0].plot()                 # plot keypoints lines including rectangle around object

        for detection in result:                             # If there are persons in frame
            
            # x,y axis and width,height of object(person)
            boxes = detection.boxes.xywhn.cpu().numpy()
            # fetch amount of persons
            person = detection.boxes.shape                   
            person = int(person[0])
            if person > 2: person = 2                       # limit people to reduce error
            
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
                    left_ear_x, left_ear_y = result_keypoint[i][get_keypoint.LEFT_EAR]
                    right_ear_x, right_ear_y = result_keypoint[i][get_keypoint.RIGHT_EAR]
                    right_ankle_x, right_ankle_y = result_keypoint[i][get_keypoint.RIGHT_ANKLE]
                    left_ankle_x, left_ankle_y = result_keypoint[i][get_keypoint.LEFT_ANKLE]
                    
                    if status == True:
                        if frame_time2 % delay_frame_stg == 0  :
                            scale.clear()
                            frame_time2 = 1
                        else :
                            frame_time2 = frame_time2 +1
                        if left_hip_y and right_hip_y < 1 :
                            center_ear = [(left_ear_x+right_ear_x)/2 , (left_ear_y+right_ear_y)/2]
                            #center_shd = [(left_shd_x+right_shd_x)/2 , (left_shd_y+right_shd_y)/2]
                            center_hip = [(left_hip_x+right_hip_x)/2 , (left_hip_y+right_hip_y)/2]
                            center_ankle = [(left_ankle_x+right_ankle_x)/2 , (left_ankle_y+right_ankle_y)/2]
                            vector_l1 = [(center_ear[0] - center_hip[0]), (center_ear[1] - center_hip[1])]
                            vector_l2 =[1-center_hip[0],0 ]

                            dot_product = (vector_l1[0]*vector_l2[0])+(vector_l1[1]*vector_l2[1])
                            dot_product = round(dot_product,5)
                            
                            size_l1 = math.sqrt(pow( vector_l1[0], 2) + pow(vector_l1[1], 2) )
                            size_l2 = math.sqrt(pow( vector_l2[0], 2) + pow(vector_l2[1], 2) )
                            size_l1, size_l2 = round(size_l1,5) ,round(size_l2,5)

                            if (size_l1*size_l2) != 0 and abs(dot_product/abs(size_l1*size_l2)) <=1 :
                                angle = math.acos(dot_product/abs(size_l1*size_l2))
                                angle = math.degrees(angle)

                            ''''' 
                            vector_l3 = [(center_ear[0] - center_ankle[0]), (center_ear[1] - center_ankle[1])]
                            vector_l4 =[1-center_ankle[0],0 ]

                            size_l3 = math.sqrt(pow( vector_l3[0], 2) + pow(vector_l3[1], 2) )
                            size_l4 = math.sqrt(pow( vector_l4[0], 2) + pow(vector_l4[1], 2) )
                            size_l3, size_l4 = round(size_l3,5) ,round(size_l4,5)

                            if (size_l3*size_l4) != 0 and abs(dot_product/abs(size_l3*size_l4)) <= 1 :
                                fall_angle = math.acos(dot_product/abs(size_l3*size_l4))
                                fall_angle = math.degrees(fall_angle)'''


                            cv2.putText(annotations_frame, ("Angle[{}]: ".format(i+1)) , (340, 40*(i+1)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
                            cv2.putText(annotations_frame, str(round(angle,2)) , (480, 40*(i+1)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
                            cv2.putText(annotations_frame, (" STATUS: {} ".format(status)), (380, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

                        ####   thess code below are conditions ####
                        
                            scale.append(angle)   
                            speed = abs((scale[len(scale)-1]-scale[0])/frame_time2)
                            cv2.putText(annotations_frame, ("Speed[{}]: ".format(i+1)) , (40, 40*(i+1)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
                            cv2.putText(annotations_frame, str(round(speed,2)) , (200, 40*(i+1)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)


                              

                            if abs(right_hip_x - right_shd_x) > abs(right_hip_y - right_shd_y):
                                print("falling............")
                                cv2.putText(annotations_frame, " FALLING FOUND ", (20, 450), cv2.FONT_HERSHEY_PLAIN, 2, (218, 224, 159), 2)
                           
                                frame_time = frame_time +1
                                if frame_time % delay_frame == 0 and frame_time != 0 :
                                    print("Notificate to LINE  Successfully......")
                                    image_path = "falling_person.jpg"
                                    cv2.imwrite(image_path, annotations_frame)
                                
                                
                                    # Send Line notification with image
                                    message = "Falling"
                                    save_exel(message)
                                    send_line_notify(message, image_path)
                                    frame_time = 0
                                    status = False
                                
                            '''if fall_angle >= 130 or fall_angle <=50:
                            
                                frame_time = frame_time +1
                                if frame_time % delay_frame == 0 and frame_time != 0 :
                                    print("falling............")
                                    cv2.putText(annotations_frame, " FALLING FOUND ", (50, 450), cv2.FONT_HERSHEY_PLAIN, 2, (218, 224, 159), 2)
                                    print("Notificate to LINE  Successfully......")
                                    image_path = "falling_person.jpg"
                                    cv2.imwrite(image_path, annotations_frame)
                                    
                                    
                                    # Send Line notification with image
                                    message = "Falling "
                                    save_exel(message)
                                    send_line_notify(message, image_path)
                                    frame_time = 0
                                    status = False'''

                
                            if (speed >= 6):
                                print("staggered.............")
                                cv2.putText(annotations_frame, " STAGGERED ", (50, 450), cv2.FONT_HERSHEY_PLAIN, 2, (218, 224, 159), 2)
                                print("Notificate to LINE  Successfully......")
                                image_path = "staggered person.jpg"
                                cv2.imwrite(image_path, annotations_frame)
                                
                                message = "Staggered"
                                save_exel(message)
                                send_line_notify(message, image_path)
                                status = False

                    else :
                        status_delay = status_delay + 1
                        if status_delay == 80:
                            status = True
                            status_delay = 0
                            status_count = status_count +1

    if status_count == 4:
        xlsx_path = excel_file
        send_email_with_attachment(xlsx_path)
        status_count = 0

    current_time = datetime.datetime.now(desired_timezone)
    if endofday(current_time):
        xlsx_path = excel_file
        send_email_with_attachment(xlsx_path)
        remove_excel_file(excel_file)

    
    
    # Display frame.
    cv2.imshow("Assistant Camera", annotations_frame)

    # press "q" for stop this program
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
   

cap.release()
cv2.destroyAllWindows()
