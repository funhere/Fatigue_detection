import transitions.extensions

from ..manager.states import DetectionState, DetectionTransition, DisplayState, DisplayTransition
from ..manager.display_machine import DisplayMachine
from ..video.detection_rules.detection import Detection
from ..video.frame_series import FrameSeries


display_machine = DisplayMachine()


class DetectionMachine(object):


	# pylint: disable-msg=E1101
	def __init__(self):
		self.states: [str] = [x.name for x in list(DetectionState)]
		self.transitions: [[str]] = [
			[DetectionTransition.detected.name, '*', DetectionState.detected.name],
			[DetectionTransition.failed.name, '*', DetectionState.failed.name],
			#[DetectionTransition.recovered.name, DetectionState.failed.name, DetectionState.ok.name],
			[DetectionTransition.ok.name, '*', DetectionState.ok.name]
		]
		self.machine: transitions.extensions.HierarchicalGraphMachine = transitions.extensions.HierarchicalGraphMachine(self, states=self.states, initial=DetectionState.ok.name, transitions=self.transitions, ignore_invalid_triggers=True)

		self.frame_series: FrameSeries = FrameSeries()


	def add_frame(self, frame: Detection):
		self.frame_series.add_frame(frame)

		display_transition = {
			DetectionState.ok: display_machine.to_ok,
			DetectionState.detected: display_machine.warn,
			DetectionState.failed: display_machine.failed
		}
		display_transition[frame.state](frame.i_frame)

		detection_transition = {
			DetectionState.ok: self.ok,
			DetectionState.detected: self.detected,
			DetectionState.failed: self.failed
		}
		detection_transition[frame.state]()


	def state_as_number(self) -> float:
		return {
			DetectionState.detected.name: 1,
			DetectionState.ok.name: 0,
			DetectionState.failed.name: -1
		}[self.state]

	
		

# import playsound
# def sound_alarm(path):
# 	playsound.playsound(path)


			# # check to see if an alarm file was supplied,
			# # and if so, start a thread to have the alarm
			# # sound played in the background
			# if args["alarm"] != "":
			# 	t = Thread(target=sound_alarm,
			# 		args=(args["alarm"],))
			# 	t.deamon = True
			# 	t.start()

if __name__ == "__main__":
	import os
	os.makedirs('out/docs', exist_ok=True)

	m = DetectionMachine()
	m.get_graph().draw('out/docs/detection_machine.png', prog='dot')
