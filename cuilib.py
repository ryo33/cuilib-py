import curses
import curses.ascii
import parse_command as pc

class cuilib:
    stdscr = None
    ENTER, LEFT, RIGHT, UP, DOWN, BS = 1, 2, 3, 4, 5, 6
    default_cursor = None
    cursor = 0
    cursor_max = 0
    typing = ""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.noecho()

    def getargv(self):
        return pc.parse_argv()

    def init_typing(self):
        self.default_cursor = self.stdscr.getyx() #coordinate of first command char
        self.cursor = 0 # relative x-coordinate
        self.cursor_max = 0
        self.typing = ""

    def get_command(self, prompt, func=None):
        """
        return a command
        call func when user press tab
        """
        self.init_typing()
        self.stdscr.addstr(prompt)
        parsed = None
        possibilities = None #is None when not have possibilities
        selected = 0 #possibilities[selected]
        while True:
            c = self.stdscr.getch()
            if curses.ascii.isprint(c):
                self.type(chr(c))
                self.insert(chr(c))
                if possibilities is not None:
                    possibilities = None
            elif c == curses.KEY_LEFT:
                if self.left():
                    possibilities = None
            elif c == curses.KEY_RIGHT:
                if self.right():
                    possibilities = None
            elif c == curses.KEY_ENTER:
                self.newline
                return pc.parse(command)
            elif c == curses.ascii.BS:
                self.backspace()
            elif c == ord("\t") and func is not None:
                if possibilities is None:
                    selected = 0
                    parsed = pc.parce(self.typing[0:self.cursor], True)
                    func(parsed)
                    if len(possibilities) > 0:
                        self.print(possibilities[selected], self.default_cursor)
                elif len(possibilities) != 0:
                    selected = (selected + 1) % len(possibilities)
                    after = ""
                    if self.cursor < len(self.typing) - 1:
                        after = self.typing[self.cursor + 1:]
                    self.print(possibilities[selected] + after, self.default_cursor)

    def __getchar(self, func=None):
        """
        getcharacter
        func: example isprint, isalpha
        """
        while True:
            char = self.stdscr.getch()
            if func is None or func(char):
                break
        return char
    
    def getchar(self, func=None):
        """
        getcharacter
        func: example isprint, isalpha
        """
        while True:
            char = self.stdscr.getch()
            if func is None or func(char):
                break
        return chr(char)

    def getstr(self, func=None):
        """
        getstring
        """
        self.init_typing()
        while True:
            char = self.getchar()
            if func is None or func(char):
                type(char)
                self.print(char)
            elif char == curses.KEY_ENTER:
                self.newline()
                return string

    def getpassword(self, func=curses.ascii.isgraph):
        """
        getpassword
        """
        string = ""
        while True:
            char = self.getchar()
            if func(char):
                string += char
            elif char == curses.ascii.BS:

            elif char == curses.KEY_ENTER:
                self.newline()
                return string

    def newline(self):
        self.print("\n")

    def backspace(self):
        if is_not_first_character():
            self.print("\b")

    def type(self, char):
        self.typing += chr(char)
        if self.cursor == self.cursor_max:
            self.cursor_max += 1
        self.cursor += 1

    def is_not_first_character(self):
        if self.cursor > 0:
            return True
        return False

    def left(self):
        if is_not_first_character():
            self.cursor -= 1
            self.move((self.default_cursor[0], self.default_cursor[1] + self.cursor))
            return True
        return False
    def right(self):
        if self.cursor_max != self.cursor:
            self.cursor += 1
            self.move((self.default_cursor[0], self.default_cursor[1] + self.cursor))
            return True
        return False

    def print(self, str, start=None):
        if start is not None:
            move(start[0])
            self.stdscr.clrtoeol()
        self.addstr(str)

    def insert(self, str):
        self.stdscr.insstr(str)

    def move(self, cursor):
        self.stdscr.move(cursor[0], cursor[1])
