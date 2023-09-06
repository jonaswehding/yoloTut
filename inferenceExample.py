from ultralytics import YOLO


model = YOLO(r'C:\Users\jweh\PycharmProjects\yolo_project\runs\detect\train\weights\best.pt') # load trained fruit model

results = model('testimage2.jpg',show = True)

while True:
    pass