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
from components.CropCompare.src.utils.response import build_response_compare
from components.CropCompare.src.models.PackageModel import PackageModel


class CompareExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.textWriterText = self.request.get_param("textWriterText")
        self.image = self.request.get_param("inputImage")
        self.secondImage = self.request.get_param("inputSecondImage")
        self.configTypeTextWriter = self.request.get_param("configTypeTextWriter")
    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}


    def TextWriter(self,img1,img2):
        font = cv2.FONT_HERSHEY_SIMPLEX
        thickness = 3
        color = (255, 255, 255)
        shadow_color = (0, 0, 0)

        def get_position_and_scale(img):
            h, w = img.shape[:2]
            base_font_scale = 1.0
            (text_width, _), _ = cv2.getTextSize(self.textWriterText, font, base_font_scale, thickness)
            target_ratio = 0.2  # metin genişliği, görselin %60'ını kapsasın
            font_scale = (w * target_ratio) / text_width

            (text_width, text_height), _ = cv2.getTextSize(self.textWriterText, font, font_scale, thickness)

            if self.configTypeTextWriter == "Center":
                x = (w - text_width) // 2
                y = (h + text_height) // 2
            elif self.configTypeTextWriter == "Top":
                x = (w - text_width) // 2
                y = text_height + 20
            elif self.configTypeTextWriter == "Bottom":
                x = (w - text_width) // 2
                y = h - 20
            elif self.configTypeTextWriter == "Left":
                x = 20
                y = (h + text_height) // 2
            elif self.configTypeTextWriter == "Right":
                x = w - text_width - 20
                y = (h + text_height) // 2
            else:
                x, y = 50, 50

            x = max(10, min(x, w - text_width - 10))
            y = max(text_height + 10, min(y, h - 20))

            return x, y, font_scale

        # img1
        x1, y1, scale1 = get_position_and_scale(img1)
        cv2.putText(img1, self.textWriterText, (x1 + 3, y1 + 3), font, scale1, shadow_color, thickness + 1, cv2.LINE_AA)
        cv2.putText(img1, self.textWriterText, (x1, y1), font, scale1, color, thickness, cv2.LINE_AA)

        # img2
        x2, y2, scale2 = get_position_and_scale(img2)
        cv2.putText(img2, self.textWriterText, (x2 + 3, y2 + 3), font, scale2, shadow_color, thickness + 1, cv2.LINE_AA)
        cv2.putText(img2, self.textWriterText, (x2, y2), font, scale2, color, thickness, cv2.LINE_AA)

        return img1, img2

    def run(self):
        img1 = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.secondImage, redis_db=self.redis_db)
        img1.value, img2.value = self.TextWriter(img1.value, img2.value)
        self.secondImage = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)
        self.image = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response_compare(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()