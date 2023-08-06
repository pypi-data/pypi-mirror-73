##~---------------------------------------------------------------------------##
##                        _      _                 _   _                      ##
##                    ___| |_ __| |_ __ ___   __ _| |_| |_                    ##
##                   / __| __/ _` | '_ ` _ \ / _` | __| __|                   ##
##                   \__ \ || (_| | | | | | | (_| | |_| |_                    ##
##                   |___/\__\__,_|_| |_| |_|\__,_|\__|\__|                   ##
##                                                                            ##
##  File      : termcolor.py                                                  ##
##  Project   : pw_py_termcolor                                               ##
##  Date      : Mar 25, 2020                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : stdmatt <stdmatt@pixelwizards.io>                             ##
##  Copyright : stdmatt 2020                                                  ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##

##----------------------------------------------------------------------------##
## Imports                                                                    ##
##----------------------------------------------------------------------------##
import sys;
import re;
import os;


##----------------------------------------------------------------------------##
## Info                                                                       ##
##----------------------------------------------------------------------------##
__version__   = "1.0.0";
__author__    = "stdmatt - <stdmatt@pixelwizards.io>";
__date__      = "Mar 25, 2020";
__copyright__ = "Copyright 2020 - stdmatt";
__license__   = 'GPLv3';



##----------------------------------------------------------------------------##
## Color Mode / Convert Mode Classes                                          ##
##----------------------------------------------------------------------------##
"""
Global Color Modes - MODIFY ALL COLORING FUNCTIONS.

This class defines how the coloring functions will behave.

To change the behavior assign a new value to color_mode.

The possible Color modes are:
    COLOR_MODE_ONLY_IF_TERMINAL
        Color escapes codes are only put into the strings if
        the os.stdout is assigned to a tty.

        This enables code to don't care the type of the stdout
        i.e. if a pipe, file, or tty.

        If the os.stdout isn't assigned to a tty all coloring
        functions will return the unmodified string.

    COLOR_MODE_ALWAYS
        Don't care for where the os.stdout is assigned.
        Put the coloring escape sequences anyway.

    COLOR_MODE_NEVER
        Don't care for where the os.stdout is assigned.
        DO NOT put the coloring escape sequences anyway.

    COLOR_MODE_DEFAULT
        Same of COLOR_MODE_ONLY_IF_TERMINAL
"""
COLOR_MODE_ONLY_IF_TERMINAL = 0;
COLOR_MODE_ALWAYS           = 1;
COLOR_MODE_NEVER            = 2;
COLOR_MODE_DEFAULT          = COLOR_MODE_ONLY_IF_TERMINAL;


"""
Global Convert Modes - MODIFY ALL COLORING FUNCTIONS.

This class defines how the conversions will be applied when values
of types is passed to any coloring function.

To change the behavior assign a new value to convert_mode

The possible convert modes are:
    CONVERT_MODE_ALL_TYPES_TO_STR
        Any given type, but str, will be passed into str().

    CONVERT_MODE_ALL_TYPES_TO_TO_EMPTY_STR
        Any given type, but str, will be replaced by an empty str.

    CONVERT_MODE_NONE_TYPE_TO_EMPTY_STR
        Only the None type will be replaced by an empty str
        all other types will passed into str().

    CONVERT_MODE_RAISE_VALUE_ERROR_FOR_ALL_TYPES
        A ValueError exception will be raised if the type isn't str.

    CONVERT_MODE_RAISE_VALUE_ERROR_FOR_NONE_TYPE
        A ValueError exception will be raised only for None type.

    CONVERT_MODE_DEFAULT
        Equal to CONVERT_MODE_ALL_TYPES_TO_STR;
"""
CONVERT_MODE_ALL_TYPES_TO_STR                = 0;
CONVERT_MODE_ALL_TYPES_TO_TO_EMPTY_STR       = 1;
CONVERT_MODE_NONE_TYPE_TO_EMPTY_STR          = 2;
CONVERT_MODE_RAISE_VALUE_ERROR_FOR_ALL_TYPES = 3;
CONVERT_MODE_RAISE_VALUE_ERROR_FOR_NONE_TYPE = 4;
CONVERT_MODE_DEFAULT                         = CONVERT_MODE_ALL_TYPES_TO_STR;


##------------------------------------------------------------------------------
color_mode   = COLOR_MODE_DEFAULT;
convert_mode = CONVERT_MODE_DEFAULT;



##----------------------------------------------------------------------------##
## Color Mode                                                                 ##
##----------------------------------------------------------------------------##
##------------------------------------------------------------------------------
class Color(object):
    """
    Holds a set of coloring parameters into a nice object.

    This enables you group a set of different parameters and reuse them with ease.

    Example:
        grey_on_red_blinking       = Color(GREY, RED, [BLINK]);
        gray_on_red_bold_underline = Color(GREY, RED, [BOLD, UNDERLINE]);

        print(grey_on_red_blinking("Hello there..."));
        print(grey_on_red_bold_underline("I <3"));
    """

    ##--------------------------------------------------------------------------
    def __init__(self, fg = None, bg = None, list_of_attr = None):
        """
        No validation checks are made on given argument values
        Users should call it only with the 'constants defined in this module.
        """
        self._foreground = fg;
        self._background = bg;
        self._attrs      = list_of_attr;

    ##--------------------------------------------------------------------------
    def __call__(self, s = "", auto_reset=True):
        """
        Applies foreground color, next background color and then attributes.

        Notice:
            This function is affected by color_mode and convert_mode.

        Example:
            red_blinking = Color(RED, None, BLINK);
            print(red_blinking("Roses are red"));
        """

        r = "";
        ## Foreground.
        if(self._foreground is not None):
            r = _put_color(self._foreground);
        ## Background.
        if(self._background is not None):
            r += _put_color(self._background);
        ## Attributes.
        if(self._attrs is not None):
            for attr in self._attrs:
                r += _put_color(attr);

        r += _convert_value(s);

        if(auto_reset):
             r+= _put_color(RESET);

        return r;




##----------------------------------------------------------------------------##
## Color Constants                                                            ##
##----------------------------------------------------------------------------##
##
## Reset
RESET = 0;

##
## Foreground Colors
BLACK          = 30;
GREY           = 30;
RED            = 31;
GREEN          = 32;
YELLOW         = 33;
BLUE           = 34;
MAGENTA        = 35;
CYAN           = 36;
WHITE          = 37;
BRIGHT_BLACK   = 90;
BRIGHT_GREY    = 90;
BRIGHT_RED     = 91;
BRIGHT_GREEN   = 92;
BRIGHT_YELLOW  = 93;
BRIGHT_BLUE    = 94;
BRIGHT_MAGENTA = 95;
BRIGHT_CYAN    = 96;
BRIGHT_WHITE   = 97;

##
## Background Colors
ON_BLACK          = 40;
ON_RED            = 41;
ON_GREEN          = 42;
ON_YELLOW         = 43;
ON_BLUE           = 44;
ON_MAGENTA        = 45;
ON_CYAN           = 46;
ON_WHITE          = 47;
ON_BRIGHT_BLACK   = 100;
ON_BRIGHT_RED     = 101;
ON_BRIGHT_GREEN   = 102;
ON_BRIGHT_YELLOW  = 103;
ON_BRIGHT_BLUE    = 104;
ON_BRIGHT_MAGENTA = 105;
ON_BRIGHT_CYAN    = 106;
ON_BRIGHT_WHITE   = 107;

##
## Attributes
BLINK     = 5;
BOLD      = 1;
CONCEALED = 8;
DARK      = 2;
REVERSE   = 7;
UNDERLINE = 4;



##----------------------------------------------------------------------------##
## Colored Function                                                           ##
##----------------------------------------------------------------------------##
##------------------------------------------------------------------------------
def colored(s, fg = None, bg = None, attrs = None):
    """
    Builds the colored output in one function.

    It will put the foreground color, then the background and after all
    the attributes if there are any.

    :str        - The string that will be colored.(Mandatory)
    :foreground - A valid foreground color code.  (Optional)
    :background - A valid background color code.  (Optional)
    :attributes - A valid attributes codes.       (Optional)

    Notice:
        This function is affected by color_mode and convert_mode.

    This function will not check the validity of the color codes,
    so is user's responsibility to ensure that them are valid.

    The best bet is use the termcolor constants.
    """
    r = "";

    ## Foreground.
    if(fg is not None):
        r = _put_color(fg);

    ## Background.
    if(bg is not None):
        r += _put_color(bg);

    ## Attributes.
    if(attrs is not None):
        for attr in attrs:
            r += _put_color(attr);

    r += _convert_value(s) + _put_color(RESET);
    return r;


##----------------------------------------------------------------------------##
## RESET                                                                      ##
##----------------------------------------------------------------------------##
##------------------------------------------------------------------------------
def reset(s = ""):
    """
    Put the reset sequence in front of the 's' canceling all previous coloring.

    Notice:
        This function is affected by color_mode and convert_mode.
    """
    return _put_color(RESET) + _convert_value(s);


##----------------------------------------------------------------------------##
## Foreground Functions                                                       ##
##----------------------------------------------------------------------------##
def grey   (s = ""): return _put_color(GREY   ) + _convert_value(s);
def red    (s = ""): return _put_color(RED    ) + _convert_value(s);
def green  (s = ""): return _put_color(GREEN  ) + _convert_value(s);
def yellow (s = ""): return _put_color(YELLOW ) + _convert_value(s);
def blue   (s = ""): return _put_color(BLUE   ) + _convert_value(s);
def magenta(s = ""): return _put_color(MAGENTA) + _convert_value(s);
def cyan   (s = ""): return _put_color(CYAN   ) + _convert_value(s);
def white  (s = ""): return _put_color(WHITE  ) + _convert_value(s);

def bright_grey   (s = ""): return _put_color(BRIGHT_GREY   ) + _convert_value(s);
def bright_red    (s = ""): return _put_color(BRIGHT_RED    ) + _convert_value(s);
def bright_green  (s = ""): return _put_color(BRIGHT_GREEN  ) + _convert_value(s);
def bright_yellow (s = ""): return _put_color(BRIGHT_YELLOW ) + _convert_value(s);
def bright_blue   (s = ""): return _put_color(BRIGHT_BLUE   ) + _convert_value(s);
def bright_magenta(s = ""): return _put_color(BRIGHT_MAGENTA) + _convert_value(s);
def bright_cyan   (s = ""): return _put_color(BRIGHT_CYAN   ) + _convert_value(s);
def bright_white  (s = ""): return _put_color(BRIGHT_WHITE  ) + _convert_value(s);


##----------------------------------------------------------------------------##
## BACKGROUND FUNCTIONS                                                       ##
##----------------------------------------------------------------------------##
def on_grey   (s = ""): return _put_color(ON_GREY   ) + _convert_value(s);
def on_red    (s = ""): return _put_color(ON_RED    ) + _convert_value(s);
def on_green  (s = ""): return _put_color(ON_GREEN  ) + _convert_value(s);
def on_yellow (s = ""): return _put_color(ON_YELLOW ) + _convert_value(s);
def on_blue   (s = ""): return _put_color(ON_BLUE   ) + _convert_value(s);
def on_magenta(s = ""): return _put_color(ON_MAGENTA) + _convert_value(s);
def on_cyan   (s = ""): return _put_color(ON_CYAN   ) + _convert_value(s);
def on_white  (s = ""): return _put_color(ON_WHITE  ) + _convert_value(s);

def on_bright_grey   (s = ""): return _put_color(ON_BRIGHT_GREY   ) + _convert_value(s);
def on_bright_red    (s = ""): return _put_color(ON_BRIGHT_RED    ) + _convert_value(s);
def on_bright_green  (s = ""): return _put_color(ON_BRIGHT_GREEN  ) + _convert_value(s);
def on_bright_yellow (s = ""): return _put_color(ON_BRIGHT_YELLOW ) + _convert_value(s);
def on_bright_blue   (s = ""): return _put_color(ON_BRIGHT_BLUE   ) + _convert_value(s);
def on_bright_magenta(s = ""): return _put_color(ON_BRIGHT_MAGENTA) + _convert_value(s);
def on_bright_cyan   (s = ""): return _put_color(ON_BRIGHT_CYAN   ) + _convert_value(s);
def on_bright_white  (s = ""): return _put_color(ON_BRIGHT_WHITE  ) + _convert_value(s);


##----------------------------------------------------------------------------##
## ATTRIBUTES FUNCTIONS                                                       ##
##----------------------------------------------------------------------------##
def bold     (s = ""): return _put_color(BOLD     ) + _convert_value(s);
def dark     (s = ""): return _put_color(DARK     ) + _convert_value(s);
def underline(s = ""): return _put_color(UNDERLINE) + _convert_value(s);
def blink    (s = ""): return _put_color(BLINK    ) + _convert_value(s);
def reverse  (s = ""): return _put_color(REVERSE  ) + _convert_value(s);
def conceale (s = ""): return _put_color(CONCEALE ) + _convert_value(s);


##----------------------------------------------------------------------------##
## HELPER FUNCTIONS                                                           ##
##----------------------------------------------------------------------------##
##------------------------------------------------------------------------------
def code_to_escape_str(code):
    """
    Returns the raw escape sequence string.

    No validation is made to ensure that the resulting sequence will be valid.
    Users should call it only with the 'constants' defined in this module.

    Example:
        code_to_escape_str(BLUE) -> "\\033[34m"
    """
    return "%s%d%s" %(__START_ESCAPE_STR, code, __END_ESCAPE_STR);

##------------------------------------------------------------------------------
def remove_all_escape_codes(s):
    """
    Removes (if any) all escapes sequences in the 's' string.

    Example:
        remove_all_escape_codes(green("Hi there")) ## "Hi there"
        remove_all_escape_codes("Plain string")    ## "Plain string"
"""
    return re.sub("\033\[\d+m", "", s);

##------------------------------------------------------------------------------
def str_len(s):
    """
    Count the number of chars in string disregarding all coloring escape sequences.

    Same as len(remove_all_escape_codes(s))
    """
    return len(remove_all_escape_codes(s));



##----------------------------------------------------------------------------##
## Private Stuff                                                              ##
##----------------------------------------------------------------------------##
__START_ESCAPE_STR = "\033[";
__END_ESCAPE_STR   = "m";

##------------------------------------------------------------------------------
def _convert_value(value):
    if(type(value) == str):
        return value;

    if(convert_mode == CONVERT_MODE_ALL_TYPES_TO_STR):
        return str(value);

    if(convert_mode == CONVERT_MODE_ALL_TYPES_TO_TO_EMPTY_STR):
        return "";

    if(convert_mode == CONVERT_MODE_NONE_TYPE_TO_EMPTY_STR):
        if(value is None): return "";
        else:              return str(value);

    if(convert_mode == CONVERT_MODE_RAISE_VALUE_ERROR_FOR_ALL_TYPES):
        raise ValueError();

    if(convert_mode == CONVERT_MODE_RAISE_VALUE_ERROR_FOR_NONE_TYPE):
        if(value is None): raise ValueError("");
        else:              return str(value);

##------------------------------------------------------------------------------
def _put_color(color):
    if(color_mode == COLOR_MODE_ALWAYS):
        return code_to_escape_str(color);
    elif(color_mode == COLOR_MODE_NEVER):
        return "";
    elif(os.isatty(sys.stdout.fileno())):
        return code_to_escape_str(color);

    return ""
