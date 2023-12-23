<h1>APU Knowledge Discord Chatbot</h1>
<h2>Introduction</h2>
This is a Discord chatbot that will provide information about the campus facilities and services in Asia Pacific University of Technology & Innovation (APU).  

You may Download Zip file from this repository, or clone it to your local through Git CLI with the commands below:  
```git
git clone https://github.com/TeoJJss/iai-chatbot.git
```  
<b>Python v3.11.6</b> is used for development.  

<h2>Getting Started</h2>

To launch the bot, ensure you have configured the Discord bot's token and channel ID in `config.py`. If there is a `config_sensitive.py`, please configure in this file instead.  
You should install the dependencies before launching the bot, with the following commands:    
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Then, you can run the following command to launch the bot:
```
python main.py
```
You should be able to see the bot with "Online" status in Discord, if the bot's token is correctly defined in `config.py` or `config_sensitive.py`. After that, it can respond to messages. 