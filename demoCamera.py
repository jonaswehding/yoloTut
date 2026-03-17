from matplotlib.pyplot import box
from ultralytics import YOLO


model = YOLO("yolov8n.pt")


while True:


    results = model(source=0, stream=True,show=True)  # Run YOLO on the current frame
    for result in results:
        pass
    

    for box in results.boxes:
        print(box.xyxy)  # x1, y1, x2, y2
        print(box.conf)  # confidence score
        print(box.cls)   # class index

 
