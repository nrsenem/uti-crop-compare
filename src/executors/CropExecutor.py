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
        self.rotation_cropVariable = self.request.get_param("CropVariable")
        self.image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def crop(self, image):
        h, w = image.shape[:2]
        crop_factor = 1 + (self.cropVariable / 100)  # Crop miktarını zoom gibi belirliyoruz
        new_h = int(h / crop_factor)
        new_w = int(w / crop_factor)

        center_y = h // 2
        center_x = w // 2
        start_y = max(center_y - new_h // 2, 0)
        start_x = max(center_x - new_w // 2, 0)
        end_y = min(start_y + new_h, h)
        end_x = min(start_x + new_w, w)

        cropped = image[start_y:end_y, start_x:end_x]
        return cropped

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.crop(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
