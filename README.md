# Bike Crash Detection System Using Machine Learning

## Project Overview

The Bike Crash Detection System is a machine learning-based project designed to detect bike accidents in real time. The system uses sensor data and a hybrid CNN-LSTM deep learning model to identify crash events and generate alerts.

The main objective of this project is to improve rider safety by detecting accidents quickly and reducing emergency response time.

## Objectives

- Detect bike crash events automatically.
- Analyze bike movement using sensor data.
- Identify crash and normal riding conditions.
- Reduce false crash detection.
- Generate emergency alerts after crash detection.

## Technologies Used

### Programming Language
- Python

### Machine Learning Technologies
- Convolutional Neural Network (CNN)
- Long Short-Term Memory (LSTM)
- Deep Learning

### Libraries
- TensorFlow
- Keras
- NumPy
- Pandas
- OpenCV

### Sensors
- Accelerometer
- Gyroscope
- GPS Module

## System Workflow

1. Collect sensor data from bike movement.
2. Preprocess and clean the collected data.
3. Extract important motion features.
4. Apply CNN-LSTM model for analysis.
5. Classify the event:
   - Crash Detected
   - Normal Riding
6. Generate alert notification.

## Features

- Real-time crash detection
- Sensor-based monitoring
- Machine learning prediction
- Emergency alert generation
- Location tracking support
- Improved accident response time

## Project Structure

```
Bike-Crash-Detection--Mini-Project/

├── Source_Code/
│   └── Complete project source code

├── Documentation/
│   ├── Project_Report.pdf
│   ├── Design_Document.pdf
│   └── User_Manual.pdf

├── Progress_Reports/
│   ├── Weekly progress reports
│   └── Meeting notes

├── Deliverables/
│   ├── Final_Presentation.pptx
│   ├── Screenshots
│   └── Demo files

└── README.md
```

## Installation

1. Download or clone the repository.

```
git clone <repository-link>
```

2. Install required libraries.

```
pip install tensorflow
pip install numpy
pip install pandas
pip install opencv-python
```

3. Open the Source_Code folder.

4. Run the project files.

## Working Principle

The system continuously monitors bike movement using sensors. The collected data is processed and given to the CNN-LSTM model. CNN extracts important features, while LSTM analyzes motion patterns over time. If an accident pattern is detected, the system generates an emergency alert.

## Results

The system is able to classify crash and non-crash events using machine learning techniques and provides reliable accident detection.

## Future Scope

- Mobile application integration
- Cloud-based monitoring
- IoT implementation
- Smart helmet integration
- Emergency service connection
- Improved accuracy with larger datasets

## Conclusion

The Bike Crash Detection System provides an intelligent solution for accident detection using sensors and deep learning. The system helps improve road safety by enabling faster accident detection and emergency response.

## Author

Mini Project Team
