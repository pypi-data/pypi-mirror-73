import cv2
import numpy as np
import time
import warnings
import numpy as np
import argparse
import time
import cv2
import os
import os
from pathlib import Path
import requests
from pped import PPE 

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == "__main__":
    file_id = 'TAKE ID FROM SHAREABLE LINK'
    destination = 'DESTINATION FILE ON YOUR DISK'
    download_file_from_google_drive(file_id, destination)
    
    
home = str(Path.home())

output1 = home+'\\'+'yolov3-tiny_obj_train_2000.weights'
output2 = home+'\\'+'yolov3-tiny_obj_test.cfg'
output3 = home+'\\'+'obj.names'

if os.path.isfile(home+'\\'+'yolov3-tiny_obj_train_2000.weights') != True:
    print("Model weights are downloading......") 
    file_id1 = '1hSTMFzD99yH05yeeT1UNA-4TnnWm27Zq'
    download_file_from_google_drive(file_id1, output1)
    Weights=output1
else:
    Weights=output1
    
if os.path.isfile(home+'\\'+'yolov3-tiny_obj_test.cfg') != True:
    print("Model configuration are downloading......") 
    file_id2 = '15AyVE4TJ_OR7Qg6rkLKtvpv-G98pNT_i'
    download_file_from_google_drive(file_id2, output2)
    CFG=output2
else:
    CFG=output2
if os.path.isfile(home+'\\'+'obj.names') != True:
    print("Model classes are downloading......") 
    file_id3 = '1qDzYm7zMpyK-9fS1ORH1OFPk6kgnzghQ'
    download_file_from_google_drive(file_id3, output3)
    label_dir=output3
else:
    label_dir=output3    
    
warnings.filterwarnings("ignore")
confthres=0.2
nmsthres=0.1
path="./"
def get_labels(label_dir):
    return open(label_dir).read().split('\n')
      
def get_colors(LABELS):
    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")
    return COLORS

def get_weights(weights_path):
    # derive the paths to the YOLO weights and model configuration
    weightsPath = os.path.sep.join([yolo_path, weights_path])
    return weightsPath

def get_config(config_path):
    configPath = os.path.sep.join([yolo_path, config_path])
    return configPath

def load_model(configpath,weightspath):
    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net

Lables=get_labels(label_dir) 


def get_predection(image,net,LABELS,COLORS):
    imS = cv2.resize(image, (650, 700))
    (H, W) = imS.shape[:2]

    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(imS, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    
    layerOutputs = net.forward(ln)
    #print(layerOutputs[0])
    

    # show timing information on YOLO
    #print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []
    num_class_0 = 0
    num_class_1 = 0

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            #print(detection)
            classID = np.argmax(scores)
            # print(classID)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > confthres:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
                if(classID==0):
                  num_class_0 +=1
                elif(classID==1):
                  num_class_1 +=1  

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confthres,
                            nmsthres)
    if(num_class_0>0 or num_class_1>0):
        index= num_class_0/(num_class_0+num_class_1)
    else:
      index=-1  
    #print(index,)    
    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            confidence = confidences[i]

            # draw a bounding box rectangle and label on the image
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(imS, (x, y), (x + w, y + h), color, 1)
            text = "{}".format(LABELS[classIDs[i]])
            
            cont_coordinates1 = np.array( [
									(x, y+h)
									, (x+int(w/10), y+h)
									, (x, y+int(h*.90))
								] )
            cont_coordinates = np.array( [
									(x, y)
									, (x+int(w/10), y)
									, (x, y+int(h/10))
								] )
            cont_coordinates2 = np.array( [
									(x+w, y)
									, (x+int(w*0.90), y)
									, (x+w, y+int(h/10))
								] )
            cont_coordinates3 = np.array( [
									(x+w, y+h)
									, (x+int(w*0.90), y+h)
									, (x+w, y+int(h*0.90))
								] )
            cv2.drawContours(imS, [cont_coordinates], 0, (0, 230, 255), -1)
            cv2.drawContours(imS, [cont_coordinates1], 0, (0, 230, 255), -1)
            cv2.drawContours(imS, [cont_coordinates2], 0, (0, 230, 255), -1)
            cv2.drawContours(imS, [cont_coordinates3], 0, (0, 230, 255), -1)
            #print(boxes)
            #print(classIDs)      
            #cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color=(69, 60, 90), thickness=2)
            cv2.rectangle(imS, (x, y-5), (x+w, y-15), color, cv2.FILLED)
           # cv2.putText(imS, text + " Confidence: " + str(round(confidence, 2)), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,0), 1)
            cv2.putText(imS, text , (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.50, (0,0,0), 1)
          #  cv2.putText(imS,'Total PPE: '+str(round(num_class_0, 2)),(40,40),cv2.FONT_HERSHEY_COMPLEX,1, (42,155,155), 1)
            #cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, color, 3)
        if(index>=0 and index<.25):
            cv2.rectangle(imS, (10, 0), (100, 15), (255,255,255), cv2.FILLED)
            cv2.putText(imS,'Adaptivity',(10,15),cv2.FONT_HERSHEY_DUPLEX,0.60, (0, 0, 0), 1)
            cv2.circle(imS, (40, 46), 30, (0,0,255), -1)
            cv2.putText(imS,'POOR',(15,50),cv2.FONT_HERSHEY_DUPLEX,0.60, (0,255,255), 1)
        else:
            cv2.rectangle(imS, (10, 0), (100, 15), (255,255,255), cv2.FILLED)
            cv2.putText(imS,'Adaptivity',(10,15),cv2.FONT_HERSHEY_DUPLEX,0.60, (0, 0, 0), 1)
            cv2.circle(imS, (40, 46), 30, (42,236,42), -1)
            cv2.putText(imS,'HIGH',(15,50),cv2.FONT_HERSHEY_DUPLEX,0.60, (0,0,0), 1)
        
    return imS



# Method to predict  Image
def change_res(stream, width, height):
    stream.set(3, width)
    stream.set(4, height)    
 
# This will not work  in colab, as colab can't access local hardware
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

    
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

import time
from IPython.display import Image
def predict_web_cam():
    stream = cv2.VideoCapture(0)
    nets=load_model(CFG,Weights)
    Colors=[(42,236,42),(0,0,255)]
    height, width = None, None
    writer = None
    #sess = K.get_session()
  
#    out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 25, get_dims(stream,'720p'))
    while True:
        # Capture frame-by-frame
        grabbed, frame = stream.read()
        if not grabbed:
            break
        if width is None or height is None:
                        
	        height, width = frame.shape[:2]
        frame=get_predection(frame,nets,Lables,Colors)
        # Run detection
        if writer is None:
            
           fourcc = cv2.VideoWriter_fourcc(*"mp4v")
           writer = cv2.VideoWriter('output.avi', fourcc, 10,(frame.shape[1], frame.shape[0]), True)
        writer.write(frame)
      #  image = Image.fromarray(frame)
     
        
      
        
        cv2.imshow('Web Cam',np.asarray(frame))
      
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            
            break
            
       
    stream.release() 
    writer.release()
    cv2.destroyAllWindows()
    

   

predict_web_cam()    