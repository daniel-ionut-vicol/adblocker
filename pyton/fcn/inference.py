import requests
import json
import os
import cv2
import sys
import numpy as np

classes = {0: 'daisy', 1: 'dandelion', 2: 'roses', 3 : 'sunflowers', 4:'tulips'}

def decode_predictions(predictions):
    labels = []
    for preds in predictions:
        labels.append(classes[np.argmax(preds)])

    return labels

def make_serving_request(image_batch):
    data = json.dumps({"signature_name": "serving_default",
                       "instances": image_batch.tolist()})

    headers = {"content-type": "application/json"}

    os.environ['NO_PROXY'] = 'localhost'
    json_response = requests.post(
        'http://localhost:8501/v1/models/flower_classifier:predict', data=data, headers=headers)

    predictions = json.loads(json_response.text)['predictions']

    return predictions

def construct_image_batch(image_group, BATCH_SIZE):
    # get the max image shape
    max_shape = tuple(max(image.shape[x] for image in image_group) for x in range(3))

    # construct an image batch object
    image_batch = np.zeros((BATCH_SIZE,) + max_shape, dtype='float32')

    # copy all images to the upper left part of the image batch object
    for image_index, image in enumerate(image_group):
        image_batch[image_index, :image.shape[0], :image.shape[1], :image.shape[2]] = image

    return image_batch

def find_type(image):
    
    image_batch = construct_image_batch(image_group, len(image_group))
    predictions = make_serving_request(image_batch)
    labels = decode_predictions(predictions)

    return labels
    

if __name__=="__main__":
    """
    Docker command to start tensorflow serving server:
    (NOTE: Run the below command inside "./flower_classifier" directory)
    $ docker run --rm -t -p 8501:8501 -v "$(pwd):/models/flower_classifier" -e MODEL_NAME=flower_classifier --name flower_classifier tensorflow/serving
    $ docker run --rm -t -p 8501:8501 --mount type=bind,source="d:/work/aplicatii develbox/adblocker/pyton/fcn/flower_classifier",target=/models/flower_classifier -e MODEL_NAME=flower_classifier --name flower_classifier tensorflow/serving
    """

    image_group = []
    image_group.append(cv2.imread("d:/work/aplicatii develbox/adblocker/pyton/fcn/processedDataSet/val/daisy/11642632_1e7627a2cc.jpg")[:,:,::-1])
    image_group.append(cv2.imread("d:/work/aplicatii develbox/adblocker/pyton/fcn/processedDataSet/val/dandelion/15987457_49dc11bf4b.jpg")[:,:,::-1])
    image_group.append(cv2.imread("d:/work/aplicatii develbox/adblocker/pyton/fcn/processedDataSet/val/roses/174109630_3c544b8a2f.jpg")[:,:,::-1])
    image_group.append(cv2.imread("d:/work/aplicatii develbox/adblocker/pyton/fcn/processedDataSet/val/sunflowers/45045005_57354ee844.jpg")[:,:,::-1])
    image_group.append(cv2.imread("d:/work/aplicatii develbox/adblocker/pyton/fcn/processedDataSet/val/tulips/11746276_de3dec8201.jpg")[:,:,::-1])
    predictions = find_type(image_group)
    print(predictions)
    image_group = []
    image_group.append(cv2.imread("d:/work/aplicatii develbox/adblocker/pyton/fcn/processedDataSet/train/daisy/7410356270_9dff4d0e2e_n.jpg")[:,:,::-1])
    image_group.append(cv2.imread("d:/work/aplicatii develbox/adblocker/pyton/fcn/processedDataSet/train/dandelion/2608937632_cfd93bc7cd.jpg")[:,:,::-1])
    image_group.append(cv2.imread("d:/work/aplicatii develbox/adblocker/pyton/fcn/processedDataSet/train/roses/7345657862_689366e79a.jpg")[:,:,::-1])
    image_group.append(cv2.imread("d:/work/aplicatii develbox/adblocker/pyton/fcn/processedDataSet/train/sunflowers/16616096711_12375a0260_n.jpg")[:,:,::-1])
    image_group.append(cv2.imread("d:/work/aplicatii develbox/adblocker/pyton/fcn/processedDataSet/train/tulips/17165583356_38cb1f231d_n.jpg")[:,:,::-1])
    predictions = find_type(image_group)
    print(predictions)
    