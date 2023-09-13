# Human-Falling-Detection
⚙️ Using YOLOv8n-pose ,OpenCV. Make own conditions by using keypoint from detection.

EASY TO CUSTOM KEYPOINTS CONDITIONS 🦾

How programs running 💾
1. Detects person ( 6 persons max)
2. Detect pose-persons
3. Check person-falling
4. Sent LINE message along with a picture
5. Records log to Exel
6. Auto-pilot managing .xlsx file
7. Weekend report via Gmail 

EXCEPTION!!⚠️
1. If a person is bending their body. falling case✔
2. If a person is too close to the camera. falling case✔

EXAMPLE ADAPTING 🔅
Use with PIR Sensor. every time there is a movement this detection would be running.
and put more conditions that if the detector finds persons do nothing with the same pose,
then it might be a falling case so the camera takes a photo and then sends it to LINE notify.
