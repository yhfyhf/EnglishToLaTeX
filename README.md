# English to LaTeX

This service powers the back-end server for the Speech-to-LaTeX iOS app. See the demo here: [https://www.youtube.com/watch?v=dqY-oIhNEQ8](https://www.youtube.com/watch?v=dqY-oIhNEQ8)

The source code of the iOS app is here: [https://github.com/MichaelGuoXY/AudioToLaTeX](https://github.com/MichaelGuoXY/AudioToLaTeX)

Created at the Big Red Hackathon.

## Install
Make sure you have installed Python, pip and virtualenv.

```
brew install python
easy_install pip
pip install virtualenv
```

Switch to the directory you want to put your project.

```
virtualenv EnglishToLaTeX
cd EnglishToLaTeX
. bin/activate
git clone https://github.com/yhfyhf/EnglishToLaTeX src
cd src
pip install -r requirements.txt
```

## Run Server
Make sure you have switched into the src directory.

```
python server.py
```

Now the server is running locally at port 5000.


## API

```
curl -X POST -d 'english=One plus 2 divided by 4' http://localhost:5000/
```

##### Return:
```
{
  "latex": "1 + \frac{2}{4}",
  "status": true
}
```