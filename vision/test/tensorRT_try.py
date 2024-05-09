import sys
import cv2
import numpy as np
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit

# 修改后的代码部分
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

class Yolov5TensorRT(object):
    def __init__(self, trt_path):
        self.engine = self.load_engine(trt_path)
        self.context = self.engine.create_execution_context()
        self.input_name = self.engine.get_binding_name(0)
        self.output_name = self.engine.get_binding_name(1)
        self.input_size = (640, 640)

    def load_engine(self, trt_path):
        with open(trt_path, 'rb') as f:
            engine_data = f.read()
        runtime = trt.Runtime(TRT_LOGGER)
        return runtime.deserialize_cuda_engine(engine_data)

    def inference(self, img_path):
        img = cv2.imread(img_path)
        or_img = cv2.resize(img, self.input_size)  # resize
        img = or_img[:, :, ::-1].transpose(2, 0, 1)  # BGR2RGB和HWC2CHW
        img = img.astype(dtype=np.float32) / 255.0  # 归一化
        img = np.expand_dims(img, axis=0)  # 增加 batch 维度

        # 分配 host 和 device 内存
        inputs, outputs, bindings, stream = allocate_buffers(self.engine)

        # 将输入数据复制到 GPU
        inputs[0].host = img
        cuda.memcpy_htod_async(inputs[0].device, inputs[0].host, stream)

        # 执行推理
        self.context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)
        cuda.memcpy_dtoh_async(outputs[1].host, outputs[1].device, stream)
        cuda.memcpy_dtoh_async(outputs[0].host, outputs[0].device, stream)
        stream.synchronize()

        # 获取推理结果
        pred = [outputs[1].host, outputs[0].host]

        return pred, or_img

def allocate_buffers(engine):
    inputs = []
    outputs = []
    bindings = []
    stream = cuda.Stream()
    for binding in engine:
        size = trt.volume(engine.get_binding_shape(binding)) * engine.max_batch_size
        dtype = trt.nptype(engine.get_binding_dtype(binding))
        host_mem = cuda.pagelocked_empty(size, dtype)
        device_mem = cuda.mem_alloc(host_mem.nbytes)
        bindings.append(int(device_mem))
        if engine.binding_is_input(binding):
            inputs.append(HostDeviceMem(host_mem, device_mem))
        else:
            outputs.append(HostDeviceMem(host_mem, device_mem))
    return inputs, outputs, bindings, stream

class HostDeviceMem(object):
    def __init__(self, host_mem, device_mem):
        self.host = host_mem
        self.device = device_mem

# 修改后的代码部分结束

if __name__ == "__main__":
    trt_path = './dog_best.trt'  # TensorRT 模型的路径
    model = Yolov5TensorRT(trt_path)
    output, or_img = model.inference('./4.png')

    # 后续处理和绘制结果的代码保持不变
