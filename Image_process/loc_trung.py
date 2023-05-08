#from Image_process.same_line_xyxy import *
from Yolo.yolov8_model import *
from Image_process.verified_iou import *
from Image_process.make_xml_yolov8 import *


def y_coordinate(lst_all):
    lst_y = []
    for box in lst_all:
        lst_temp = [box[1], box[3]]
        lst_y.append(lst_temp)
    return lst_y


def check_iou_y(lst_all, lst_y):
    lst_box = []
    lst_box_index = []
    for i in range(len(lst_all)):
        lst_temp = []
        index = []
        for j in range(len(lst_all)):
            ymin = max(float(lst_all[i][1]), float(lst_all[j][1]))
            ymax = min(float(lst_all[i][3]), float(lst_all[j][3]))
            minus = min(float(lst_all[i][3]) - float(lst_all[i][1]), float(lst_all[j][3]) - float(lst_all[j][1]))
            iou = (ymax - ymin) / minus
            if iou > 0.85:
                lst_temp.append(lst_y[j])
                index.append(j)
        lst_box.append(lst_temp)
        lst_box_index.append(index)
    return lst_box, lst_box_index


def delete(lst_box_index):
    box_index, s = [], set()
    for t in lst_box_index:
        w = tuple(sorted(t))
        if not w in s:
            box_index.append(t)
            s.add(w)
    return box_index


def box_same_line(box_index, lst_all):
    box_point = []
    for i in box_index:
        box_point_temp = []
        for j in i:
            box_point_temp.append(lst_all[j])
        box_point.append(box_point_temp)
    return box_point


# tra ve list gom cac box cung 1 line
def process_box_same_line(lst_all):
    lst_y = y_coordinate(lst_all)
    lst_box, lst_box_index = check_iou_y(lst_all, lst_y)
    box_index = delete(lst_box_index)
    box_point = box_same_line(box_index, lst_all)
    return box_point


def sort_box_process_x_axis(lst_all):
    lst_y = y_coordinate(lst_all)
    lst_box, lst_box_index = check_iou_y(lst_all, lst_y)
    box_index = delete(lst_box_index)
    box_point = box_same_line(box_index, lst_all)
    box_point_sort = []
    for sub_lst in box_point:
        # print('sub_lst', sub_lst)
        # print('sub list not sort', sub_lst)
        sub_lst.sort(key=lambda x: x[0])
        # print(sub_lst[0][0])
        # print('sub list sort', sub_lst)
        box_point_sort.append(sub_lst)
    return box_point_sort


def sort_box_precess_y_axis(box_point_sort_x):
    box_ymin_line = []  # toa do y min tung hang theo thu tu ban dau
    box_point_sort_y = []
    for box_line in box_point_sort_x:  # xet tung hang trong list
        box_temp = []
        for box in box_line:  # xet tung box trong tung hang
            box_temp.append(box[1])  # lay ra toa do ymin tung box
        box_ymin_line.append(min(box_temp))  # lay ra toa do ymin tung hang
    box_ymin_line_sort = sorted(box_ymin_line)  # sap xep box ymin theo thu tu tang dan
    for ymin in box_ymin_line_sort:
        index = box_ymin_line.index(ymin)
        box_point_sort_y.append(box_point_sort_x[index])
    return box_point_sort_y


def sort_xy(lst_all):
    box_point_sort_x = sort_box_process_x_axis(lst_all)
    box_point_sort_xy = sort_box_precess_y_axis(box_point_sort_x)
    return box_point_sort_xy


def crop_image_predict(box_point_sort_xy, frame):
    for box_line in box_point_sort_xy:
        # print('box_same_line', box)
        for box in box_line:
            # print('box', box)
            img_crop = frame[box[1]:box[3], box[0]:box[2]]
            img_gray = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)

'''
def loc_trung(frameA_lst, frameB_lst):
    lst_A = sort_xy(frameA_lst)  # truyền vào root từ file xml cua frame
    lst_B = sort_xy(frameB_lst)
    # print('lst_frame_0_sort ', lst_A)
    # print('lst_frame_1_sort', lst_B)
    if len(lst_A) != len(lst_B):  # neu do dai cac hang trong frame A va B khac khau thi Frame A va B khac nhau
        return False  # False la khong trung
    else:
        for i in range(len(lst_A)):
            if len(lst_A[i]) != len(lst_B[
                                        i]):  # so sanh so luong box trong cung tung hang cua frame A va B, neu khac nhau thi Frame A va B khac nhau
                return False
            else:  # neu bang nhau thi tiep tuc tinh iou cua tung box voi 2 frame A va B
                for j in range(len(lst_A[i])):  # so sanh tung box trong 1 hang cua frame A va B
                    iou = calculate_iou(lst_A[i][j], lst_B[i][j])
                    # print('iou', iou)
                    if iou > 0.80:
                        continue
                    else:
                        return False

'''
def loc_trung(frameA_lst, frameB_lst):
    lst_A = sort_xy(frameA_lst)  # truyền vào root từ file xml cua frame
    lst_B = sort_xy(frameB_lst)
    #print('lst_frame_0_sort ', lst_A)
    #print('lst_frame_1_sort', lst_B)
    iou = 0
    count = 0
    for i in range(len(frameA_lst)):
        for j in range(len(frameB_lst)):
            iou_temp = calculate_iou(frameA_lst[i], frameB_lst[j])
            iou += iou_temp
            if iou_temp > 0:
                count += 1
    if count != 0:
        print('count', count)

        iou_ave = iou/count
        #print('iou_ave', iou_ave)
        if iou_ave > 0.94:
            return True
        else:
            return False
    else:
        return True


if __name__ == "__main__":
    '''
    model = YOLOv8()
    lst_all = model.predict(
        '/home/dungdinh/Downloads/train_split_test_1_delete/4cfb4b54-791c-4607-944e-137658586af6.jpg')
    print(lst_all)
    lst_sort = sort_box_process_x_axis(lst_all)
    # lst = model.predict('/home/dungdinh/Downloads/train_split_test_1_delete/4cb18a1a-9533-44ae-a950-a6a488f4aa40.jpg')
    print(lst_sort)'''

