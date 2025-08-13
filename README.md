# AI Log Anomaly Detector

A full-stack web application that uses a pre-trained LSTM Autoencoder model to detect anomalies in sequences of log event IDs.

## Overview

This project provides a simple and interactive web interface to an AI model trained for anomaly detection. Users can either input a sequence of numerical log IDs directly or paste raw text from a Windows System Log file. The application will automatically parse the Event IDs from the text and use a Keras/TensorFlow model to determine if the sequence is normal or anomalous based on its reconstruction error.

The entire application, including the Python backend (Flask) and the HTML/CSS/JS frontend, is contained within a single `app.py` file for simplicity and ease of deployment.

## Features

* **Interactive Web UI:** A clean user interface for submitting log data.
* **Flexible Input:** Supports both direct comma-separated number sequences and raw text log file content.
* **Automatic Log Parsing:** Intelligently extracts Event IDs from raw log text.
* **Real-time Analysis:** Get instant feedback on whether a sequence is normal or an anomaly.
* **Detailed Results:** Shows the model's reconstruction error and the threshold used for classification.
* **Self-Contained:** The entire frontend and backend are in one Python file.
* **Pre-trained Model:** Comes with a `lstm_autoencoder.keras` model ready for use.

## Prerequisites

Before you begin, ensure you have the following installed:
* Python 3.7+
* `pip` (Python package installer)

* Go to this drive https://drive.google.com/drive/folders/19o20TH4Nol-QlZVSoVQqqDrloz4e-Rhw
 and download the model to save in your root dir

## Setup & Installation

1.  **Clone the repository or download the project files.**

2.  **Navigate to the project directory:**
    ```bash
    cd path/to/your/project
    ```

3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4.  **Install the required Python packages from `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Ensure the model is present:** Make sure the pre-trained model file `lstm_autoencoder.keras` is in the same directory as `app.py`.

## Running the Application

1.  **Start the Flask server from your terminal:**
    ```bash
    python app.py
    ```

2.  You should see output indicating the model has loaded and the server is running, like this:
    ```
    ✅ Model loaded successfully from lstm_autoencoder.keras
     * Running on http://127.0.0.1:5000
    ```

## How to Use the Application

1.  **Open your web browser** and navigate to:
    http://127.0.0.1:5000

2.  You will see the **Log Anomaly Detector** user interface. You have two ways to input data:

    * **Option 1: Paste Raw Log Text (Recommended)**
        * Copy the content from a Windows log file (like `System_log.txt`).
        * Paste the text into the large text area.
        * The app will automatically find and process the Event IDs.

    * **Option 2: Enter Sequence Manually**
        * Enter a sequence of numbers into the "Manual Sequence Input" box, separated by commas.
        * *Example of a normal sequence:* `10, 25, 10, 3, 18, 5`
        * *Example of a potentially anomalous sequence:* `10, 25, 100, 3, 18, 5`

3.  Click the **"Check for Anomaly"** button.

4.  The result will be displayed below the form, showing the status (Normal or Anomaly Detected) and the model's reconstruction error.

## (Optional) Retraining the Model

If you wish to retrain the model with new data:

1.  **Place your dataset** in the `dataset/Dataset-ThreatSlayers/` directory. The training script expects `Event_traces.csv` and `anomaly_label.csv`.

2.  **Run the training script:**
    ```bash
    python modelTrainingCode/ai_train_lstm_encoder.py
    ```
    *(Note: You may need to escape the parentheses in some shells, as shown above)*

3.  This will generate a new `lstm_autoencoder.keras` file in the project's root directory, which the application will use the next time it is started.
# AI_Log_Anomaly_Detector
