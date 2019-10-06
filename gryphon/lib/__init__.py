__version__ = '0.1'

def main():
    """Entry point for the application script"""
    print("Call your main application code here")

def monkeypatch_decimal_to_decimal():
    # monkeypatch the "decimal" library in.
    # this is a drop-in replacement for "decimal".
    # try:
    #     import decimal
    #     import sys
    #     sys.modules['decimal'] = decimal
    # except ImportError:
    #     pass
    pass

def prepare():
    monkeypatch_decimal_to_decimal()
