import os

if os.name == 'posix':
    import readline

from utils.colors import COLORS, TextColor

class Window():
    def __init__(self, title: str="Window", border: str = '|') -> None:
        self.__clear = 'cls' if os.name == 'nt' else 'clear'
        os.system(self.__clear)
        self.__buffer = []
        self.__pos = (0,0)
        self.title = title
        self.border=border
        self.window_size = (
            os.get_terminal_size().lines - 1,
            os.get_terminal_size().columns,
        )
        self.__set_buffer()

    def __remove_emoji(self, txt:str) -> int:
        if any(element in txt for element in ['📖', '🧹', '📊', '🔒', '🌿', '😊', '😌', '😔', '😤', '😎', '💭', "👋" ]):
            return txt.count(txt[0]) + 1
        elif any(element in txt for element in ['✍️','😊', '😌', '😔', '😤', '😎' ]):
            return 0 if txt.count(txt[0]) == 1 else -1
        else:
            return 1

    def __format(self, txt: str, centered: bool=False, padding: int=0):
        if txt[:2] == "\x1b[":
            main = txt[7:-4]
        else:
            main = txt
        partial = f"{self.border}{' '*((self.window_size[1] - len(main))//2 - (self.__remove_emoji(main)))}{txt}" if centered else f"{self.border} {' '*padding}{txt}"
        return f"{partial}{' '*(self.window_size[1] - len(partial) + (0 if main == txt else 11) - (self.__remove_emoji(main)))}{self.border}"

    def __set_buffer(self):
        self.__buffer.append(TextColor(f"+{'-' * (self.window_size[1] - 2)}+", COLORS.LIGHT_GRAY))
        for _ in range(self.window_size[0] - 2):
            self.__buffer.append(self.__format(" "))
        self.__buffer.append(TextColor(f"+{'-' * (self.window_size[1] - 2)}+", COLORS.LIGHT_GRAY))
        self.__pos = (1, 1)

    def __add_slots(self, num: int):
        currPos = self.__pos
        self.__buffer[-1] = self.__format(" ")
        for _ in range(0, num):
            self.__buffer.append(self.__format(" "))
        self.__buffer.append(TextColor(f"+{'-' * (self.window_size[1] - 2)}+", COLORS.LIGHT_GRAY))
        self.__pos = (currPos[0]-1, currPos[1])
        self.render()

    def close(self) -> None:
        os.system(self.__clear)
        self.__buffer = []

    def clear(self) -> None:
        os.system(self.__clear)
        self.__buffer = []
        self.__set_buffer()

    def quit(self) -> None:
        exit()

    def render(self) -> None:
        os.system(self.__clear)
        for buf in self.__buffer:
            print(buf)

    def CenterText(self, msg: str, color: str=COLORS.LIGHT_WHITE):
        self.__buffer[self.window_size[0]//2] = self.__format(TextColor(msg, color), True)
        self.__pos = (self.window_size[0]//2+1, self.__pos[1])

    def truncate(self, text):
        if len(text) <= self.window_size[1]-4:
            return text

        break_pos = text.rfind(' ', 0,  self.window_size[1]-4)
        if break_pos == -1:
            break_pos =  self.window_size[1]-4

        line = text[:break_pos].rstrip()
        remaining = text[break_pos:].lstrip()
        return line + "\n" + self.truncate(remaining)


    def print(self, msg: str=" ", centered: bool = False, color: str=COLORS.LIGHT_WHITE, padding:int = 10) -> None:
        try:
            for line in self.truncate(msg).split('\n'):
                self.__buffer[self.__pos[0]] = self.__format(TextColor(line, color), centered, padding)
                self.__pos = (self.__pos[0]+1, self.__pos[1])
        except IndexError:
            self.__add_slots(self.window_size[0])

    def editor(self, msg: str, terminate: str="END", color: str = COLORS.LIGHT_WHITE) -> str:
        self.print(msg, color=color)
        self.render()
        lines = []
        try:
            while True:
                line = input(TextColor("> ", color))
                if line == terminate:
                    break
                t = self.truncate(line).split("\n")
                try:
                    for i in range(0, len(t)):
                        self.__buffer[self.__pos[0]-1 + i] = self.__format(TextColor(msg,color) + t[i], padding=10)
                        self.render()
                except IndexError:
                    self.__add_slots(2)
                self.__pos = (self.__pos[0] + len(t), self.__pos[1])
                lines.append(line)
        except EOFError:
            return '\n'.join(lines)
        return '\n'.join(lines)

    def line(self, char: str = '-',color: str= COLORS.YELLOW, centered: bool = True):
        self.print(char*(os.get_terminal_size().columns-20), centered, color)

    def input(self, msg: str, hidden: bool = False, color: str = COLORS.LIGHT_WHITE) -> str:
        self.print(msg, color=color)
        self.render()
        result = input(">>> ")
        if not hidden:
            self.__buffer[self.__pos[0]-1] = self.__format(TextColor(msg + result, color), padding=10)
        else:
            self.__buffer[self.__pos[0]-1] = self.__format(TextColor(msg + ('*'*len(result)), color), padding=10)
        self.render()
        return result
