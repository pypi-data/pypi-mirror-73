# @Time   : 2020-04-25
# @Author : zhangxinhao
if False:
    # video_capture
    class FrameMap:
        @staticmethod
        def map(frame, frame_num):
            return frame

        @staticmethod
        def width_map(width, height):
            return width

        @staticmethod
        def height_map(width, height):
            return height


    class VideoCapture:
        def __init__(self, endpoint):
            pass

        @property
        def endpoint(self) -> str:
            pass

        @property
        def device_name(self) -> str:
            pass

        @property
        def cur_frame_num(self) -> int:
            pass

        @property
        def height(self) -> int:
            pass

        @property
        def map_height(self) -> int:
            pass

        @property
        def width(self) -> int:
            pass

        @property
        def map_width(self) -> int:
            pass

        @property
        def frame_map(self) -> FrameMap:
            pass

        @property
        def retrieve_step(self) -> int:
            pass

        @property
        def history_size(self) -> int:
            pass

        @property
        def fps(self) -> int:
            pass

        @property
        def cap_lock(self) -> threading.Lock:
            pass

        @property
        def catch(self) -> dict:
            pass

        def new_catch_space(self, name, space_cls) -> typing.Any:
            pass

        def get_catch_space(self, name) -> typing.Any:
            pass

        def get_or_new_catch_space(self, name, space_cls) -> typing.Any:
            pass

        def get_frame(self, frame_num) -> np.ndarray:
            pass

        def get_map_frame(self, frame_num) -> np.ndarray:
            pass

        def read(self, is_return_num=False, timeout=8, is_copy=True) -> typing.Any:
            pass

        def read_map(self, is_return_num=False, timeout=8, is_copy=True) -> typing.Any:
            pass

        def read_non_blocking(self, is_return_num=False, is_copy=True) -> typing.Any:
            pass

        def read_map_non_blocking(self, is_return_num=False, is_copy=True) -> typing.Any:
            pass


    def create_cap(endpoint, device_name, retrieve_step=1,
                   grab_sleep_time=None, history_size=0, map_history_size=0,
                   reconnect_time=0, frame_map=None) -> VideoCapture:
        pass

from .video_capture import *