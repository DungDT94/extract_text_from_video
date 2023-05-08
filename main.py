from Image_process.loc_trung import *
from Yolo.yolov8_model import *
from CRNN.load_model_crnn import *
from PIL import Image
from Image_process.convert import *


class ExtractMutex:
    def __init__(self):
        self.modelYolo = YOLOv8()
        self.modelCrnn = ModelCrnn()

    def extractFrame(self, lst_frame_sort, frame):
        lst_frame_temp = []
        for box_line in lst_frame_sort:
            lst_line_temp = []
            # print('box_same_line', box)
            # print("\n")
            for box in box_line:
                # print('box', box)
                img_crop = frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                img_gray = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
                im_pil = Image.fromarray(img_gray).convert('L')
                pred = self.modelCrnn.predict(im_pil)
                # print(pred, end = ' ' )
                lst_line_temp.append(pred)
            lst_frame_temp.append(lst_line_temp)
        text = ' '.join(' '.join(sent) for sent in lst_frame_temp) + '.'
        return text

    def process(self, video_path, time_get_frame):
        cap = cv2.VideoCapture(video_path)
        # frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        # FPS = cap.get(cv2.CAP_PROP_FPS)
        # clip_duration = frame_count / FPS
        # print(frame_count, FPS, clip_duration)
        if not cap.isOpened():
            print('error opening video stream')
        count = 1
        cap.set(cv2.CAP_PROP_POS_MSEC, count * 1000)
        lst_video_temp = []
        ret, frame = cap.read()
        lst_frame = self.modelYolo.predict(frame)
        lst_frame_sort = sort_xy(lst_frame)
        text = self.extractFrame(lst_frame_sort, frame)
        lst_video_temp.append(text)

        while cap.isOpened():
            frame_0 = frame
            lst_frame_0 = self.modelYolo.predict(frame_0)
            lst_frame_0_sort = sort_xy(lst_frame_0)  # truyền vào root từ file xml cua frame
            cap.set(cv2.CAP_PROP_POS_MSEC, count * 1000)
            ret, frame = cap.read()
            lst_frame_1 = self.modelYolo.predict(frame)
            lst_frame_1_sort = sort_xy(lst_frame_1)

            # print(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)
            # print(cap.get(cv2.CAP_PROP_POS_FRAMES))
            # print(frame)
            # print(frame.shape)

            if ret:
                # imshow('Frame', frame)
                # print('lst_frame_0', lst_frame_0)
                # print('lst_frame_1', lst_frame_1)
                # print('lst_frame_0_sort', lst_frame_0_sort)
                # print('lst_frame_1_sort', lst_frame_1_sort)
                if loc_trung(lst_frame_0, lst_frame_1) == False and (len(lst_frame_1) != 0) or (len(lst_frame_0) == 0):
                    print('khong trung')
                    text = self.extractFrame(lst_frame_1_sort, frame)
                    print(text)
                    lst_video_temp.append(text)
                else:
                    print('trung')
                count += time_get_frame
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        # print(lst_video_temp)
        print(' '.join(lst_video_temp))
        text_video = ' '.join(lst_video_temp)
        cap.release()
        cv2.destroyAllWindows()
        return text_video, lst_video_temp

    def check(self, lst_video_temp):
        index = []
        for i in range(len(lst_video_temp)-1):
            # print(lst_video_temp[i])
            lst_can_check = convert(lst_video_temp[i]).split()
            for j in range(i+1, len(lst_video_temp)):
                # print(lst_video_temp[j])
                lst_check = convert(lst_video_temp[j]).split()
                # print(lst_check)
                if check_sublist(lst_can_check, lst_check):
                    index.append(j)
                    # lst_video_temp.remove(lst_video_temp[j])
                else:
                    break
        print(index)
        lst_index = list(dict.fromkeys(index))
        print(lst_index)
        lst_temp = []
        for i in lst_index:
            temp = lst_video_temp[i]
            lst_temp.append(temp)
        for i in lst_temp:
            lst_video_temp.remove(i)
        return lst_video_temp


if __name__ == '__main__':

    model = ExtractMutex()
    text_video, lst_video_temp = model.process('/home/dungdinh/Documents/DATA/video_mutex_2/videoplayback (53).mp4', 1)
    print(lst_video_temp)
    lst_video_final = model.check(lst_video_temp)
    print(lst_video_final)