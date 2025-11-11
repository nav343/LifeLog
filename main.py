import shutil
from plot import Plot
from help import ShowHelp
from utils.colors import COLORS
from utils.window import Window
import pickle
import time
import os
from datetime import datetime

moods = {
    1: "😊 Happy",
    2: "😌 Calm",
    3: "😔 Sad",
    4: "😤 Stressed",
    5: "😎 Confident",
}
logo =  f""" __        __   ______          __                           
/  |      /  | /      \\        /  |                          
$$ |      $$/ /$$$$$$  |_____  $$ |        ______    ______  
$$ |      /  |$$ |_ $$/      \\ $$ |       /      \\  /      \\ 
$$ |      $$ |$$   | /$$$$$$  |$$ |      /$$$$$$  |/$$$$$$  |
$$ |      $$ |$$$$/  $$    $$ |$$ |      $$ |  $$ |$$ |  $$ |
$$ |_____ $$ |$$ |   $$$$$$$$/ $$ |_____ $$ \\__$$ |$$ \\__$$ |
$$       |$$ |$$ |   $$       |$$       |$$    $$/ $$    $$ |
$$$$$$$$/ $$/ $$/     $$$$$$$/ $$$$$$$$/  $$$$$$/   $$$$$$$ |
                                                   /  \\__$$ |
                                                   $$    $$/ 
                                                    $$$$$$/  
"""

def Header(msg: str, color: str = COLORS.LIGHT_WHITE):
    screen.line("-", COLORS.YELLOW)
    screen.print(msg, True, color)
    screen.line("-", COLORS.YELLOW)
    screen.print()

def Login():
    users = []
    data = []
    if os.path.exists(".lifelog/user.dat"):
        with open(".lifelog/user.dat", 'rb') as F:
            while True:
                try:
                    element = pickle.load(F)
                    data.append(element)
                    users.append(element['username'])
                except EOFError:
                    break
    showASCII(r"""
 __                            __           
/  |                          /  |          
$$ |        ______    ______  $$/  _______  
$$ |       /      \  /      \ /  |/       \ 
$$ |      /$$$$$$  |/$$$$$$  |$$ |$$$$$$$  |
$$ |      $$ |  $$ |$$ |  $$ |$$ |$$ |  $$ |
$$ |_____ $$ \__$$ |$$ \__$$ |$$ |$$ |  $$ |
$$       |$$    $$/ $$    $$ |$$ |$$ |  $$ |
$$$$$$$$/  $$$$$$/   $$$$$$$ |$$/ $$/   $$/ 
                    /  \__$$ |              
                    $$    $$/               
                     $$$$$$/                """)
    screen.print()
    screen.line()
    screen.render()
    username = screen.input("Username (or q to quit): ", color=COLORS.YELLOW)
    if username == 'q':
        screen.quit()
    if username not in users:
        screen.print()
        screen.line()
        screen.print(f"[X] User not found. It seems like you have not created an account. Try creating it", color=COLORS.LIGHT_RED)
        screen.line()
        screen.render()
        screen.quit()

    password = screen.input("Password: ", True, color=COLORS.YELLOW)
    user = {}
    for u in data:
        if u['username'] == username:
            user = u

    if user['username'] == username and user['password'] != password:
        screen.print()
        screen.line()
        screen.print("[x] Incorrent Password. Try again", color=COLORS.LIGHT_RED)
        screen.line()
        screen.render()
        time.sleep(1)
        screen.clear()
        Login()

    else:
        stats = loadStats()
        stats['logged'] = True
        with open(".lifelog/stats.dat", 'wb') as file:
            pickle.dump(stats, file)
        screen.print()
        screen.line()
        screen.print(f"[✔] Login successful! Welcome back, {username} !!", color=COLORS.LIGHT_GREEN)
        screen.print("Loading your dashboard...")
        screen.line()
        screen.render()
        time.sleep(1)
        screen.clear()
        screen.render()
        Dashboard(username)

def ViewAll(username: str):
    Header("📖  VIEW ALL ENTRIES  📖", color=COLORS.LIGHT_GREEN)
    screen.print("All of Diary entries: ", color=COLORS.YELLOW)
    screen.print()
    idx = 1
    for i in os.listdir(f".lifelog/{username}"):
        with open(f".lifelog/{username}/{i}", 'rb') as file:
            data = pickle.load(file)
            mood = moods[int(data['mood'])]
            date = data['date']
            content = data['content'][:30] + "..."
            screen.print(f"[{idx}] [{date}] - [{mood} ]", color=COLORS.LIGHT_GREEN)
            screen.print(f"Title: {i.replace('_', ' ').title()[:-4]}", color=COLORS.LIGHT_CYAN)
            screen.line()
            screen.print(content, color=COLORS.LIGHT_GRAY)
            screen.line()
        idx += 1
        screen.print()
        screen.print()

    try:
        choice = screen.input("Which entry do you want to see? (-1 to quit): ", color=COLORS.YELLOW)
        if choice == '': choice = 1
        choice = int(choice)
        if choice > len(os.listdir(f".lifelog/{username}")):
            screen.print("[X] Invalid. Try again", color=COLORS.LIGHT_RED)
            screen.render()
        else:
            if choice == -1:
                screen.clear()
                screen.render()
            else:
                screen.clear()
                screen.render()
                with open(f".lifelog/{username}/{os.listdir(f'.lifelog/{username}')[choice-1]}", 'rb') as file:
                    data = pickle.load(file)
                    mood = moods[int(data['mood'])]
                    date = data['date']
                    content = data['content']
                    screen.print(os.listdir(f'.lifelog/{username}')[choice-1].replace('_', ' ').title()[:-4], color=COLORS.LIGHT_GREEN, centered=True)
                    screen.line()
                    screen.print("-> " + date, color=COLORS.LIGHT_GREEN)
                    screen.print("-> " + mood, color=COLORS.LIGHT_GREEN)
                    screen.line()
                    screen.print(content)
                    screen.line()
                screen.print()
                screen.line()
                screen.input("Press ENTER to go back!", color=COLORS.LIGHT_GRAY)
                screen.clear()
                screen.render()
    except Exception:
        screen.clear()
        screen.render()

def ViewDateRange(username: str):
    Header("📖  VIEW ENTRIES BY DATE 📖", color=COLORS.LIGHT_GREEN)
    screen.print("Choose how you’d like to view your entries:", color=COLORS.YELLOW)
    screen.print()
    screen.line()
    start = datetime.strptime(screen.input("Enter Start Date: (DD-MM-YYYY) ", color=COLORS.LIGHT_GRAY), '%d-%m-%Y')
    end = datetime.strptime(screen.input("Enter End Date: (DD-MM-YYYY) ", color=COLORS.LIGHT_GRAY), '%d-%m-%Y')
    screen.print()
    screen.line()
    idx = 1
    for i in os.listdir(f".lifelog/{username}"):
        with open(f".lifelog/{username}/{i}", 'rb') as file:
            data = pickle.load(file)
            mood = moods[int(data['mood'])]
            date = datetime.strptime(datetime.strptime(data['date'], "%d %B %Y").strftime("%d-%m-%Y"), "%d-%m-%Y")
            content = data['content'][:30] + "..."
            if date > start and date < end:
                screen.print(f"[{idx}] Title: {i.replace('_', ' ').title()[:-4]}", color=COLORS.LIGHT_GREEN)
                screen.print(f"[{date.strftime('%d %b %Y')}] - [{mood} ]", color=COLORS.YELLOW)
                screen.line()
                screen.print(content, color=COLORS.LIGHT_GRAY)
                screen.line()
        idx += 1
        screen.print()
        screen.print()
        screen.render()
    screen.line()
    screen.input("Press ENTER to go back!!", color=COLORS.DARK_GRAY)
    screen.clear()
    screen.render()

def ViewByMood(username: str):
    Header("💭 VIEW ENTRIES BY MOOD 💭", color=COLORS.LIGHT_GREEN)
    screen.print("Which mood would you like to explore?", color=COLORS.YELLOW)
    screen.print()
    screen.line()
    screen.print("> [1] 😊 Happy", color=COLORS.LIGHT_GREEN)
    screen.print("[2] 😌 Calm", color=COLORS.LIGHT_GRAY)
    screen.print("[3] 😔 Sad", color=COLORS.LIGHT_GRAY)
    screen.print("[4] 😤 Stressed", color=COLORS.LIGHT_GRAY)
    screen.print("[5] 😎 Confident", color=COLORS.LIGHT_GRAY)
    screen.print("[6] Back to menu", color=COLORS.LIGHT_GRAY)
    mood = screen.input("Enter your mood: ", color=COLORS.YELLOW)
    if mood == '': mood = 1
    mood = int(mood)
    if mood == 6:
        screen.clear()
        screen.render()
    else:
        mood = moods[mood]
        idx = 1
        screen.clear()
        screen.render()
        Header(f"{mood[0]} ENTRIES WITH MOOD [{mood[2:]}] {mood[0]}", color=COLORS.LIGHT_GREEN)
        for i in os.listdir(f".lifelog/{username}"):
            with open(f".lifelog/{username}/{i}", 'rb') as file:
                data = pickle.load(file)
                dMood = moods[int(data['mood'])]
                date = data['date']
                content = data['content'][:30] + "..."
                if mood == dMood:
                    screen.print(f"[{idx}] [{date}] - Title: {i.replace('_', ' ').title()[:-4]}", color=COLORS.YELLOW)
                    screen.line()
                    screen.print(content, color=COLORS.LIGHT_GRAY)
                    screen.line()
            idx += 1
            screen.print()
            screen.print()
            screen.render()
        screen.input("Press ENTER to go back!!", color=COLORS.DARK_GRAY)
        screen.clear()
        screen.render()
        ViewByMood(username)

def ViewEntries(username: str):
    Header("📖  VIEW PAST ENTRIES  📖", color=COLORS.LIGHT_GREEN)
    if len(os.listdir(f".lifelog/{username}/")) == 0:
        screen.print("You don't have any diary entries. Create one first", color=COLORS.YELLOW)
        screen.input("Press ENTER to go back", color=COLORS.DARK_GRAY)
        screen.clear()
        screen.render()
    else:
        screen.print("Choose how you’d like to view your entries:", color=COLORS.YELLOW)
        screen.line()
        screen.print()
        screen.print("> [1] View all entries", color=COLORS.LIGHT_GREEN)
        screen.print("[2] View by date range", color=COLORS.LIGHT_GRAY)
        screen.print("[3] View by mood", color=COLORS.LIGHT_GRAY)
        screen.print("[4] Back to dashboard", color=COLORS.LIGHT_GRAY)
        screen.line()
        choice = screen.input("Enter your choice (1-4): ", color=COLORS.YELLOW)
        if choice == '':
            choice = 1
        choice = int(choice)
        screen.clear()
        screen.render()
        if choice == 1:
            ViewAll(username)

        elif choice == 2:
            ViewDateRange(username)

        elif choice == 3:
            ViewByMood(username)

        elif choice == 4:
            screen.clear()
            screen.render()
        else:
            screen.clear()
            screen.render()

def MoodAnalytics(username: str):
    Header("📊  MOOD ANALYTICS  📊", color=COLORS.LIGHT_GREEN)
    screen.print("Your Mood record:", color=COLORS.YELLOW)
    screen.line()
    stats = {1:0,2:0,3:0,4:0,5:0}
    for i in os.listdir(f".lifelog/{username}"):
        with open(f".lifelog/{username}/{i}", 'rb') as file:
            data = pickle.load(file)
            mood = int(data['mood'])
            stats[mood] += 1
    screen.print(f"😊 Happy     →  {stats[1]} days", color=(COLORS.LIGHT_GREEN if stats[1] !=0 else COLORS.DARK_GRAY))
    screen.print(f"😌 Calm      →  {stats[2]} days", color=(COLORS.YELLOW if stats[2] !=0 else COLORS.DARK_GRAY))
    screen.print(f"😔 Sad       →  {stats[3]} days", color=(COLORS.LIGHT_PURPLE if stats[3] !=0 else COLORS.DARK_GRAY))
    screen.print(f"😤 Stressed  →  {stats[4]} days", color=(COLORS.LIGHT_RED if stats[4] !=0 else COLORS.DARK_GRAY))
    screen.print(f"😎 Confident →  {stats[5]} days", color=(COLORS.CYAN if stats[5] !=0 else COLORS.DARK_GRAY))
    screen.line()
    if stats != {1:0,2:0,3:0,4:0,5:0}:
        max = 0
        mostCommon = 1
        for i in stats.items():
            if i[1] > max: 
                mostCommon = i[0]
                i = max
        screen.print()
        screen.line()
        screen.print(f"Most common mood: {moods[mostCommon]}", color=COLORS.LIGHT_GREEN)
        screen.line()
        screen.print("Plotting chart....", color=COLORS.LIGHT_GRAY)
        screen.render()
        try:
            Plot(stats)
            pass
        except Exception as E:
            screen.print("[x] Could not plot chart due to some unforseen reasons. Sorry", color=COLORS.LIGHT_RED)
            screen.print(str(E))
            screen.render()
            time.sleep(1)
        screen.render()
    screen.input("Press ENTER to go back!!", color=COLORS.DARK_GRAY)
    screen.clear()
    screen.render()

def EditDelete(username: str):
    Header("🧹  EDIT / DELETE ENTRIES  🧹", color=COLORS.LIGHT_GREEN)
    screen.print("Here are your recent entries:", color=COLORS.YELLOW)
    screen.line()
    idx = 1
    titles = []
    for i in os.listdir(f".lifelog/{username}"):
        with open(f".lifelog/{username}/{i}", 'rb') as file:
            data = pickle.load(file)
            mood = moods[int(data['mood'])][2:]
            titles.append(i.replace("_", " ").title()[:-4])
            date = datetime.strptime(data['date'], "%d %B %Y").strftime("%d %b %Y")
            screen.print(f"[{idx}] [{date}] - {i.replace('_', ' ').title()[:-4]} ({mood})", color=COLORS.LIGHT_GRAY)
        idx += 1
    if titles == []:
        screen.print("You don't have any Diary entries as of now!", color=COLORS.YELLOW)
        screen.input("Press ENTER to go back", color=COLORS.DARK_GRAY)
        screen.clear()
        screen.render()

    else:
        try:
            choice = int(screen.input("Index of the entry to edit/delete (or ENTER to go back):", color=COLORS.YELLOW))-1
            if choice < 0 or choice > idx:
                screen.print(f"[x] You only have {idx-1} diaries!", color=COLORS.LIGHT_RED)
                screen.render()
                time.sleep(1)
                screen.clear()
                screen.render()
            else:
                screen.clear()
                screen.render()
                screen.print(f"TITLE: {titles[choice]}", color=COLORS.YELLOW)
                screen.print()
                screen.print("What would you like to do?", color=COLORS.YELLOW)
                screen.line()
                screen.print("> [1] Edit this entry", color=COLORS.LIGHT_GREEN)
                screen.print("[2] Delete this entry", color=COLORS.LIGHT_GRAY)
                screen.print("[3] Cancel", color=COLORS.LIGHT_GRAY)
                screen.line()
                action = screen.input("Enter your choice: ", color=COLORS.YELLOW)
                if action == '':action =1
                action = int(action)
                if action == 1:
                    screen.clear()
                    screen.render()
                    screen.print()
                    screen.print(titles[choice], color=COLORS.LIGHT_GREEN, centered=True)
                    screen.line()
                    screen.print("Editing Entry...", color=COLORS.YELLOW)
                    newMood = screen.input("New Mood: ", color=COLORS.YELLOW)
                    if not newMood.isnumeric() or int(newMood) > 5 or int(newMood)<0:
                        screen.print("[x] Invalid mood", color=COLORS.LIGHT_RED)
                        screen.render()
                        time.sleep(1)
                        screen.clear()
                        screen.render()
                    else:
                        screen.print("Modify text below (type END when done):", color=COLORS.LIGHT_GRAY)
                        diary = screen.editor("> ", color=COLORS.DARK_GRAY)
                        screen.print()
                        screen.line()
                        screen.print()
                        with open(f".lifelog/{username}/{titles[choice].replace(' ','_').lower()}.dat", 'wb') as file:
                            data = { "content": diary, "mood": newMood, "date": datetime.now().strftime("%d %B %Y") }
                            pickle.dump(data, file)
                        screen.line()
                        screen.print("[✔] Entry updated successfully!", color=COLORS.LIGHT_GREEN)
                        screen.input("Press ENTER to go back", color=COLORS.DARK_GRAY)
                        screen.clear()
                        screen.render()

                elif action == 2:
                    confirm = screen.input("Are you sure you want to delete this entry? (Y/N)", color=COLORS.LIGHT_RED)
                    if confirm.upper() == 'Y':
                        os.remove(f'.lifelog/{username}/{titles[choice].replace(" ", "_").lower()}.dat')
                    screen.clear()
                    screen.render()
                else:
                    screen.clear()
                    screen.render()
        except Exception:
            screen.clear()
            screen.render()
    
def killSwitch():
    screen.clear()
    screen.render()
    logo = """
###, ,##, ,##,
#  # #  # #  #
###  #  # #  #
#  # #  # #  #
###' '##' '##'
            .--,
           /  (
          /    \
         /      \\                      <---- THIS IS YOUR ACCOUNT NOW
        /  0  0  \\                      <---- POOR GUY
((()   |    ()    |   ()))
\\  ()  (  .____.  )  ()  /
 |` \\_/ \\  `""`  / \\_/ `|
 |       `.'--'.`       |
  \\        `""`        /
   \\                  /
    `.              .'    ,
jgs  |`             |  _.'|
     |              `-'  /
     \\                 .'
      `.____________.-'
    """
    showASCII(logo, False)
    screen.render()
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    exit()

def Settings(username: str):
    file = open(".lifelog/user.dat", 'rb+')
    acc = pickle.load(file)
    Header("⚙️  Settings", COLORS.LIGHT_GREEN)
    screen.print(f"> [1] Password Protected Diary: {'ENABLED' if acc['usePass'] == 'y' else 'DISABLED'}", color=COLORS.LIGHT_GREEN)
    screen.print()
    screen.line(color=COLORS.RED)
    screen.print('DANGER ZONE', color=COLORS.LIGHT_RED)
    screen.line(color=COLORS.RED)
    screen.print("[2] Delete All Diaries", color=COLORS.LIGHT_RED)
    screen.print("[3] Delete Account", color=COLORS.LIGHT_RED)
    screen.print("[4] Go back", color=COLORS.LIGHT_GRAY)
    screen.line(color=COLORS.RED)
    screen.print()
    choice = screen.input("Enter your choice: ", color=COLORS.YELLOW)
    if choice == '':
        choice = 1
    choice = int(choice)
    if choice == 1:
        acc['usePass'] = 'y' if acc['usePass'] == 'n' else 'n'
        pickle.dump(acc, file)
    elif choice == 2:
        ans=screen.input("Are you sure you want to delete all diaries. This action is irreversible (y/n)", color=COLORS.LIGHT_RED)
        if ans.lower() == 'y':
            shutil.rmtree(f".lifelog/{username}")
            os.mkdir(f".lifelog/{username}")
    elif choice == 3:
        ans=screen.input("Are you sure you want to permanentely delete your account.\nThis action is irreversible and you will loose all your data (y/n)", color=COLORS.LIGHT_RED)
        if ans.lower() == 'y':
            shutil.rmtree(f".lifelog/")
            screen.print("Account deleted successfully!", color=COLORS.RED)
            killSwitch()
    else:
        screen.clear()
        screen.render()
    pickle.dump(acc, file)
    file.close()

def Dashboard(username: str):
    lastLogged = loadStats()['lastLogged']

    Header("🌿 LifeLog Dashboard 🌿", COLORS.LIGHT_GREEN)
    screen.print(f"Welcome back {username}!!", color=COLORS.YELLOW)
    screen.print(f"Last Login: {lastLogged} | Total Entires: {len(os.listdir(f'.lifelog/{username}/'))}", color=COLORS.YELLOW)
    screen.print()
    screen.line()
    screen.print()
    screen.print("> [1] ✍️   Add a new entry", color=COLORS.LIGHT_GREEN)
    screen.print("[2] 📖  View past entries", color=COLORS.LIGHT_GRAY)  
    screen.print("[3] 🧹  Edit or delete an entry", color=COLORS.LIGHT_GRAY)  
    screen.print("[4] 📊  View mood analytics", color=COLORS.LIGHT_GRAY)  
    screen.print("[5] ⚙️   Settings", color=COLORS.LIGHT_GRAY)  
    screen.print("[6] 🔒  Log out", color=COLORS.LIGHT_GRAY)  
    screen.print("[7] 👋  Quit", color=COLORS.LIGHT_GRAY)  
    screen.print()
    screen.line()
    screen.print()
    try:
        choice = screen.input("What would you like to do today? ", color=COLORS.LIGHT_GREEN)
        if choice == '':
            choice = 1
        choice = int(choice)
        screen.render()
        screen.clear()
        if choice == 1:
            AddEntry(username)
        elif choice == 2:
            ViewEntries(username)
        elif choice == 3:
            EditDelete(username)
        elif choice == 4:
            MoodAnalytics(username)
        elif choice == 5:
            Settings(username)
        elif choice == 6:
            Logout()
            Quit(username, logged=True)
        elif choice == 7:
            Quit(username, logged=False)
            screen.quit()
        else:
            screen.print("Invalid")
            screen.render()
            screen.clear()
    except Exception:
        screen.clear()
        screen.render()

def Logout():
    stats = loadStats()
    stats['logged'] = False
    with open(".lifelog/stats.dat", 'wb') as file:
        pickle.dump(stats, file)

def AddEntry(username: str):
    Header("✍️  ADD A NEW ENTRY  ✍️")
    screen.print(f"Date: {datetime.now().strftime('%d %B %Y')} | User: {username}", color=COLORS.YELLOW)
    title = screen.input("Title: ", color=COLORS.YELLOW)
    if title.strip().lower().replace(" ", "_") + ".dat" in os.listdir(f".lifelog/{username}/"):
        screen.print("[X] You already have a diary with the same name. Choose a different name", color=COLORS.LIGHT_RED)
        screen.render()
        time.sleep(1)
        screen.clear()
        AddEntry(username)
    elif len(title.strip()) == 0:
        screen.print("[X] Title cannot be empty.", color=COLORS.LIGHT_RED)
        screen.render()
        time.sleep(1)
        screen.clear()
        AddEntry(username)
    else:
        screen.line()
        screen.print("Write your diary below (Type END on a new line to finish)", color=COLORS.DARK_GRAY)
        screen.line()
        diary = screen.editor("> ", color=COLORS.DARK_GRAY) 
        screen.print()
        screen.line()
        screen.print("[1] 😊 Happy")
        screen.print("[2] 😌 Calm")
        screen.print("[3] 😔 Sad")
        screen.print("[4] 😤 Stressed")
        screen.print("[5] 😎 Confident")
        screen.line()
        mood = screen.input("Enter your mood (1-5):", color=COLORS.YELLOW)
        screen.line()
        if not mood.isnumeric() or int(mood) < 0 or int(mood) > 5:
            screen.print("[X] Invalid mood", color=COLORS.LIGHT_RED)
            screen.print("Selecting [1] Happy by default. (You can change this later)", color=COLORS.DARK_GRAY)
            mood = '1'
        if mood == '':
            mood = '1'

        with open(f".lifelog/{username}/{title.replace(' ','_').lower()}.dat", 'wb') as file:
            data = { "content": diary, "mood": mood, "date": datetime.now().strftime("%d %B %Y") }
            pickle.dump(data, file)

        screen.print()
        screen.print("""Saving your entry...
    [✔] Entry saved successfully! 🌿
    “Remember, your thoughts are seeds — keep planting good ones.”""", color=COLORS.LIGHT_GREEN)
        screen.line()
        screen.input("Press ENTER to continue: ", color=COLORS.DARK_GRAY)
        screen.clear()

def CreateUser():
    users = []

    if os.path.exists(".lifelog/user.dat"):
        with open(".lifelog/user.dat", 'rb') as F:
            while True:
                try:
                    users.append(pickle.load(F)['username'])
                except EOFError:
                    break
    showASCII(r"""
      ______                                   __               
 /      \                                 /  |              
/$$$$$$  |  ______    ______    ______   _$$ |_     ______  
$$ |  $$/  /      \  /      \  /      \ / $$   |   /      \ 
$$ |      /$$$$$$  |/$$$$$$  | $$$$$$  |$$$$$$/   /$$$$$$  |
$$ |   __ $$ |  $$/ $$    $$ | /    $$ |  $$ | __ $$    $$ |
$$ \__/  |$$ |      $$$$$$$$/ /$$$$$$$ |  $$ |/  |$$$$$$$$/ 
$$    $$/ $$ |      $$       |$$    $$ |  $$  $$/ $$       |
 $$$$$$/  $$/        $$$$$$$/  $$$$$$$/    $$$$/   $$$$$$$/
""")
    screen.print()
    screen.line()
    screen.render()
    username = screen.input("Username (or q to quit): ", color=COLORS.YELLOW)
    if username in users:
        screen.print()
        screen.line()
        screen.print("[x] Username already exists on this system. Try another name", color=COLORS.LIGHT_RED)
        screen.line()
        screen.render()
        time.sleep(1)
        screen.clear()
        screen.render()
        CreateUser()

    else:
        if username == 'q':
            screen.quit()

        password = screen.input("Password: ", True, color=COLORS.LIGHT_GREEN)
        confirm = screen.input("Confirm Password: ", True, color=COLORS.LIGHT_GREEN)
        if password != confirm:
            screen.line()
            screen.print("[x] Your password does not match. Try again", color=COLORS.LIGHT_RED)
            screen.line()
            screen.render()
            time.sleep(1)
            screen.clear()
            screen.render()
            CreateUser()
        else:
            usePass = screen.input("Do you want to protect your Diaries (remember your password) (Y/N): ", color=COLORS.YELLOW)
            if usePass.upper() not in ['Y', 'N']:
                screen.line()
                screen.print("[x] Invalid answer. Expected Y or N. Try again!", color=COLORS.LIGHT_RED)
                screen.line()
                screen.render()
                time.sleep(1)
                screen.clear()
                screen.render()
                CreateUser()
            else:
                try:
                    if not os.path.isdir(".lifelog/"):
                        os.mkdir(".lifelog")
                    with open('.lifelog/user.dat', 'ab') as file:
                        pickle.dump({ "username": username, "password": password, "usePass":usePass}, file)
                    with open(".lifelog/stats.dat", 'wb') as file:
                        pickle.dump({"lastLogged": datetime.now().strftime("%d %B %Y"), "username":username}, file)
                    if not os.path.isdir(f".lifelog/{username}"):
                        os.mkdir(f".lifelog/{username}")

                except Exception:
                    exit()

                screen.line()
                screen.print("[✔] Account created successfully! 🌱", color=COLORS.LIGHT_GREEN)
                screen.print("You can now log in to start your journal.")
                screen.line()
                screen.render()
                screen.input("Press ENTER to continue", color=COLORS.LIGHT_GRAY)

def Quit(username: str,logged: bool):
    if logged:
        with open(".lifelog/stats.dat", 'wb') as file:
            pickle.dump({"lastLogged": datetime.now().strftime("%d %B %Y"), "username":username}, file)

    screen.CenterText("-"*(os.get_terminal_size().columns - 20), COLORS.YELLOW)
    screen.print("🌿  BYE!! 🌿", True)
    screen.print("Remember to log your thoughts tomorrow!!", True)
    screen.line()
    screen.render()
    time.sleep(1)
    screen.clear()

def showASCII(txt: str, center: bool = True):
    for line in txt.split('\n'):
        if line.strip() == 'LifeLog':
            screen.print(line, center, COLORS.YELLOW)
        else:
            screen.print(line, center, COLORS.LIGHT_GREEN)

def loadStats():
    with open(".lifelog/stats.dat", 'rb') as stats:
        return pickle.load(stats)
try:
# WELCOME SCREEN
    while True:
        screen = Window('LifeLog', border='*')
        showASCII(logo)
        screen.line()
        screen.print("🌿  WELCOME TO LIFELOG 🌿", True, color=COLORS.CYAN)
        screen.line()
        screen.print("Your personal digital diary & mood companion.", True, COLORS.LIGHT_GREEN)
        screen.print()
        screen.print("> [1] Start LifeLog", color=COLORS.LIGHT_GREEN, padding=10)
        screen.print("[2] View Docs", color=COLORS.LIGHT_GRAY, padding=10)
        screen.print("[3] Exit", color=COLORS.LIGHT_GRAY, padding=10)
        screen.print()
        screen.line()
        choice = screen.input("What do you want to do?", color=COLORS.LIGHT_RED)
        screen.clear()
        if choice == '1' or choice == '':
            if not os.path.isdir('.lifelog'):
                screen.print("You seem new here!!!\nCreate an account to start your diary journey right now!!", True)

            while True:
                logged = False
                if os.path.isdir('.lifelog'):
                    stats = loadStats()
                    try:
                        if stats['logged']:
                            logged = True
                    except KeyError:
                            logged = False


                if not logged:
                    # DASHBOARD SCREEN
                    showASCII(r"""
 __       __            __                                             
/  |  _  /  |          /  |                                            
$$ | / \ $$ |  ______  $$ |  _______   ______   _____  ____    ______  
$$ |/$  \$$ | /      \ $$ | /       | /      \ /     \/    \  /      \ 
$$ /$$$  $$ |/$$$$$$  |$$ |/$$$$$$$/ /$$$$$$  |$$$$$$ $$$$  |/$$$$$$  |
$$ $$/$$ $$ |$$    $$ |$$ |$$ |      $$ |  $$ |$$ | $$ | $$ |$$    $$ |
$$$$/  $$$$ |$$$$$$$$/ $$ |$$ \_____ $$ \__$$ |$$ | $$ | $$ |$$$$$$$$/ 
$$$/    $$$ |$$       |$$ |$$       |$$    $$/ $$ | $$ | $$ |$$       |
$$/      $$/  $$$$$$$/ $$/  $$$$$$$/  $$$$$$/  $$/  $$/  $$/  $$$$$$$/
""")

                    screen.print()
                    screen.line()
                    screen.print("• [1] Login to your account",  color=COLORS.LIGHT_GREEN)
                    screen.print("○ [2] Create a new account",  color=COLORS.LIGHT_GRAY)  
                    screen.print("○ [3] Exit", color=COLORS.LIGHT_GRAY)  
                    screen.line()
                    screen.render()
                    opt = ''
                    try:
                        opt = int(input(">>> "))
                    except Exception:
                        if opt == '':
                            opt = 1
                    screen.clear()

                    if opt == 1:
                        if logged:
                            stats = loadStats()
                            try:
                                if stats['logged']:
                                    Dashboard(stats['username'])
                            except KeyError:
                                Login()
                        else:
                            Login() 

                    elif opt == 2:
                        CreateUser()

                    elif opt == 3:
                        Quit("", logged=False)
                        exit()

                    else:
                        screen.clear()
                        screen.render()
                    screen.clear()
                else:
                    stats = loadStats()
                    Dashboard(stats['username'])
        elif choice == '2':
            ShowHelp(screen)
            screen.input("Press ENTER to go back", color=COLORS.DARK_GRAY)

        elif choice == '3':
            screen.clear()
            screen.CenterText("-"*(os.get_terminal_size().columns - 20),COLORS.YELLOW)
            screen.print("🌿  BYE!! 🌿", True)
            screen.print("Remember to log your thoughts tomorrow!!", True)
            screen.line()
            screen.render()
            time.sleep(1)
            break
 
        else:
            continue

except KeyboardInterrupt:
    exit()
