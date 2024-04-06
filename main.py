
# importing library
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import time as ttime_

# options
custom_options = Options()
# open webbrowser in maximimum window
custom_options.add_argument("--start-maximized")
# path to webdriver
path_driver = Service(r"E:\Python\Devman\Parcing Dev\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=path_driver, options=custom_options)
# url on page webbrowser
ref = "https://www.flashscore.com/"
# driver get ref on page
driver.get(ref)


# a code which print main tabs on website
class_elements = driver.find_elements(By.CLASS_NAME, 'menuTop.menuTop--soccer')

tabs_sports = []

for catalog in class_elements:
    res = catalog.text.splitlines()
    tabs_sports.append(res)

print(tabs_sports)

# switch to another tab
element = driver.find_elements(By.CLASS_NAME, 'menuTop__item')

sports_dict = {
    'FAVORITES': 0,
    'FOOTBALL': 1,
    'TENNIS': 2,
    'BASKETBALL': 3,
    'HOCKEY': 4,
    'GOLF': 5,
    'BASEBALL': 6,
    'SNOOKER': 7,
    'VOLLEYBALL': 8
}

selected_sport_element = element[sports_dict['HOCKEY']]
selected_sport_element.click()



# open menu summary match
def create_df(selected_sport_element):

    id_matches = driver.find_elements(By.CLASS_NAME, 'event__match.event__match--twoLine')
    print(id_matches)

    array_id = []

    for id in id_matches:
        res_id = id.get_attribute('id')
        array_id.append(res_id[4:])


    print(array_id)
    for id_matchi in array_id:
        url_match_summary = f'https://www.flashscore.com/match/{id_matchi}/#/match-summary/match-summary'
        driver.get(url_match_summary)


        # parcing basic data detailed statistics

        name_liga = driver.find_elements(By.CLASS_NAME, 'tournamentHeader__country')[0].text
        command_one = driver.find_elements(By.CLASS_NAME, 'duelParticipant__home ')[0].text
        command_two = driver.find_elements(By.CLASS_NAME, 'duelParticipant__away ')[0].text
        date_game = driver.find_elements(By.CLASS_NAME, 'duelParticipant__startTime')[0].text
        status_match = driver.find_elements(By.CLASS_NAME, 'detailScore__status')[0].text
        game_score = driver.find_elements(By.CLASS_NAME, 'detailScore__wrapper')[0].text.splitlines()

        print(status_match)



        # parcing detailed data from tab match detailed statistics
        url_stats = f'https://www.flashscore.com/match/{id_matchi}/#/match-summary/match-statistics/0'
        time.sleep(5)
        driver.get(url_stats)
        time.sleep(5)

        sf = driver.find_elements(By.CLASS_NAME, '_row_1csk6_9')


        dict_stat = {}

        for details in sf:
            res_details_in_sf = details.text.splitlines()
            key = res_details_in_sf[1]
            hos = res_details_in_sf[0]
            gost = res_details_in_sf[-1]
            dict_stat[key] = [hos, gost]

        print(dict_stat)

        # make a dataframe
        #gpt
        all_info = [name_liga, command_one, command_two, date_game, status_match]
        if status_match == 'FINISHED':
            all_info.append(game_score[0])
            all_info.append(game_score[-1])

        else:
            all_info.append('-')
            all_info.append('-')
        desc_info = ['name_liga', 'command_one', 'command_two', 'date_game', 'status_match', 'result_1', 'result_2']
        df = pd.DataFrame([all_info], columns=desc_info)
        print(df)



        if not dict_stat:
            dict_stat['-'] = ['-', '-']
            df_details = pd.DataFrame(dict_stat)
            print(df_details)

        else:
            df_details = pd.DataFrame(dict_stat)
            df_details = df_details[['Shots on Goal', 'Blocked Shots', 'Goalkeeper Saves', 'Saves PCT']]
            home_info = df_details.loc[[0]]
            home_info = home_info.add_suffix('_home')
            print(home_info)

            away_info = df_details.loc[[1]]
            away_info = away_info.add_suffix('_away')
            away_info = away_info.reset_index(drop=True)
            print(away_info)

            fin_info = pd.merge(home_info, away_info, left_index=True, right_index=True)
            res_df = pd.merge(df, fin_info, left_index=True, right_index=True)
            print(res_df)

            res_df.to_excel(r"E:\Python\Devman\Parcing Dev\Parcing lesson 3\english_option_Parcing_lesson_3\dddd.xlsx", index=False)














create_df(selected_sport_element)

driver.quit()