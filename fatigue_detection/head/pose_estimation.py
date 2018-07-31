
import cv2
import numpy as np

POINT_Sellion = (0., 0., 0.)
POINT_RightEye = (-20., -65.5, -5.)
POINT_LeftEye = (-20., 65.5, -5.)
POINT_RightEar = (-100., -77.5, -6.)
POINT_LeftEar = (-100., 77.5, -6.)
POINT_Nose = (21., 0., -48.)
POINT_Stommion = (10., 0., -75.)
POINT_Menton = (0., 0., -133.)

NOSE=30
RIGHT_EYE=36
LEFT_EYE=45
RIGHT_SIDE=0
LEFT_SIDE=16
EYEBROW_RIGHT=21
EYEBROW_LEFT=22
MOUTH_UP=51
MOUTH_DOWN=57
MOUTH_RIGHT=48
MOUTH_LEFT=54
SELLION=27
MOUTH_CENTER_TOP=62
MOUTH_CENTER_BOTTOM=66
MENTON=8

model_points = np.array([
    POINT_Sellion, POINT_RightEye, POINT_LeftEye, POINT_RightEar, POINT_LeftEar, POINT_Menton, POINT_Nose, POINT_Stommion
])


class PoseEstimation:


    def __init__(self):
        self.rotation_vector = None
        self.translation_vector = None


    def pose(self, im, shape, frame):

        size = im.shape
        focal_length = size[1]
        center = (size[1]/2, size[0]/2)
        camera_matrix = np.array(
                         [[focal_length, 0, center[0]],
                         [0, focal_length, center[1]],
                         [0, 0, 1]], dtype="double"
                         )
 
        stomion = (shape[MOUTH_CENTER_TOP] + shape[MOUTH_CENTER_BOTTOM]) * .5
        image_points = np.array([
            shape[SELLION],
            shape[RIGHT_EYE],
            shape[LEFT_EYE],
            shape[RIGHT_SIDE],
            shape[LEFT_SIDE],
            shape[MENTON],
            shape[NOSE],
            stomion
        ], dtype="double")

        camera_matrix = np.array([[focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]], dtype = "double")

        dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
        (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
 
        # print("Rotation Vector:\n {0}".format(rotation_vector))
        # print("Translation Vector:\n {0}".format(translation_vector))
        
        # Project a 3D point (0, 0, 1000.0) onto the image plane.
        # We use this to draw a line sticking out of the nose        
        
        (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
        
        for p in image_points:
            cv2.circle(frame, (int(p[0]), int(p[1])), 1, (0,0,255), -1)
        
        # p1 = ( int(image_points[0][0]), int(image_points[0][1]))
        # p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))        
        # cv2.line(frame, p1, p2, (255,0,0), 2)

        # axes = np.array([(0,0,0),(10,0,0),(0,10,0),(0,0,10)])
        length = 50.
        axes = np.array([(0.,0.,0.),(length,0.,0.),(0.,length,0.),(0.,0.,length)])
        (projected_axes, _) = cv2.projectPoints(axes, rotation_vector, translation_vector, camera_matrix, dist_coeffs)

        p0 = tuple(projected_axes[0, 0].astype(int))
        pz = tuple(projected_axes[3, 0].astype(int))
        py = tuple(projected_axes[2, 0].astype(int))
        px = tuple(projected_axes[1, 0].astype(int))
        cv2.line(frame, p0, pz, (255, 0, 0), 1)
        cv2.line(frame, p0, py, (0, 255, 0), 1)
        cv2.line(frame, p0, px, (0, 0, 255), 1)

        self.rotation_vector = rotation_vector
        self.translation_vector = translation_vector
        
        # import transforms3d
        # import math
        # euler_ryxz = transforms3d.euler.EulerFuncs('ryxz')
        # rv, angle = transforms3d.axangles.mat2axangle(euler_ryxz.euler2mat(math.pi/2, -math.pi/2, 0))

        # (projected_axes, _) = cv2.projectPoints(axes, rv*angle, translation_vector, camera_matrix, dist_coeffs)

        # p0 = tuple(projected_axes[0, 0].astype(int))
        # pz = tuple(projected_axes[3, 0].astype(int))
        # py = tuple(projected_axes[2, 0].astype(int))
        # px = tuple(projected_axes[1, 0].astype(int))
        # cv2.line(frame, p0, pz, (255, 0, 0), 1)
        # cv2.line(frame, p0, py, (0, 255, 0), 1)
        # cv2.line(frame, p0, px, (0, 0, 255), 1)

        return rotation_vector, translation_vector
