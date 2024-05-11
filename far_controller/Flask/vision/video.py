import cv2

class V:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print("Error: Unable to open camera.")
            return

    def __iter__(self):
        return self

    def __next__(self):
        ret, frame = self.cap.read()
        if not ret:
            raise StopIteration
        return frame

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise StopIteration
        return frame

    def release(self):
        self.cap.release()
