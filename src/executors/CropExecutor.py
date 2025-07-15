
"""
    It is one of the preprocessing components in which the image is rotated.
"""

import os
import cv2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.CropCompare.src.utils.response import build_response
from components.CropCompare.src.models.PackageModel import PackageModel


class CropExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.rotation_degree = self.request.get_param("cropVariable")
        self.image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def crop(self, img):
        h, w = img.shape[:2]
        crop_cfg = self.cropVariable
        new_w, new_h = int(w * crop_cfg), int(h * crop_cfg)
        x = (w - new_w) // 2
        y = (h - new_h) // 2
        cropped = img[y:y + new_h, x:x + new_w]
        return cropped

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.crop(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
    