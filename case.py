"""
Source: https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
Answered Date: Jul 7, 2011 at 6:09
Author: adamh

Description:
Python implementation for a typical switch/case statement
"""
class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))