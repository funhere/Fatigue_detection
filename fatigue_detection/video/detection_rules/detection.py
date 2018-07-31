
import abc

from driver_tracking.manager.states import DetectionState
from driver_tracking.logging.log_data import LogData


class Detection(abc.ABC):


    def __init__(self):
        self.state: DetectionState = None


    @abc.abstractmethod
    def detect(self) -> bool:
        pass


    @abc.abstractmethod
    def get_log_values(self) -> [LogData]:
        pass


    def failed(self) -> bool:
	    return self.state == DetectionState.failed

    