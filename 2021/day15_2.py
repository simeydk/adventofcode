import numpy as np
import heapq



def search(mx: np.ndarray) -> int:
    queue = [(0, (0, 0))]
    
