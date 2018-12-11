# Getting started

## Prerequisites

- Python 3

## Installation

First, clone the repo:

```
git clone https://github.com/calebstdenis/playlist-maker.git
```

Then install the depencies:

```
cd playlist-maker/server
pip install pipenv
pipenv install
```

## Running the performance analysis script

```
pipenv shell
python evaluation.py
```

## Using the Android client

### Prerequisities

- [adb](https://android.gadgethacks.com/how-to/android-basics-install-adb-fastboot-mac-linux-windows-0164225/) (comes with [Android Studio](https://developer.android.com/studio/))
- An Android device with USB debugging enabled
- [Expo Client](https://play.google.com/store/apps/details?id=host.exp.exponent&hl=en) installed on the Android device (available on Google Play)

### Running the app client

Start the server

```
cd server
pipenv install
pipenv shell
python app.py
```

Connect the the Android device to the server machine via USB, then run the following command on the server machine:

```
adb reverse tcp:5000 tcp:5000
```

Finally, open the following app in Expo on the Android device: https://expo.io/@calebstdenis/spotify-playlist-maker

### Running the app client locally

With Node.js installed and the Android device connected:

```
cd client
npm install
npm start
```

Select "Run on Android device" in the web interface that appears.
