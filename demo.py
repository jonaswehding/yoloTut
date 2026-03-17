from ultralytics import YOLO

model = YOLO("yolov8n.pt")
results = model("image.jpg", show=True)
# result indeholder information om de detekterede objekter i billedet, 
# såsom deres position, klasse og confidence score.


#for at finde koordinatet for den første detekterede boks i formatet x1, y1, x2, y2:
print(results[0].boxes[0].xyxy) # x1, y1, x2, y2 for box 0
print(results[0].boxes[0].conf)  # confidence score for box 0
print(results[0].boxes[0].cls)   # class index for box 0
print(results[0].boxes[0].xywhn)  # class names


#for at gå igennem alle detekterede bokse og udskrive deres koordinater, confidence score og klasseindeks:
for box in results[0].boxes:
    print(box.xyxy)  # x1, y1, x2, y2
    print(box.conf)  # confidence score
    print(box.cls)   # class index


# Et eksmpel på at filtrere detekterede objekter baseret på deres klasse, for eksempel for kun at få personer:
listOfPersons = [box for box in results[0].boxes if box.cls == 0]  # Assuming class index 0 represents persons
print(f"Number of persons detected: {len(listOfPersons)}")


print(results[0].names)  # class names



# Hvad hvis vi skal detektere om der er et objekt i en bestemt del af billedet? 
# For eksempel, hvis vi kun er interesserede i objekter i den øverste venstre 
# kvadrant af billedet?
# 

if results[0].boxes[0].xywhn[0] < 0.5 and results[0].boxes[0].xywhn[1] < 0.5:
    print("Object is in the upper left quadrant of the image.")


