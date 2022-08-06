'''
    File name: imageEditor.py
    Author: Cristian R. Guarachi Ibanez
    Date created: 01.06.2021
    Date last modified: 09.06.2021
    Python Version: 3.8
'''

from numpy import ndarray, array, asarray, append, round, hstack, mean, newaxis, reshape
from matplotlib.pyplot import hist, title, show, plot
from cv2 import imread, imshow, waitKey, destroyAllWindows,calcHist, resize, convertScaleAbs, equalizeHist, createCLAHE, \
    cvtColor,  COLOR_BGR2GRAY, THRESH_BINARY, IMREAD_GRAYSCALE, IMREAD_COLOR , threshold, INTER_AREA
from typing import List, Tuple, Callable, TypeVar
class ImageEditor:
    A:TypeVar = TypeVar('A', str, ndarray)
    def __init__(self, path:str) -> None:
        self.__img:ndarray = self.__readImage(path);
        if(self.__img is None):
            raise ValueError

    def editImgArray(self, equa_method: str, scale:Tuple[int,int] = (256,256)):

        #grayImg:ndarray = self.__resizeImage(self.__convertImgToGS(imgArray=self.__img), scale_percent=scale)
        grayImg:ndarray = self.__convertImgToGS(imgArray=self.__img)
        grayImg = self.reshapeImage(scale, ext_img=grayImg)
        #print('gray', grayImg.shape)
        if(equa_method == 'clahe'):
            return self.__claheEqualization(grayImg);
        elif(equa_method=='equalizationHist'):
            return self.__equalizeHistagram(grayImg);
        elif(equa_method=='binary'):
            return self.__convertToBinary(grayImg);
        elif(equa_method=='gray'):
            return grayImg

    def getNoEditedImg(self) -> ndarray:
        return self.__img;

    def __readImage(self, path:str) -> ndarray:
        assert (isinstance(path, str)), 'this is not a string path'
        return imread(path, IMREAD_COLOR);

    def __convertImgToBW(self, imgArray: ndarray) -> ndarray:
        grayImgArray: ndarray = self.__convertImgToGS(imgArray)
        return threshold(grayImgArray, 110, 255, THRESH_BINARY)[1];

    @staticmethod
    def addNewChannel(img, channel: int, new_axis: bool = False) -> ndarray:
        if (new_axis):
            return img[..., newaxis];
        elif(len(img.shape)<3):
            return img.reshape((img.shape[0], img.shape[1], channel))
        elif(len(img.shape)<4):
            return  img.reshape((img.shape[0], img.shape[1], img.shape[2], channel))
        else:
            return img.reshape((img.shape[0], img.shape[1], img.shape[2], img.shape[3],  channel))

    @staticmethod
    def __convertImgToGS(imgArray: ndarray)->ndarray:
        assert(imgArray.shape[0] > 0), "the image array is empty";
        return cvtColor(imgArray, COLOR_BGR2GRAY);

    @staticmethod
    def __resizeImage(imgArray: ndarray, scale_percent:int ) -> ndarray:

        width: int = int(imgArray.shape[1]* scale_percent /100);
        height: int = int(imgArray.shape[0]*scale_percent/100);
        rescale_v: Tuple[int, int] = (width, height)
        return resize(imgArray, rescale_v)
        #return imgArray.reshape([rescale_v[0], rescale_v[1]])

    def reshapeImage(self, new_shape:Tuple[int, int], ext_img:ndarray= None) -> A:

        if(ext_img is None):
            assert ((self.__img.shape[0] > 0) and (len(new_shape) > 0))
            return resize(self.__img, new_shape, interpolation=INTER_AREA)
        elif(ext_img.shape[0] > 0):
            return resize(ext_img, new_shape);
        else:
            return 'the external image array is empty or the input is not valid'

    @staticmethod
    def __claheEqualization(imgArray: ndarray) -> ndarray:
        clahe: createCLAHE = createCLAHE(clipLimit=2.0, tileGridSize=(8,8));
        return clahe.apply(imgArray);
    @staticmethod
    def __equalizeHistagram(imgArray: ndarray) -> ndarray:
        equali: ndarray = equalizeHist(imgArray);
        #return hstack((imgArray, equali));
        return equali;

    @staticmethod
    def __convertToBinary(imgArray: ndarray, rescale: bool = False ) -> ndarray:
        assert(imgArray.ndim ==2), 'The image dimension is not too big'
        size: Tuple[int, int] = None;
        if(rescale):
            size = (150, 150)
        else:
            size = imgArray.shape
        img: Callable = resize(imgArray, size);
        return convertScaleAbs(img, alpha=1.10, beta=20);

    @staticmethod
    def histogram(imgArray: ndarray, preedit: bool = True) -> None:
        #print(imgArray.shape)
        hist(imgArray.ravel(), 256, [0,256]);
        if(preedit):
            title("Color Image Histogram");
        else:
            title("Black and White Image")
        show();
    @staticmethod
    def calculateHist(imgArray: ndarray, preedit:bool=True, output: bool = False) -> ndarray:
        if(preedit):
            channels: List[int] = [0]
        else:
            channels: List[int] = [0,1,2]
        hist: Callable = calcHist(imgArray, channels, None, [256], [0,256]);
        plot(hist)
        show()
        if(output):
            return asarray(hist)

    @staticmethod
    def showImage(imgArray: ndarray, index: int=0) -> None:
        imshow('Current Image'+ '{}'.format(index), imgArray);
        waitKey(200000);
        #destroyAllWindows();


if __name__ == '__main__':

    imgName: str = r"00000.jpg"
    #pic: ndarray = imread(imgName);

    edition: ImageEditor = ImageEditor(imgName);
    print('loaded image',edition.getNoEditedImg().shape)
    reshaped:ndarray=edition.editImgArray('gray', (256,256))
    print('rescaled image',reshaped.shape)
    resized:ndarray = edition.reshapeImage((256,256))
    print('resized image',resized.shape)
    reshaped = edition.addNewChannel(reshaped,1)
    print('new channel added', reshaped.shape)
    #edition.histogram(pic)
    #print(pic.shape)
    #bwimage: ndarray = edition.editImagArray(edition.getNoEditedImg(), 'gray', scale=0)
    #print(bwimage.shape)

    #edition.showImage(bwimage)
    #edition.histogram(bwimage)
