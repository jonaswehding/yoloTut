

# Sådan træner du din drage

## Indsamling og forberedelse af data

Indsamle data/billeder og annoter dem i LABELIMG
Lav et ny python project i Pycharm.
Installer "ultralytics" python modul.
I terminalen: kør labelimg

Rediger '.yaml' fil med de rigtige stier og klasseangivelser
    f.eks. mitDataset.yaml
    Denne fil er en tekst fil der infdeholder information om hvor dine billeder og labels er på disken, og hvad klasserne hedder.
    Train indeholder de data der skal trænes på. Images er billederne: eks. mitBillede1.jpg. labels er tekst filer med klasse nummer og koordinater på objekter der        skal genkendes.

    
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

path: ../datasets/mydataset  # dataset root dir. 
train: images/train  # train images (relative to 'path') 128 images
val: images/val  # val images (relative to 'path') 128 images
test:  # test images (optional)

## Klasser
names:
  0: apple
  1: cherry


## Træning
from ultralytics import YOLO

eller

Du kan træne din model i Google Colab (jupyter).
Se i mappen Colab i denne git for at finde en ipynb fil der kan åbnes i google colab.
Fordelen ved Google Colab er at du kan få adgang til en T4 Tesla GPU, så træning er meget hurtigere.

### Load en pretrænet model (giver bedre træning)
model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)

Du kan vælge mellem forskelllige størrelser af modeller. Jo større, jo bedre resultat, men det tager længere tid at træne og lave inference.
Modellerne er: 
yolov8n.pt - nano
yolov8s.pt - small
yoloy8m.pt - medium
yolov8l.pt - large
yolov8x.pt - extra large

### Træn modellen med GPU
model.train(data='datasets/frugt.yaml', epochs=1000, imgsz=640, device=0)


## Inferens - test modellen
from ultralytics import YOLO

model = YOLO(r'C:\Users\jweh\PycharmProjects\yolo_project\runs\detect\train\weights\best.pt') # load trained fruit model
results = model('testimage2.jpg',show = True)
while True:
    pass
