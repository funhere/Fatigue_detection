#!/bin/sh

if [ -z "$2" ]
then
  echo "Wrong usage: $0 $1 $2"
  echo "$0 <input_video_root_path> <output_root_path>"
  echo "At project root,"
  echo "sh sh/run_for_dir.sh ~/Works/FtWorks/dataset ~/Works/FtWorks/experiments"
fi

FILES=`find $1 -type f -depth 2 -name "*.mp4"`
for f in $FILES
do
  DIR=`dirname $f`
  echo "$DIR"
  mkdir -p "$2/`basename $DIR`"

  sleep 1
  echo "python -m driver_tracking.distraction_detector -p resources/models/shape_predictor_68_face_landmarks.dat -f $f"
  python -m driver_tracking.distraction_detector -p resources/models/shape_predictor_68_face_landmarks.dat -f $f

  sleep 1
  echo "ls -Art out/video | grep `basename $f` | grep ".avi$" | tail -n 1"
  RECENT_VIDEO_FILE=`ls -Art out/video | grep $(basename $f) | grep ".avi$" | tail -n 1`
  if [ -f "out/video/$RECENT_VIDEO_FILE" ]
  then  
    echo "mv out/video/$RECENT_VIDEO_FILE $2/`basename $DIR`/"
    mv "out/video/$RECENT_VIDEO_FILE" "$2/`basename $DIR`/"
    echo "mv" "out/logs/dt_experiment.log" "$2/`basename $DIR`/dt_experiment-$(basename $f).log"
    mv "out/logs/dt_experiment.log" "$2/`basename $DIR`/dt_experiment-$(basename $f).log"
    echo "mv" "out/logs/dt_experiment.csv" "$2/`basename $DIR`/dt_experiment-$(basename $f).csv"
    mv "out/logs/dt_experiment.csv" "$2/`basename $DIR`/dt_experiment-$(basename $f).csv"
  fi

  echo
done
