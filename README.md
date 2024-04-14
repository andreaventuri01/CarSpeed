# OBJECT TRACKER AND CAR SPEED DETECTOR
This is a project that me and my university collegue Gianluca Maugeri developed during our Master's Degree in Computer Engineering at the University of Modena and Reggio Emilia.

The goals of the project were multiple:
- Segment the video frames
- Detect the object on and off the road
- Track the other cars
- Detect the speed of the other cars, given the current speed of the reference car (the one on which the camera is installed).

**This is a Master's Degree class project, and such was its only purpose. Surely, there are thousands of better ways to do this kind of project. Moreover, it dates back to 2019 (perhaps even 2018). Hence, the pretrained model employed here are certainly obsolete! Eventually I will update everything, but the process will certainly take a long time (pull requests are more than welcome here!)**

### BEFORE THE EXECUTION:
Make sure you have installed the libraries present in requirements.txt

### EXAMPLE OUTPUT
[![Output Example](https://img.youtube.com/vi/G6mmCd5I_4E/0.jpg)](https://www.youtube.com/watch?v=G6mmCd5I_4E)

### HOW IT WORKS
Coming soon

### CODE STRUCTURE
Files:
- object_tracker.py: main file to execute.
- models.py: contains the network model for the detection
- moving_object.py: contains the MovingObject class
- sort.py: The SORT algorithm: Original code on: https://github.com/abewley/sort
- evaluation.py: Contains the code for the evaluation of segmentation.

Directories:
- config: Contains the configuration file of yolov3. https://github.com/pjreddie/darknet
- eval: contains the prediction frames and its respective hand-labeled groundtruth frame for evaluation purposes (see evaluation.py)
- pretrained_models: contains the pretrained DeepLabV3 and ResNet used in segmentation.
- segmentation_models: contains the implementation of DeepLabV3 architecture. Original Code on: https://github.com/fregu856/deeplabv3
- utils: contains utilities for the code.
- videos: directory where dataset videos should be put.
	  It contains 2 Dr(eye)ve example: 02 and 11 with its corrispective output (30 seconds each).


### HOW TO EXECUTE:
```python object_tracker.py [-p <path-to-video-directory>][-fps <fps>][-mf <minframes>][-sb <seconds-to-wait>][-se <seconds-to-end>]```

Options:
- `p <path>`: optional. Default 'videos/02/'. It specifies the path of the video directory (example: videos/02/).	NB: video_garmin.avi and speed_course_coord.txt are required in the selected directory, otherwise the program won't work. These names and extensions of the files are mandatory (they are the same as provided in DR(eye)VE dataset).

- `-fps <fps>`: optional. Default = 25. Frame per seconds of the video in input.

- `-mf <minframes>`: optional. Default = 10. Number of frames for the speed sampling.

- `-sb <seconds-to-wait>`: optional. Default = 0. This specifies how many seconds of the video should not be included in the analysis. SHOULD BE LOWER THAN 300 and LOWER THAN `se` argument if specified.

- `-se <seconds-to-wait>`: optional. Default = 300. This specifies how many seconds of the video to include in the analysis starting from `sb`. SHOULD BE LOWER or EQUAL THAN 300 and HIGHER THAN `sb`.

The outputs of the model are located in the same directory specified by `-p` argument:
- video_garmin-det.avi is the output of the detection phase with speed evaluation of moving objects and position evaluation of objects on the road
- video_garmin-seg.avi is the output of the segmentation phase.
