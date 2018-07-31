#!/bin/bash

LOG_DIR=out/logs/
OLD_DIR=out/logs/old/

mkdir -p ${OLD_DIR}
mv ${LOG_DIR}dt_experiment.log ${OLD_DIR}dt_experiment.log.`date +%Y-%m-%d_%H`
mv ${LOG_DIR}dt_experiment.csv ${OLD_DIR}dt_experiment.csv.`date +%Y-%m-%d_%H`



