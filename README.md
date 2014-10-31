cuilib-py
=========
Library for console application in python
###Description
  cuilib-py is a library for Python.  
  cuilib-py contains functions for console application.  
  But cuilib-py also contains functions for not only console application.(example: parse_command)  
  You can make a application easily such as a command line interpreter.
###Requirement
  Python2 or Python3
###Installation
  Copy *.py to your directory.
###Usage
  ```
  from cuilib import *
  
  def main(con):
    con.add_string("Hello World!\n") #display "Hello World!"
    print con.getargv() #get a parsed sys.argv
    print con.get_string("Enter anything > ") #get a string
    
  if __name__ == "__main__":
    wrapper(main)
  ```
###License
  see [License](LICENSE)
###Author
  [ryo33](https://github.com/ryo33/ "ryo33's github page")
