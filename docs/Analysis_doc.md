In order to analysis the relation between drowsiness and the detection information from a driving video, we'd like to do something listed below:

0. Get ready:

Before the work started, set up the environment for both project and log analysis (ElasticSearch, FileBeat, etc.)

1. Labeling of videos:

The label helps to train the model check the accuracy of the algorithm. Checked the data set, chose a video carefully which included both usual driving and drowsy period, then labeled the video to 0 or 1 by each of the frame of the log file which contained the information such as eyes changing and rotation of head throughout the video. The value of the labeling means the state of the driver at that time, and is determined by human.

2. Corrected the information:

The log may has wrong data. Fixed the localization information in the log caused by the difference between surface of camera and surface of driver face to get a better angle. What's more, some period of the video may not be detected correctly, so that no information will be get, so the state of the driver at these time should be checked.

3. Process of analysis:

We hope to get the prediction that whether the driver is drowsy or not at any time as accurate as possible based on mainly the eyes changing and rotation of head (three directions included x, y and z) information. Now that we got the labeled data, we can analyze like this:
(1) try to find the possible drowsy period,
(2) visualization the result,
(3) check the result by confusion matrix.

4. Details of the code:

Reference: https://cpyplgit01.x.smflc.co.jp/Org-DriversCompass/driving-alert/tree/tasks/threshold_tuning/analysis/README.md

