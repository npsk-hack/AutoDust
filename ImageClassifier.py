import numpy as np
import cv2
import time
import os

class ObjectDetection:
    def __init__(self, folder='classifiers', confidence=50): # Start the classifier 
        self.dir = folder
        self.confidence = float(confidence)/100
        self.threshold = 0.3
        self.LABELS = open(self.dir+'\\coco.names').read().strip().split("\n")
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),dtype="uint8")
        weightsPath = os.path.sep.join([self.dir, "yolov3.weights"])
        configPath = os.path.sep.join([self.dir, "yolov3.cfg"])
        self.net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

    def load(self, img=r'images\img.jpg'): # Convert to format for classification
        image = cv2.imread(img)
        return image

    def save(self, image_data, file=r'images\clf.jpg'): # Save as .jpg file format
        cv2.imwrite(file, image_data)

    def classify(self, img_data): # Attempts to classify objects in the image
        image = img_data
        (H, W) = image.shape[:2]
        ln = self.net.getLayerNames()
        ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        layerOutputs = self.net.forward(ln)
        boxes = []
        confidences = []
        classIDs = []
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if confidence > self.confidence:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence, self.threshold)
        data = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                color = [int(c) for c in self.COLORS[classIDs[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.LABELS[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 5)
                name = text.split(":")[0]
                accuracy = eval(text.split(":")[1])
                data.append((name,accuracy))
        self.save(image)
        res = {"image_data":image,
               "detections":data}
        return res
