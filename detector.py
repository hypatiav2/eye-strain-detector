from datetime import datetime
import numpy as np
import argparse,time
import cv2
import dlib

def euclidean_dist(ptA, ptB):
    # compute and return the euclidean distance between the two
    # points
    return np.linalg.norm(ptA - ptB)


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = euclidean_dist(eye[1], eye[5])
    B = euclidean_dist(eye[2], eye[4])
    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = euclidean_dist(eye[0], eye[3])
    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    # return the eye aspect ratio
    return ear

def crop_center(img,w,h) :
   w1,h1=img.shape[1],img.shape[0]
   y1,y2 = int(h1/2-h/2), int(h1/2+h/2) 
   x1,x2 = int(w1/2-w/2), int(w1/2+w/2)
   img = img[y1:y2, x1:x2]
   return img

class BlinkCounter() :
    
    def __init__(self, shape_predictor) :
        self.EAR_THRESHOLD = 0.3
        self.BLINK_THRESHOLD = 3
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(shape_predictor)
        
    def count(self,images) :
        possible_blink = 0
        blinks = 0
        start = time.time()
        for img in images : 
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray,0)
            # todo : what happens if we find more than 1 face? 
            if len(faces)  > 0 : 
                face = faces[0]
                # determine the facial landmarks for the face region 
                shape = self.predictor(gray, face)

                # loop over the (x, y)-coordinates for the facial landmarks
                # and draw them on the image
                if shape.num_parts == 68 : 
                    # right eye is 6 points from position 36
                    right_eye = np.zeros((6,2), dtype=int)
                    for i in range(len(right_eye)):
                        right_eye[i] = (shape.part(i+36).x, shape.part(i+36).y)

                    # right eye is 6 points from position 42
                    left_eye = np.zeros((6,2), dtype=int)
                    for i in range(len(left_eye)):
                        left_eye[i] = (shape.part(i+42).x, shape.part(i+42).y)

                    leftEAR = eye_aspect_ratio(left_eye)
                    rightEAR = eye_aspect_ratio(right_eye)
                    # average the eye aspect ratio together for both eyes
                    ear = (leftEAR + rightEAR) / 2.0

                    #for (x, y) in left_eye:
                    #cv2.circle(img, (x, y), 2, (0, 255, 0), -1)
                    possible_blink = possible_blink+1 if ear < self.EAR_THRESHOLD else 0
                    # if N successive low ear, count as a real blink
                    if possible_blink > self.BLINK_THRESHOLD: possible_blink=0;blinks += 1

        end = time.time()
        return blinks,(end-start)


FPS = 20
MONITOR_TIME = 10

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920) # set Width
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1080) # set Height
cap.set(cv2.CAP_PROP_FPS, FPS) # fps

blink_counter = BlinkCounter("./shape_predictor_68_face_landmarks.dat")

ret=True
while(ret==True) :
    
    images = []
    blinks = 0

    start = time.time()
    for i in range(FPS * MONITOR_TIME) : 
        ret, img = cap.read()
        images.append(crop_center(img, 640, 480))
        print(".",end="",flush=True)
    
    blinks = blink_counter.count(images)[0]
    
    print("")
    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),blinks,time.time()-start)
    
    
    #cv2.imshow('frame', img)


    k = cv2.waitKey(1) & 0xFF 
    if k == ord('q') or k == 27 : # ESC or q to quit 
        break;
else:
    print("Video Capture Failed")

cap.release()
cv2.destroyAllWindows()

