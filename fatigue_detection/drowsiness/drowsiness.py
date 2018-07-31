
from scipy.spatial import distance as dist
import numpy as np


# from driver_tracking.manager.states import DetectionState

#from driver_tracking.logging.log_data import LogData
from driver_tracking.video.detection_rules.detection import Detection, LogData, DetectionState

EYE_AR_THRESHOLD = 0.23


class Drowsiness(Detection):
	

	def __init__(self, left_eye: [], right_eye: [], i_frame: int, failed: bool=False, threshold=EYE_AR_THRESHOLD):
		self.left_eye = left_eye
		self.right_eye = right_eye
		if left_eye is not None:
			self.left_eye_ar = self.eye_aspect_ratio(left_eye)
		if right_eye is not None:
			self.right_eye_ar = self.eye_aspect_ratio(right_eye)
		self.threshold = threshold
		self.i_frame = i_frame
 
		if left_eye is not None and right_eye is not None:
			self.eye_ar = (self.left_eye_ar + self.right_eye_ar) / 2.0

		if failed:
			self.state = DetectionState.failed
		else:
			if self.detect():
				self.state = DetectionState.detected
			else:
				self.state = DetectionState.ok
	

	def eye_aspect_ratio(self, eye) -> float:
		A = dist.euclidean(eye[1], eye[5])
		B = dist.euclidean(eye[2], eye[4])

		C = dist.euclidean(eye[0], eye[3])

		ear = (A+B)/(2.0*C)

		return ear

	
	def detect(self) -> bool:
		return self.eye_ar < self.threshold

	
	def get_log_values(self) -> [LogData]:
		if self.failed():
			return []

		return [
			LogData(['drowsiness', 'eye_ar'], self.eye_ar, self.i_frame),

			LogData(['drowsiness', 'left_eye', '0', 'x'], self.left_eye[0][0], self.i_frame),
			LogData(['drowsiness', 'left_eye', '0', 'y'], self.left_eye[0][1], self.i_frame),
			LogData(['drowsiness', 'left_eye', '1', 'x'], self.left_eye[1][0], self.i_frame),
			LogData(['drowsiness', 'left_eye', '1', 'y'], self.left_eye[1][1], self.i_frame),
			LogData(['drowsiness', 'left_eye', '2', 'x'], self.left_eye[2][0], self.i_frame),
			LogData(['drowsiness', 'left_eye', '2', 'y'], self.left_eye[2][1], self.i_frame),
			LogData(['drowsiness', 'left_eye', '3', 'x'], self.left_eye[3][0], self.i_frame),
			LogData(['drowsiness', 'left_eye', '3', 'y'], self.left_eye[3][1], self.i_frame),
			LogData(['drowsiness', 'left_eye', '4', 'x'], self.left_eye[4][0], self.i_frame),
			LogData(['drowsiness', 'left_eye', '4', 'y'], self.left_eye[4][1], self.i_frame),
			LogData(['drowsiness', 'left_eye', '5', 'x'], self.left_eye[5][0], self.i_frame),
			LogData(['drowsiness', 'left_eye', '5', 'y'], self.left_eye[5][1], self.i_frame),
			
			LogData(['drowsiness', 'right_eye', '0', 'x'], self.right_eye[0][0], self.i_frame),
			LogData(['drowsiness', 'right_eye', '0', 'y'], self.right_eye[0][1], self.i_frame),
			LogData(['drowsiness', 'right_eye', '1', 'x'], self.right_eye[1][0], self.i_frame),
			LogData(['drowsiness', 'right_eye', '1', 'y'], self.right_eye[1][1], self.i_frame),
			LogData(['drowsiness', 'right_eye', '2', 'x'], self.right_eye[2][0], self.i_frame),
			LogData(['drowsiness', 'right_eye', '2', 'y'], self.right_eye[2][1], self.i_frame),
			LogData(['drowsiness', 'right_eye', '3', 'x'], self.right_eye[3][0], self.i_frame),
			LogData(['drowsiness', 'right_eye', '3', 'y'], self.right_eye[3][1], self.i_frame),
			LogData(['drowsiness', 'right_eye', '4', 'x'], self.right_eye[4][0], self.i_frame),
			LogData(['drowsiness', 'right_eye', '4', 'y'], self.right_eye[4][1], self.i_frame),
			LogData(['drowsiness', 'right_eye', '5', 'x'], self.right_eye[5][0], self.i_frame),
			LogData(['drowsiness', 'right_eye', '5', 'y'], self.right_eye[5][1], self.i_frame)
		]





