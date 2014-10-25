import sys

white_characters = {" ", "\t", "\n"}

def parse_argv():
    """
    parse sys.argv
    """
    return parse(sys.argv[1:])


def parse(args, space=False): # if space = True "aa AA " will be [["aa"], ["AA"], [""]]
    """
    parsing
    """
    if isinstance(args, str):
        args = __parse_string(args, space)
    arg_groups = []#will be returned
    arg_group = []#will be appended to arg_groups
    for arg in args:
        if arg[0] == "-":
            if len(arg_group):#if there is a not appended group
                arg_groups.append(arg_group[:])
                arg_group = []
            if arg[1] == "-":#double hyphen
                arg_groups.append([arg])
            else:#one hyphen
                arg_group.append(arg)
        else:
            if len(arg_group):#if there is a not appended group
                arg_group.append(arg)
            else:
                arg_groups.append([arg])
    if len(arg_group):
        arg_groups.append(arg_group)
    return arg_groups


def __parse_string(command, space=False):
    """
    parse string
    """
    args = [] #will be returned
    arg = "" #will be appended to args
    in_dq = False #is true when in double quotation
    for char in command:
        if in_dq:
            if char == "\"":
                in_dq = False
                if len(arg): #if there is a not appended arg
                    args.append(arg[:])
                    arg = ""
            else:
                arg += char
        elif char in white_characters:
            if len(arg): #if there is a not appended arg
                args.append(arg[:])
                arg = ""
        elif char == "\"":
            in_dq = True
        else:
            arg += char
    if len(arg): #if there is a not appended arg
        args.append(arg)
    if space and command[-1] == " ":
        args.append("")
    return args


if __name__ == "__main__":
    print(parse_argv());
