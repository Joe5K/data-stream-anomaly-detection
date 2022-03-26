from typing import List

from config import LAST_COL_IS_CLASS


class Vector:
    def __init__(self, data: List[str]):
        if LAST_COL_IS_CLASS:
            self.data = tuple(float(i) for i in data[:-1])
            self.cls = data[-1]
        else:
            self.data = tuple(float(i) for i in data)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index) -> float:
        if index < len(self):
            return self.data[index]

    def __iter__(self) -> iter:
        return iter(self.data)

    def __repr__(self) -> str:
        return f"class: {self.cls}; data: {str(self.data)}"
