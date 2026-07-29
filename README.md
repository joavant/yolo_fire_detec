# YOLO Fire Detection

This repository tracks my project. It uses a YOLOv8s model trained on over 40,000 images found on Roboflow Universe.

## Why?

In July 2026, France faced severe wildfires. Having heard that YOLO models are easy to train, I started training one using Google Colab. Initially, I thought it would be a simple project, but I quickly realized how effective the model was at detecting fire and smoke. I then looked for a small edge-computing camera that could run the model independently. 

By sharing this project on GitHub I want that anyone improve it to help prevent major wildfires.

## Installation

For this project, I used the **MaixCAM**, an all-in-one AI camera.

1. Download the `best.cvimodel` file.
2. Connect your camera and upload the file.
3. Use the `main.py` file to run the model and trigger alerts when fire is detected.
4. Download the script and update the Telegram bot token and chat ID with your own credentials.

## Proof & Results

Here is the model in action:

![Fire Detection Proof](screenshots/proof.png)
