
from collections import deque

from .detection_rules.detection import Detection
from .detection_rules.counter_rule import CounterRule


class FrameSeries:
    N_SOFT_MAX_FRAMES = 48

    def __init__(self, rule: CounterRule=CounterRule(), n_frames: int=N_SOFT_MAX_FRAMES):
        self.n_frames: int = n_frames
        self.rule: CounterRule = rule
        self.frames: [Detection] = deque([], maxlen=n_frames)


    def add_frame(self, frame):
        
        self.frames.append(frame)
        # return self.detected()


    def detected(self) -> bool:
        return self.rule.detected(self.frames)
