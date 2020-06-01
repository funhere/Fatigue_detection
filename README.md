

### Prerequisites
1. python
2. opencv
3. dlib

```sh
brew install opencv --with-ffmpeg
brew install graphviz
brew install cmake
```

#### Optional
1. anaconda

### Installation
```sh
#python 3.6
conda create -n drowsiness_detection python=3.6
source activate drowsiness_detection

pip install -r requirements.txt
```


### Run
```sh
# with a video file input
python -m driver_tracking.distraction_detector -p resources/models/shape_predictor_68_face_landmarks.dat -f resources/sample_inputs/your_detection_movie.mov

# webcam
python -m driver_tracking.distraction_detector -p resources/models/shape_predictor_68_face_landmarks.dat
```

### Debug
```sh
ipdb3 driver_tracking/distraction_detector.py -p resources/models/shape_predictor_68_face_landmarks.dat -f resources/sample_inputs/your_detection_movie.mov

pudb3 driver_tracking/distraction_detector.py -p resources/models/shape_predictor_68_face_landmarks.dat -f resources/sample_inputs/your_detection_movie.mov
```

#### Run

### Tested environment
1. imac MacOS 10.13.3, i5 1.4 GHz, 8GB Memory
    1. Python 3.6
	1. opencv 3.4
1. Raspberry pi 3
    1. Python 3.6
    1. opencv 3.3



