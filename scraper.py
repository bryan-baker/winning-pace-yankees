#!/usr/bin/env python
# coding: utf-8

# # Yankees Win Pace 2022
# Goals
# - Import schedule and record data using pybaseball package
# - Scrape 2022 Yankees record 

# In[1]:


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


# In[2]:


yankees1 = schedule_and_record(1927, 'NYY')
yankees2 = schedule_and_record(1961, 'NYY')
yankees3 = schedule_and_record(1998, 'NYY')
mariners = schedule_and_record(2001, 'SEA')


# In[3]:


mariners


# In[4]:


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.baseball-reference.com/teams/NYY/2022-schedule-scores.shtml')
time.sleep(1)
yankees4 = pd.read_html(driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[5]/div[2]/table').get_attribute('outerHTML'))
yankees4 = yankees4[0]
yankees4


# In[5]:


pd.set_option('display.max_columns', None)
yankees4 = yankees4.dropna(subset=['cLI'])


# In[6]:


yankees4 = yankees4[yankees4['Gm#'].str.contains('Gm#')==False]


# In[7]:


yankees4['W/L'] = yankees4['W/L'].str.replace('W-wo', 'W')
yankees4['W/L'] = yankees4['W/L'].str.replace('L-wo', 'L')
yankees3['W/L'] = yankees3['W/L'].str.replace('W-wo', 'W')
yankees3['W/L'] = yankees3['W/L'].str.replace('L-wo', 'L')
yankees2['W/L'] = yankees2['W/L'].str.replace('W-wo', 'W')
yankees2['W/L'] = yankees2['W/L'].str.replace('L-wo', 'L')
yankees1['W/L'] = yankees1['W/L'].str.replace('W-wo', 'W')
yankees1['W/L'] = yankees1['W/L'].str.replace('L-wo', 'L')
yankees1['W/L'] = yankees1['W/L'].str.replace('W &H', 'W')
yankees2['W/L'] = yankees2['W/L'].str.replace('W &H', 'W')
mariners['W/L'] = mariners['W/L'].str.replace('W-wo', 'W')
mariners['W/L'] = mariners['W/L'].str.replace('L-wo', 'L')


# In[8]:


yankees1['win-count'] = np.where(yankees1['W/L']=='W', 1, 0).cumsum()
yankees2['win-count'] = np.where(yankees2['W/L']=='W', 1, 0).cumsum()
yankees3['win-count'] = np.where(yankees3['W/L']=='W', 1, 0).cumsum()
yankees4['win-count'] = np.where(yankees4['W/L']=='W', 1, 0).cumsum()
mariners['win-count'] = np.where(mariners['W/L']=='W', 1, 0).cumsum()


# In[9]:


plt.plot(yankees1['win-count'], 'g', label=" 1927")
plt.plot(yankees2['win-count'], 'b', label=" 1961")
plt.plot(yankees3['win-count'], 'tab:orange', label=" 1998")
plt.plot(yankees4['win-count'], 'r', label=" 2022")
plt.legend(loc=4)
plt.xlabel('Games')
plt.ylabel('Win Count')
plt.title('Winning Pace');
plt.savefig('charts/win-count.svg')


# In[10]:


yankees4.R = yankees4.R.astype(float)
yankees4.RA = yankees4.RA.astype(float)


# In[11]:


yankees1['scorediff'] = (yankees1['R'] - yankees1['RA']).cumsum()
yankees2['scorediff'] = (yankees2['R'] - yankees2['RA']).cumsum()
yankees3['scorediff'] = (yankees3['R'] - yankees3['RA']).cumsum()
yankees4['scorediff'] = (yankees4['R'] - yankees4['RA']).cumsum()


# In[12]:


plt.plot(yankees1['scorediff'], 'g', label=" 1927")
plt.plot(yankees2['scorediff'], 'b', label=" 1961")
plt.plot(yankees3['scorediff'], 'tab:orange', label=" 1998")
plt.plot(yankees4['scorediff'], 'r', label=" 2022")
plt.legend(loc=4)
plt.xlabel('Games')
plt.ylabel('Runs Scored - Runs Against')
plt.title('Cumulative Run Differential');
plt.savefig('charts/run-differential.svg')


# In[13]:


yankees1


# In[14]:


yankees1.to_csv('data/yankees_1927.csv')
yankees2.to_csv('data/yankees_1961.csv')
yankees3.to_csv('data/yankees_1998.csv')
yankees4.to_csv('data/yankees_2022.csv')
mariners.to_csv('data/mariners_2001.csv')


# In[15]:


pd.set_option('display.max_rows', None)
yankees4


# In[16]:


# Scrape for Judge
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.baseball-reference.com/players/gl.fcgi?id=judgeaa01&t=b&year=2022')
time.sleep(1)
judge = pd.read_html(driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[4]/div[3]/table').get_attribute('outerHTML'))
judge = judge[0]
judge


# In[17]:


# Drop unnecessary columns
judge = judge.drop(columns=['Rk', 'Gcar', 'Unnamed: 5', 'RE24', 'DFS(DK)', 'DFS(FD)' ])


# In[18]:


# Check data
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
judge


# In[19]:


# More cleaning + adding HR count column
judge = judge[judge['Rslt'].str.contains('Rslt')==False]
judge = judge[judge['Gtm'].notna()]
judge.HR = judge.HR.astype(int)
judge['HR_count'] = judge['HR'].cumsum()
judge


# In[20]:


# Scrape for Maris
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.baseball-reference.com/players/gl.fcgi?id=marisro01&t=b&year=1961')
time.sleep(1)
maris = pd.read_html(driver.find_element(By.ID, 'batting_gamelogs').get_attribute('outerHTML'))
maris = maris[0]
maris


# In[21]:


# Clean and add HR Count 
maris = maris.drop(columns=['Rk', 'Gcar', 'Unnamed: 5', 'RE24'])
maris = maris[maris['Rslt'].str.contains('Rslt')==False]
maris.HR = maris.HR.astype(int)
maris.WPA = maris.WPA.astype(float)
maris['HR_count'] = maris['HR'].cumsum()
maris = maris[maris['Gtm'].notna()]
maris


# In[22]:


# Scrape for Ruth
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.baseball-reference.com/players/gl.fcgi?id=ruthba01&t=b&year=1927')
time.sleep(1)
ruth = pd.read_html(driver.find_element(By.ID, 'batting_gamelogs').get_attribute('outerHTML'))
ruth = ruth[0]
ruth


# In[23]:


# Clean and add HR count column
ruth = ruth.drop(columns=['Rk', 'Gcar', 'Unnamed: 5', 'RE24'])
ruth = ruth[ruth['Rslt'].str.contains('Rslt')==False]
ruth.HR = ruth.HR.astype(int)
ruth['HR_count'] = ruth['HR'].cumsum()
ruth = ruth[ruth['Gtm'].notna()]
ruth


# In[24]:


# Scrape for Bonds
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.baseball-reference.com/players/gl.fcgi?id=bondsba01&t=b&year=2001')
time.sleep(1)
bonds = pd.read_html(driver.find_element(By.ID, 'batting_gamelogs').get_attribute('outerHTML'))
bonds = bonds[0]
bonds


# In[25]:


# Clean and add HR count column
bonds = bonds.drop(columns=['Rk', 'Gcar', 'Unnamed: 5', 'RE24'])
bonds = bonds[bonds['Rslt'].str.contains('Rslt')==False]
bonds = bonds[bonds['Gtm'].notna()]
bonds.HR = bonds.HR.astype(int)
bonds['HR_count'] = bonds['HR'].cumsum()
bonds


# In[26]:


# Add WPA Count column
bonds['WPA_count'] = bonds['WPA'].cumsum()
maris['WPA_count'] = maris['WPA'].cumsum()
judge['WPA_count'] = judge['WPA'].cumsum()


# In[27]:


# Change aLI to float
bonds.aLI = bonds.aLI.astype(float)
maris.aLI = maris.aLI.astype(float)
judge.aLI = judge.aLI.astype(float)


# In[28]:


# Save data to CSV files
bonds.to_csv('data/bonds.csv')
maris.to_csv('data/maris.csv')
judge.to_csv('data/judge.csv')
ruth.to_csv('data/ruth.csv')


# In[29]:


plt.plot(ruth['HR_count'], 'g', label="Babe Ruth (1927)")
plt.plot(maris['HR_count'], 'b', label="Roger Maris (1961)")
plt.plot(bonds['HR_count'], 'tab:orange', label="Barry Bonds (2001)")
plt.plot(judge['HR_count'], 'r', label="Aaron Judge (2022)")
plt.legend(loc=4)
plt.xlabel('Games')
plt.ylabel('Home Runs')
plt.title('Home Run Pace')
plt.savefig('charts/hr-pace.svg')


# In[ ]:




