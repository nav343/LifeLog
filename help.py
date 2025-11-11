from utils.colors import COLORS
from utils.window import Window

def showASCII(txt: str, screen: Window):
    for line in txt.split('\n'):
        screen.print(line,False, COLORS.LIGHT_GREEN)


meme = """
        _nnnn_                      
        dGGGGMMb     ,''''''''''''''.
       @p -p~ qMb    | LifeLog Yay! |
       M|@||@) M|   _;..............'
       @,----.JM| -'
      JS^\\__/  qKL
     dZP        qKRb
    dZP          qKKb                           
   fZP            SMMb
   HZM            MMMM
   FqM            MMMM
 __| ".        |\\dS"qML
 |    `.       | `' \\Zq
_)      \\.___.,|     .'
\\____   )MMMMMM|   .'
     `-'       `--' hjm
"""

def ShowHelp(screen: Window):
    showASCII(meme, screen)
    screen.line("=", color=COLORS.YELLOW)
    screen.print("LIFELOG - HELP PAGE", True, color=COLORS.LIGHT_GREEN)
    screen.line("=", color=COLORS.YELLOW)
    screen.print("""Welcome to LifeLog, your personal digital diary and mood
tracking application. This help page explains how to use
every feature of the program.""")

    screen.print()
    screen.line()
    screen.print("1. LOGGIN IN", True, COLORS.LIGHT_GREEN)
    screen.line()
    screen.print("""At startup, you can choose to log in, create an account,
or exit the application.

LOGIN:
- Enter your username.
- Enter your password.

If you forget your password, you will need to create a new
account.
""")
    screen.print()
    screen.line()
    screen.print("2. CREATING AN ACCOUNT", True,COLORS.LIGHT_GREEN)
    screen.line()
    screen.print("""Select "Create a new account" and enter:
- A unique username
- A password
""")

    screen.print()
    screen.line()
    screen.print("3. DASHBOARD OVERVIEW", True, COLORS.LIGHT_GREEN)
    screen.line()
    screen.print("""After logging in, you will see the main dashboard with the
following options:

1. Add a new entry
2. View past entries
3. Edit or delete an entry
4. View Mood analytics
5. Logout
6. Quit

Enter the number of the option you want to use.
""")

    screen.print()
    screen.line()
    screen.print("5. ADDING A NEW ENTRY", True,COLORS.LIGHT_GREEN)
    screen.line()
    screen.print("""When adding a new entry, you will be asked to provide:
- A title for the entry
- The content of your diary log
  - To end your diary, on a new line, type "END" and press ENTER
- Your mood for the day (Happy, Calm, Sad, Stressed, etc.)

LifeLog automatically records today's date and saves your entry
""")

    screen.print()
    screen.line()
    screen.print("6. VIEWING ENTRIES", True, COLORS.LIGHT_GREEN)
    screen.line()
    screen.print("""You can view past entries in several ways:

VIEW BY DATE RANGE:
- Enter a start date in DD-MM-YYYY format.
- Enter a end date in DD-MM-YYYY format.
- LifeLog displays all entries belonging in the range.

VIEW BY MOOD:
- Select a mood.
- All entries tagged with that mood are shown.
""")

    screen.print()
    screen.line()
    screen.print("7. EDITING/DELETING AN ENTRY", True, COLORS.LIGHT_GREEN)
    screen.line()
    screen.print("""Select "Edit an entry" to update old logs.
You can modify:
- Title
- Mood
- Content

Choose "Delete an entry" and select the entry you want to
remove. The entry is permanently deleted from the file and you cannot recover lost diaries
""")

    screen.print()
    screen.line()
    screen.print("8. MOOD ANALYTICS", True, COLORS.LIGHT_GREEN)
    screen.line()
    screen.print("""LifeLog provides simple mood insights using bar charts
Charts are created using the matplotlib library.
""")

    screen.print()
    screen.line()
    screen.print("9. COLORS AND USER INTERFACE", True, COLORS.LIGHT_GREEN)
    screen.line()
    screen.print("""The application uses a clean color theme:
- Cyan: Titles
- Yellow: Option numbers
- White: Explanations and text
- Green: Input prompts and success messages
- Red: Error messages
- Magenta/Blue: Borders and separators
""")
    
    screen.print()
    screen.line()
    screen.print("10. QUITTING", True, COLORS.LIGHT_GREEN)
    screen.line()
    screen.print("""Choose "Quit" (Option 6) to safely quit your session *WITHOUT LOGGING OUT* and return to
the main menu. All data is saved automatically.
You will be automatically logged in the next time you open LifeLog
""")

    screen.print()
    screen.line()
    screen.print("11. LOGGING OUT", True, COLORS.LIGHT_GREEN)
    screen.line()
    screen.print("""Choose "Logout" to safely exit your session and return to
the main menu. All data is saved automatically.
You will need to enter your username and password to access your account after logging out
""")

    screen.print()
    screen.line('=')
    screen.print("End of Help Page", True, COLORS.LIGHT_GREEN)
    screen.line('=')
