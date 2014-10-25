import curses
import curses.ascii
import parse_command as pc

class cuilib:
    stdscr = None
    ENTER, LEFT, RIGHT, UP, DOWN, BS = 1, 2, 3, 4, 5, 6
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.noecho()

    def getargv(self):
        return pc.parse_argv()

    def get_command(self, prompt, func=None):
        """
        return a command
        call func when user press tab
        """
        self.stdscr.addstr(prompt)
        default_cursor = self.stdscr.getyx() #coordinate of first command char
        cursor = 0 # relative x-coordinate
        cursor_max = 0
        command = ""
        parsed = None
        possibilities = None #is None when not have possibilities
        selected = 0 #possibilities[selected]
        while True:
            c = self.stdscr.getch()
            if curses.ascii.isprint(c):
                command += chr(c)
                self.insert(chr(c))
                if possibilities is not None:
                    possibilities = None
                if cursor == cursor_max:
                    cursor_max += 1
                cursor += 1
            elif c == curses.KEY_LEFT:
                if cursor > 0:
                    cursor -= 1
                    self.move((default_cursor[0], default_cursor[1] + cursor))
                    possibilities = None
            elif c == curses.KEY_RIGHT:
                if cursor_max != cursor:
                    cursor += 1
                    self.move((default_cursor[0], default_cursor[1] + cursor))
                    possibilities = None
            elif c == curses.KEY_ENTER:
                self.stdscr.addch("\n")
                return pc.parse(command)
            elif c == ord("\t") and func is not None:
                if possibilities is None:
                    selected = 0
                    parsed = pc.parce(command[0:cursor], True)
                    func(parsed)
                    if len(possibilities) > 0:
                        self.print(possibilities[selected], default_cursor)
                elif len(possibilities) != 0:
                    selected = (selected + 1) % len(possibilities)
                    after = ""
                    if cursor < len(command) - 1:
                        after = command[cursor + 1:]
                    self.print(possibilities[selected] + after, default_cursor)

    def print(self, str, start=None):
        if start is not None:
            move(start[0])
            self.stdscr.clrtoeol()
        self.addstr(str)

    def insert(self, str):
        self.stdscr.insstr(str)

    def move(self, cursor):
        self.stdscr.move(cursor[0], cursor[1])
