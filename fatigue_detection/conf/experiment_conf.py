
import time
import os

class ExperimentConfig:
	i_experiment = int(time.strftime('%Y%m%d%H%M%S'))

	OUT_DIR = 'out/'
	VIDEO_DIR = OUT_DIR + 'video/'
	LOG_DIR = OUT_DIR + 'logs/'

	LOGGER_NAME = 'experiment'

	os.makedirs(LOG_DIR, exist_ok=True)
	os.makedirs(VIDEO_DIR, exist_ok=True)

exp_conf = ExperimentConfig
