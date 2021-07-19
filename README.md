# simple_cspgen - a simple python based password generator
## Purpose
This program is a very simple password generator written in Python 3. 
It uses the [secrets](https://docs.python.org/3/library/secrets.html) library to generate passwords based on cryptographically secure randomness. 
The options are very limited. However, the generated password is stored in the clipboard and can also be printed to the stdout. 
Also you are free to choose whether to use special characters during password creation.

## Requirements
- [Python 3](https://www.python.org/downloads/)
- `pip install clipboard python-secrets`

## How to use
`python simple_cspgen.py `[`characters`]` `[`other_parameters_in_any_order`]`

On Linux (Debian, Ubuntu, Kali, ...), you can use `pwgen.sh` instead (the parameters remain the same).  
On Windows, you can use `pwgen.bat` instead (the parameters remain the same).

### Parameters:
`characters` - simply the number (positive integer) of characters the password should have (default=16)  

**The parameters below can be used in any order or combination. You do not have to use `-`.**  
`h` - shows help text instead of executing the actual program (overwrites other parameters)\
`a` - use also special characters for the password creation (along letters and numbers)\
`f` - skips the pool-shuffling feature (decreases time and probably randomness)\
`o` - prints the password to the console (respectively stdout)\
`n` - disables clipboard pasting, should be used with parameter `o` exclusively\
`v` - verbose mode (prints out some information about current program state)\
`d` - debug mode (prints out detailed information about program state, not recommended)

### Examples:
- `python simple_cspgen.py`         - generates 16 character password, copies it to the clipboard  

- `python simple_cspgen.py -h`      - shows help text (note that h will overthrow all other parameters)  
- `python simple_cspgen.py drwho`   - shows help text (note that h will overthrow all other parameters)  

- `python simple_cspgen.py a`       - generates 16 character password with special character and copies it to the clipboard  
- `python simple_cspgen.py 64 a`    - generates 64 character password with special characters and copies it to the clipboard  
- `python simple_cspgen.py f`       - generates 16 character password without pool-shuffling, copies it to the clipboard (is faster, probably a little less random)  
- `python simple_cspgen.py no`      - generates 16 character password and prints it to the stdout (the clipboard is not overwritten)  
- `python simple_cspgen.py --debug` - generates 16 character password, copies it to the clipboard and shows detailed information about program state (debug outputs)  

- `python simple_cspgen.py -n`      - generated password remains unused --> results in error  

### Exit Codes

`0`: no error  
`1`: unexpected error  
`2`: module import failed, check if secrets and clipboard are installed correctly (`pip install clipboard python-secrets`)  
`3`: no output defined, generated password will be dumped (fix by not using the `n` parameter without the `o` parameter)

### Additional points
- The program is very rudimentary.
- The parameter system is very rudimentary.
- If you feel offended by any of these points, please feel free to contribute ;)
- If you are for some reason using this program to create very large passwords (thousands of digits or more), you may want to use the `f` parameter. Otherwise you might be overwhelmed by the excitement of facing exponential(ish) runtime...
