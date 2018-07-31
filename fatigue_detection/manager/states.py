
from aenum import Enum

DetectionState = Enum('DetectionState', "ok detected failed")
DetectionTransition = Enum('DetectionTransition', "ok detected failed recovered")

DisplayState = Enum('DisplayState', "loading ok warn0 warn1 warned0 warned1 failed")
DisplayTransition = Enum('DisplayTransition', "loaded ok warn failed recovered")

