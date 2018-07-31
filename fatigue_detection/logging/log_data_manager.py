from collections import deque
import numpy as np
import cv2
import time
from singleton_decorator import singleton

import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

from ..conf import static
from .log_data import LogData

csv_logging_columns = ["drowsiness.eye_ar", "distraction.x_rotation", "distraction.y_rotation", "distraction.z_rotation", 
	"distraction.x_theta", "drowsiness.series", "distraction.series",
	"states.display.state", "profiling.predict", "profiling.detect01"]

@singleton
class LogDataManager:
	def __init__(self):
		self.fig = plt.figure(1)
		self.data_series = deque([], maxlen=1000)
		self.timing = True

		self.current_frame_id: int = 0
		self.current_frame_csv_logs: [LogData] = []

		static.G.f_logger.debug("frame_id," + ",".join(csv_logging_columns))

		# x1 = np.linspace(0.0, 5.0)
		# x2 = np.linspace(0.0, 2.0)

		# y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
		# y2 = np.cos(2 * np.pi * x2)

		# for n in names:
		# 	line1, = plt.plot(x1, y1, 'ko-')  


	def add_frame_log_data(self, log_data: [LogData]):
		self.data_series.extend(log_data)

		if not log_data:
			return
			
		for log in log_data:
			static.G.exp_logger.debug(log)

		# not log_data[0].i_frame for display_machine callback logging
		if log_data[0].i_frame and self.current_frame_id != log_data[0].i_frame:
			if self.current_frame_id > 0:
				static.G.f_logger.debug(self.get_current_csv_line())
				self.current_frame_csv_logs = []
			self.current_frame_id = log_data[0].i_frame

		for log in log_data:
			self.current_frame_csv_logs.append(log)			

	# def get_recent_values(self, name):
	# 	return np.array(list(self.dataset[name]))

	def get_current_csv_line(self) -> str:
		log_dict = {}
		for log in self.current_frame_csv_logs:
			log_dict[".".join(log.paths)] = log.value

		return str(self.current_frame_id) + "," + ",".join([str(log_dict[x]) if x in log_dict else "" for x in csv_logging_columns])

	#TODO:
	def plot(self, plt):
		self.fig.canvas.draw()
		# convert canvas to image
		img = np.fromstring(self.fig.canvas.tostring_rgb(), dtype=np.uint8,
				sep='')
		img = img.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))

		# img is rgb, convert to opencv's default bgr
		img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		# for i, name in enumerate(self.names):
		# 	plt.subplot(211 + i)
		# 	values = self.get_recent_values(name)
		# 	plt.plot(np.arrange(values), values)
		# 	plt.title(name)
		# 	plt.grid(True)

		return img
	

	def timeit(self, name: str, i_frame: int, method, *args):
		if self.timing:
			ts = time.time()
		result = method(*args)
		if self.timing:
			te = time.time()
			# method_name = method.__name__ if method.__name__ else method.__class__.__name__
			self.add_frame_log_data([LogData(['profiling', name], te - ts, i_frame)])

		return result

