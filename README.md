This is the final project for Introduction of Computer Network, 2019 Spring, National Taiwan University. 
This entire project is highly inspired by [this repo](https://github.com/dxue2012/python-webcam-flask). (Big thanks for open-sourcing!)

### Workflow

1) The web client sends video stream data (from the user's webcam) to a flask server using socketio
2) The server detects the facial expressions and sound in the video, and overlays task images on frames
3) The client receives the processed video stream and re-displays the results in a different frame

### How to play

1) Open any browser (Chrome prefered) and access the url down below.
2) Allow webcam and microphone access during the first time visit. (might need to refresh the page after allowing)
3) Look at the video on the right. Try to make your face as similar as any cartoon faces in the video. The cartoon icons would disappear if the similarity is high enough.
4) If the task image is not a cartoon icon (i.e. a real person's face...), you should shout at the microphone. The face would explode only if the sound is loud enough.
5) The game does not end, nor does it record the score. This is just for fun, so please have fun!

### Demo
[Live Demo](https://stark-badlands-83896.herokuapp.com/)

## Setup
#### If you would like to setup a server on your own, please follow the steps below.

### Prerequisites

- sign up a heroku account on Heroku official [website](https://dashboard.heroku.com/apps)
- install heroku (`brew install heroku` for mac)
- install heroku cli (`brew tap heroku/brew && brew install heroku` for mac)
- `git clone https://github.com/evamo0508/Face-Dance-Machine-python-webcam-flask.git`
- `cd Face-Dance-Machine-python-webcam-flask`
- download `landmarks.dat` [here](goo.gl/Z2JCch) and put it in current directory
- `heroku login`
- `heroku create`

### Deploy to heroku

- `git push heroku master` (will remotely install dependencies in `requirements.txt` automatically)
- `heroku open` (redirects to your default browser) 
