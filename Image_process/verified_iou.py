import xml.etree.cElementTree as ET
import os


def calculate_iou(boxA, boxB):
    x_min = max(int(boxA[0]), int(boxB[0]))
    y_min = max(int(boxA[1]), int(boxB[1]))
    x_max = min(int(boxA[2]), int(boxB[2]))
    y_max = min(int(boxA[3]), int(boxB[3]))
    intersection_area = max((x_max - x_min), 0)*max((y_max - y_min), 0)
    boxA_area = (int(boxA[2]) - int(boxA[0])) * (int(boxA[3]) - int(boxA[1]))
    boxB_area = (int(boxB[2]) - int(boxB[0])) * (int(boxB[3]) - int(boxB[1]))
    area_union = boxA_area + boxB_area - intersection_area
    iou = intersection_area / area_union
    return iou


def box_coordinate(root):
    lst_all = []
    for bndbox in root.iter('bndbox'):
        temp_lst = []
        for i in range(4):
            temp_lst.append(bndbox[i].text)
        lst_all.append(temp_lst)
    return lst_all


if __name__ == "__main__":
    '''
    folder = '/home/dungdinh/yolo_v5/datasets/box/xml'
    list_link = [f for f in os.listdir(folder) if ".xml" in f]
    for file in list_link:
        xml_path = os.path.join(folder, file)
        print(xml_path)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        box_result = box_coordinate(root)
        for i in range(len(box_result)):
            index = []
            for j in range(len(box_result)):
                if i == j:
                    continue
                else:
                    if 0.1 < calculate_iou(box_result[i], box_result[j]):
                        index.append(j)
            if len(index) == 0:
                continue
            else:
                print('box %i trung voi box thu:' % i, index)'''


    lst_a = [10, 10, 20, 20]
    lst_b = [15, 15, 30, 30]
    print(calculate_iou(lst_a, lst_b))









