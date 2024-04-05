import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
import pyperclip


class QR:

    def __call__(self, img):
        return self.go(img)

    # 抽象接口
    def go(self, img):
        return self.decode_qrcode(img)

    # 具体实现
    @staticmethod
    def decode_qrcode(img):
        # 解码二维码
        decoded_objects = decode(img)
        # 存储解码结果的字符串
        decoded_data = ""
        for obj in decoded_objects:
            decoded_data += f"{obj.data.decode('utf-8')}\n\n"
        print('decoded_data', decoded_data)
        return decoded_data
