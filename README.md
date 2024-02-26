<h1>APU Knowledge Discord Chatbot</h1>
<h2>Introduction</h2>
This is a chatbot that will provide information about the campus facilities and services in Asia Pacific University of Technology & Innovation (APU).  

You may Download Zip file from this repository, or clone it to your local through Git CLI with the commands below:  
```git
git clone https://github.com/TeoJJss/iai-chatbot.git
```  
<b>Python v3.11.6</b> is used for development.  

<h2>Getting Started</h2>

<h3>Prerequisite</h3>

You should install the dependencies before launching the bot, with the following commands:    
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
The source codes can host the chatbot on Discord and Streamlit, depending on preferences.  

<h3>Option 1: Hosting with Discord</h3>

To launch the bot, ensure that you have configured the Discord bot's token and channel ID in `config.py`. If there is a `config_sensitive.py`, please configure in this file instead.   
Read <a href="https://turbofuture.com/internet/Discord-Channel-ID">this</a> for guide on obtaining channel ID in Discord.  
Run the following command to launch the bot in Discord:
```
python main.py
```
You should be able to see the bot with "Online" status in Discord, if the bot's token is correctly defined in `config.py` or `config_sensitive.py`. After that, it can respond to messages in the allowed channels.  

<h3>Option 2: Hosting with Streamlit</h3>

This chatbot supports Streamlit too. You may launch the bot in Streamlit through the following commands:  
```
streamlit run main_st.py
```
You will be redirected to a localhost website, where Streamlit is hosted on. 

<h2>Credits</h2>
- <a href="https://github.com/TeoJJss">Teo Jun Jia</a><br>
- <a href="https://github.com/shengyaosiew">Siew Sheng Yao</a><br>
- <a href="https://github.com/Lonelywolf88">Sin Boon Leon</a><br>
- <a href="https://github.com/DamienCKj2812">Chong Kah Jun</a><br>
- <a href="https://github.com/ysolo01">Yong Lee Wai</a><br>
- <a href="https://github.com/omeowrice">Ting Zi Qing</a>