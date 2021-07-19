"""
Copyright (C) 2021 Anubosiris
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

requirement_msg = """
    +–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+
    |  This program requires the libraries "secrets" and "clipboard".       |
    |  Both can be installed using pip. You may use the following command:  |
    |  pip install clipboard python-secrets                                 |
    +–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+
"""
try:
    import sys, secrets, clipboard, string
except ModuleNotFoundError:
    print(requirement_msg)
    exit(2)

def checkIfDecNumber(text):             # checks if string can be converted to decimal number
    if len(text) < 1: return False      # too short
    try:
        int(text, 10)                   # conversion, raises ValueError if not possible
        return True
    except ValueError:
        return False

def dprint(content):
    if _debuggingmode:print(content)
def dwrite(content):
    if _debuggingmode:print(content, end='')
def vprint(content):
    if _verboseprints or _debuggingmode:print(content)
def vwrite(content):
    if _verboseprints or _debuggingmode:print(content, end='')

def showhelp():
    helpmsg = """
    +––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+
    |                                                                                              |
    |   This program is a very basic random password generator written in Python 3.                |
    |   It relies on the secrets library for cryptographically safe randomness.                    |
    |   By default, the generated password is stored in the clipboard (check parameters below).    |
    |   Both the secrets and the clipboard library are required:                                   |
    |   pip install clipboard python-secrets                                                       |
    |                                                                                              |
    |   How to use:                                                                                |
    |   python simple_cspgen.py [password-length] [additional parameters]                          |
    |                                                                                              |
    |   Parameters:                                                                                |
    |   password-length: The length of the generated password, the default is 16 characters        |
    |      <<<note: all other parameters are prioritized and can be used in any order>>>           |    
    |   h - shows this help text instead of executing the actual program                           |
    |   a - use also special characters for the password creation (along letters and numbers)      |
    |   f - skips the pool-shuffling feature (decreases time and probably randomness)              |
    |   o - prints the password to the console (respectively stdout)                               |
    |   n - disables the clipboard feature, should be used with parameter o exclusively            |
    |   v - verbose mode (prints out information about current program state)                      |
    |   d - debug mode (prints out detailed information about program state, not recommended)      |
    |                                                                                              |
    |   All parameters are internally prioritized and therefore can be used in any order.          |
    |   Unknown characters are ignored. For instance, it does not matter if you use h or --help.   |
    |                                                                                              |
    |   Examples:                                                                                  |
    |   simple_cspgen.py -h      --> shows this help                                               |
    |   simple_cspgen.py drwho   --> shows this help                                               |
    |   simple_cspgen.py         --> 16 character password into clipboard                          |
    |   simple_cspgen.py a       --> 16 character password with special character into clipboard   |
    |   simple_cspgen.py 64 a    --> 64 character password with special characters into clipboard  |
    |   simple_cspgen.py f       --> 16 character password into clipboard, no pool-shuffling       |
    |   simple_cspgen.py no      --> 16 character password into stdout (not clipboard)             |
    |   simple_cspgen.py --debug --> 16 character password into clipboard, shows debug outputs     |
    |   simple_cspgen.py -n      --> generated password is not used, results in error              |
    |                                                                                              |
    |   Please feel free to report any bugs or ideas on GitHub:                                    |
    |   https://github.com/Develaupair/simple_cspgen                                               |
    |                                                                                              |
    +––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+
    
    """
    print(helpmsg)

_passwordlegth = 16     # can be overwritten by first argument
_printhelpexit = False  # h --> prints out help instead of executing the program, ignores other params
_allprintables = False  # a --> generated password using all printable characters instead of letters and numbers only
_skipshuffling = False  # f --> skips pool shuffle for each character
_printpassword = False  # o --> prints out the password
_noclipboardcp = False  # n --> prevents the password from being copied into the clipboard
_verboseprints = False  # v --> prints information about main phases of program
_debuggingmode = False  # d --> prints detailed information (not recommended for security reasons)

if len(sys.argv) > 1:
    if checkIfDecNumber(sys.argv[1]):                           # if argument is valid number
        _passwordlegth = int(sys.argv[1], 10)                   # password length is overwritten
        sys.argv.pop(1)
    try:
        bouillabaise = "".join(sys.argv[1:])                    # unordered soup of single character opt-in arguments
        if bouillabaise.find("h") != -1:
            showhelp()
            exit(0)
        if bouillabaise.find("a") != -1: _allprintables = True  # if param is found, set flag
        if bouillabaise.find("v") != -1: _verboseprints = True
        if bouillabaise.find("f") != -1: _skipshuffling = True
        if bouillabaise.find("d") != -1: _debuggingmode = True
        if bouillabaise.find("o") != -1: _printpassword = True
        if bouillabaise.find("n") != -1: _noclipboardcp = True
        dprint(f"\nFlags:\nallprintables={_allprintables}\nverboseprints={_verboseprints}\ndebuggingmode="
               f"{_debuggingmode}\nprintpassword={_printpassword}\nnoclipboardcp={_noclipboardcp}\n")
    except IndexError:
        dprint("no further arguments received.")
    vprint(f"password length set to {_passwordlegth}")

def main():
    if not _allprintables:
        vprint("using letters and numbers for pool (alphabet).")
        pool = [c for c in (string.ascii_lowercase + string.ascii_uppercase + string.digits)]
    else:
        vprint("using letters, numbers and special characters for pool (alphabet).")
        pool = [c for c in string.printable[:95]]           # limits the number to avoid usage of untypeable characters ('♂', '♀', ...)
    dprint(f"pool defined  > [ {''.join(pool)} ]\n")
    passwd = ""
    if not _skipshuffling:
        vprint("pool shuffle is enabled.")
        for c in range(_passwordlegth):
            pool = sorted([char for char in pool], key =    # sort the alphabet of the characters based on a
            lambda x: int(secrets.randbelow(1337**42)))     # lambda expression generating a large random number
            vwrite("pool shuffled ")
            dwrite("> [ " + str("".join(pool)).replace("\n", "") + " ]")
            vprint("")
            passwd += secrets.choice(pool)
    else:
        vprint("pool shuffle is disabled")
        passwd = "".join(secrets.choice(pool) for c in range(_passwordlegth)) # alternative password creation
    vprint("\npassword generated")
    if not _noclipboardcp:
        clipboard.copy(passwd)
        vprint("copied to clipboard")
    else:
        vprint("NOT copied to clipboard")
    if _printpassword:print(passwd)
    passwd = ""
    if not _printpassword and _noclipboardcp:
        print("No output set! Generated password dumped!")
        exit(3)
    dprint("Program finished\n\n")
    exit(0)

if __name__ == "__main__":
    main()
