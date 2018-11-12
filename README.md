# osrs_world_pinger
A tool for oldschool runescape that retrieves world information and its latency.
* The user can choose to ping a specific world or to ping all worlds.   
* The top five worlds with best latency is displayed when user pings all worlds.  
* Works by parsing the OSRS server list for information and pings the worlds.

If you dont have python installed, there is an compiled executable available named `osrs_world_pinger.exe`

### Requirements
* python 3
* beautifulsoup 4

### Setup
To install requirements:
```
python setup.py install
```
To run the script:
```
python osrs_world_pinger.py
```

### Screenshots
* User pings specific world  
![Image](https://i.imgur.com/9yJSWtX.png)  

* User pings all worlds  
![Image](https://i.imgur.com/LVVAJyT.png)  

* Top five worlds  
![Image](https://i.imgur.com/B0kJU6Z.png)  
