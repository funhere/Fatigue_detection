import numpy as np

FRAME_SCALE = 0.000001

from driver_tracking.conf.experiment_conf import exp_conf


class LogData:
	def __init__(self, paths: [str], value: float, i_frame: int, i_experiment :int=exp_conf.i_experiment):
		self.paths: [str] = paths
		self.value: float = value
		self.i_frame: int = i_frame
		self.i_experiment: int = i_experiment


	def __structlog__(self):
		return {
			"paths": '.'.join(self.paths),
			"value": self.value,
			"experiment_id": self.i_experiment,
			"frame_id": self.i_frame
		}


	def __repr__(self):
		return "%s %f %d %d" % ('.'.join(self.paths), self.value, self.i_experiment, self.i_frame)