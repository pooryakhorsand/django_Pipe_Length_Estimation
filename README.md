# Pipe Length Estimation on Production Line

## Overview

This project is a Django web application developed for the **Iran National Steel Group**. It estimates the lengths of pipes on the production line using a combination of image processing and machine learning techniques. The application captures images of pipes as they reach the end of the production line and utilizes a pre-trained segmentation model to accurately segment the pipe from the background.

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Videos](#Videos)


## Features

- **Automated Image Capture**: Captures screenshots of pipes at the production line.
- **Segmentation Model**: Uses a custom-trained segmentation model for accurate pipe detection.
- **Length Estimation**: Estimates pipe lengths based on predefined labels and distances between them.

## How It Works

1. **Image Capture**: As a pipe reaches the end of the production line, a camera automatically captures a screenshot.
2. **Segmentation**: The captured image is processed using a pre-trained segmentation model, specifically trained on a custom dataset of pipe images.
3. **Length Estimation**: By identifying the first and last points of the segmented pipe and comparing these points with defined labels, the application accurately estimates the pipe's length.

For a more detailed explanation of the methodology, please refer to our [published paper](link_to_paper).

## Videos

Here are demonstration videos of the Helmet Detection Application
