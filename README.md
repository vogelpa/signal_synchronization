# Biosignal Synchronization Across Devices in Robotics Application

This repository contains the code to the semester thesis on "Biosignal Synchronization Across Devices in Robotics Application" along with the thesis document and presentation slides.

## Overview

The project focuses on synchronizing biosignals across different devices, specifically for robotics applications. The program is designed to process and align signals from multiple sensors to achieve synchronization. 

The program was developed and tested using **Python 3.12.5**.

## Libraries Used

The following Python libraries are required:
- `numpy` (1.26.4)
- `pandas` (2.2.2)
- `scikit-learn` (1.5.0)
- `fastdtw` (0.3.4)
- `plotly` (5.24.1)
- `matplotlib` (3.9.0)

## Configuration

The program settings should be defined in the `config.yaml` file. This file specifies:
- The **reference signal**
- The **signal to be aligned**
- Their respective **sensors**

## Usage

### Running the Main Program
To run the main synchronization pipeline, use the following command:
```bash
python main.py --config config.yaml
```

## Folder Structure
The **pipeline_steps** folder includes the modules for the single synchronization steps and in the utils folder there are functions for data management and plotting.

The **error_quantification** folder contains files to calculate the error and also the test run script. Just call
```bash
python run_tests.py
python error_quantification.py
```
The **data** folder includes some example data and also the drifted datasets used for the test runs.
The **various** folder contains utils used to extract data from the SCAI-SENSEI V2 dataset. It might be helpful for some, but can be ignored if just the pipeline wants to be used.   