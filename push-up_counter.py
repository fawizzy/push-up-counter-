import cv2
import mediapipe as mp
import math


mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False,
                        min_detection_confidence=0.7,
                         min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

count = 0
direction = 0
form = 0

def findAngle(lmList, p1, p2, p3):
       #Get the landmarks
       x1, y1 = lmList[p1]
       x2, y2 = lmList[p2]
       x3, y3 = lmList[p3]
      
       #Calculate Angle
       angle = math.degrees(math.atan2(y3-y2, x3-x2) -
                            math.atan2(y1-y2, x1-x2))
       if angle < 0:
           angle += 360
           if angle > 180:
               angle = 360 - angle
       elif angle > 180:
           angle = 360 - angle
       return angle


cap = cv2.VideoCapture(0)
while cap.isOpened():
   # read frame
   _, frame = cap.read()
   try:
        # resize the frame for portrait video
        # frame = cv2.resize(frame, (350, 600))
        # convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
       
        # process the frame for pose detection
        pose_results = pose.process(frame_rgb)
        landmarks_list = []


        if pose_results.pose_landmarks:
            for landmark in pose_results.pose_landmarks.landmark:
               landmarks_list.append([landmark.x, landmark.y])
            print(landmarks_list)

        if landmarks_list != []:    
            #get angles at the key joints
            elbow_angle = findAngle(landmarks_list, 12, 14, 16)
            shoulder_angle = findAngle(landmarks_list, 14, 12, 24)
            hip_angle = findAngle(landmarks_list, 12, 24, 26)
        
            
            #Check to ensure right form before starting the program
            if elbow_angle > 160 and shoulder_angle > 40 and hip_angle > 160:
                form = 1

            
            # Check for the full range of motion for the push-up
            if form == 1:
                if elbow_angle <= 90: # and hip_angle > 160:
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1
        
            if elbow_angle > 160 and shoulder_angle > 40:# and hip_angle > 160:
                feedback = "Down"
                if direction == 1:
                    count += 0.5
                    direction = 0
            
            # draw skeleton on the frame
            mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            # display the frame
        cv2.rectangle(frame, (0, 380), (100, 480), (0, 0, 0), cv2.FILLED)
        cv2.putText(frame, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)
        cv2.imshow('Output', frame)
   except:
        break
  
   if cv2.waitKey(1) == ord('q'):
         break

          
cap.release()
cv2.destroyAllWindows()