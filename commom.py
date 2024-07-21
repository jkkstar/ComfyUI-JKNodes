class JKAnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


Any = JKAnyType("*")
