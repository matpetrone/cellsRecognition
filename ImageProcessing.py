from skimage import io, transform, filters
from skimage.util import view_as_blocks
from skimage import color
import os
import plotly.plotly as py
import plotly.graph_objs as go
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(threshold=np.nan)
import warnings
import torch

def conv2grayFrR(image):
    grayImage = image[:,:,0]
    return grayImage /255.0

def conv2grayFrB(image):
    grayImage = image[:,:,2]
    return grayImage.reshape(256,256,1) /255.0

def gaussianConv(image, sigma):
    return filters.gaussian(image, sigma, multichannel=False)

def scaleHeatmap(image, newSize):  #WARNING: this method work well only if the new tuple is a divider for old size
    if isinstance(newSize, tuple):
        blockedImage = view_as_blocks(image, (image.shape[0]//newSize[0], image.shape[1]//newSize[1]))
        scaledImage = np.zeros(newSize)
        for i in range(blockedImage.shape[1]):
            for j in range(blockedImage.shape[0]):
                scaledImage[i,j] = np.array(np.sum(blockedImage[i,j]))
                scaledImage = scaledImage
        return scaledImage
    else:
        warnings.warn('WARNING: second input must be a tuple (n, m)')

def sparseImage(image):
    newImage = np.zeros(image.shape)
    for i in range(image.shape[1]):
        for j in range(image.shape[0]):
            if image[i,j] != 0 :
                newImage[i,j] = 1
    return newImage

def createHeatMap64(image, sigma = 7):
    heatMap = conv2grayFrR(image)
    heatMap1 = gaussianConv(heatMap, sigma)
    heatMap2 = scaleHeatmap(heatMap1, (64,64))
    heatMap2 = heatMap2.reshape(64,64,1)
    return heatMap2

def visualizeImage(image):
    plt.imshow(image)
    plt.show()

def visualizeTorchImage(tensor, str =''):
    image = tensor.view(tensor.shape[1], tensor.shape[2], tensor.shape[0])
    image = np.squeeze(tensor.detach().numpy())
    image = (image - np.min(image)) / (np.max(image) - np.min(image))
    plt.imshow(image)
    plt.title(str)
    plt.show()

def compareTorchImages(tensor1, tensor2):
    plt.subplot(1,2,1)
    image1 = tensor1.view(tensor1.shape[1],tensor1.shape[2], tensor1.shape[0])
    image1 = np.squeeze(image1.detach().numpy())
    image1 = (image1 - np.min(image1)) / (np.max(image1) - np.min(image1))
    plt.imshow(image1)
    plt.title('CNN Output')

    plt.subplot(1,2,2)
    image2 = tensor2.view(tensor2.shape[1], tensor2.shape[2], tensor2.shape[0])
    image2 = np.squeeze(image2.detach().numpy())
    image2 = (image2 - np.min(image2)) / (np.max(image2) - np.min(image2))
    plt.imshow(image2)
    plt.title('Landmark')

    plt.show()



#TEST








