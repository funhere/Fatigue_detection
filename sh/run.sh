#!/bin/bash

FILES=`find $1 -type f -name *.mp4`
echo $FILES
for f in $FILES
do
  DIR=`dirname $f`
  echo "python -m driver_tracking.distraction_detector.py -p resources/models/shape_predictor_68_face_landmarks.dat -f $f"
  #python -m driver_tracking.distraction_detector.py -p resources/models/shape_predictor_68_face_landmarks.dat -f "$f"

  echo "mkdir -p $2/$DIR"
  #mkdir -p "$2/$DIR"
  echo "mv out/video/... $2/$DIR/"
  echo "mv out/logs/dt_experiments.log $2/$DIR/"
  echo "mv out/logs/dt_experiments.csv $2/$DIR/"
  echo
done
