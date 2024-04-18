# ROAD OBJECT TRACKER AND CAR SPEED DETECTOR
This project was developed by my university colleague [Gianluca Maugeri](https://github.com/gianlucamaugeri) and myself during our Master's Degree in Computer Engineering at the University of Modena and Reggio Emilia.

Though it was initially a class project, it includes several notable features. Most significantly, we managed to "accurately" track the speed of vehicles in the video using only the speed of the recording camera and the dimensions of the reference car's hood.

The project had several goals:
- Segmenting video frames
- Identifying objects on and off the road
- Tracking other vehicles
- Estimating the speeds of other cars based on the speed of the reference car, which carried the camera

Our work utilized the DR(eye)VE dataset, which can be found here: [dataset page](https://aimagelab.ing.unimore.it/imagelab/page.asp?IdPage=8) 

**DISCLAIMER #1: This is a Master's Degree class project, and such was its only purpose. It was completed in 2019 (possibly even 2018), and the technology used, including pre-trained models, is undoubtedly outdated. I plan to update it eventually, but that will be a lengthy process. Meanwhile, feel free to fork the project and modify any part of the code from that period!**

## EXAMPLE OUTPUT
[![Output Example](https://img.youtube.com/vi/G6mmCd5I_4E/0.jpg)](https://www.youtube.com/watch?v=G6mmCd5I_4E)

## HOW IT WORKS
Scene segmentation and object tracking are achieved through straightforward operations. We input the current frame into two separate Deep Learning (DL) models that have been pre-trained for these specific tasks.

We utilize DeepLabV3 ([Original Code](https://github.com/fregu856/deeplabv3)) for segmentation and Yolov3 ([Original Code](https://github.com/pjreddie/darknet)) for object detection. For tracking, we use SORT ([Original Code](https://github.com/abewley/sort)). Although these models were adequate at the time of development, they are now considered outdated.

The unique aspect of our project is the method of speed detection.

Considering the camera is moving, it's essential to know the speed of our egocentric camera to calculate the absolute speeds of other moving objects. Fortunately, the DR(eye)VE dataset provides this data in a text file for each video.

Our process is outlined as follows:
1. **PROJECTION**: We convert the scene into a bird's-eye view.
2. **PIXEL DISTANCE**: We measure the distance from the camera to the objects in pixels.
3. **METER DISTANCE**: We convert the pixel distance to real-world meters.
4. **SPEED COMPONENTS**: We calculate the speed's x and y components.
5. **FINAL SPEED**: We combine these components to determine the overall speed.


### PROJECTION
In order to find the pixel distance, we need to deal with perspective.
This would be straightforward with specific camera parameters, but in their absence, we turn to homographies ([OpenCV tutorial](https://docs.opencv.org/4.x/d9/dab/tutorial_homography.html)). Essentially, a planar homography transforms how points on a plane, seen by one camera, would appear from another camera at a different viewpoint. Our goal is to transform the frame captured by our camera to a bird's-eye perspective. An illustrative example is shown in the figure below.

![Homographic transformation](image.png)

The concept is straightforward: by achieving a bird's-eye view of the street and every object on it, we eliminate the complications of perspective, making it easier to measure distances directly.

Without delving into the complex mathematics, we need to identify the elements of the 3x3 matrix \(H\) that facilitate this transformation:
```math
\begin{bmatrix} t_i  x'_i \\\ t_i y_i' \\\ t_i \end{bmatrix} = H \cdot \begin{bmatrix} x_i \\\ y_i \\\ 1 \end{bmatrix} 
```

where $x_i, y_i$ are coordinates in the original plane, and $x_i', y_i'$ are coordinates in the transformed, bird's eye view plane.

This transformation requires manually selecting the coordinates of quadrangle vertices in the source frame (the normal street view from our camera) and matching them to the corresponding vertices in the bird's-eye view.

We select points such that the street lines appear parallel in the bird's-eye view.

**DISCLAIMER #2: Ideally, this point selection should be customized for each video to achieve maximum accuracy. However, due to the consistent camera angle across all videos, we use the same transformation matrix for simplicity. Despite this approximation, the results have been satisfactory across various dataset videos.**

With the bird's-eye view obtained, we move on to the next phase.

### PIXEL DISTANCE
Having transformed our footage into a bird's-eye view, we now calculate the distance from the reference camera to the vehicles on the street.

We use the center $c$ of the upper end of our car's hood as the reference point. For moving objects, the reference point is the center of the base of their bounding box, identified during the detection phase. The pixel distance for each object $i$ in the bird’s eye view is calculated as follows:
```math
d_x[i] = x[i] - x[c]; 
```
```math
d_y[i] = y[i] - y[c]
```
Here, $x[i]$ represents the pixel coordinates of object $i$ in the bird's eye view.

### METER DISTANCE
To convert these pixel distances into meters, we calculate the meter-per-pixel ratio using the known length of our car's hood in the bird's-eye perspective.

Ratio m/px: 0.09717

### SPEED COMPONENTS
To estimate the speed of cars in the scene, we assume they travel at a constant speed between two consecutive frames.

For each tracked vehicle, the speed components along the x and y axes (in m/s) are calculated using the following formulas:
```math
v_x(i) = \frac{d_x(i) - d'_x(i)}{1/FPS}
```
```math
v_y(i) = \frac{d_y(i) - d'_y(i)}{1/FPS}
```
Here, $d(i)$ represents the distance of the object in the current frame, and $d'(i)$ represents its distance in the previous frame (see Figure below).

![Car distance](image-1.png)

Calculating speeds at every frame proved to be imprecise, so to stabilize the measurements, we compute speeds over intervals of `<min_frames>` frames, maintaining the assumption of constant speed over these intervals. The parameter `<min_frames>` can be adjusted at runtime (refer to the [HOW TO EXECUTE](#how-to-execute) section).

The modified formulas become:
```math
v_x(i) = \frac{d_x(i) - d'_x(i)}{min\_frames/FPS}
```
```math
v_y(i) = \frac{d_y(i) - d'_y(i)}{min\_frames/FPS}
```

In addition, to calculate the final vertical speed component $v^f_y(i)$, we add the camera’s speed to the computed y-axis speed.
```math
v^f_y(i) = v_y(i) + v(camera)
```
This calculation is feasible because the dataset provides the camera speed $v(camera)$ for each timeframe.

### FINAL SPEED
The total speed is derived by combining the x and y components, as shown below:

![Final speed](image-2.png)

Moreover, to make our results more robust, we display the mean of the speeds we find in two consecutive frames.


## BEFORE THE EXECUTION:
Make sure you have installed the libraries present in requirements.txt.


## CODE STRUCTURE
Files:
- object_tracker.py: main file to execute.
- models.py: contains the network model for the detection
- moving_object.py: contains the MovingObject class
- sort.py: The SORT algorithm: Original code on: https://github.com/abewley/sort
- evaluation.py: Contains the code for the evaluation of segmentation.

Directories:
- config: Contains the configuration file of yolov3. https://github.com/pjreddie/darknet
- eval: contains the prediction frames and their respective hand-labeled groundtruth frame for evaluation purposes (see evaluation.py)
- pretrained_models: contains the pretrained DeepLabV3 and ResNet used in segmentation.
- segmentation_models: contains the implementation of DeepLabV3 architecture. Original Code on: https://github.com/fregu856/deeplabv3
- utils: contains utilities for the code.
- videos: directory where dataset videos should be put.
	  It contains 2 Dr(eye)ve examples (02 and 11) with their corresponding outputs (30 seconds each).


## HOW TO EXECUTE:
```python object_tracker.py [-p <path-to-video-directory>][-fps <fps>][-mf <minframes>][-sb <seconds-to-wait>][-se <seconds-to-end>]```

Options:
- `p <path>`: optional. Default 'videos/02/'. It specifies the path of the video directory (example: videos/02/).	NB: video_garmin.avi and speed_course_coord.txt are required in the selected directory, otherwise the program won't work. These names and extensions of the files are mandatory (they are the same as provided in DR(eye)VE dataset).

- `-fps <fps>`: optional. Default = 25. Frames per second of the video in input.

- `-mf <minframes>`: optional. Default = 10. Number of frames for the speed sampling.

- `-sb <seconds-to-wait>`: optional. Default = 0. This specifies how many seconds of the video should not be included in the analysis. SHOULD BE LOWER THAN 300 and LOWER THAN `se` argument if specified.

- `-se <seconds-to-wait>`: optional. Default = 300. This specifies how many seconds of the video to include in the analysis starting from `sb`. SHOULD BE LOWER or EQUAL THAN 300 and HIGHER THAN `sb`.

The outputs of the model are located in the same directory specified by the `-p` argument:
- video_garmin-det.avi is the output of the detection phase with speed evaluation of moving objects and position evaluation of objects on the road
- video_garmin-seg.avi is the output of the segmentation phase.
