import random

from authmail.behavior import IResponseGenerator

class RandomIntResponseGenerator(IResponseGenerator):

    _length: int

    def __init__(self, length: int):
        self._length = length

    def generate_response(self) -> str:
        resp: list[str] = []

        for _ in range(0, self._length):
            list.append(str(random.randint(0, 9)))
        
        return ''.join(resp)