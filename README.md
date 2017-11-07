# TaBOT
AI powered Chatbot for Answering Question about University Technology Malaysia (UTM)

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites
To get started with the development of the project, these python packages are required to install first.
  * [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - Python library for pulling data out of HTML and XML files
  * [requests](https://github.com/requests/requests) - Python library to handle the HTTP request
  * [pywit](https://github.com/wit-ai/pywit) - Python SDK for Wit.ai
  * [python-prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit) - library for building powerful interactive command lines and terminal applications in Python
  
### Installing
Follow the step by step guide to start the development for the project.
```
git clone https://github.com/erichooi/TaBOT.git
python -m venv env
```
Start the python virtual environment
#### For Mac or Linux Users
```
source bin/activate
```
#### For Window Users
```
> \path\to\env\Scripts\activate.bat
```
Install the prerequisites python packages via pip
```
pip install bs4
pip install requests
pip install pywit
pip install python-prompt-toolkit
```
Then run the program by running the command
```
python tabot.py
```
