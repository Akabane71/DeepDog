import cv2
import pyzbar.pyzbar as pyzbar


class QR():
    """
        输入一个
    """
    def __int__(self,cap):
        self.cap = cap
    def go(self):
        res = ''
        return res


cap = cv2.VideoCapture(0)
qr_list = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    else:
        cv2.imshow('frame', frame)
        decoded_data = ""
        qrcodes = pyzbar.decode(frame)
        if qrcodes:
            print('1')
            for obj in qrcodes:
                print('Data:', obj.data.decode('utf-8'))
                decoded_data = obj.data.decode('utf-8')
                qr_list.append(decoded_data)
        if len(qr_list) > 3:
            if qr_list[0] == qr_list[1] == qr_list[2]:
                print('res:',qr_list[0])
                break
            else:
                qr_list.pop(0)
            print(qr_list)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
# 关闭所有窗口
cv2.destroyAllWindows()




