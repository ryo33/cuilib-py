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

    def get_command(self, prompt, func=lambda:):
        """
        return a command
        call func when user press tab
        """
        self.stdscr.addstr(prompt)
        default_cursor = self.stdscr.getyx() #coordinate of first command char
        cursor = 0 # relative x-coordinate
        command = ""
        parsed = None
        possibilities = None #is None when not have possibilities
        selected = 0 #possibilities[selected]
        while True:
            c = self.stdscr.getch()
            if curses.ascii.isprint(c):
                command += chr(c)
                self.stdscr.addch(chr(c))
                if not possibilities:
                    possibilities = None
            elif c == curses.KEY_LEFT:
                #TODO
                pass
            elif c == curses.KEY_RIGHT:
                #TODO
                pass
            elif c == curses.KEY_ENTER:
                self.stdscr.addch("\n")
                return pc.parse(command)
            elif c == ord("\t"):
                if possibilities is None:
                    selected = 0
                    parsed = pc.parce(command[0:cursor], True)
                    func(parsed)
                    if len(possibilities) > 0:
                        self.stdscr.setyx(default_cursor)
                        self.stdscr.clrtoeol()
                        self.print(possiblilities[selected])
                elif len(possibilities) != 0:
                    selected = (selected + 1) % len(possibilities)

    def print(self, str, start=None):
        if start is not None:
            self.stdscr.move(start[0], start[1])


    def insert(self, str):
        self.stdscr.insstr(str)
