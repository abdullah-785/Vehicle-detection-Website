# from datetime import datetime
from urllib import request
from django.shortcuts import render
from django.http import StreamingHttpResponse
# from webcam.models import Detection
import yolov5,torch
# from yolov5.utils.general import scale_coords
from yolov5.utils.general import (check_img_size, non_max_suppression, 
                                  check_imshow, xyxy2xywh, increment_path)
from yolov5.utils.torch_utils import select_device, time_sync
from yolov5.utils.plots import Annotator, colors
from deep_sort.utils.parser import get_config
from deep_sort.deep_sort import DeepSort
import cv2
from PIL import Image as im
import pyrebase
import datetime
from django.contrib import auth

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


firebaseConfig = {
    'apiKey': "AIzaSyBBU5WLvfTLczxeCtlCxuGrpIK0UKK5Pig",
    'authDomain': "automatedvehicledetection.firebaseapp.com",
    'databaseURL': "https://automatedvehicledetection-default-rtdb.firebaseio.com",
    'projectId': "automatedvehicledetection",
    'storageBucket': "automatedvehicledetection.appspot.com",
    'messagingSenderId': "446921544901",
    'appId': "1:446921544901:web:90eb3bfe0274096f2e8cac",
    'measurementId': "G-HFXP97QT4B"
}
  
firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()

db = firebase.database()
storage = firebase.storage()

# Create your views here.

def detectionFunc(request):
    return render(request,'detection.html')


print(torch.cuda.is_available())
print("Start model loading")
#load model
model = yolov5.load('Yolov5_DeepSort_Pytorch/yolov5n.pt')
# model = torch.hub.load('ultralytics/yolov5', 'yolov5n')
device = select_device('') # 0 for gpu, '' for cpu
# initialize deepsort
cfg = get_config()
cfg.merge_from_file("Yolov5_DeepSort_Pytorch/deep_sort/configs/deep_sort.yaml")
deepsort = DeepSort('osnet_x0_25',
                    device,
                    max_dist=cfg.DEEPSORT.MAX_DIST,
                    max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                    max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                    )
# Get names and colors
names = model.module.names if hasattr(model, 'module') else model.names

def stream():
    # "Yolov5_DeepSort_Pytorch/videos/Traffic.mp4"
    # "videos/Traffic.mp4"
    cap = cv2.VideoCapture(0) 
    model.conf = 0.45
    model.iou = 0.5
    model.classes = [0,1,2,3,5,7]
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: failed to capture image")
            break

        results = model(frame, augment=True)
        # proccess
        annotator = Annotator(frame, line_width=2, pil=not ascii) 
        det = results.pred[0]
        if det is not None and len(det):   
            xywhs = xyxy2xywh(det[:, 0:4])
            confs = det[:, 4]
            clss = det[:, 5]
            outputs = deepsort.update(xywhs.cpu(), confs.cpu(), clss.cpu(), frame)
            if len(outputs) > 0:
                for j, (output, conf) in enumerate(zip(outputs, confs)):

                    bboxes = output[0:4]
                    id = output[4]
                    cls = output[5]

                    c = int(cls)  # integer class
                    label = f'{names[c]} {conf:.2f} {id}'
                    annotator.box_label(bboxes, label, color=colors(c, True)),
                    print(f"{id} {names[c]} {conf:.2f}")
                    

                    # for i in annotator.result():
                    #     data = im.fromarray(i)
                    #     data.save("demo1.jpg")
                    # cv2.imwrite('demo1.jpg', frame)


                    if f'{names[c]}' == 'person' and f'{conf:.2f}' >= '0.50':
                        # for storing the record
                        for i in annotator.result():
                            data = im.fromarray(i)
                            data.save("demo1.jpg")
                        cv2.imwrite('demo1.jpg', frame)
                        # file = cv2.imwrite('demo1.jpg', frame)

                        # data and time picking
                        date = datetime.datetime.now()
                        date_string = date.strftime('%Y-%m-%d %H:%M:%S')

                        # for sending image on storage 
                        image = storage.child('detectionResults').child(date_string).put('demo1.jpg')
                        # print(image)
                        
                        current_user_uid = db.child('currentUser').shallow().get().val()

                        # send data on firebase 
                        firebaseData = {'detection': f'{id} {names[c]} {conf:.2f}', 'counting': f'{id}', 'names': f'{names[c]}', 'percentage': f'{conf:.2f}', 'image': 'https://images.unsplash.com/photo-1596605872817-7615f7ea2aac?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8Zmxvd2VycyUyMG5hdHVyZXxlbnwwfHwwfHw%3D&w=1000&q=80'}
                        db.child("notification").child(date_string).set(firebaseData)
                        db.child("userDetectionRecord").child(current_user_uid).child(date_string).set(firebaseData)

        else:
            deepsort.increment_ages()

        im0 = annotator.result()    
        image_bytes = cv2.imencode('.jpg', im0)[1].tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')  

def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')    
