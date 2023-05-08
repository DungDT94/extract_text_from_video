import torch
from torch.autograd import Variable
from CRNN import utils
from CRNN import dataset
from PIL import Image
import cv2
from CRNN.models import crnn as crnn
from CRNN import params


class ModelCrnn:
    def __init__(self):
        self.nclass = len(params.alphabet) + 1
        self.model = crnn.CRNN(params.imgH, params.nc, self.nclass, params.nh)
        if torch.cuda.is_available():
            self.model = self.model.cuda()
        self.model.load_state_dict(torch.load('/home/dungdinh/Prj_tach_chu_video/yolov5/crnn-pytorch/expr/exp3/netCRNN_50.pth'))
        self.converter = utils.strLabelConverter(params.alphabet)
        self.transformer = dataset.resizeNormalize((100, 32))
        self.model.eval()

    def predict(self, image):
        # print('number of class', self.nclass)
        # image = Image.open(img).convert('L')
        # print(type(image))
        image = self.transformer(image)
        if torch.cuda.is_available():
            image = image.cuda()
        image = image.view(1, *image.size())
        image = Variable(image)
        preds = self.model(image)
        _, preds = preds.max(2)
        preds = preds.transpose(1, 0).contiguous().view(-1)
        preds_size = Variable(torch.LongTensor([preds.size(0)]))
        raw_pred = self.converter.decode(preds.data, preds_size.data, raw=True)
        sim_pred = self.converter.decode(preds.data, preds_size.data, raw=False)
        return sim_pred


if __name__ == "__main__":
    model = MODEL_CRNN()
    '''
    root = '/home/dungdinh/Documents/DATA/train/data_test_crop'
    for file in glob.glob(root + '/*'):
        print(file)
        model.predict(file)
    '''
    image = cv2.imread('/home/dungdinh/Documents/DATA/train/train_2_crop/0a0c295ea01845d0b2d6b2779aa76c3c.jpg')
    # image = Image.open('/home/dungdinh/Documents/DATA/train/train_2_crop/0a0c295ea01845d0b2d6b2779aa76c3c.jpg
    # ').convert('L')
    im_pil = Image.fromarray(image).convert('L')
    print('type image', type(im_pil))
    model.predict(im_pil)

