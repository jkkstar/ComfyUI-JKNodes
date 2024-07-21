import math
import typing as tp
from ..commom import Any

CATALOGUE = "👿𝓳𝓴 Nodes/utils"


def approx_multiple_of_8(n):
    if n % 8 < 4:
        return n - n % 8
    else:
        return n + 8 - n % 8


def calc_resolution(aspect_ratio: str, n_pixels: int = 1024 * 1024) -> tp.Tuple[int, int]:
    w, h = map(int, aspect_ratio.split(':'))
    aspect_ratio = w / h
    h = approx_multiple_of_8(int(math.sqrt(n_pixels / aspect_ratio)))
    w = approx_multiple_of_8(int(h * aspect_ratio))
    return w, h


class JKSDXLAspectRatioToWidthHeight:
    @classmethod
    def INPUT_TYPES(s):
        aspect_ratios = ['1:1',
                         '4:1', '21:9', '2:1', '16:9', '3:2', '4:3', '5:4',
                         '4:5', '3:4', '2:3', '9:16', '1:2', '9:21', '1:4']

        return {
            "required": {
                "aspect_ratio": (aspect_ratios,),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "run"
    CATEGORY = CATALOGUE

    def run(self, aspect_ratio):
        w, h = calc_resolution(aspect_ratio)
        return w, h


class JKConcentrator6To1:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "any_1": (Any,),
                "any_2": (Any,),
                "any_3": (Any,),
                "any_4": (Any,),
                "any_5": (Any,),
                "any_6": (Any,),
            }
        }

    RETURN_TYPES = ("HUB6IN1",)
    RETURN_NAMES = ("hub_6in1",)
    FUNCTION = "run"
    CATEGORY = CATALOGUE

    def run(self, any_1=None, any_2=None, any_3=None, any_4=None, any_5=None, any_6=None):
        original = [any_1, any_2, any_3, any_4, any_5, any_6]
        return [x if x is not None else None for x in original],


class JKConcentrator8To1:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "any_1": (Any,),
                "any_2": (Any,),
                "any_3": (Any,),
                "any_4": (Any,),
                "any_5": (Any,),
                "any_6": (Any,),
                "any_7": (Any,),
                "any_8": (Any,),
            }
        }
    
    RETURN_TYPES = ("HUB8IN1",)
    RETURN_NAMES = ("hub_8in1",)
    FUNCTION = "run"
    CATEGORY = CATALOGUE

    def run(self, any_1=None, any_2=None, any_3=None, any_4=None, any_5=None, any_6=None, any_7=None, any_8=None):
        original = [any_1, any_2, any_3, any_4, any_5, any_6, any_7, any_8]
        return [x if x is not None else None for x in original],


class JKDeconcentrator1To6:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "hub_6in1": ("HUB6IN1",),
            }
        }

    RETURN_TYPES = (Any, Any, Any, Any, Any, Any)
    # RETURN_NAMES = ("any_1", "any_2", "any_3", "any_4", "any_5", "any_6")
    RETURN_NAMES = ("1", "2", "3", "4", "5", "6")
    FUNCTION = "run"
    CATEGORY = CATALOGUE

    def run(self, hub_6in1):
        return hub_6in1


class JKDeconcentrator1To8:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "hub_8in1": ("HUB8IN1",),
            }
        }

    RETURN_TYPES = (Any, Any, Any, Any, Any, Any, Any, Any)
    # RETURN_NAMES = ("any_1", "any_2", "any_3", "any_4", "any_5", "any_6", "any_7", "any_8")
    RETURN_NAMES = ("1", "2", "3", "4", "5", "6", "7", "8")
    FUNCTION = "run"
    CATEGORY = CATALOGUE

    def run(self, hub_8in1):
        return hub_8in1
