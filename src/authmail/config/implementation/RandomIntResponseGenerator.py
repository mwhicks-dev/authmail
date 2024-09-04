import random

from behavior import IResponseGenerator

class RandomIntResponseGenerator(IResponseGenerator):
    """
    No additional dependencies needed. When constructing, pass in the length of
    your challenges. For instance, if 6 is passed, challenges will look 
    something like 345356.
    """

    _length: int

    def __init__(self, length: int):
        self._length = length

    def generate_response(self) -> str:
        resp: list[str] = []

        for _ in range(0, self._length):
            resp.append(str(random.randint(0, 9)))
        
        return ''.join(resp)