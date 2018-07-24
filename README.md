# Pure Gym Data Collector

Python3 script to automate collection of the number of people currently in pure gym using the number listed in their members login area.

You must have a valid pure gym email and pin to use this as it requires logging in to the site.

The main driver for this project was to get a little more experience working with python while creating something as I don't use it regularly.

## Getting Started

You need to have google chrome installed on your system as well as chromedriver as this project uses selenium to drive the web scraping.
To install Chrome:
Install dependencies:
```
sudo apt-get update
sudo apt-get install -y unzip openjdk-8-jre-headless xvfb libxi6 libgconf-2-4
```
Install pip3 if you don't have it already 
```
sudo apt-get install python3-pip
```
Install python requirements via pip3
```
pip3 install -r requirements.txt
```

Then chrome:
```
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
sudo apt-get -y update
sudo apt-get -y install google-chrome-stable
```

To install chromedriver (requires unzip):
```
wget -N http://chromedriver.storage.googleapis.com/2.10/chromedriver_linux64.zip -P ~/
unzip ~/chromedriver_linux64.zip -d ~/
rm ~/chromedriver_linux64.zip
sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
sudo chown root:root /usr/local/bin/chromedriver
sudo chmod 0755 /usr/local/bin/chromedriver
```
