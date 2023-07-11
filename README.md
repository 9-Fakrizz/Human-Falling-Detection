# Human-Falling-Detection
Using YOLOv8n-pose ,OpenCV. Make own conditions by using keypoint from detection.

How programs running
1. detect person (more than 1 person, max 6 persons)
2. detect pose-persons
3. check person-falling
4. sent LINE message along with a picture

EXCEPTION!!
1. if a person is bending their body. falling case✔
2. if a person is too close to the camera. falling case✔

EXAMPLE ADAPTING
Use with PIR Sensor. every time there is a movement this detection would be running.
and put more conditions that if the detector found persons do nothing with the same pose,
then it might be a falling case so the camera take a photo and then sent to LINE notify.
