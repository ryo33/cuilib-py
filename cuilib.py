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
    command_history = []

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.idcok(False)

    def get_str(self, func=curses.ascii.isprint, option=None, history=None, possibilities_func=None):
        """
        getstring
        """
        if possibilities_func is not None:
            parsed = None
            possibilities = None #is None when not have possibilities
            selected = 0 #possibilities[selected]
        if history is not None:
            selected_history = 0
            backup = None
        possibilities = None #default is None
        self.init_typing()
        while True:
            char = self.__get_char()
            if char == 10 or char == curses.KEY_ENTER:
                self.__newline()
                return self.typing
            elif self.is_left(char):
                self.__left()
            elif self.is_right(char):
                self.__right()
            elif self.is_bs(char):
                self.__backspace()
            elif history is not None and self.is_up(char):
                if len(history) > selected_history:
                    if selected_history == 0:
                        backup = self.typing
                    selected_history += 1
                    self.__replace_typing(history[-selected_history])
            elif history is not None and self.is_down(char):
                if selected_history > 1:
                    selected_history -= 1
                    self.__replace_typing(history[-selected_history])
                elif selected_history == 1:
                    selected_history = 0
                    self.__replace_typing(backup)
            elif possibilities_func is not None and self.is_tab(char):
                if possibilities is None:
                    selected = 0
                    parsed = pc.parce(self.typing[0:self.cursor], True)
                    possibilities = possibilities_func(parsed)
                    if len(possibilities) > 0:
                        self.__replace_typing(possibilities[selected])
                elif len(possibilities) != 0:
                    selected = (selected + 1) % len(possibilities)
                    after = ""
                    if self.cursor < len(self.typing) - 1:
                        after = self.typing[self.cursor + 1:]
                    self.__replace_typing(possibilities[selected] + after)
            elif func is None or func(char):
                insert = self.__type(char)
                if option != "password":
                    if insert:
                        self.insert(chr(char))
                    else:
                        self.print(chr(char), end="")
                else:
                    self.right()

    def get_command(self, func=None, history=None, possibilities_func=None):
        if history is None:
            history = self.command_history
        self.command_history.append(self.get_str(func=func, history=history, possibilities_func=possibilities_func))
        return pc.parse(self.command_history[-1])

    def get_argv(self):
        return pc.parse_argv()

    def parse_command(self, command):
        return pc.parse(command)

    def init_typing(self):
        self.default_cursor = self.stdscr.getyx() #coordinate of first command char
        self.cursor = 0 # relative x-coordinate
        self.cursor_max = 0
        self.typing = ""

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

    def wait(self, prompt=""):
        self.print(prompt, end="")
        self.stdscr.getch()

    def get_char(self, prompt="", func=curses.ascii.isprint):
        """
        get_character
        func: example isprint, isalpha
        """
        self.print(prompt, end="")
        return chr(self.__get_char(func))

    def input(self, prompt="", func=curses.ascii.isprint, history=None, possibilities_func=None):
        self.print(prompt, end="")
        return self.get_str(func=func, history=history, possibilities_func=possibilities_func)

    def get_password(self, prompt, func=curses.ascii.isgraph):
        """
        getpassword
        """
        self.print(prompt, end="")
        return self.get_str(option="password", func=func)

    def __newline(self):
        self.move((self.default_cursor[0], self.default_cursor[1] + self.cursor_max))
        self.print("")

    def __backspace(self):
        if self.__is_not_first_character():
            self.__left()
            self.stdscr.delch()
            self.cursor_max -= 1
            self.typing = self.typing[:self.cursor] + self.typing[self.cursor + 1:]

    def __type(self, char):
        result = False
        if self.cursor == self.cursor_max:
            self.typing += chr(char)
        else:
            self.typing = self.typing[:self.cursor] + chr(char) + self.typing[self.cursor:]
            result = True
        self.cursor += 1
        self.cursor_max += 1
        return result

    def __replace_typing(self, text):
        self.typing = text
        self.print(self.typing, end="", start=self.default_cursor)
        self.cursor =  self.cursor_max = len(self.typing)

    def __is_not_first_character(self):
        if self.cursor > 0:
            return True
        return False

    def __left(self):
        if self.__is_not_first_character():
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

    def print(self, text, end="\n", start=None):
        if start is not None:
            self.move(start)
            self.stdscr.clrtoeol()
        self.stdscr.addstr(str(text) + end)

    def insert(self, str):
        self.stdscr.insstr(str)
        self.right(len(str))

    def move(self, cursor):
        self.stdscr.move(cursor[0], cursor[1])

    def right(self, move=1):
        """
        move cursor to right
        """
        cursor = self.get_cursor()
        self.move((cursor[0], cursor[1] + move))

    def left(self, move=1):
        """
        move cursor to right
        """
        cursor = self.get_cursor()
        if cursor[1] > move - 1:
            self.move((cursor[0], cursor[1] - move))

    def get_cursor(self):
        return self.stdscr.getyx()

    def is_left(self, char):
        if char == curses.KEY_LEFT:
            return True
        return False

    def is_right(self, char):
        if char == curses.KEY_RIGHT:
            return True
        return False

    def is_bs(self, char):
        if char == curses.KEY_BACKSPACE:
            return True
        return False

    def is_up(self, char):
        if char == curses.KEY_UP:
            return True
        return False
    
    def is_down(self, char):
        if char == curses.KEY_DOWN:
            return True
        return False

    def is_tab(self, char):
        if char == ord("\t"):
            return True
        return False

    def is_ctrl_tab(self, char):
        if char == 353:
            return True
        return False

def __wrapper(stdscr, main):
    con = Cuilib(stdscr)
    main(con)

def wrapper(main):
    curses.wrapper(__wrapper, main)
