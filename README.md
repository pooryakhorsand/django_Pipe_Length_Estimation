# Pipe Length Estimation on Production Line

## Overview

This project is a Django web application developed for the **Iran National Steel Group**. It estimates the lengths of pipes on the production line using a combination of image processing and machine learning techniques. The application captures images of pipes as they reach the end of the production line and utilizes a pre-trained segmentation model to accurately segment the pipe from the background.

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Videos](#Videos)
- [Research Paper](#Research-Paper)
Research Paper
## Features

- **Automated Image Capture**: Captures screenshots of pipes at the production line.
- **Segmentation Model**: Uses a custom-trained segmentation model for accurate pipe detection.
- **Length Estimation**: Estimates pipe lengths based on predefined labels and distances between them.

## How It Works

1. **Image Capture**: As a pipe reaches the end of the production line, a camera automatically captures a screenshot.
2. **Segmentation**: The captured image is processed using a pre-trained segmentation model, specifically trained on a custom dataset of pipe images.
3. **Length Estimation**: By identifying the first and last points of the segmented pipe and comparing these points with defined labels, the application accurately estimates the pipe's length.



## Videos

Here are demonstration videos of the Helmet Detection Application.


https://github.com/user-attachments/assets/f14603d3-c476-4689-99b2-396e1b83d16b

### Original Image
![2002](https://github.com/user-attachments/assets/9f21dd4d-b37e-4231-b29b-1fbf4dc720c4)

### Segmented Image
![segmented_image](https://github.com/user-attachments/assets/511267b5-2f9a-477a-b1b0-f7f4a8de0740)

## Research Paper

This project is based on the methodology described in our research paper: **Controlling seamless steel pipe thickness in 
production process using computer vision and deeplearning techniques**. The paper outlines the process of using a custom-trained segmentation model for accurate pipe length estimation on the production line.


[Controlling Steel Pipe Thickness.pdf](https://github.com/user-attachments/files/17278943/Controlling.Steel.Pipe.Thickness.pdf)

