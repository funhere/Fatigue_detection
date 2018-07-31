import cv2
import imutils.face_utils
from singleton_decorator import singleton


# from driver_tracking.logging.log_data import LogData
from driver_tracking.logging.log_data_manager import LogDataManager, LogData
from driver_tracking.manager.states import DetectionState, DetectionTransition, DisplayState, DisplayTransition
from driver_tracking.manager.display_machine import DisplayMachine
from driver_tracking.manager.detection_machine import DetectionMachine
from driver_tracking.drowsiness.drowsiness import Drowsiness


logger = LogDataManager()

display_machine = DisplayMachine()

(lStart, lEnd) = imutils.face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = imutils.face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

#[For demo only]: drowsiness frame range on video: drowsiness_11.mp4 
frame_drowsiness = list(range(782,961)) + list(range(5080,5259)) + list(range(5381,5470)) 

@singleton
class DrowsinessMachine(DetectionMachine):


	def __init__(self):
		super().__init__()


	def logging(self, logger: LogDataManager, drowsiness: Drowsiness, i_frame: int):
		
		logger.add_frame_log_data([LogData(['drowsiness', 'series'], self.state_as_number(), i_frame)])
		logger.add_frame_log_data(drowsiness.get_log_values())


	def draw(self, frame, leftEye: [], rightEye: [], drowsiness: Drowsiness, i_frame: int):
		if display_machine.state in [x.name for x in display_machine.warnings]:
			# draw an alarm on the frame
			cv2.putText(frame, "DROWSINESS!", (10, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			#[For demo only]: show the detection result.
			# if i_frame in frame_drowsiness:
			# 	cv2.putText(frame, "O [TP:Detection success]", (10, 50),
			# 		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
			# else:
			# 	cv2.putText(frame, "X [FP:Invalid Detection]", (10, 50),
			# 		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
		# else:
		# 	if i_frame in frame_drowsiness:
		# 		cv2.putText(frame, "X [FN:Detection failure]", (10, 50),
		# 			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)

		(_, width) = frame.shape[:2]

		if not drowsiness.failed():
			leftEyeHull = cv2.convexHull(leftEye)
			cv2.drawContours(frame, [leftEyeHull], -1, (128, 0, 128), 1)
			rightEyeHull = cv2.convexHull(rightEye)
			cv2.drawContours(frame, [rightEyeHull], -1, (128, 0, 128), 1)
			cv2.putText(frame, "EAR: {:.2f}/{:.2f}".format(drowsiness.eye_ar, drowsiness.threshold), (width-150, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)		


	def handle_next_frame(self, shape: [], frame, i_frame: int):
		# extract the left and right eye coordinates, then use the
		# coordinates to compute the eye aspect ratio for both eyes
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]

		drowsiness = Drowsiness(leftEye, rightEye, i_frame, False)

		self.add_frame(drowsiness)

		self.logging(logger, drowsiness, i_frame)
		self.draw(frame, leftEye, rightEye, drowsiness,i_frame)


	def handle_error_frame(self, frame, i_frame: int):
		failure = Drowsiness(None, None, None, i_frame, True)
		self.add_frame(failure)

		self.logging(logger, failure, i_frame)
		self.draw(frame, None, None, failure,i_frame)

