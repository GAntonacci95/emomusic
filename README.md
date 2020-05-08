## Introduction

Our methods in exploring, experiencing, and getting creative with music have changed drastically over time. And today we are surrounded by all types of new and adapting technology, something not familiar to us even 10 years ago.

Why don't we use more technology to our advantage when it comes to music? How can we better our current methods in choosing music, making the experience more personal and immersive.

## EmoMusic (Emotional Music)

With EmoMusic we aim to give the user a finer tuned experience to what they're feeling. EmoMusic is not just a visual addition to Spotify but:

- connects to your Webcam
- detects your current emotional state
- plays music representing your emotions
- Uses features of the selected music to drive a correlating visual, personalizing experience

In our Prototype we allowed premium Spotify users could log in, capture an image of themselves, submit to detect their emotion, and a song and correlating color would execute to match. The new and improved EmoMusic now includes control over your Spotify directly from our application (Pause/Play, Skip Functions) and now automatically upon pressing play your emotion is detected. EmoMusic graphics have been revamped drawing different signals to match your emotion, as well as a coordinating gradient color to really bring together your experience.

How?

1. The user connects to their premium Spotify account, giving permission for EmoMusic to use personal data (Spotify API), as well as accepts the use of their webcam
2. Upon pressing Play, EmoMusic then sends your captured image to Microsoft Azure Facial Recognition Service, using a pre-trained model to detect your emotion.
3. This information is returned and use to drive Spotify in choosing the perfect song

## Requirements

Actually EmoMusic is just an offline application. If you want to test the application, you are required to have:

- Spotify Premium Account
- Microsoft Azure Facial Recognition Service Plan
- Python


**Microsoft Azure Facial Recognition** - Running EmoMusic require to create a Face Azure resource. Azure Cognitive Services are represented by Azure resources that you subscribe to.

Create a resource for Face using the [Azure portal](https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=multiservice%2Clinux) or [Azure CLI](https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account-cli?tabs=linux) on your local machine. Once finished copy your *endpoint url* and *key* in *.env* file

- AZURE_APIKEY=yourkey
- AZURE_URI=yourendpoint


[Here](https://docs.microsoft.com/en-us/azure/cognitive-services/Face/Quickstarts/client-libraries?pivots=programming-language-python&tabs=linux#prerequisites) you can find the reference to use the Face client library.

**Python** - EmoMusic require a python version >= 3.7v. We suggest to use [anaconda](https://www.anaconda.com/products/enterprise) to manage your packages. If you have *conda* already working on your machine, create a new environment and activate it


 ```python
 conda create -n emomusic python=3.7 anaconda
 conda activate emomusic
 ```

 Install *python/dotenv* library

 ```python
 pip install python/dotenv
 ```

 Now you can execute the server running

 ```python
flask run
 ```

At this point your server will be running on your local machine [127.0.0.1:5000](127.0.0.1:5000)

**Reminder**

Before using EmoMusic turn off any application using your webcam (Skype, Zoom, Others.) this can cause conflict using your cam
