# from transitions.extensions import HierarchicalGraphMachine
# from singleton_decorator import singleton
import transitions.extensions
import singleton_decorator


from .states import DetectionState, DetectionTransition, DisplayState, DisplayTransition

from ..logging.log_data import LogData
from ..logging.log_data_manager import LogDataManager

logger = LogDataManager()


def transition(transition: DisplayTransition, source: DisplayState, target: DisplayState, after: str):
	return {
		'trigger': transition.name,
		'source': source.name,
		'dest': target.name,
		'after': after
	}
	

@singleton_decorator.singleton
class DisplayMachine(object):

	# pylint: disable-msg=E1101
	def __init__(self):
		self.states = [x.name for x in list(DisplayState)]
		self.warnings = [DisplayState.warn0, DisplayState.warn1, DisplayState.warned0, DisplayState.warned1]
		self.transitions = [
			transition(DisplayTransition.loaded, DisplayState.loading, DisplayState.ok, 'logging'),
			transition(DisplayTransition.warn, DisplayState.failed, DisplayState.warn0, 'logging'),
			transition(DisplayTransition.warn, DisplayState.ok, DisplayState.warn0, 'logging'),
			transition(DisplayTransition.warn, DisplayState.warn0, DisplayState.warn1, 'logging'),
			transition(DisplayTransition.warn, DisplayState.warn1, DisplayState.warned0, 'logging'),
			transition(DisplayTransition.warn, DisplayState.warned0, DisplayState.warned1, 'logging'),
			transition(DisplayTransition.warn, DisplayState.warned1, DisplayState.warn0, 'logging'),
			{'trigger': DisplayTransition.ok.name,
				'source': [x.name for x in list(self.warnings)], 
				'dest': DisplayState.ok.name,
				'after': 'logging'},
			transition(DisplayTransition.failed, DisplayState.ok, DisplayState.failed, 'logging'),
			transition(DisplayTransition.failed, DisplayState.warn0, DisplayState.warn1, 'logging'),
			transition(DisplayTransition.failed, DisplayState.warn1, DisplayState.warned0, 'logging'),
			transition(DisplayTransition.failed, DisplayState.warned0, DisplayState.warned1, 'logging'),
			transition(DisplayTransition.failed, DisplayState.warned1, DisplayState.warn0, 'logging'),
			transition(DisplayTransition.ok, DisplayState.failed, DisplayState.ok, 'logging')
		]
		#self.machine = HierarchicalGraphMachine.__init__(self, states=self.states, initial=DisplayState.loading.name, transitions=self.transitions)
		self.machine = transitions.extensions.HierarchicalGraphMachine(self, states=self.states, initial=DisplayState.ok.name, transitions=self.transitions, ignore_invalid_triggers=True)
	

	def state_as_number(self) -> float:
		return {
			DisplayState.ok.name: 0.0,
			DisplayState.warn0.name: 0.5,
			DisplayState.warn1.name: 1.0,
			DisplayState.warned0.name: 1.5,
			DisplayState.warned1.name: 2.0,
			DisplayState.failed.name: -1
		}[self.state]

	def warning_text(self) -> str:
		return {
			DisplayState.ok.name: "",
			DisplayState.warn0.name: "warn0",
			DisplayState.warn1.name: "warn1",
			DisplayState.warned0.name: "warned0",
			DisplayState.warned1.name: "warned1"
		}


	def logging(self, i_frame: int):
		log = LogData(['states', 'display', 'state'], self.state_as_number(), i_frame)
		logger.add_frame_log_data([log])


if __name__ == "__main__":
	import os
	os.makedirs('out/docs', exist_ok=True)

	m = DisplayMachine()
	m.get_graph().draw('out/docs/display_machine.png', prog='dot')
