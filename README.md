# English to LaTeX

This packages converts english into LaTeX.

## Install
Make sure you have installed Python, pip and virtualenv.

```
brew install python
pip instal virtualenv
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
curl -X POST -d 'english=One plus 2' http://localhost:5000/
```

##### Return:
```
{
  "latex": "1 + 2",
  "status": true
}
```