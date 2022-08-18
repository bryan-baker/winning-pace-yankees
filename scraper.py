#!/usr/bin/env python
# coding: utf-8

# # Yankees Win Pace 2022
# Goals
# - Import schedule and record data using pybaseball package
# - Scrape 2022 Yankees record 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.offline as pyo

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


# In[26]:


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


# In[27]:


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


yankees4.dtypes


# In[17]:


yankees4.R.mean()


# In[18]:


yankees3.R.mean()


# In[19]:


mariners


# In[ ]:




