import atexit
import queue
import threading
from concurrent.futures import Future, wait
import logging

from typing import List, Dict

from libc.stdint cimport uint32_t
from cpython.mem cimport PyMem_Malloc, PyMem_Free

import numpy as np
from . cimport c_tpu


LOGGER = logging.getLogger("iva_tpu")

_shutdown = False


def _python_exit():
    global _shutdown
    _shutdown = True


atexit.register(_python_exit)


cdef class TPUPlaceholder:
    cdef const c_tpu.TPUIONode *_ptr


cpdef parse_placeholder_description(placeholder: TPUPlaceholder):
    """Parses metadata description to Python dictionary"""
    cdef const c_tpu.TPUIONode *desc = placeholder._ptr
    result = dict()
    result['address'] = desc.address
    result['scale'] = [scale for scale in desc.scale[:desc.scale_len]]

    user_shape_intermediate = <const int *>desc.user_shape
    result['user_shape'] = [axis for axis in user_shape_intermediate[:desc.user_shape_len]]
    result['user_shape_len'] = desc.user_shape_len
    result['user_order'] = desc.user_order

    padding_intermediate = desc.padding
    result['padding'] = [tuple(dic.values()) for dic in padding_intermediate[:desc.user_shape_len]]

    tpu_shape_intermediate = <const int *>desc.tpu_shape
    result['tpu_shape'] = [axis for axis in tpu_shape_intermediate[:desc.tpu_shape_len]]
    result['tpu_order'] = desc.tpu_order
    result['tpu_shape_len'] = desc.tpu_shape_len
    result['dtype'] = desc.dtype
    result['layer_name'] = desc.anchor.decode('utf-8') if desc.anchor else desc.layer_name.decode('utf-8')
    result['size'] = desc.size
    return result


class TPUProgramException(Exception):
    pass


class TPUDeviceException(Exception):
    pass


class NOTPUDeviceException(TPUDeviceException):
    pass


cdef class TPUProgram:
    cdef c_tpu.TPUProgram* c_tpu_program
    cdef c_tpu.TPUProgramZipLoader *c_loader

    def __cinit__(self, path: str):
        cdef b_path = path.encode("utf-8")
        cdef char *c_path = b_path
        self.c_loader = c_tpu.tpu_program_zip_loader_open(c_path)

        if not self.c_loader:
            raise TPUProgramException("Failed to open program file %s" % path)

        self.c_tpu_program = c_tpu.tpu_program_open(self.c_loader)
        if not self.c_tpu_program:
            raise TPUProgramException("Failed to open TPU program")

    def __dealloc__(self):
        if self.c_loader:
            c_tpu.tpu_program_zip_loader_close(self.c_loader)

        if self.c_tpu_program:
            c_tpu.tpu_program_close(self.c_tpu_program)

    @property
    def inputs_count(self):
        return <int>c_tpu.tpu_program_get_inputs_count(self.c_tpu_program)

    @property
    def outputs_count(self):
        return <int>c_tpu.tpu_program_get_outputs_count(self.c_tpu_program)

    @property
    def inputs(self):
        """Returns verbose description of input parameters"""
        return [self.get_input_description(i) for i in range(self.inputs_count)]

    @property
    def outputs(self):
        """Returns verbose description of output parameters"""
        return [self.get_output_description(i) for i in range(self.outputs_count)]

    def get_input_name(self, index):
        py_byte_str = c_tpu.tpu_program_get_input_name_by_index(self.c_tpu_program, index)
        return py_byte_str.decode('utf-8')

    def get_input_index(self, name: str):
        py_bytes = name.encode('utf-8')
        index = c_tpu.tpu_program_get_input_index_by_name(self.c_tpu_program, <char *>py_bytes)
        if index < 0:
            raise TPUProgramException(f"input layer name {name} not found")
        return index

    def get_input_size(self, index):
        return <int>c_tpu.tpu_program_get_input_buffer_size(self.c_tpu_program, index)

    def get_output_name(self, index: int):
        py_byte_str = c_tpu.tpu_program_get_output_name_by_index(self.c_tpu_program, index)
        return py_byte_str.decode('utf-8')

    def get_output_index(self, name: str):
        py_bytes = name.encode('utf-8')
        index = c_tpu.tpu_program_get_output_index_by_name(self.c_tpu_program, <char *>py_bytes)
        if index < 0:
            raise TPUProgramException(f"output layer name {name} not found")
        return index

    def get_output_size(self, index):
        return <int>c_tpu.tpu_program_get_output_buffer_size(self.c_tpu_program, index)

    def get_input_description(self, index):
        """Returns verbose description of network input"""
        cdef TPUPlaceholder wrapper = TPUPlaceholder.__new__(TPUPlaceholder)
        wrapper._ptr = c_tpu.tpu_program_get_input_node(self.c_tpu_program, index)
        return parse_placeholder_description(wrapper)

    def get_output_description(self, index):
        """Returns verbose description of network output"""
        cdef TPUPlaceholder wrapper = TPUPlaceholder.__new__(TPUPlaceholder)
        wrapper._ptr = c_tpu.tpu_program_get_output_node(self.c_tpu_program, index)
        return parse_placeholder_description(wrapper)

    cdef c_tpu.tpu_io_descriptor* create_io_descriptor(self):
        return c_tpu.tpu_io_descriptor_create(self.c_tpu_program)

    cdef get_output_tensor(self, c_tpu.TPUTensor *tensor, c_tpu.tpu_io_descriptor *io_descriptor, int i):
        rc = c_tpu.tpu_program_get_output_tensor(self.c_tpu_program, io_descriptor, tensor, i)
        if rc != 0:
            raise TPUProgramException(f"can't get output tensor {i}")

    cdef set_input_tensor(self, c_tpu.tpu_io_descriptor *io_descriptor, c_tpu.TPUTensor *tensor, int i):
        rc = c_tpu.tpu_program_set_input_tensor(self.c_tpu_program, io_descriptor, tensor, i)
        if rc != 0:
            raise TPUProgramException(f"can't set input tensor {i}")

    cdef c_tpu.TPUTensor new_output_tensor(self, dtype, int i):
        cdef c_tpu.TPUTensor tensor = c_tpu.tpu_program_make_output_user_tensor(self.c_tpu_program, i)
        tensor.dtype = np_to_tpu_type[np.dtype(dtype)]
        tensor.size = c_tpu.tpu_tensor_get_size(&tensor)
        tensor.data = <char *>PyMem_Malloc(tensor.size)
        if not tensor.data:
            raise MemoryError
        return tensor

    cdef c_tpu.TPUTensor make_input_tensor(self, i):
        return c_tpu.tpu_program_make_input_user_tensor(self.c_tpu_program, i)

    cdef free_tensor(self, c_tpu.TPUTensor *tensor):
        PyMem_Free(tensor.data)

    @property
    def driver_version(self):
        py_byte_str = c_tpu.tpu_program_get_driver_version(self.c_tpu_program)
        if py_byte_str:
            return py_byte_str.decode('utf-8')

    @property
    def ip_version(self):
        py_byte_str = c_tpu.tpu_program_get_ip_version(self.c_tpu_program)
        if py_byte_str:
            return py_byte_str.decode('utf-8')


np_to_tpu_type = {np.dtype('int8'): 0,
                  np.dtype('float32'): 1,
                  np.dtype('float16'): 2,
                  np.dtype('float64'): 3}

tpu_type_to_dtype = {v: k for k, v in np_to_tpu_type.items()}

MAX_TENSORS = 32
MAX_IO_DESCRIPTORS = 64


cdef class TPUWorkItem:
    cdef dict __dict__
    cdef c_tpu.tpu_io_descriptor *io_descriptor

    def __cinit__(self):
        self.io_descriptor = NULL

    def __init__(self, future: Future, features: List[np.ndarray] or Dict[np.ndarray], dtype=np.int8, raw_mode=False):
        self.future = future
        self.features = features
        self.dtype = dtype
        self.raw_mode = raw_mode

    cdef set_io_descriptor(self, c_tpu.tpu_io_descriptor *io_descriptor):
        self.io_descriptor = io_descriptor

    cdef c_tpu.tpu_io_descriptor *get_io_descriptor(self):
        return self.io_descriptor

cdef _worker(inference, work_queue):
    try:
        while True:
            work_item = work_queue.get(block=True)
            if work_item is None:  # EOL
                break

            if not work_item.future.set_running_or_notify_cancel():
                return

            # wait inference
            counter = inference.wait()
            while True:
                result = c_get_results(inference, work_item)
                work_item.future.set_result(result)
                # Delete references to object. See issue16284
                del work_item
                counter -= 1
                if counter == 0:
                    break

                work_item = work_queue.get(block=True)
                if work_item is None:  # EOL
                    break
                if not work_item.future.set_running_or_notify_cancel():
                    return

            # Exit if:
            #   - The interpreter is shutting down OR
            if _shutdown:
                return
    except BaseException:
        LOGGER.critical('Exception in worker', exc_info=True)


cdef tpu_tensor_to_ndarray(c_tpu.TPUTensor *tensor):
    shape = []
    for j in range(tensor.shape_len):
        shape.append(tensor.shape[j])
    c_buffer = <char *> tensor.data
    buffer = c_buffer[:tensor.size]
    arr = np.frombuffer(buffer, dtype=tpu_type_to_dtype[tensor.dtype]).reshape(shape)
    return arr


cdef class TPUDevice:
    cdef c_tpu.TPUDevice* c_tpu_device
    cdef c_tpu.TPUProgram* c_tpu_program

    def __cinit__(self):
        self.c_tpu_device = c_tpu.tpu_device_build()
        if not self.c_tpu_device:
            raise NOTPUDeviceException()
        self.c_tpu_program = NULL
        self.program = None

    def __init__(self, queue_len=16):
        assert queue_len <= 64
        self.program = None

    def __dealloc__(self):
        if self.c_tpu_device:
            c_tpu.tpu_device_close(self.c_tpu_device)

    def load(self, program: TPUProgram):
        if c_tpu.tpu_program_check_hardware_parameters(self.c_tpu_device, program.c_tpu_program) != 0:
            raise TPUProgramException("Program compiled for different device")

        rc = c_tpu.tpu_program_load(self.c_tpu_device, program.c_tpu_program)
        if rc != 0:
            raise TPUProgramException("Failed to load program")

        self.program = program

    def run(self, features: List[np.ndarray] or Dict[str, np.ndarray], dtype=np.float32):
        with TPUInference(self) as inference:
            future = inference.submit(features, dtype=dtype)
            wait([future])
            return future.result()

    def run_raw(self, features: Dict[str, bytes] or List[bytes]):
        with TPUInference(self) as inference:
            future = inference.submit(features, raw_mode=True)
            wait([future])
            return future.result()

        raise TPUProgramException("Expected list or dict of inputs")

    cdef submit_inference(self, c_tpu.tpu_io_descriptor *io_descriptor):
        rc = c_tpu.tpu_inference_submit(self.c_tpu_device, io_descriptor)
        if rc != 0:
            raise TPUProgramException("Failed to submit inference")

    def wait_inference(self):
        cdef uint32_t counter
        with nogil:
            rc = c_tpu.tpu_inference_wait(self.c_tpu_device, &counter)
        if rc != 0:
            raise TPUProgramException(f"Failed to wait inference: return code {rc}")
        return counter

    @property
    def hardware_id(self):
        return <int>c_tpu.tpu_get_hardware_id(self.c_tpu_device)

    @property
    def control_unit_version(self):
        return <int>c_tpu.tpu_get_control_unit_version(self.c_tpu_device)

    @property
    def ewp_banks_count(self):
        return <int>c_tpu.tpu_get_ewp_banks_count(self.c_tpu_device)

    @property
    def ewp_bank_size(self):
        return <int>c_tpu.tpu_get_ewp_bank_size(self.c_tpu_device)

    @property
    def psp_buffer_size(self):
        return <int>c_tpu.tpu_get_psp_buffer_size(self.c_tpu_device)

    @property
    def ddr_banks_count(self):
        return <int>c_tpu.tpu_get_ddr_banks_count(self.c_tpu_device)

    @property
    def ddr_bank_size(self):
        return <int>c_tpu.tpu_get_ddr_bank_size(self.c_tpu_device)

    @property
    def axi_word_length(self):
        return <int>c_tpu.tpu_get_axi_word_length(self.c_tpu_device)

    @property
    def cache_word_length(self):
        return <int>c_tpu.tpu_get_cache_word_length(self.c_tpu_device)

    @property
    def cache_bank_size(self):
        return <int>c_tpu.tpu_get_cache_bank_size(self.c_tpu_device)

    @property
    def cache_banks_count(self):
        return <int>c_tpu.tpu_get_cache_banks_count(self.c_tpu_device)

    @property
    def systolic_array_size(self):
        cdef c_tpu.int_pair p = c_tpu.tpu_get_systolic_array_size(self.c_tpu_device)
        return <int>p.first, <int>p.second

    @property
    def driver_version(self):
        py_byte_str = c_tpu.tpu_get_driver_version(self.c_tpu_device)
        if py_byte_str:
            return py_byte_str.decode('utf-8')

    @property
    def ip_version(self):
        py_byte_str = c_tpu.tpu_get_ip_version(self.c_tpu_device)
        if py_byte_str:
            return py_byte_str.decode('utf-8')


cdef class TPUInference:
    cdef dict __dict__
    cdef c_tpu.tpu_io_descriptor* io_descriptors[64]
    cdef int io_descriptors_count
    cdef uint32_t inference_count
    cdef TPUProgram program
    cdef TPUDevice device

    def __init__(self, device: TPUDevice, queue_len: int = 8):
        self.device = device
        self.program = device.program
        self._queue_len = queue_len
        self._inference_queue = queue.Queue(maxsize=queue_len)
        self._worker_thread = None
        self.queued_inferences = 0
        self.inference_count = 0

    def __enter__(self):
        self.io_descriptors_count = self._queue_len + 1
        for i in range(self.io_descriptors_count):
            self.io_descriptors[i] = self.program.create_io_descriptor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._inference_queue.put(None)  # stop worker thread
        for i in range(self.io_descriptors_count):
            c_tpu.tpu_io_descriptor_free(self.io_descriptors[i])

    def wait(self):
        return self.device.wait_inference()

    def submit(self, features: List[np.ndarray] or Dict[str, np.ndarray],
               dtype=np.int8, raw_mode: bool = False) -> Future:

        cdef c_tpu.tpu_io_descriptor *io_descriptor = self.io_descriptors[
            self.queued_inferences % self.io_descriptors_count]
        self.queued_inferences += 1
        self.set_features(features, io_descriptor, raw_mode)

        f = Future()
        work_item = TPUWorkItem(f, features, dtype, raw_mode)
        work_item.set_io_descriptor(io_descriptor)
        self.device.submit_inference(io_descriptor)
        self._inference_queue.put(work_item)
        self._adjust_worker()
        return f

    def _adjust_worker(self):
        if self._worker_thread is None:
            args = (self, self._inference_queue)
            self._worker_thread = threading.Thread(target=_worker, args=args)
            self._worker_thread.start()

    def get_input_from_tensor_dict(self, features: Dict[str, np.ndarray]):
        for name, tensor in features.items():
            index = self.program.get_input_index(name)
            yield index, tensor

    def get_input_from_tensor_list(self, features: List[np.ndarray]):
        for index, tensor in enumerate(features):
            yield index, tensor

    def get_features_iterator(self, features):
        getter = None
        if type(features) == dict:
            getter = self.get_input_from_tensor_dict(features)
        elif type(features) == list:
            getter = self.get_input_from_tensor_list(features)
        if getter is None:
            raise TPUProgramException("Expected dict or list as features")
        return getter

    cdef set_features(self, features: List[np.ndarray] or Dict[str, np.ndarray], c_tpu.tpu_io_descriptor *io_descriptor,
                      raw_mode: bool=False):
        features_count = len(features)
        assert features_count == self.program.inputs_count

        feature_getter = self.get_features_iterator(features)
        cdef c_tpu.TPUTensor feature_tensors[32]

        for index, tensor in feature_getter:
            if raw_mode:
                self.set_input_buffer(io_descriptor, tensor, index)
            else:
                self.set_input_tensor(io_descriptor, tensor, feature_tensors, index)

    cdef get_raw_results(self, c_tpu.tpu_io_descriptor *io_descriptor, dtype=np.int8, as_dict=False):
        outputs_count = self.program.outputs_count
        result = [self.get_output_buffer(io_descriptor, i) for i in range(outputs_count)]
        if as_dict:
            node_names = [self.program.get_output_name(i) for i in range(outputs_count)]
            result = dict(zip(node_names, result))
        return result

    cdef get_results(self, c_tpu.tpu_io_descriptor *io_descriptor, dtype=np.int8, as_dict=False):
        cdef c_tpu.TPUTensor result_tensors[32]
        outputs_count = self.program.outputs_count

        for i in range(outputs_count):
            result_tensors[i] = self.program.new_output_tensor(dtype, i)
            self.program.get_output_tensor(&result_tensors[i], io_descriptor, i)

        try:
            result = [tpu_tensor_to_ndarray(&result_tensors[i]) for i in range(outputs_count)]
            if as_dict:
                node_names = [self.program.get_output_name(i) for i in range(outputs_count)]
                result = dict(zip(node_names, result))
            return result
        finally:
            for i in range(outputs_count):
                self.program.free_tensor(&result_tensors[i])

    cdef set_input_buffer(self, c_tpu.tpu_io_descriptor *io_descriptor, buffer: bytes, index: int):
        """
        Set input buffer by index
        """
        cdef char* c_buffer = <char *>buffer
        c_tpu.tpu_program_set_input_buffer(io_descriptor, index, c_buffer, len(buffer))

    cdef set_input_tensor(self, c_tpu.tpu_io_descriptor *io_descriptor, tensor: np.ndarray,
                          c_tpu.TPUTensor *feature_tensors, index: int):
        allowed_types = (np.int8, np.float32, np.float64)
        if tensor.dtype not in allowed_types:
            raise TPUProgramException("unexpected tensor type %s. Expected %s" % (tensor.dtype, allowed_types))

        input_bytes = tensor.tobytes()
        feature_tensors[index] = self.program.make_input_tensor(index)
        feature_tensors[index].data = <char *>input_bytes
        feature_tensors[index].size = len(input_bytes)
        feature_tensors[index].dtype = np_to_tpu_type[tensor.dtype]
        self.program.set_input_tensor(io_descriptor, &feature_tensors[index], index)

    cdef bytes get_output_buffer(self, c_tpu.tpu_io_descriptor *io_descriptor, index: int):
        """
        Get output buffer by index
        """
        cdef char *output = <char *>c_tpu.tpu_program_get_output_buffer(io_descriptor, index)
        cdef bytes b = output[:self.program.get_output_size(index)]
        return b


cdef c_get_results(TPUInference inference, TPUWorkItem work_item):
    cdef c_tpu.tpu_io_descriptor *io_descriptor = work_item.get_io_descriptor()
    as_dict = type(work_item.features) == dict
    if work_item.raw_mode:
        return inference.get_raw_results(io_descriptor, dtype=work_item.dtype, as_dict=as_dict)
    else:
        return inference.get_results(io_descriptor, dtype=work_item.dtype, as_dict=as_dict)
