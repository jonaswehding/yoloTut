
# YOLO - Træning

## Indsamling og forberedelse af data til objekt detektering

Indsamle data/billeder og annoter dem i Yolo Label Imager (GIT)
Lav et ny python project i Pycharm eller VS Code eller et andet sted:)
pip install "ultralytics" python modul til træning of inferens
pip install "pillow" python modul. Skal bruges til Yolo Image Labeller

Når man forbereder data til træning, skal man have billeder og labels til både at træne, "train" og
validere hvor godt modellen klarer opgave "val"
En tommelfinger regel er 80/20 ,altså 80 procent af billederne skal i train mappen og 20% skal i val mappen.

    
### Mappestruktur:
```
Woking directory
    ├── datasets
    |	   ├── train
    |	   |     ├── images
    |	   |     └── labels
    |	   ├── val
    |	         ├── images
    |	         └── labels
    |	   
    |	        
    |	        
    |	   
    └── data.yaml
```


```
Woking directory
    ├── datasets
    |	   ├── images
    |	   |     ├── train
    |	   |     └── val
    |	   ├── labels
    |	         ├── train
    |	         └── val
    |	   
    |	        
    |	        
    |	   
    └── data.yaml
```

Rediger '.yaml' fil med de rigtige stier og klasseangivelser
    f.eks. mitDataset.yaml
    Denne fil er en tekst fil der infdeholder information om hvor dine billeder og labels er på disken, og hvad klasserne hedder.
    Train indeholder de data der skal trænes på. Images er billederne: eks. mitBillede1.jpg. labels er tekst filer med klasse nummer og koordinater på objekter der skal genkendes.

### YAML fil eksempel
```
path: ../datasets/mydataset  # dataset root dir. 
train: train  # train images (relative to 'path') 128 images
val: val  # val images (relative to 'path') 128 images
test:  # test images (optional)

names: #klasser
  0: apple
  1: cherry
```
## Træning
from ultralytics import YOLO

eller

Du kan træne din model i Google Colab (jupyter).
Se i mappen Colab i denne git for at finde en ipynb fil der kan åbnes i google colab.
Fordelen ved Google Colab er at du kan få adgang til en T4 Tesla GPU, så træning er meget hurtigere.

### Load en pretrænet yolyo 11 model (giver bedre træning)
model = YOLO('yolov11n.pt')  

Du kan vælge mellem forskelllige størrelser af modeller. Jo større, jo bedre resultat, men det tager længere tid at træne og lave inference.
Modellerne er: 
yolov11n.pt - nano
yolov11n.pt - small
yoloy11m.pt - medium
yolov11l.pt - large
yolov11x.pt - extra large

### Træn modellen  - 
model.train(data='datasets/frugt.yaml', epochs=1000, imgsz=640)

#evaluer model
metrics = model.val()

## Inferens - test modellen
from ultralytics import YOLO

#her loader i den model i har trænet, som ligger i weights. best.pt er den mode der har mindst loss (den bedste)
model = YOLO(r'absolute path to project\runs\detect\train\weights\best.pt') # load trained fruit model

#nu udfører du inferens på modellen, altså gir den et billede den aldrig har set før.
results = model('path to test image/test.jpg',show = True)

while True:
    pass
