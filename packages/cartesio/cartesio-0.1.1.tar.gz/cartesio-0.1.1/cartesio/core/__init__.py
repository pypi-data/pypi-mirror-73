import numpy as np

__all__ = [
    "segment_length"
]


def segment_length(
        segment: np.ndarray
) -> float:
    x1, y1, x2, y2 = segment
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
