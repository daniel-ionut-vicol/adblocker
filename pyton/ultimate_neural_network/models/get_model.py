import os
import sys
from .resnet50 import resNet50 
from .vgg16 import vgg16
from .vgg19 import vgg19
from .inception_v3 import inceptionV3
from .xception import xception
from .efficientnet_b0 import efficientNetB0
from .mobilenet import mobileNet
from .densenet121 import denseNet121

sys.path.append("..")
sys.path.append(os.getcwd())
import config

def get_model(strategy):
    if config.MODEL == 'RESNET50':
        return resNet50(strategy)
    elif config.MODEL == 'VGG16':
        return vgg16(strategy)
    elif config.MODEL == 'VGG19':
        return vgg19(strategy)
    elif config.MODEL == 'INCEPTION_V3':
        return inceptionV3(strategy)
    elif config.MODEL == 'XCEPTION':
        return xception(strategy)
    elif config.MODEL == 'EFFICIENTNET_B0':
        return efficientNetB0(strategy)
    elif config.MODEL == 'MOBILENET':
        return mobileNet(strategy)
    elif config.MODEL == 'DENSENET121':
        return denseNet121(strategy)
    else:
        raise ValueError("Invalid model identifier in config file.")
