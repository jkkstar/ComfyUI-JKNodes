import torch
from PIL import Image
import numpy as np

CATALOGUE = "👿𝓳𝓴 Nodes/image"


def tensor_to_pil(inp):
    """
    Parameters:
        inp: Torch tensor with shape (H, W, C), float32.

    Return:
        PIL Image.
    """
    return Image.fromarray(np.clip(inp.cpu().numpy() * 255., 0, 255).astype(np.uint8))


def pil_to_tensor(inp):
    """
    Parameters:
        inp: PIL Image.

    Return:
        Torch tensor with shape (H, W, C), float32.
    """
    return torch.from_numpy(np.array(inp).astype(np.float32) / 255.0)


def lanczos(image, width, height):
    """
    image: Torch tensor with shape (H, W, C)
    """
    image_ = tensor_to_pil(image)
    image_ = image_.resize((width, height), resample=Image.Resampling.LANCZOS)
    image_ = pil_to_tensor(image_)
    image_ = image_.to(image.device, image.dtype)  # move to device
    return image_


def common_upscale(image, width, height, upscale_method):
    """
    Parameters:
        image: Torch tensor with shape (H, W, C).

    Returns:
        Torch tensor with shape (H', W', C).
    """
    if upscale_method == "lanczos":
        return lanczos(image, width, height)
    else:
        return torch.nn.functional.interpolate(
            image.movedim(-1, 0).unsqueeze(0),  # (H, W, C) -> (B, C, H, W)
            size=(height, width),
            mode=upscale_method
        ).squeeze(0).movedim(0, -1)  # (B, C, H, W) -> (C, H, W) -> (H, W, C)


class JKConcatenateImages:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "image1": ("IMAGE",),
            "image2": ("IMAGE",),
            "method": (
                ["lanczos", "nearest", "bilinear", "bicubic", "area", "nearest-exact"],
                {"default": "lanczos"}
            ),
            "direction": (
                ["right", "down", "left", "up"],
                {"default": "right"}
            ),
            "match_image_size": ("BOOLEAN", {"default": True}),
        }}

    RETURN_TYPES = ("IMAGE",)
    # RETURN_NAMES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = CATALOGUE
    DESCRIPTION = """
Concatenates the image2 to image1 in the specified direction.
"""

    def run(self, image1, image2, method, direction, match_image_size):
        # image shape: B, H, W, C
        image1 = image1[0]  # (H, W, C)
        image2 = image2[0]  # (H, W, C)

        if match_image_size:
            target_shape = image1.shape

            original_height = image2.shape[0]
            original_width = image2.shape[1]
            original_aspect_ratio = original_width / original_height

            if direction in ['left', 'right']:
                # Match the height and adjust the width to preserve aspect ratio
                target_height = target_shape[0]
                target_width = int(target_height * original_aspect_ratio)
            elif direction in ['up', 'down']:
                # Match the width and adjust the height to preserve aspect ratio
                target_width = target_shape[1]
                target_height = int(target_width / original_aspect_ratio)

            # Resize image2 to match the target size while preserving aspect ratio
            image2_resized = common_upscale(image2, target_width, target_height, method)
        else:
            image2_resized = image2

        # Concatenate based on the specified direction
        if direction == 'right':
            concatenated_image = torch.cat((image1, image2_resized), dim=1)  # Concatenate along width
        elif direction == 'down':
            concatenated_image = torch.cat((image1, image2_resized), dim=0)  # Concatenate along height
        elif direction == 'left':
            concatenated_image = torch.cat((image2_resized, image1), dim=1)  # Concatenate along width
        elif direction == 'up':
            concatenated_image = torch.cat((image2_resized, image1), dim=0)  # Concatenate along height

        return concatenated_image.unsqueeze(0),  # (H, W, C) -> (1, H, W, C)


class JKGetImageShape:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("INT", "INT", "INT", "INT")
    RETURN_NAMES = ("B", "H", "W", "C")
    # RETURN_NAMES = ("Batch Size","HEIGHT", "WIDTH", "CHANNELS")
    FUNCTION = "run"
    CATEGORY = CATALOGUE
    OUTPUT_NODE = True
    DESCRIPTION = """
Get the shape of IMAGE
"""

    def run(self, image):
        b, h, w, c = image.shape
        # return b, h, w, c
        return {"ui": {"text": [f"[{b}, {h}, {w}, {c}]"]}, "result": (b, h, w, c)}


class JKResizeImage:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "image": ("IMAGE", {"forceInput": True}),
            "height": ("INT", {"default": 512, "min": 1, "max": 1000000}),
            "width": ("INT", {"default": 512, "min": 1, "max": 1000000}),
            "method": (
                ["lanczos", "nearest", "bilinear", "bicubic", "area", "nearest-exact"],
                {"default": "lanczos"}
            ),
        }}

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = CATALOGUE

    def run(self, image, height, width, method):
        # image shape: B, H, W, C

        # image = image[0]  # (H, W, C)
        # image_resized = common_upscale(image, width, height, method)
        # return image_resized.unsqueeze(0),  # (H, W, C) -> (1, H, W, C)

        image_resized = [common_upscale(x, width, height, method) for x in image]
        image_resized = torch.stack(image_resized)

        return image_resized,


def center_crop(
        image,
        aspect_ratio: float = 1.0
):
    """
    Crops the given image at the center.
    The aspect ratio of the cropped image is defined by 'aspect_ratio'. The cropping area will extend to the edge
    of the image.

    :param image: The image to be cropped. Shape (..., H, W, C).
    :param aspect_ratio: The aspect ratio of the cropped image. Default is 1.0.
    :return: The cropped image with shape (..., H', W', C). W' / H' = aspect_ratio. If the aspect ratio
        is greater than the original aspect ratio, the width of the cropped image will be the same as
        the original image, i.e., W' = W. Otherwise, H' = H.
    """
    h, w = image.shape[-3:-1]
    ar = w / h
    if ar > aspect_ratio:
        new_w = int(h * aspect_ratio)
        x1 = (w - new_w) // 2
        x2 = x1 + new_w
        return image[..., :, x1:x2, :]
    else:
        new_h = int(w / aspect_ratio)
        y1 = (h - new_h) // 2
        y2 = y1 + new_h
        return image[..., y1:y2, :, :]


class JKCenterCropImage:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "image": ("IMAGE", {"forceInput": True}),
            "aspect_ratio": ("FLOAT", {"default": 1, "min": 0.1, "max": 10}),
        }}

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = CATALOGUE

    def run(self, image, aspect_ratio):
        # image shape: B, H, W, C
        image_ = center_crop(image, aspect_ratio)
        return image_,


def _check_image_dimensions(tensors, names):
    reference_dimensions = tensors[0].shape[1:]  # Ignore batch dimension
    mismatched_images = [names[i] for i, tensor in enumerate(tensors) if tensor.shape[1:] != reference_dimensions]

    if mismatched_images:
        raise ValueError(
            f"Stack Images To Batch Warning: Input image dimensions do not match for images: {mismatched_images}")


class JKStackImagesToBatch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
            },
            "optional": {
                "images_1": ("IMAGE",),
                "images_2": ("IMAGE",),
                "images_3": ("IMAGE",),
                "images_4": ("IMAGE",),
                # "images_5": ("IMAGE",),
                # "images_6": ("IMAGE",),
                # Theoretically, an infinite number of image input parameters can be added.
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = CATALOGUE

    def run(self, **kwargs):
        tensors = [kwargs[key] for key in kwargs if kwargs[key] is not None]
        names = [key for key in kwargs if kwargs[key] is not None]

        if not tensors:
            raise ValueError("At least one input image must be provided.")

        _check_image_dimensions(tensors, names)
        batched_tensors = torch.cat(tensors, dim=0)
        return batched_tensors,
