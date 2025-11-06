import os

class Window():
    def __init__(self, title: str="Window") -> None:
        self.__clear = 'cls' if os.name == 'nt' else 'clear'
        os.system(self.__clear)
        self.__buffer = []
        self.__pos = (0,0)
        self.title = title
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

    def __format(self, txt: str, centered: bool=False):
        """
        struc = list(" "*(self.window_size[1]))
        txt = txt.strip()
        struc[0] = struc[-1] = "|"
        if centered:
            for i in range(0, len(txt)):
                struc[len(struc)//2 - len(txt)//2 + i] = txt[i]
        else:
            for i in range(0, len(txt)):
                struc[2 + i] = txt[i]
        struc = ''.join(struc)
        return struc
        """
        partial = f"|{' '*((self.window_size[1] - len(txt))//2 - (self.__remove_emoji(txt)))}{txt}" if centered else f"| {txt}"
        return f"{partial}{' '*(self.window_size[1] - len(partial)- (self.__remove_emoji(txt)))}|"

    def __set_buffer(self):
        self.__buffer.append(f"+{'-' * (self.window_size[1] - 2)}+")
        for _ in range(self.window_size[0] - 2):
            self.__buffer.append(self.__format(" "))
        self.__buffer.append(f"+{'-' * (self.window_size[1] - 2)}+")
        self.__pos = (1, 1)

    def __add_slots(self, num: int):
        currPos = self.__pos
        self.__buffer[-1] = self.__format(" ")
        for _ in range(0, num):
            self.__buffer.append(self.__format(" "))
        self.__buffer.append(f"+{'-' * (self.window_size[1] - 2)}+")
        self.__pos = (currPos[0]-1, currPos[1])
        self.render()

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

    def CenterText(self, msg: str):
        self.__buffer[self.window_size[0]//2] = self.__format(msg, True)
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


    def print(self, msg: str=" ", centered: bool = False) -> None:
        try:
            for line in self.truncate(msg).split('\n'):
                self.__buffer[self.__pos[0]] = self.__format(line, centered)
                self.__pos = (self.__pos[0]+1, self.__pos[1])
        except IndexError:
            self.__add_slots(self.window_size[0])

    def editor(self, msg: str, terminate: str="END") -> str:
        self.print(msg)
        self.render()
        lines = []
        try:
            while True:
                line = input("> ")
                t = self.truncate(line).split("\n")
                try:
                    for i in range(0, len(t)):
                        self.__buffer[self.__pos[0]-1 + i] = self.__format(msg + t[i])
                        self.render()
                except IndexError:
                    self.__add_slots(20)
                self.__pos = (self.__pos[0] + len(t), self.__pos[1])
                lines.append(line)
                if line == terminate:
                    break
        except EOFError:
            return '\n'.join(lines)
        return '\n'.join(lines)

    def input(self, msg: str, hidden: bool = False) -> str:
        self.print(msg)
        self.render()
        result = input(">>> ")
        if not hidden:
            self.__buffer[self.__pos[0]-1] = self.__format(msg + result)
        else:
            self.__buffer[self.__pos[0]-1] = self.__format(msg + ('*'*len(result)))
        self.render()
        return result
