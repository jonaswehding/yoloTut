

# Sådan træner du din drage

## Indsamling og forberedelse af data

Indsaml billeder og annoter dem.
Rediger '.yaml' fil med de rigtige stier og klasseangivelser
Brug labelimg til at annotere billeder
kør labelimg i terminal i Pycharm

### Mappestruktur:
```
Woking directory
    ├── datasets
    |	   ├── train
    |	   |     ├── images
    |	   |     └── labels
    |	   ├── test
    |	   |     ├── images
    |	   |     └── labels
    |	   ├── valid
    |	   |     ├── images
    |	   |     └── labels
    |	   └── data.yaml
    └── data.yaml
```
### YAML fil
#Train/val/test sets as:
#1) dir: path/to/imgs,
#2) file: path/to/imgs.txt, or 
#3) list: [path/to/imgs1, path/to/imgs2, ..]

path: ../datasets/mydataset  # dataset root dir
train: images/train  # train images (relative to 'path') 128 images
val: images/val  # val images (relative to 'path') 128 images
test:  # test images (optional)

## Klasser
names:
  0: apple
  1: cherry




## Træning
from ultralytics import YOLO

### Load en model (giver bedre træning)
model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)

### Træn modellen med GPU
model.train(data='datasets/frugt.yaml', epochs=1000, imgsz=640, device=0)


## Inferens - test modellen
from ultralytics import YOLO

model = YOLO(r'C:\Users\jweh\PycharmProjects\yolo_project\runs\detect\train\weights\best.pt') # load trained fruit model
results = model('testimage2.jpg',show = True)
while True:
    pass
