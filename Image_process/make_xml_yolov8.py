import xml.etree.cElementTree as eT
#from Image_process.same_line_xyxy import *
import sys
sys.path.append('Yolo')


def filename_xml(path):
    filename = path.split('/')[-1]
    filename = filename.split('.')[0] + '.jpg'
    return filename


def make_xml(directory, file, img, lst):
    root = eT.Element("annotation")
    folder = eT.SubElement(root, "folder")
    folder.text = 'yolo'
    filename = eT.SubElement(root, 'filename')
    filename.text = file
    path = eT.SubElement(root, "path")
    path.text = directory + file
    source = eT.SubElement(root, "source")
    database = eT.SubElement(source, 'database')
    database.text = 'unknown'
    size = eT.SubElement(root, 'size')
    width = eT.SubElement(size, 'width')
    width.text = str(img.shape[1])
    height = eT.SubElement(size, 'height')
    height.text = str(img.shape[0])
    depth = eT.SubElement(size, 'depth')
    depth.text = str(img.shape[2])
    segmented = eT.SubElement(root, 'segmented')
    segmented.text = 0
    for i in lst:
        objects = eT.SubElement(root, 'object')
        name = eT.SubElement(objects, 'name')
        name.text = 'text'
        pose = eT.SubElement(objects, 'pose')
        pose.text = "Unspecified"
        truncated = eT.SubElement(objects, 'truncated')
        truncated.text = str(0)
        difficult = eT.SubElement(objects, 'difficult')
        difficult.text = str(0)
        bndbox = eT.SubElement(objects, 'bndbox')
        xmin = eT.SubElement(bndbox, 'xmin')
        xmin.text = str(i[0])
        ymin = eT.SubElement(bndbox, 'ymin')
        ymin.text = str(i[1])
        xmax = eT.SubElement(bndbox, 'xmax')
        xmax.text = str(i[2])
        ymax = eT.SubElement(bndbox, 'ymax')
        ymax.text = str(i[3])
    tree = eT.ElementTree(root)
    file_xml = file.split('.')[0] + '.xml'
    tree.write(directory + file_xml)


def make_xml_sort(directory, file, img, lst_sort):
    root = eT.Element("annotation")
    folder = eT.SubElement(root, "folder")
    folder.text = 'yolo'
    filename = eT.SubElement(root, 'filename')
    filename.text = file
    path = eT.SubElement(root, "path")
    path.text = directory + file
    source = eT.SubElement(root, "source")
    database = eT.SubElement(source, 'database')
    database.text = 'unknown'
    size = eT.SubElement(root, 'size')
    width = eT.SubElement(size, 'width')
    width.text = str(img.shape[1])
    height = eT.SubElement(size, 'height')
    height.text = str(img.shape[0])
    depth = eT.SubElement(size, 'depth')
    depth.text = str(img.shape[2])
    segmented = eT.SubElement(root, 'segmented')
    segmented.text = 0
    for box in lst_sort: # for cac hang
        for box_box in box: # for cac box tren cung 1 hang
            objects = eT.SubElement(root, 'object')
            name = eT.SubElement(objects, 'name')
            name.text = 'text'
            pose = eT.SubElement(objects, 'pose')
            pose.text = "Unspecified"
            truncated = eT.SubElement(objects, 'truncated')
            truncated.text = str(0)
            difficult = eT.SubElement(objects, 'difficult')
            difficult.text = str(0)
            bndbox = eT.SubElement(objects, 'bndbox')
            xmin = eT.SubElement(bndbox, 'xmin')
            xmin.text = str(box_box[0])
            ymin = eT.SubElement(bndbox, 'ymin')
            ymin.text = str(box_box[1])
            xmax = eT.SubElement(bndbox, 'xmax')
            xmax.text = str(box_box[2])
            ymax = eT.SubElement(bndbox, 'ymax')
            ymax.text = str(box_box[3])
    tree = eT.ElementTree(root)
    file_xml = file.split('.')[0] + '.xml'
    tree.write(directory + file_xml)
if __name__ == "__main__":
    '''
    # make xml for yolov8
    folder_img = '/home/dungdinh/Downloads/train_test_split_2_delete/'
    pre = YOLOv8()
    for file_name in os.listdir(folder_img):
        file_name = os.path.join(folder_img, file_name)
        print(file_name)
        image = cv2.imread(file_name)
        box = pre.predict(image)
        print(box)
        print('-------------------------')
        make_xml(folder_img, filename_xml(file_name), image, box)'''


    # make xml for rectangle in same line
    '''
    folder_img = '/home/dungdinh/Downloads/train/test_draw_rectangle_xml/'
    list_link = [f for f in os.listdir(folder_img) if ".jpg" in f]
    for file_name in list_link:
        file_name_jpg = os.path.join(folder_img, file_name)
        file_name_xml = os.path.join(folder_img, file_name.split('.')[0] + '.xml')
        print(file_name)
        image = cv2.imread(file_name_jpg)
        tree = ET.parse(file_name_xml)
        root = tree.getroot()
        box_point_rec = process(root)
        print('-------------------------')
        make_xml(folder_img, filename_xml(file_name), image, box_point_rec)'''
    
    
    # sap xep box tu trai sang phai tu tren xuong duoi
    folder_img = '/home/dungdinh/Downloads/train/train_6_1k4/'
    file_link = [f for f in os.listdir(folder_img) if ".xml" in f]
    for file_name in file_link:
        tree = ET.parse(file_name)
        root = tree.getroot()
        file_name = os.path.join(folder_img, file_name)
        print(file_name)
        image = cv2.imread(file_name)
        sorted_box = sort_xy(root)
        print(sorted_box)
        print('-------------------------')
        make_xml(folder_img, filename_xml(file_name), image, sorted_box)
