
import math
import transforms3d
import numpy as np

from driver_tracking.conf import static

# from driver_tracking.manager.states import DetectionState

# from driver_tracking.logging.log_data import LogData
from driver_tracking.video.detection_rules.detection import Detection, LogData, DetectionState

from .pose import Pose


ANGLE_THRESHOLD = 20

def setup_Distraction():
	euler_rxzy = transforms3d.euler.EulerFuncs('rxzy')
	rotation_0_th_mat = euler_rxzy.euler2mat(-math.pi/2, math.pi/2., 0)
	# transforms3d.axangles.mat2axangle(rotation_0_th_mat)
	# Out[137]:
	# (array([ 0.57735027, -0.57735027, -0.57735027]), -2.0943951023931957)

	# adjustment for video dt_experiment-drosiness_11.mp4 only (2018-05-28)
	rotation_0_th_mat = radians_array_to_rotation_matrix(list(map(math.radians, [-55, 65.82292878826026, 83.2663256759596])))

	normal_x_vector = np.matmul(rotation_0_th_mat, np.array([1, 0, 0]).reshape(3, 1))

	return normal_x_vector

def radians_array_to_rotation_matrix(array):
	rotation_vec = array
	rotation_vec_norm = np.linalg.norm(rotation_vec)

	# Same as cv2.Rodrigues()
	mat = transforms3d.axangles.axangle2mat(rotation_vec, rotation_vec_norm)
	# print(rotation_vec, rotation_vec_norm, mat)
	return mat



class Distraction(Detection):

	normal_x_vector = setup_Distraction()
	# print(normal_x_vector)
	
	def __init__(self, head_pose, i_frame: int, failed: bool=False, threshold: float=ANGLE_THRESHOLD):
		super().__init__()

		self.head_pose = head_pose
		self.threshold: float = threshold
		self.i_frame: int = i_frame
 
		if failed:
			self.state: DetectionState = DetectionState.failed
		else:
			if self.detect():
				self.state: DetectionState = DetectionState.detected
			else:
				self.state: DetectionState = DetectionState.ok

	
	def detect(self):
		theta = self.distracted_x_theta()
		degrees = abs(math.degrees(theta))
		
		# static.G.f_logger.debug("direction %f %r " % (degrees, degrees > self.threshold))
		return degrees > self.threshold


	def rotation_matrix(self):
		rotation_vec = np.array(self.head_pose.rotation_vector).reshape(1, 3)[0]

		return radians_array_to_rotation_matrix(rotation_vec)


	def x_rotation_vector(self):
		return np.matmul(self.rotation_matrix(), np.array([1, 0, 0]).reshape(3, 1))


	def distracted_x_theta(self):
		cos_theta = np.dot(self.normal_x_vector.flatten(), self.x_rotation_vector().flatten())
		return np.arccos(cos_theta)


	def get_log_values(self):
		if self.failed():
			return [
			]
		else:
			return [
				LogData(['distraction', 'x_rotation'], math.degrees(self.head_pose.rotation_vector[0]), self.i_frame),
			    LogData(['distraction', 'y_rotation'], math.degrees(self.head_pose.rotation_vector[1]), self.i_frame),
			    LogData(['distraction', 'z_rotation'], math.degrees(self.head_pose.rotation_vector[2]), self.i_frame),
			    LogData(['distraction', 'x_theta'], math.degrees(self.distracted_x_theta()), self.i_frame)
		    ]

		