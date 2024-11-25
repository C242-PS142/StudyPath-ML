# Big Five Personality Prediction API
This project provides a RESTful API for predicting Big Five Personality traits based on input data using a pre-trained TensorFlow model. It uses Flask as the web framework.

## Table of Contents
- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [Setup](#setup)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Example Request](#example-request)
- [Example Response](#example-response)

## Project Overview
This API takes an array of 50 numerical values representing user responses, processes them through a machine learning model, and returns predictions for the five personality traits based on the Big Five Personality framework:

* Keterbukaan Sosial, Energi, dan Antusiasme (Extroversion)
* Kestabilan Emosi (Neuroticism)
* Kesepakatan (Agreeableness)
* Ketelitian (Conscientiousness)
* Keterbukaan terhadap Pengalaman (Openness)

## Requirements
* Python 3.8 or higher
* TensorFlow 2.x
* Flask
* NumPy

## Setup
1. Clone this repository:
```bash
git clone https://github.com/C242-PS142/StudyPath-ML.git
cd StudyPath-ML
```
2. Install the dependencies:
```bash
pip install -r requirements.txt
```
3. Ensure the `model.h5` file is in the project root directory. This is the pre-trained TensorFlow model.

## Running the API
To start the Flask server locally:
```bash
python app.py
```
The server will run on `http://127.0.0.1:5000`.

## API Endpoints
# POST `/predict`

Description: Predicts the Big Five Personality traits based on input data.

Request Body:

* Content-Type: application/json
* Parameters: A JSON object with an input field containing an array of 50 numerical values.

### Example Request
```json
{
    "input": [0.5, 1.2, 3.4, ..., 2.1]  // 50 values in total
}
```

### Example Response
```json
{
    "prediction": {
        "Keterbukaan Sosial, Energi, dan Antusiasme": 3.75,
        "Kestabilan Emosi": 2.45,
        "Kesepakatan": 4.20,
        "Ketelitian": 3.80,
        "Keterbukaan terhadap Pengalaman": 4.10
    }
}
```
