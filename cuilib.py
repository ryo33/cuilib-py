import curses
import curses.ascii
import parse_command as pc

class Cuilib:
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

    def get_argv(self):
        return pc.parse_argv()

    def parse_command(self, command):
        return pc.parse(command)

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
                self.__type(chr(c))
                self.insert(chr(c))
                if possibilities is not None:
                    possibilities = None
            elif c == curses.KEY_LEFT:
                if self.__left():
                    possibilities = None
            elif c == curses.KEY_RIGHT:
                if self.__right():
                    possibilities = None
            elif c == curses.KEY_ENTER:
                self.newline
                return pc.parse(command)
            elif c == curses.ascii.BS:
                self.__backspace()
            elif c == ord("\t") and func is not None:
                if possibilities is None:
                    selected = 0
                    parsed = pc.parce(self.typing[0:self.cursor], True)
                    func(parsed)
                    if len(possibilities) > 0:
                        self.__print(possibilities[selected], self.default_cursor)
                elif len(possibilities) != 0:
                    selected = (selected + 1) % len(possibilities)
                    after = ""
                    if self.cursor < len(self.typing) - 1:
                        after = self.typing[self.cursor + 1:]
                    self.__print(possibilities[selected] + after, self.default_cursor)

    def __get_char(self, func=None):
        """
        get_character
        func: example isprint, isalpha
        """
        while True:
            char = self.stdscr.getch()
            if func is None or func(char):
                break
        return char
    
    def get_char(self, func=None):
        """
        get_character
        func: example isprint, isalpha
        """
        while True:
            char = self.stdscr.getch()
            if func is None or func(char):
                break
        return chr(char)

    def input(self, prompt, func=None):
        self.__print(prompt)
        return self.get_str(func)

    def get_str(self, func=None):
        """
        getstring
        """
        self.init_typing()
        while True:
            char = self.__get_char()
            if char == 10 or char == curses.KEY_ENTER:
                self.newline()
                return self.typing
            elif func is None or func(char):
                self.__type(char)
                self.__print(chr(char))

    def get_password(self, func=curses.ascii.isgraph):
        """
        getpassword
        """
        self.init_typing()
        while True:
            char = self.__get_char()
            if char == curses.KEY_ENTER or char == 10:
                self.newline()
                return self.typing
            elif func is None or func(char):
                self.__type(char)

    def newline(self):
        self.__print("\n")

    def __backspace(self):
        if __is_not_first_character():
            self.__print("\b")

    def __type(self, char):
        self.typing += chr(char)
        if self.cursor == self.cursor_max:
            self.cursor_max += 1
        self.cursor += 1

    def __is_not_first_character(self):
        if self.cursor > 0:
            return True
        return False

    def __left(self):
        if __is_not_first_character():
            self.cursor -= 1
            self.move((self.default_cursor[0], self.default_cursor[1] + self.cursor))
            return True
        return False
    
    def __right(self):
        if self.cursor_max != self.cursor:
            self.cursor += 1
            self.move((self.default_cursor[0], self.default_cursor[1] + self.cursor))
            return True
        return False

    def __print(self, text, start=None):
        if start is not None:
            move(start[0])
            self.stdscr.clrtoeol()
        self.stdscr.addstr(str(text))

    def print(self, text, start=None):
        if start is not None:
            move(start[0])
            self.stdscr.clrtoeol()
        self.stdscr.addstr(str(text) + "\n")

    def insert(self, str):
        self.stdscr.insstr(str)

    def move(self, cursor):
        self.stdscr.move(cursor[0], cursor[1])


def __wrapper(stdscr, main):
    con = Cuilib(stdscr)
    main(con)

def wrapper(main):
    curses.wrapper(__wrapper, main)
