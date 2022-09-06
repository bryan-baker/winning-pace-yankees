# How Do the 2022 Yankees Stack Up Against Other Legendary Teams from the Past?
## Link: https://bryan-baker.github.io/winning-pace-yankees/

## Table of contents
* [Inspiration](#inspiration)
* [Process](#process)
* [Setup](#setup)

# Inspiration
- The 2022 New York Yankees got off to one of the hottest starts in MLB history. Many fans and writers began comparing them to the 1998 World Series winning team, who finished the season with 114 wins. At the time, it was the second-winningest season of all time behind the 1906 Chicago Cubs. Through their first 80 games, the 2022 team was only games behind the 1998 team's winning pace. 
- I wanted to look at how the 2022 team compares to other legendary teams from the past in terms of winning pace and run differential. I ended up choosing 1998 (obviously), 1961 and 1927. Along the way, I also realized that this year's team had something else in common with the 1961 team. A player is chasing history.
- Aaron Judge has been on pace to break Roger Maris's American League home run record set in the 1961 season. in 1961, Maris and Mickey Mantle were in a race to pass the record of 60 set by Babe Ruth in 1927. I decided it would be worth it to look at Judge's home run pace compared to Maris and Ruth (for some fun I added Barry Bonds's 2001 season when he hit 73 HRs)

# Process
# Setup
## Import necessary libraries and packages
Using Selenium to scrape for the 2022 Yankees so it can update the chart daily
```
from pybaseball import schedule_and_record
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path  
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)
```
## Use Pybaseball to get schedule and record data from the 1927, 1961 and 1998 seasons
```
yankees1 = schedule_and_record(1927, 'NYY')
yankees2 = schedule_and_record(1961, 'NYY')
yankees3 = schedule_and_record(1998, 'NYY')
```
## Selenium webdriver to scrape for the 2022 team's schedule and record page
```
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.baseball-reference.com/teams/NYY/2022-schedule-scores.shtml')
time.sleep(1)
driver.refresh()
time.sleep(1)
yankees4 = pd.read_html(driver.find_element(By.ID, 'team_schedule').get_attribute('outerHTML'))
yankees4 = yankees4[0]
yankees4
```

## Fixing an issue with the string in the 'W/L' column
Some rows had "L-wo" and "W-wo" so they weren't being registered in the calculations. Do this for each team's dataset.
```
yankees4['W/L'] = yankees4['W/L'].str.replace('W-wo', 'W')
yankees4['W/L'] = yankees4['W/L'].str.replace('L-wo', 'L')
```
## Adding a win count column using the .cumsum() function
```
yankees1['win-count'] = np.where(yankees1['W/L']=='W', 1, 0).cumsum()
yankees2['win-count'] = np.where(yankees2['W/L']=='W', 1, 0).cumsum()
yankees3['win-count'] = np.where(yankees3['W/L']=='W', 1, 0).cumsum()
yankees4['win-count'] = np.where(yankees4['W/L']=='W', 1, 0).cumsum()
```
## Winning pace plot using matplotlib
```
plt.plot(yankees1['win-count'], 'g', label=" 1927")
plt.plot(yankees2['win-count'], 'b', label=" 1961")
plt.plot(yankees3['win-count'], 'tab:orange', label=" 1998")
plt.plot(yankees4['win-count'], 'r', label=" 2022")
plt.legend(loc=4)
plt.xlabel('Games')
plt.ylabel('Win Count')
plt.title('Winning Pace');
```
![win-count](https://user-images.githubusercontent.com/107493329/188752336-729c908a-181b-4c83-93ad-fea5af4ac1b3.svg)

## Converting 'Runs scored' and 'Runs allowed' into floats to calculate run differential
```
yankees4.R = yankees4.R.astype(float)
yankees4.RA = yankees4.RA.astype(float)
```
```
yankees1['scorediff'] = (yankees1['R'] - yankees1['RA']).cumsum()
yankees2['scorediff'] = (yankees2['R'] - yankees2['RA']).cumsum()
yankees3['scorediff'] = (yankees3['R'] - yankees3['RA']).cumsum()
yankees4['scorediff'] = (yankees4['R'] - yankees4['RA']).cumsum()
```
## Run differential plot
```
plt.plot(yankees1['scorediff'], 'g', label=" 1927")
plt.plot(yankees2['scorediff'], 'b', label=" 1961")
plt.plot(yankees3['scorediff'], 'tab:orange', label=" 1998")
plt.plot(yankees4['scorediff'], 'r', label=" 2022")
plt.legend(loc=4)
plt.xlabel('Games')
plt.ylabel('Runs Scored - Runs Against')
plt.title('Cumulative Run Differential');
```
![run-differential](https://user-images.githubusercontent.com/107493329/188752301-9be8907b-e537-4c3c-9b98-9ace2b086456.svg)

# Home Run Pace
## Scrape Judge's 2022 batting game logs
```
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.baseball-reference.com/players/gl.fcgi?id=judgeaa01&t=b&year=2022')
time.sleep(3)
driver.refresh()
time.sleep(3)
judge = pd.read_html(driver.find_element(By.ID, 'batting_gamelogs').get_attribute('outerHTML'))
judge = judge[0]
judge
```
## Drop unnecessary columns, clean data and add HR count column
```
judge = judge.drop(columns=['Rk', 'Gcar', 'Unnamed: 5', 'RE24', 'DFS(DK)', 'DFS(FD)' ])
judge = judge[judge['Rslt'].str.contains('Rslt')==False]
judge = judge[judge['Gtm'].notna()]
judge.HR = judge.HR.astype(int)
judge['HR_count'] = judge['HR'].cumsum()
judge
```
## Repeat process for Maris, Bonds, and Ruth
Links to game logs for scraping
-https://www.baseball-reference.com/players/gl.fcgi?id=bondsba01&t=b&year=2001
-https://www.baseball-reference.com/players/gl.fcgi?id=marisro01&t=b&year=1961
-https://www.baseball-reference.com/players/gl.fcgi?id=ruthba01&t=b&year=1927

## Plot Home Run Pace
```
plt.plot(ruth['HR_count'], 'g', label="Babe Ruth (1927)")
plt.plot(maris['HR_count'], 'b', label="Roger Maris (1961)")
plt.plot(bonds['HR_count'], 'tab:orange', label="Barry Bonds (2001)")
plt.plot(judge['HR_count'], 'r', label="Aaron Judge (2022)")
plt.legend(loc=4)
plt.xlabel('Games')
plt.ylabel('Home Runs')
plt.title('Home Run Pace')
```
![hr-pace](https://user-images.githubusercontent.com/107493329/188753809-ea1e9bff-4a4a-4bd5-a951-52ee425a1d05.svg)


