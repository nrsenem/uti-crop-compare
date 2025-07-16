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
        self.rotation_degree = self.request.get_param("CropVariable")
        self.keep_side = self.request.get_param("KeepSide")
        self.image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def crop_image(self, image):
        h, w = image.shape[:2]
        crop_percent = self.cropVariable / 100.0  # örn. 20 → 0.2
        new_h = int(h * (1 - crop_percent))
        new_w = int(w * (1 - crop_percent))

        center_y = h // 2
        center_x = w // 2
        start_y = center_y - new_h // 2
        start_x = center_x - new_w // 2

        cropped = image[start_y:start_y + new_h, start_x:start_x + new_w]
        return cropped

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.crop_image(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
