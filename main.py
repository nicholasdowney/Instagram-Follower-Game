#Initialize the game
import requests, random, time
import art as messages
from bs4 import BeautifulSoup
from instagramy import *
#Initialize global variables
wiki_url = "https://en.wikipedia.org/wiki/List_of_most-followed_Instagram_accounts"
insta_api_url = "https://instagram-data1.p.rapidapi.com/followers"
list_accounts = []
data = {
    1:{"username":"@test1", "followers":500},
    }
win_status = ""
question_number = 0
score = 0
winning_score = 5
#Print loading screen
print(messages.welcome_message)
#Grab session-id
session_id = input("""
Please enter your session id from Instagram webpage session cookie.
This authenticates the application to make instagram requests.\n\n""")
#Build list of insta accounts
print("Please wait while Top 50 Instagram accounts are being updated...\n\n")
response = requests.request("GET", wiki_url, headers="", params="")
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.findAll("a", {"class":"external text"})
account_number = 0
for string in soup.stripped_strings:
    if string[0] == "@":
        list_accounts.append(string)
        account_number += 1
        data[account_number] = {"username":string}
    else:
        continue
print(f"Successfully updated the top {len(list_accounts)} Instagram accounts!\n")
###########################################################################
#FOR TESTING ONLY - TRIM LIST OF ACCOUNTS TO REDUCE WEB SCRAPING WORKLOAD
list_accounts = list_accounts[0:10]
###########################################################################
#Create dictionary of account follower totals
iteration = 0
account_number = 0
print(f"Updating current followers from Instagram website...")
for account in list_accounts:
    iteration += 1
    print(f"Updating account {iteration} of {len(list_accounts)}")
    # time.sleep(2)
    user = InstagramUser(account[1:], sessionid=session_id)
    # print(f"{account} current number of followers: ")
    followers = user.number_of_followers
    # print(format (followers, ",d"))
    account_number += 1
    data[account_number]["followers"] = followers
    # print(data[account_number])
#Send Loading finished message
print("FINISHED LOADING!")
#Gameplay
###########################################################################
#FOR TESTING ONLY - TRIMMED TO 10 ITERATIONS TO MATCH # OF SCRAPED ACCOUNTS
###########################################################################
while question_number < 10:
    option_1 = random.randint(1, 10)
    option_2 = random.randint(1, 10)
    while option_1 == option_2:
        option_2 = random.randint(1, 10)
    option_1 = data[option_1]
    option_2 = data[option_2]
#Determine answer key
    if option_1["followers"] > option_2["followers"]:
        correct_answer = "1"
    elif option_1["followers"] < option_2["followers"]:
        correct_answer = "2"
    else:
        pass
#Ask for user selection for which is higher sub count
    print(f"""
    Who has a higher follower count?
    1) {option_1["username"]}
    2) {option_2["username"]}
    """)
    user_choice = input()
    question_number += 1
#Compare answer against distionary values
    if user_choice == correct_answer:
        print("CORRECT!")
        score += 1
    else:
        print("WRONG ANSWER")
        pass
#Won
if score >= winning_score:
    print(messages.win_message)
    print(f"{score} POINTS!!!")
#Lost
else:
    print(messages.lose_message)
#Quit game
quit_game = input("PRESS ENTER TO QUIT GAME")
print(messages.exit_message)
time.sleep(3)
