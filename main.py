import pandas as pd
import numpy as np
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# helper function to go from American odds to implied probability
def odds_to_probability(american_odds):
    probabilities = []
    probability = 0
    for odd in american_odds:
        if odd < 0:
            probability = -(odd / (-1*odd + 100))
        if odd > 0:
            probability = 100 / (odd + 100)
        probabilities.append(probability)
    return probabilities



# initialize web driver for Selenium
options = Options()
driver = webdriver.Chrome('/Users/hnunez/Downloads/chromedriver_mac64 (1)/chromedriver', options=options)
driver.get('https://www.actionnetwork.com/mlb/odds')

# actionnetwork attempts to avoid parsing by changing the odds twice before fully loading the page, so delaying the code gets around this
time.sleep(3)

# the site is

odds = driver.find_elements(By.XPATH, '//span[@class="css-1qynun2 ena22472"]')

teams_names = driver.find_elements(By.XPATH, '//div[@class="game-info__team--desktop"]')


books_with_best_odds = driver.find_elements(By.XPATH, '//div[@class="LazyLoad is-visible"]/picture/img')
for book in books_with_best_odds:
    print(book.get_attribute('srcset'))
name_of_matches= []

for x in range(0, len(teams_names), 2):
    name_of_matches.append(teams_names[x].text + " vs " + teams_names[x+1].text)
print(name_of_matches)
# start as list for dynamic sizing and because we cannot apply a broad formula to each list
away_team_odds = []
home_team_odds = []

# step by 22 because there are 11 books on the site after 'best odds', with two entries each book
for x in range(0, len(odds), 22):
    away_team_odds.append(float(odds[x].text))
for x in range(1, len(odds), 22):
    home_team_odds.append( float(odds[x].text))


home_implied_probabilities = odds_to_probability(home_team_odds)
away_implied_probabilities = odds_to_probability(away_team_odds)

match_implied_probability= [i+j for i,j in zip(home_implied_probabilities, away_implied_probabilities)]



