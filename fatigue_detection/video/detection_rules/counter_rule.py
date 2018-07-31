from .detection import Detection


class CounterRule:

    
    #TODO: validation
    def __init__(self, positive_count_threshold: int=10, recent_frame_count: int=30):
        self.positive_count_threshold = positive_count_threshold
        self.recent_frame_count = recent_frame_count


    def detected(self, frames):
        if len(frames) < self.recent_frame_count:
            return False

        count = 0
        for f in list(frames)[-self.recent_frame_count:]:
            if f.detected():
                count += 1

        return count > self.positive_count_threshold
            