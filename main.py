from plot import Plot
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
logo = f"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣧⠀⠀⣴⠄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⡀⣰⣏⡤⠀⢀⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢳⣦⣄⡘⢿⣿⣇⢏⣱⠖⣠⣿⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣦⠹⡈⡎⢫⣾⣿⡟⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⡝⣿⣧⠹⠀⣾⡿⠟⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣀⣀⡙⣖⠻⡞⡔⢰⢩⡷⣻⡁⢀⣤⣶⠖⠀
⠀⠀⠀⠀⣠⣾⡿⠟⠛⠻⢷⡛⠘⢸⠃⠊⠿⢁⣾⣿⡿⠃⠀⠀
⠀⠀⢠⣾⠟⠃⠀⠀⠀⠀⠀⠹⡀⠈⢀⣠⣴⡿⠟⠋⢀⣀⣤⠤
⠀⠀⠀⠀⢀⣠⣤⣤⣄⠀⠀⠀⢀⠗⠁⠀⣠⣴⣶⣿⣿⡿⠋⠀
⠀⠀⣠⣾⣿⣿⣿⣿⠟⠃⠢⡄⡜⠀⢠⣾⣿⣿⡿⠟⠋⠀⠀⠀
⠒⠛⠛⠻⠟⠿⠛⠁⠀⠀⠀⢈⢋⠶⡛⠋⠉⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠖⠁⢠⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡈⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀ ⠀⠙⣿⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
LifeLog
"""

def Header(msg: str, color: str = COLORS.LIGHT_WHITE):
    screen.line("═", COLORS.PURPLE)
    screen.print(msg, True, COLORS.CYAN)
    screen.line("═", COLORS.PURPLE)
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
    Header("🌿 LOGIN 🌿")
    screen.render()
    username = screen.input("Username (or q to quit): ")
    if username == 'q':
        screen.quit()
    if username not in users:
        screen.print(f"User not found. It seems like you have not created an account. Try creating it")
        screen.render()
        screen.quit()

    password = screen.input("Password: ", True)
    user = {}
    for u in data:
        if u['username'] == username:
            user = u

    if user['username'] == username and user['password'] != password:
            screen.print(f"Incorrent Password. Try again")
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
        screen.print(f"[✔] Login successful! Welcome back, {username} !!")
        screen.print("Loading your dashboard...")
        screen.render()
        time.sleep(1)
        screen.clear()
        screen.render()
        Dashboard(username)

def ViewAll(username: str):
    Header("📖  VIEW ALL ENTRIES  📖")
    screen.print("All of Diary entries: ")
    screen.print()
    idx = 1
    for i in os.listdir(f".lifelog/{username}"):
        with open(f".lifelog/{username}/{i}", 'rb') as file:
            data = pickle.load(file)
            mood = moods[int(data['mood'])]
            date = data['date']
            content = data['content'][:30] + "..."
            screen.print(f"[{idx}] [{date}] - [{mood} ]")
            screen.print(f"Title: {i.replace('_', ' ').title()[:-4]}")
            screen.print("-"*(os.get_terminal_size().columns - 4))
            screen.print(content)
            screen.print("-"*(os.get_terminal_size().columns - 4))
        idx += 1
        screen.print()
        screen.print()

    try:
        choice = int(screen.input("Which entry do you want to see? (-1 to quit): "))
        if choice > len(os.listdir(f".lifelog/{username}")):
            screen.print("Invalid. Try again")
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
                    screen.print(f"[{date}] - [{mood} ]")
                    screen.print(f"Title: {os.listdir(f'.lifelog/{username}')[choice-1].replace('_', ' ').title()[:-4]}")
                    screen.print("-"*(os.get_terminal_size().columns - 4))
                    screen.print(content)
                    screen.print("-"*(os.get_terminal_size().columns - 4))
                screen.print()
                screen.input("Press ENTER to go back!")
                screen.clear()
                screen.render()
    except Exception:
        screen.clear()
        screen.render()

def ViewDateRange(username: str):
    Header("📖  VIEW ENTRIES BY DATE 📖")
    screen.print("Choose how you’d like to view your entries:")
    screen.print()
    start = datetime.strptime(screen.input("Enter Start Date: (DD-MM-YYYY) "), '%d-%m-%Y')
    end = datetime.strptime(screen.input("Enter End Date: (DD-MM-YYYY) "), '%d-%m-%Y')
    screen.print()
    idx = 1
    for i in os.listdir(f".lifelog/{username}"):
        with open(f".lifelog/{username}/{i}", 'rb') as file:
            data = pickle.load(file)
            mood = moods[int(data['mood'])]
            date = datetime.strptime(datetime.strptime(data['date'], "%d %B %Y").strftime("%d-%m-%Y"), "%d-%m-%Y")
            content = data['content'][:30] + "..."
            if date > start and date < end:
                screen.print(f"[{idx}] [{date.strftime('%d %b %Y')}] - [{mood} ]")
                screen.print(f"Title: {i.replace('_', ' ').title()[:-4]}")
                screen.print("-"*(os.get_terminal_size().columns - 4))
                screen.print(content)
                screen.print("-"*(os.get_terminal_size().columns - 4))
        idx += 1
        screen.print()
        screen.print()
        screen.render()
    screen.input("Press ENTER to go back!!")
    screen.clear()
    screen.render()

def ViewByMood(username: str):
    Header("💭 VIEW ENTRIES BY MOOD 💭")
    screen.print("Which mood would you like to explore?")
    screen.print()
    screen.print("""[1] 😊 Happy
[2] 😌 Calm
[3] 😔 Sad
[4] 😤 Stressed
[5] 😎 Confident
[6] Back to menu
    """)
    mood = int(screen.input("Enter your mood: "))
    if mood == 6:
        screen.clear()
        screen.render()
    else:
        mood = moods[mood]
        idx = 1
        screen.clear()
        screen.render()
        Header(f"{mood[0]} ENTRIES WITH MOOD [{mood[1:]}] {mood[0]}")
        for i in os.listdir(f".lifelog/{username}"):
            with open(f".lifelog/{username}/{i}", 'rb') as file:
                data = pickle.load(file)
                dMood = moods[int(data['mood'])]
                date = data['date']
                content = data['content'][:30] + "..."
                if mood == dMood:
                    screen.print(f"[{idx}] [{date}] - Title: {i.replace('_', ' ').title()[:-4]}")
                    screen.print("-"*(os.get_terminal_size().columns - 4))
                    screen.print(content)
                    screen.print("-"*(os.get_terminal_size().columns - 4))
            idx += 1
            screen.print()
            screen.print()
            screen.render()
        screen.input("Press ENTER to go back!!")
        screen.clear()
        screen.render()

def ViewEntries(username: str):
    Header("📖  VIEW PAST ENTRIES  📖")
    screen.print("Choose how you’d like to view your entries:")
    screen.print()
    screen.print("""[1] View all entries  
[2] View by date range  
[3] View by mood  
[4] Back to dashboard""")
    screen.print("-"*(os.get_terminal_size().columns - 4))
    choice = int(screen.input("Enter your choice (1-4): "))
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
    Header("📊  MOOD ANALYTICS  📊")
    screen.print("Your Mood record:")
    screen.print()
    stats = {1:0,2:0,3:0,4:0,5:0}
    for i in os.listdir(f".lifelog/{username}"):
        with open(f".lifelog/{username}/{i}", 'rb') as file:
            data = pickle.load(file)
            mood = int(data['mood'])
            stats[mood] += 1
    screen.print(f"😊 Happy     →  {stats[1]} days")
    screen.print(f"😌 Calm      →  {stats[2]} days")
    screen.print(f"😔 Sad       →  {stats[3]} days")
    screen.print(f"😤 Stressed  →  {stats[4]} days")
    screen.print(f"😎 Confident →  {stats[5]} days")
    screen.print()
    if stats != {1:0,2:0,3:0,4:0,5:0}:
        max = 0
        mostCommon = 1
        for i in stats.items():
            if i[1] > max: 
                mostCommon = i[0]
                i = max
        screen.print()
        screen.print('-'*(os.get_terminal_size().columns-4))
        screen.print(f"Most common mood: {moods[mostCommon]}")
        screen.print('-'*(os.get_terminal_size().columns-4))
        screen.print("Plotting chart....")
        screen.render()
        try:
            Plot(stats)
            pass
        except Exception as E:
            screen.print("[x] Could not plot chart due to some unforseen reasons. Sorry")
            screen.print(str(E))
            screen.render()
            time.sleep(1)
        screen.render()
    screen.input("Press ENTER to go back!!")
    screen.clear()
    screen.render()

def EditDelete(username: str):
    Header("🧹  EDIT / DELETE ENTRIES  🧹")
    screen.print("Here are your recent entries:")
    idx = 1
    titles = []
    for i in os.listdir(f".lifelog/{username}"):
        with open(f".lifelog/{username}/{i}", 'rb') as file:
            data = pickle.load(file)
            mood = moods[int(data['mood'])][2:]
            titles.append(i.replace("_", " ").title()[:-4])
            date = datetime.strptime(data['date'], "%d %B %Y").strftime("%d %b %Y")
            screen.print(f"[{idx}] [{date}] - {i.replace('_', ' ').title()[:-4]} ({mood})")
        idx += 1
    screen.print('-'*(os.get_terminal_size().columns-4))

    try:
        choice = int(screen.input("Index of the entry to edit/delete (or ENTER to go back):"))-1
        if choice < 0 or choice > idx:
            screen.clear()
            screen.render()
        else:
            screen.clear()
            screen.render()
            screen.print(f"You selected: {titles[choice]}")
            screen.print()
            screen.print("What would you like to do?")
            screen.print("[1] Edit this entry")
            screen.print("[2] Delete this entry")
            screen.print("[3] Cancel")
            screen.print('-'*(os.get_terminal_size().columns-4))
            action = int(screen.input("Enter your choice: "))
            if action == 1:
                screen.clear()
                screen.render()
                screen.print("Editing Entry...")
                newMood = screen.input("New Mood: ")
                screen.print("Modify text below (type END when done):")
                diary = screen.editor("> ") 
                screen.print()
                screen.print("-"*(os.get_terminal_size().columns - 4))
                screen.print()
                with open(f".lifelog/{username}/{titles[choice].replace(' ','_').lower()}.dat", 'wb') as file:
                    data = { "content": diary, "mood": newMood, "date": datetime.now().strftime("%d %B %Y") }
                    pickle.dump(data, file)
                screen.print("[✔] Entry updated successfully!")
                screen.input("Press ENTER to go back")
                screen.clear()
                screen.render()

            elif action == 2:
                confirm = screen.input("Are you sure you want to delete this entry? (Y/N)")
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
    

def Dashboard(username: str):
    lastLogged = loadStats()['lastLogged']

    Header("🌿 LifeLog Dashboard 🌿", COLORS.LIGHT_BLUE)
    screen.print(f"Welcome back {username}!!", color=COLORS.LIGHT_GREEN)
    screen.print(f"Last Login: {lastLogged} | Total Entires: {len(os.listdir(f'.lifelog/{username}/'))}", color=COLORS.LIGHT_GREEN)
    screen.print()
    screen.line()
    screen.print("What would you like to do today?", color=COLORS.YELLOW)
    screen.print()
    screen.print("[1] ✍️   Add a new entry")
    screen.print("[2] 📖  View past entries")  
    screen.print("[3] 🧹  Edit or delete an entry")  
    screen.print("[4] 📊  View mood analytics")  
    screen.print("[5] 🔒  Log out", color=COLORS.LIGHT_RED)  
    screen.print("[6] 👋  Quit", color=COLORS.LIGHT_RED)  
    screen.print()
    screen.line()
    screen.print()
    try:
        choice = int(screen.input("Enter your choice: ", color=COLORS.LIGHT_GREEN))
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
            Logout()
            Quit(username, logged=True)
        elif choice == 6:
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
    screen.print(f"Date: {datetime.now().strftime('%d %B %Y')} | User: {username}")
    title = screen.input("Title: ")
    screen.print("-"*(os.get_terminal_size().columns - 4))
    screen.print("Write your diary below (Type END on a new line to finish)")
    diary = screen.editor("> ") 
    screen.print()
    screen.print("-"*(os.get_terminal_size().columns - 4))
    screen.print()
    screen.print("[1] 😊 Happy")
    screen.print("[2] 😌 Calm")
    screen.print("[3] 😔 Sad")
    screen.print("[4] 😤 Stressed")
    screen.print("[5] 😎 Confident")
    mood = screen.input("Enter your mood (1-5):")
    screen.print()

    with open(f".lifelog/{username}/{title.replace(' ','_').lower()}.dat", 'wb') as file:
        data = { "content": diary, "mood": mood, "date": datetime.now().strftime("%d %B %Y") }
        pickle.dump(data, file)

    screen.print("""Saving your entry...
[✔] Entry saved successfully! 🌿
“Remember, your thoughts are seeds — keep planting good ones.”""")
    screen.print("-"*(os.get_terminal_size().columns - 4))
    screen.input("Press enter to continue: ")
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
    Header("🌿 Create Account 🌿")
    screen.render()
    username = screen.input("Username (or q to quit): ")
    if username in users:
        screen.print("X Username already exists on this system. Try another name")
        screen.render()
        time.sleep(1)
        screen.clear()
        screen.render()
        CreateUser()

    else:
        if username == 'q':
            screen.quit()

        password = screen.input("Password: ", True)
        confirm = screen.input("Confirm Password: ", True)
        if password != confirm:
            screen.print("X Your password does not match. Try again")
            screen.render()
            time.sleep(1)
            screen.clear()
            screen.render()
            CreateUser()
        else:
            usePass = screen.input("Do you want to protect your Diaries (remember your password) (Y/N): ")
            if usePass.upper() not in ['Y', 'N']:
                screen.print("Invalid answer. Expected Y or N. Try again!")
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

                screen.print("[✔] Account created successfully! 🌱")
                screen.print("You can now log in to start your journal.")
                screen.render()

def Quit(username: str,logged: bool):
    if logged:
        with open(".lifelog/stats.dat", 'wb') as file:
            pickle.dump({"lastLogged": datetime.now().strftime("%d %B %Y"), "username":username}, file)

    screen.CenterText("═"*(os.get_terminal_size().columns - 6))
    screen.print("🌿  BYE!! 🌿", True)
    screen.print("Remember to log your thoughts tomorrow!!", True)
    screen.print("═"*(os.get_terminal_size().columns - 10), True)
    screen.render()
    time.sleep(1)
    screen.clear()

def genLogo():
    for line in logo.split('\n'):
        if line.strip() == 'LifeLog':
            screen.print(line, True, COLORS.YELLOW)
        else:
            screen.print(line, True, COLORS.LIGHT_GREEN)

def loadStats():
    with open(".lifelog/stats.dat", 'rb') as stats:
        return pickle.load(stats)
try:
# WELCOME SCREEN
    screen = Window('LifeLog')
    genLogo()
    screen.render()
    time.sleep(2)
    screen.clear()
    screen.CenterText("═"*(os.get_terminal_size().columns - 6))
    screen.print("🌿  WELCOME TO LIFELOG 🌿", True)
    screen.print("═"*(os.get_terminal_size().columns - 10), True)
    screen.print("Your personal digital diary & mood companion.", True, COLORS.LIGHT_GREEN)
    screen.render()
    time.sleep(2)
    screen.clear()

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
            Header("🌿  WELCOME TO LIFELOG 🌿")
            screen.print("""• [1] Login to your account  
○ [2] Create a new account  
○ [3] Exit""")
            screen.render()
            opt = ''
            try:
                opt = int(input(">>> "))
            except Exception:
                if opt == '':
                    opt = 1
            screen.clear()
            Header("🌿  WELCOME TO LIFELOG 🌿")
            screen.print(f"""{'•' if opt == 1 else '○'} [1] Login to your account  
{'•' if opt == 2 else '○'} [2] Create a new account  
{'•' if opt == 3 else '○'} [3] Exit""")
            screen.render()
            time.sleep(0.5)
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
                break

            else:
                screen.clear()
                screen.render()
            screen.clear()
        else:
            stats = loadStats()
            Dashboard(stats['username'])

except KeyboardInterrupt:
    exit()
