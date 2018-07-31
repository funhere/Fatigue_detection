import cv2
import math
from singleton_decorator import singleton

#from driver_tracking.logging.log_data import LogData
from driver_tracking.logging.log_data_manager import LogDataManager, LogData
# from .states import DetectionState, DetectionTransition, DisplayState, DisplayTransition
# from .display_machine import DisplayMachine
# from .detection_machine import DetectionMachine
from driver_tracking.manager.states import DetectionState, DetectionTransition, DisplayState, DisplayTransition
from driver_tracking.manager.display_machine import DisplayMachine
from driver_tracking.manager.detection_machine import DetectionMachine
from driver_tracking.head.distraction import Distraction

logger = LogDataManager()

display_machine = DisplayMachine()

#[For demo only]: distraction frames range on video: drowsiness_11.mp4 
iframe_distraction_range = list(range(0,240)) + list(range(301,420)) + list(range(1593,1683))

@singleton
class DistractionMachine(DetectionMachine):


	def __init__(self):
		super().__init__()


	def logging(self, logger, distraction: Distraction, i_frame: int):
		
		logger.add_frame_log_data([LogData(['distraction', 'series'], self.state_as_number(), i_frame)])
		logger.add_frame_log_data(distraction.get_log_values())


	def draw(self, frame, distraction: Distraction, i_frame: int):
		(height, width) = frame.shape[:2]

		if display_machine.state in [x.name for x in display_machine.warnings]:
			cv2.putText(frame, "DISTRACTION!", (10, height-60), 
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 180), 2)
			#[For demo only]: show the detection result.
		# 	if i_frame in iframe_distraction_range:
		# 		cv2.putText(frame, "O [TP:Detection success]", (10, height-40),
		# 			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
		# 	else:
		# 		cv2.putText(frame, "X [FP:Invalid Detection]", (10, height-40),
		# 			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
		# else:
		# 	if i_frame in iframe_distraction_range:
		# 		cv2.putText(frame, "X [FN:Detection failure]", (10, height-40),
		# 			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)				

		if not distraction.failed():
			cv2.putText(frame, "theta: {:.2f}/{:.2f}".format(math.degrees(distraction.distracted_x_theta()), distraction.threshold), (width-150, height-60),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 180), 2)				


	def handle_next_frame(self, pose, frame, i_frame: int):
		distraction = Distraction(pose, i_frame, False)
		self.add_frame(distraction)

		self.logging(logger, distraction, i_frame)
		self.draw(frame, distraction,i_frame)


	def handle_error_frame(self, frame, i_frame: int):
		failure = Distraction(None, None, i_frame, True)
		self.add_frame(failure)

		self.logging(logger, failure, i_frame)
		self.draw(frame, failure,i_frame)
		
