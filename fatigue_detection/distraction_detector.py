'''
# Command to use to run this program...
python3 detect_drowsiness.py \
--shape-predictor models/shape_predictor_68_face_landmarks.dat \
--alarm sounds/bell.wav

# Link.
https://www.pyimagesearch.com/2017/05/08/drowsiness-detection-opencv/

'''

# import ipdb; ipdb.set_trace()
# import pudb; pu.db()

import numpy as np

import argparse
import time
import dlib
import cv2
import math

import profilehooks
import warnings
import ntpath
# import logging
# logging.basicConfig(filename='experiment.log',level=logging.DEBUG)

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
print(sys.path)

from threading import Thread

# from driver_tracking.conf import static
from driver_tracking.logging.log_data_manager import LogDataManager, static
from driver_tracking.head.pose_estimation import PoseEstimation

# from driver_tracking.manager.display_machine import DisplayMachine
from driver_tracking.manager.distraction_machine import DistractionMachine, DisplayMachine
from driver_tracking.manager.drowsiness_machine import imutils, DrowsinessMachine

#import imutils
import imutils.video

#from utils import WebcamVideoStream
#from driver_tracking.utils import FPS
from imutils.video import FPS

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", type=str, default="resources/models/shape_predictor_68_face_landmarks.dat",
	help="path to facial landmark predictor")
ap.add_argument("-a", "--alarm", type=str, default="",
	help="path alarm .WAV file")
ap.add_argument("-w", "--webcam", type=int, default=0,
	help="index of webcam on system")
ap.add_argument("-f", "--video_file", type=str, default="",
	help="input video path")

args = vars(ap.parse_args())


print("[INFO] loading facial landmark predictor")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])


video_path = args["video_file"]
if video_path != "":
	#from imutils.video import FileVideoStream
	print("[INFO] starting video stream from file...")
	vs = imutils.video.FileVideoStream(video_path).start()
	time.sleep(1.0)
	print(vs.more())
	video_file_name = ntpath.basename(video_path)
else:
	print("[INFO] starting video stream thread...")
	vs = imutils.video.VideoStream(src=args["webcam"]).start()
	time.sleep(1.0)
	video_file_name = "webcam"

pose = PoseEstimation()

fps = FPS().start()

@profilehooks.profile
def detector_timecall(*args):
	return detector(*args)


@profilehooks.profile
def predictor_timecall(*args):
	return predictor(*args)


# Workaround:
# Without print statement, exception is not shown. 
# Only following statement is shown: "/Users/leeilgu/anaconda3/envs/ddd36/bin/python: Error while finding module specification for 'driver_tracking.distraction_detector.py' (AttributeError: module 'driver_tracking.distraction_detector' has no attribute '__path__')"
# I don't know why.
print("while loop")

def main():
	i_frame = 0

	logger = LogDataManager()
	shared_drowsiness_machine = DrowsinessMachine()
	shared_distraction_machine = DistractionMachine()

	writer = None

	while True:

		i_frame += 1

		if i_frame % 10000 == 0:
			print(i_frame)
		
		if isinstance(vs, imutils.video.FileVideoStream) and not vs.more():
			time.sleep(0.1)
			if not vs.more():
				print("No more for 0.1s.", vs, vs.more())
				time.sleep(1)
				if not vs.more():
					print("No more for 1.1s.", vs, vs.more())
					break

		frame = vs.read()
		
		# update the FPS counter
		fps.update()		

		frame = imutils.resize(frame, width=450)
		(height, width) = frame.shape[:2]
		if writer is None:
			# https://www.pyimagesearch.com/2016/02/22/writing-to-video-with-opencv/
			fourcc = cv2.VideoWriter_fourcc(*'MJPG')
			writer = cv2.VideoWriter('%sdriver_recording-%s_%d.avi' % 
				(static.exp_conf.VIDEO_DIR, video_file_name, static.exp_conf.i_experiment), fourcc, 25.0, (width, height), True)

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# detect faces in the grayscale frame
		rects = logger.timeit('detect01', i_frame, 
			detector, *(gray, 0)
			)

		for rect in rects:
			# determine the facial landmarks for the face region, then
			# convert the facial landmark (x, y)-coordinates to a NumPy
			# array
			shape = logger.timeit('predict', i_frame, 
				predictor, *(gray, rect)
				)
			shape = imutils.face_utils.shape_to_np(shape)
			pose.pose(gray, shape, frame)

			shared_drowsiness_machine.handle_next_frame(shape, frame, i_frame)
			shared_distraction_machine.handle_next_frame(pose, frame, i_frame)
		if not rects:
			shared_drowsiness_machine.handle_error_frame(frame, i_frame)
			shared_distraction_machine.handle_error_frame(frame, i_frame)
	

		# img = logger.plot(plt)
		# cv2.imshow("plot", img)

		# show the frame
		cv2.imshow("Frame", frame)
		writer.write(frame)
		key = cv2.waitKey(1) & 0xFF

		# plt.show(False)
		# plt.draw()
	
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break
		# print("end of while")

	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
	
	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()
	if writer:
		writer.release()

if __name__ == "__main__":
	try:
		main()
		print("end")
	except Exception as e:
		print("Error", e)
		raise e
