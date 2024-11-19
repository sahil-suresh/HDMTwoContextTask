# HDM Dot Cloud Task

This repository contains a Python script for running the **Dot Cloud Task**, a cognitive psychology experiment designed to study decision-making processes and cognitive flexibility. The task involves participants making judgments based on visual stimuli, specifically dot clouds with varying proportions of red and yellow dots, and images of faces and scenes.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Experiment Details](#experiment-details)
- [Dependencies](#dependencies)
- [Credits](#credits)
- [License](#license)

## Overview

The Dot Cloud Task presents participants with a series of trials where they must determine the predominant color in a dot cloud and then make a decision based on that color. The task aims to investigate how participants adapt to changing contexts and mappings between stimuli and responses.

## Features

- **Customizable Experiment Parameters:** Set parameters like difficulty levels, inter-stimulus intervals (ISI), inter-trial intervals (ITI), and more via a user-friendly GUI.
- **Tutorial Instructions:** Option to include a tutorial phase to familiarize participants with the task.
- **Randomized Trial Difficulties and Contexts:** Trials vary in difficulty and context to prevent predictability.
- **Data Logging:** Participant responses, reaction times, and accuracy are recorded and saved in a CSV file.
- **Compatibility with Behavioral and fMRI Methods:** Adjustable settings to accommodate different experimental setups.

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/dot-cloud-task.git
```

### Navigate to the Project Directory

```bash
cd dot-cloud-task
```

### Install Required Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Prepare the Stimuli

#### Faces:
- Place male face images (.png or .jpg) in `Faces/male/`.
- Place female face images in `Faces/female/`.

#### Scenes:
- Place rural scene images in `Scenes/rural/`.
- Place urban scene images in `Scenes/urban/`.

#### Icons:
- Place icon images named `male.png`, `female.png`, `city.png`, and `landscape.png` in the `Icons/` directory.

### Run the Script

```bash
python dot_cloud_task.py
```

## Set Experiment Parameters

A GUI window will appear prompting you to enter experiment details such as:

- **Method:** Choose between "BEH" (Behavioral) or "fMRI".
- **Subject ID:** Enter a unique identifier for the participant.
- **Block:** Select the block number or "practice" for a practice session.
- **Difficulty Levels:** Set the proportion differences for easiest, easy, medium, and hard levels.
- **ISI and ITI Ranges:** Define the lower and upper bounds for inter-stimulus and inter-trial intervals.
- **Other Settings:** Toggle tutorial inclusion and self-guided mode, and set stimuli presentation times.

---

### Complete the Tutorial (Optional)

If the tutorial option is enabled, follow the on-screen instructions to understand the task.

---

### Participate in the Experiment

- Trials will proceed automatically unless self-guided mode is enabled.
- Use the arrow keys to make selections during the response phases.

## Experiment Details

### Trial Structure

#### Dot Cloud Presentation
- A dot cloud appears with a mixture of red and yellow dots.
- The proportion of red to yellow dots varies based on the difficulty level.

#### Stimulus Presentation

- An image is displayed, which can be a face (male/female) or a scene (city/landscape).
- The type of image to focus on is determined by the predominant color in the dot cloud.

#### Response Phase

- Participants choose among four options: **male**, **female**, **city**, or **landscape**.
- Choices are made using the arrow keys corresponding to on-screen icons.

#### Color Dominance Confirmation

- Participants are then asked to confirm which color they thought was predominant in the initial dot cloud.

#### Feedback

- Immediate feedback is displayed based on the participant's response:
  - **Correct**
  - **Incorrect**
  - **Miss**

#### Context Switching

- The mapping between dot color and task (face or scene judgment) changes covertly after a certain number of trials.
- Participants need to adapt to these changes throughout the experiment.

#### Difficulty Levels

- **Easiest:** Largest proportion difference between red and yellow dots.
- **Easy**
- **Medium**
- **Hard:** Smallest proportion difference, making it difficult to discern the predominant color.

### Responses

#### Arrow Keys:
- **Up Arrow:** One of the options (randomized per trial).
- **Down Arrow:** One of the options (randomized per trial).
- **Left Arrow:** One of the options (randomized per trial).
- **Right Arrow:** One of the options (randomized per trial).

#### No Response:
- If the participant does not respond within the set time window, it is recorded as a **miss**.

### Recorded Data
- Proportion difference of colors in the dot cloud.
- Majority color (red or yellow).
- ISI (Inter-Stimulus Interval) and ITI (Inter-Trial Interval) durations.
- Participant's chosen option and reaction time.
- Correctness of the response.
- Current context (mapping of color to task).
- Running accuracy score.

## Dependencies

- **Python 3.x**
- **Pygame:** For rendering the experiment interface.
- **Tkinter:** For the GUI to set experiment parameters.
- **NumPy:** For numerical operations.
- **Pandas:** For data handling and CSV output.

## Credits

- **Author:** Sahil  
- **Lab Affiliation:** Halassa Lab, 2024

## License

This project is licensed under the **MIT License**.
