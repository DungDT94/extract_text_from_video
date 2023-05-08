from ultralytics import YOLO
import numpy as np
import cv2


class YOLOv8:
    def __init__(self):
        self.model = YOLO("best.pt")

    def predict(self, img):
        result = self.model(source=img, show=False)
        boxes = result[0].boxes
        list_box = []
        for box in boxes:
            temp_list = []
            box2list = box.xyxy.tolist()
            box2list = np.reshape(box2list, (4,))
            box2list = box2list.tolist()
            list_box.append(box2list)
        return list_box


if __name__ == "__main__":
    #model = YOLOv8()
    #image = cv2.imread('/home/dungdinh/Downloads/train_split_test_1_delete/4cb18a1a-9533-44ae-a950-a6a488f4aa40.jpg')
    #lst = model.predict('/home/dungdinh/Downloads/train_split_test_1_delete/4cb18a1a-9533-44ae-a950-a6a488f4aa40.jpg')
    #print(lst)
