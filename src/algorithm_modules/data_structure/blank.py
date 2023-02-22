from typing import Union

"""
Blank is a float that equals/is greater and smaller than ...
... any other int or float at the same time.
"""
class Blank(float):
    def __init__(self) -> None:
        super().__init__()

    def __eq__(self, __x: Union[int, float]) -> bool:
        return True

    def __lt__(self, __x: Union[int, float]) -> bool:
        return True

    def __gt__(self, __x: Union[int, float]) -> bool:
        return True

    def __ge__(self, __x: Union[int, float]) -> bool:
        return True

    def __le__(self, __x: Union[int, float]) -> bool:
        return True