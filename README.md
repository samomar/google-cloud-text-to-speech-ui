# Google Cloud Text-to-Speech UI using PyQt5

This is a simple UI that uses the Google Cloud Text-to-Speech API to synthesize speech from text input.

## Prerequisites

- Python 3.6 or higher
- A Google Cloud project with the Text-to-Speech API enabled

## Setup

1. Clone the repository:

`git clone https://github.com/samomar/google-cloud-text-to-speech-ui.git`


2. Create a virtual environment and activate it:

`python3 -m venv venv`

`source venv/bin/activate`


3. Install the required dependencies:

`pip install PyQt5 google-cloud-texttospeech`


4. Create a service account and download the private key file:

- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Click the project drop-down and select the project that you want to enable the API for.
- Click the hamburger menu and select APIs & Services > Credentials.
- On the Credentials page, click Create credentials > Service account key.
- Select the service account and click Create.

5. Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of the private key file:

`"GOOGLE_APPLICATION_CREDENTIALS"] = "your_api_key.json"`

## Run the application

`python main.py`
