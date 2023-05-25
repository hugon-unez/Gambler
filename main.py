from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

#must zoom all the way out in order to load all sports book images

# I CANNOT FIGURE OUT HOW TO AUTOSCROLL FOR ALL BOOK NAMES

driver.execute_script("document.body.style.zoom='40%'")



# actionnetwork attempts to avoid parsing by changing the odds twice before fully loading the page, so delaying the code gets around this
time.sleep(5)

# find by XPATH is slowest, and not readable, but the css was convoluted so this is easier
odds = driver.find_elements(By.XPATH, '//span[@class="css-1qynun2 ena22472"]')
teams_names = driver.find_elements(By.XPATH, '//div[@class="game-info__team--desktop"]')


books_with_best_odds = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/table/tbody/tr/td/div/div/div/span/div/picture/img')

books = []

for book in books_with_best_odds:
    sportsbook_name = book.get_attribute('alt')
    # we have to subtract 8 from the sportsbook_name since selenium also includes " IL Logo" after the name of the book
    length_of_bookName = len(sportsbook_name) - 8
    books.append(sportsbook_name[:length_of_bookName])


name_of_matches= []

# take list of team names and make convert it to a familiar readable format for when we need to report arbitrage
for x in range(0, len(teams_names), 2):
    name_of_matches.append(teams_names[x].text + " at " + teams_names[x+1].text)

# start as list for dynamic sizing and because we cannot apply a broad formula to each list
away_team_odds = []
home_team_odds = []

# step by 22 because there are 11 books on the site after 'best odds', with two entries each book
for x in range(0, len(odds), 22):
    away_team_odds.append(float(odds[x].text))

for x in range(1, len(odds), 22):
    home_team_odds.append(float(odds[x].text))


# apply the function that converts American odds to implied probability 
home_implied_probabilities = odds_to_probability(home_team_odds)
away_implied_probabilities = odds_to_probability(away_team_odds)

# add the home and away implied probabilities in order to find arbitrage
match_implied_probability= [i+j for i,j in zip(home_implied_probabilities, away_implied_probabilities)]

arb_count = 0 

for x in range (0, len(match_implied_probability)):
    if match_implied_probability[x] < 1:
        print("There is arbitrage in the game " + name_of_matches[x] + " , with " + str(away_team_odds[x]) + " offered at " + books[2 * x] + " and " + str(home_team_odds[x]) + " at " + books[2 * x + 1] + ".")
        arb_count += 1
        
if arb_count == 0:
    print("There is currently no arbitrage opportunity")