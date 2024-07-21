from .nodes.image import *
from .nodes.text import *
from .nodes.utils import *

NAME_PREFIX = "𝓳𝓴 "

NODE_CONFIG = {
    "JKConcatenateImages": {"class": JKConcatenateImages, "name": f"{NAME_PREFIX}Concat Images"},
    "JKGetImageShape": {"class": JKGetImageShape, "name": f"{NAME_PREFIX}Get Image Shape"},
    "JKResizeImage": {"class": JKResizeImage, "name": f"{NAME_PREFIX}Resize Image"},
    "JKCenterCropImage": {"class": JKCenterCropImage, "name": f"{NAME_PREFIX}Center Crop Image"},
    "JKStackImagesToBatch": {"class": JKStackImagesToBatch, "name": f"{NAME_PREFIX}Stack Images To Batch"},

    "JKInputText": {"class": JKInputText, "name": f"{NAME_PREFIX}Input Text"},
    "JKToText": {"class": JKToText, "name": f"{NAME_PREFIX}Convert To Text"},
    "JKPreviewText":  {"class": JKPreviewText, "name": f"{NAME_PREFIX}Preview As Text"},

    "JKSDXLAspectRatioToWidthHeight":  {"class": JKSDXLAspectRatioToWidthHeight, "name": f"{NAME_PREFIX}SDXL - Aspect Ratio To Width & Height"},
    "JKConcentrator6To1": {"class": JKConcentrator6To1, "name": f"{NAME_PREFIX}Concentrator (6To1)"},
    "JKDeconcentrator1To6": {"class": JKDeconcentrator1To6, "name": f"{NAME_PREFIX}Deconcentrator (1To6)"},
    "JKConcentrator8To1": {"class": JKConcentrator8To1, "name": f"{NAME_PREFIX}Concentrator (8To1)"},
    "JKDeconcentrator1To8": {"class": JKDeconcentrator1To8, "name": f"{NAME_PREFIX}Deconcentrator (1To8)"},
}


def generate_node_mappings(node_config):
    node_class_mappings = {}
    node_display_name_mappings = {}

    for node_name, node_info in node_config.items():
        node_class_mappings[node_name] = node_info["class"]
        node_display_name_mappings[node_name] = node_info.get("name", node_info["class"].__name__)

    return node_class_mappings, node_display_name_mappings


NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = generate_node_mappings(NODE_CONFIG)

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
