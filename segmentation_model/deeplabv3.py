# camera-ready

import torch.nn as nn
import torch.nn.functional as F

import os

from segmentation_model.resnet import ResNet18_OS8
from segmentation_model.aspp import ASPP, ASPP_Bottleneck

class DeepLabV3(nn.Module):
    def __init__(self, model_id, project_dir):
        super(DeepLabV3, self).__init__()

        self.num_classes = 20

        self.model_id = model_id
        self.project_dir = project_dir

        self.resnet = ResNet18_OS8() # NOTE! specify the type of ResNet here
        self.aspp = ASPP(num_classes=self.num_classes) # NOTE! if you use ResNet50-152, set self.aspp = ASPP_Bottleneck(num_classes=self.num_classes) instead

    def forward(self, x):
        # (x has shape (batch_size, 3, h, w))

        h = x.size()[2]
        w = x.size()[3]

        feature_map = self.resnet(x) # (shape: (batch_size, 512, h/16, w/16)) (assuming self.resnet is ResNet18_OS16 or ResNet34_OS16. If self.resnet is ResNet18_OS8 or ResNet34_OS8, it will be (batch_size, 512, h/8, w/8). If self.resnet is ResNet50-152, it will be (batch_size, 4*512, h/16, w/16))

        output = self.aspp(feature_map) # (shape: (batch_size, num_classes, h/16, w/16))

        output = F.interpolate(output, size=(h, w), mode="bilinear", align_corners=True) # (shape: (batch_size, num_classes, h, w))

        return output