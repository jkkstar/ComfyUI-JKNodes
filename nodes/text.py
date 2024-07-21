from ..commom import Any


CATALOGUE = "👿𝓳𝓴 Nodes/text"


class JKInputText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": '', "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = CATALOGUE

    def run(self, text):
        return text.strip(),


class JKToText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any": (Any, {"forceInput": True})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "run"
    CATEGORY = CATALOGUE

    def run(self, any):
        return str(any),


class JKPreviewText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any": (Any, {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)
    OUTPUT_NODE = True
    FUNCTION = "run"
    CATEGORY = CATALOGUE

    def run(self, any):
        any = list(map(str, any))
        return {"ui": {"text": any}, "result": (any,)}
