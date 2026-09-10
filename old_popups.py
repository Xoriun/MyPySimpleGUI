

from quick_tkinter import (
    DEFAULTS,
    MAX_SCROLLED_TEXT_BOX_HEIGHT,
    MESSAGE_BOX_LINE_WIDTH,
    Button,
    Column,
    DummyButton,
    Image,
    Multiline,
    Push,
    Sizegrip,
    Text,
    Window,
    _get_num_lines_needed,
    textwrap,
)

# MM"""""""`YM
# MM  mmmmm  M
# M'        .M .d8888b. 88d888b. dP    dP 88d888b. .d8888b.
# MM  MMMMMMMM 88'  `88 88'  `88 88    88 88'  `88 Y8ooooo.
# MM  MMMMMMMM 88.  .88 88.  .88 88.  .88 88.  .88       88
# MM  MMMMMMMM `88888P' 88Y888P' `88888P' 88Y888P' `88888P'
# MMMMMMMMMMMM          88                88
#                       dP                dP
# ------------------------------------------------------------------------------------------------------------------ #
# =====================================   Upper PySimpleGUI ======================================================== #
# ------------------------------------------------------------------------------------------------------------------ #
# ----------------------------------- The mighty Popup! ------------------------------------------------------------ #

# -------------------------  Popup Buttons Types  ------------------------- #
POPUP_BUTTONS_YES_NO = 1
POPUP_BUTTONS_CANCELLED = 2
POPUP_BUTTONS_ERROR = 3
POPUP_BUTTONS_OK_CANCEL = 4
POPUP_BUTTONS_OK = 0
POPUP_BUTTONS_NO_BUTTONS = 5

def popup(*args, title=None, button_color=None, background_color=None, text_color=None, button_type=POPUP_BUTTONS_OK, auto_close=False,
          auto_close_duration=None, custom_text=(None, None), non_blocking=False, icon=None, line_width=None, font=None, no_titlebar=False, grab_anywhere=False,
          keep_on_top=None, location=(None, None), relative_location=(None, None), any_key_closes=False, image=None, modal=True, button_justification=None, drop_whitespace=True):
    """
    Popup - Display a popup Window with as many parms as you wish to include.  This is the GUI equivalent of the
    "print" statement.  It's also great for "pausing" your program's flow until the user can read some error messages.

    If this popup doesn't have the features you want, then you can easily make your own. Popups can be accomplished in 1 line of code:
    choice, _ = sg.Window('Continue?', [[sg.T('Do you want to continue?')], [sg.Yes(s=10), sg.No(s=10)]], disable_close=True).read(close=True)


    :param *args:                 Variable number of your arguments.  Load up the call with stuff to see!
    :type *args:                  (Any)
    :param title:                 Optional title for the window. If none provided, the first arg will be used instead.
    :type title:                  (str)
    :param button_color:          Color of the buttons shown (text color, button color)
    :type button_color:           (str, str) | str
    :param background_color:      Window's background color
    :type background_color:       (str)
    :param text_color:            text color
    :type text_color:             (str)
    :param button_type:           NOT USER SET!  Determines which pre-defined buttons will be shown (Default value = POPUP_BUTTONS_OK). There are many Popup functions and they call Popup, changing this parameter to get the desired effect.
    :type button_type:            (int)
    :param auto_close:            If True the window will automatically close
    :type auto_close:             (bool)
    :param auto_close_duration:   time in seconds to keep window open before closing it automatically
    :type auto_close_duration:    (int)
    :param custom_text:           A string or pair of strings that contain the text to display on the buttons
    :type custom_text:            (str, str) | str
    :param non_blocking:          If True then will immediately return from the function without waiting for the user's input.
    :type non_blocking:           (bool)
    :param icon:                  icon to display on the window. Same format as a Window call
    :type icon:                   str | bytes
    :param line_width:            Width of lines in characters.  Defaults to MESSAGE_BOX_LINE_WIDTH
    :type line_width:             (int)
    :param font:                  specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
    :type font:                   str | Tuple[font_name, size, modifiers]
    :param no_titlebar:           If True will not show the frame around the window and the titlebar across the top
    :type no_titlebar:            (bool)
    :param grab_anywhere:         If True can grab anywhere to move the window. If no_titlebar is True, grab_anywhere should likely be enabled too
    :type grab_anywhere:          (bool)
    :param location:              Location on screen to display the top left corner of window. Defaults to window centered on screen
    :type location:               (int, int)
    :param relative_location:     (x,y) location relative to the default location of the window, in pixels. Normally the window centers.  This location is relative to the location the window would be created. Note they can be negative.
    :type relative_location:      (int, int)
    :param keep_on_top:           If True the window will remain above all current windows
    :type keep_on_top:            (bool)
    :param any_key_closes:        If True then will turn on return_keyboard_events for the window which will cause window to close as soon as any key is pressed.  Normally the return key only will close the window.  Default is false.
    :type any_key_closes:         (bool)
    :param image:                 Image to include at the top of the popup window
    :type image:                  (str) or (bytes)
    :param modal:                 If True then makes the popup will behave like a Modal window... all other windows are non-operational until this one is closed. Default = True
    :type modal:                  bool
    :param right_justify_buttons: If True then the buttons will be "pushed" to the right side of the Window
    :type right_justify_buttons:  bool
    :param button_justification:  Speficies if buttons should be left, right or centered. Default is left justified
    :type button_justification:   str
    :param drop_whitespace:       Controls is whitespace should be removed when wrapping text.  Parameter is passed to textwrap.fill. Default is to drop whitespace (so popup remains backward compatible)
    :type drop_whitespace:        bool
    :return:                      Returns text of the button that was pressed.  None will be returned if user closed window with X
    :rtype:                       str | None
    """
    args_to_print = args or [""]
    local_line_width = MESSAGE_BOX_LINE_WIDTH if line_width is None else line_width
    _title = title if title is not None else args_to_print[0]

    layout = [[]]
    max_line_total, total_lines = 0, 0
    if image is not None:
        if isinstance(image, str):
            layout += [[Image(filename=image)]]
        else:
            layout += [[Image(data=image)]]

    for message in map(str, args_to_print):
        if message.count('\n'):  # if there are line breaks, then wrap each segment separately
            # message_wrapped = message         # used to just do this, but now breaking into smaller pieces
            message_wrapped = ''
            msg_list = message.split('\n')  # break into segments that will each be wrapped
            message_wrapped = '\n'.join([textwrap.fill(msg, local_line_width) for msg in msg_list])
        else:
            message_wrapped = textwrap.fill(message, local_line_width, drop_whitespace=drop_whitespace)
        message_wrapped_lines = message_wrapped.count('\n') + 1
        longest_line_len = max([len(line) for line in message.split('\n')])
        width_used = min(longest_line_len, local_line_width)
        max_line_total = max(max_line_total, width_used)
        # height = _GetNumLinesNeeded(message, width_used)
        height = message_wrapped_lines
        layout += [[
            Text(message_wrapped, auto_size_text=True, text_color=text_color, background_color=background_color)]]
        total_lines += height
    
    layout = [[Column(layout=layout, vertical_scroll_only=True)]]

    popup_button = DummyButton if non_blocking else Button # important to use or else button will close other windows too!
    # show either an OK or Yes/No depending on paramater
    if custom_text != (None, None):
        if type(custom_text) is not tuple:
            layout += [[popup_button(custom_text, size=(len(custom_text), 1), button_color=button_color, focus=True,
                                    bind_return_key=True)]]
        elif custom_text[1] is None:
            layout += [[
                popup_button(custom_text[0], size=(len(custom_text[0]), 1), button_color=button_color, focus=True,
                            bind_return_key=True)]]
        else:
            layout += [[popup_button(custom_text[0], button_color=button_color, focus=True, bind_return_key=True,
                                    size=(len(custom_text[0]), 1)),
                        popup_button(custom_text[1], button_color=button_color, size=(len(custom_text[1]), 1))]]
    elif button_type == POPUP_BUTTONS_YES_NO:
        layout += [[popup_button('Yes', button_color=button_color, focus=True, bind_return_key=True,
                                size=(5, 1)), popup_button('No', button_color=button_color, size=(5, 1))]]
    elif button_type == POPUP_BUTTONS_CANCELLED:
        layout += [[
            popup_button('Cancelled', button_color=button_color, focus=True, bind_return_key=True )]]
    elif button_type == POPUP_BUTTONS_ERROR:
        layout += [[popup_button('Error', size=(6, 1), button_color=button_color, focus=True, bind_return_key=True)]]
    elif button_type == POPUP_BUTTONS_OK_CANCEL:
        layout += [[popup_button('OK', size=(6, 1), button_color=button_color, focus=True, bind_return_key=True),
                    popup_button('Cancel', size=(6, 1), button_color=button_color)]]
    elif button_type == POPUP_BUTTONS_NO_BUTTONS:
        pass
    else:
        layout += [[popup_button('OK', size=(5, 1), button_color=button_color, focus=True, bind_return_key=True)]]
    if button_justification is not None:
        justification = button_justification.lower()[0]
        if justification == 'r':
            layout[-1] = [Push()] + layout[-1]
        elif justification == 'c':
            layout[-1] = [Push()] + layout[-1] + [Push()]


    window = Window(_title, layout, auto_size_text=True, background_color=background_color, button_color=button_color,
                    auto_close=auto_close, auto_close_duration=auto_close_duration, icon=icon, font=font,
                    no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location, relative_location=relative_location, return_keyboard_events=any_key_closes,
                    modal=modal)

    if non_blocking:
        button, _ = window.read(timeout=0)
    else:
        button, _ = window.read()
        window.close()
        del window

    return button


# ========================  Scrolled Text Box   =====#
# ===================================================#
def popup_scrolled(*args, title=None, button_color=None, background_color=None, text_color=None, yes_no=False, no_buttons=False, button_justification='l', auto_close=False, auto_close_duration=None, size=(None, None), location=(None, None), relative_location=(None, None), non_blocking=False, no_titlebar=False, grab_anywhere=False, keep_on_top=None, font=None, image=None, icon=None, modal=True, no_sizegrip=False):
    """
    Show a scrolled Popup window containing the user's text that was supplied.  Use with as many items to print as you
    want, just like a print statement.

    :param *args:                 Variable number of items to display
    :type *args:                  (Any)
    :param title:                 Title to display in the window.
    :type title:                  (str)
    :param button_color:          button color (foreground, background)
    :type button_color:           (str, str) | str
    :param yes_no:                If True, displays Yes and No buttons instead of Ok
    :type yes_no:                 (bool)
    :param no_buttons:            If True, no buttons will be shown. User will have to close using the "X"
    :type no_buttons:             (bool)
    :param button_justification:  How buttons should be arranged.  l, c, r for Left, Center or Right justified
    :type button_justification:   (str)
    :param auto_close:            if True window will close itself
    :type auto_close:             (bool)
    :param auto_close_duration:   Older versions only accept int. Time in seconds until window will close
    :type auto_close_duration:    int | float
    :param size:                  (w,h) w=characters-wide, h=rows-high
    :type size:                   (int, int)
    :param location:              Location on the screen to place the upper left corner of the window
    :type location:               (int, int)
    :param relative_location:     (x,y) location relative to the default location of the window, in pixels. Normally the window centers.  This location is relative to the location the window would be created. Note they can be negative.
    :type relative_location:      (int, int)
    :param non_blocking:          if True the call will immediately return rather than waiting on user input
    :type non_blocking:           (bool)
    :param background_color:      color of background
    :type background_color:       (str)
    :param text_color:            color of the text
    :type text_color:             (str)
    :param no_titlebar:           If True no titlebar will be shown
    :type no_titlebar:            (bool)
    :param grab_anywhere:         If True, than can grab anywhere to move the window (Default = False)
    :type grab_anywhere:          (bool)
    :param keep_on_top:           If True the window will remain above all current windows
    :type keep_on_top:            (bool)
    :param font:                  specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
    :type font:                   (str or (str, int[, str]) or None)
    :param image:                 Image to include at the top of the popup window
    :type image:                  (str) or (bytes)
    :param icon:                  filename or base64 string to be used for the window's icon
    :type icon:                   bytes | str
    :param modal:                 If True then makes the popup will behave like a Modal window... all other windows are non-operational until this one is closed. Default = True
    :type modal:                  bool
    :param no_sizegrip:           If True no Sizegrip will be shown when there is no titlebar. It's only shown if there is no titlebar
    :type no_sizegrip:            (bool)
    :return:                      Returns text of the button that was pressed.  None will be returned if user closed window with X
    :rtype:                       str | None | TIMEOUT_KEY
    """

    if not args:
            return None
    width, height = size
    width = width or MESSAGE_BOX_LINE_WIDTH

    layout = [[]]

    if image is not None:
        if isinstance(image, str):
            layout += [[Image(filename=image)]]
        else:
            layout += [[Image(data=image)]]
    max_line_total, max_line_width, total_lines, height_computed = 0, 0, 0, 0
    complete_output = ''
    for message in map(str, args):
        longest_line_len = max([len(line) for line in message.split('\n')])
        width_used = min(longest_line_len, width)
        max_line_total = max(max_line_total, width_used)
        max_line_width = width
        lines_needed = _get_num_lines_needed(message, width_used)
        height_computed += lines_needed + 1
        complete_output += message + '\n'
        total_lines += lines_needed
    height_computed = min(MAX_SCROLLED_TEXT_BOX_HEIGHT, height_computed)
    if height:
        height_computed = height
    layout += [[Multiline(complete_output, size=(max_line_width, height_computed), background_color=background_color, text_color=text_color, expand_x=True,
                          expand_y=True, key='-MLINE-')]]
    # show either an OK or Yes/No depending on paramater
    button = DummyButton if non_blocking else Button

    if yes_no:
        buttons = [button('Yes'), button('No')]
    elif no_buttons is not True:
        buttons =  [button('OK', size=(5, 1), button_color=button_color)]
    else:
        buttons = None

    if buttons is not None:
        if button_justification.startswith('l'):
            layout += [buttons]
        elif button_justification.startswith('c'):
            layout += [[Push(), *buttons, Push()]]
        else:
            layout += [[Push(), *buttons]]

    if no_sizegrip is not True:
        layout[-1] += [Sizegrip()]

    window = Window(title or args[0], layout, auto_size_text=True, button_color=button_color, auto_close=auto_close,
                    auto_close_duration=auto_close_duration, location=location, relative_location=relative_location, resizable=True, font=font, background_color=background_color,
                    no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, modal=modal, icon=icon)
    if non_blocking:
        button, _ = window.read(timeout=0)
    else:
        button, _ = window.read()
        window.close()
        del window
    return button


# ============================== sprint ======#
# Is identical to the Scrolled Text Box       #
# Provides a crude 'print' mechanism but in a #
# GUI environment                             #
# This is in addition to the Print function   #
# which routes output to a "Debug Window"     #
# ============================================#


# --------------------------- popup_no_buttons ---------------------------
def popup_no_buttons(*args, title=None, background_color=None, text_color=None, auto_close=False,
                     auto_close_duration=None, non_blocking=False, icon=None, line_width=None, font=None,
                     no_titlebar=False, grab_anywhere=False, keep_on_top=None, location=(None, None), relative_location=(None, None), image=None, modal=True):
    """Show a Popup but without any buttons

    :param *args:               Variable number of items to display
    :type *args:                (Any)
    :param title:               Title to display in the window.
    :type title:                (str)
    :param background_color:    color of background
    :type background_color:     (str)
    :param text_color:          color of the text
    :type text_color:           (str)
    :param auto_close:          if True window will close itself
    :type auto_close:           (bool)
    :param auto_close_duration: Older versions only accept int. Time in seconds until window will close
    :type auto_close_duration:  int | float
    :param non_blocking:        If True then will immediately return from the function without waiting for the user's input. (Default = False)
    :type non_blocking:         (bool)
    :param icon:                filename or base64 string to be used for the window's icon
    :type icon:                 bytes | str
    :param line_width:          Width of lines in characters
    :type line_width:           (int)
    :param font:                specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
    :type font:                 (str or (str, int[, str]) or None)
    :param no_titlebar:         If True no titlebar will be shown
    :type no_titlebar:          (bool)
    :param grab_anywhere:       If True, than can grab anywhere to move the window (Default = False)
    :type grab_anywhere:        (bool)
    :param location:            Location of upper left corner of the window
    :type location:             (int, int)
    :param relative_location:   (x,y) location relative to the default location of the window, in pixels. Normally the window centers.  This location is relative to the location the window would be created. Note they can be negative.
    :type relative_location:    (int, int)
    :param image:               Image to include at the top of the popup window
    :type image:                (str) or (bytes)
    :param modal:               If True then makes the popup will behave like a Modal window... all other windows are non-operational until this one is closed. Default = True
    :type modal:                bool
    :return:                    Returns text of the button that was pressed.  None will be returned if user closed window with X
    :rtype:                     str | None | TIMEOUT_KEY    """
    popup(*args, title=title, background_color=background_color, text_color=text_color,
          button_type=POPUP_BUTTONS_NO_BUTTONS,
          auto_close=auto_close, auto_close_duration=auto_close_duration, non_blocking=non_blocking, icon=icon,
          line_width=line_width,
          font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location, relative_location=relative_location, image=image, modal=modal)


# --------------------------- popup_non_blocking ---------------------------
def popup_non_blocking(*args, title=None, button_type=POPUP_BUTTONS_OK, button_color=None, background_color=None,
                       text_color=None, auto_close=False, auto_close_duration=None, non_blocking=True, icon=None,
                       line_width=None, font=None, no_titlebar=False, grab_anywhere=False, keep_on_top=None,
                       location=(None, None), relative_location=(None, None), image=None, modal=False):
    """
    Show Popup window and immediately return (does not block)

    :param *args:               Variable number of items to display
    :type *args:                (Any)
    :param title:               Title to display in the window.
    :type title:                (str)
    :param button_type:         Determines which pre-defined buttons will be shown (Default value = POPUP_BUTTONS_OK).
    :type button_type:          (int)
    :param button_color:        button color (foreground, background)
    :type button_color:         (str, str) | str
    :param background_color:    color of background
    :type background_color:     (str)
    :param text_color:          color of the text
    :type text_color:           (str)
    :param auto_close:          if True window will close itself
    :type auto_close:           (bool)
    :param auto_close_duration: Older versions only accept int. Time in seconds until window will close
    :type auto_close_duration:  int | float
    :param non_blocking:        if True the call will immediately return rather than waiting on user input
    :type non_blocking:         (bool)
    :param icon:                filename or base64 string to be used for the window's icon
    :type icon:                 bytes | str
    :param line_width:          Width of lines in characters
    :type line_width:           (int)
    :param font:                specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
    :type font:                 (str or (str, int[, str]) or None)
    :param no_titlebar:         If True no titlebar will be shown
    :type no_titlebar:          (bool)
    :param grab_anywhere:       If True: can grab anywhere to move the window (Default = False)
    :type grab_anywhere:        (bool)
    :param location:            Location of upper left corner of the window
    :type location:             (int, int)
    :param relative_location:   (x,y) location relative to the default location of the window, in pixels. Normally the window centers.  This location is relative to the location the window would be created. Note they can be negative.
    :type relative_location:    (int, int)
    :param image:               Image to include at the top of the popup window
    :type image:                (str) or (bytes)
    :param modal:               If True then makes the popup will behave like a Modal window... all other windows are non-operational until this one is closed. Default = False
    :type modal:                bool
    :return:                    Reason for popup closing
    :rtype:                     str | None
    """

    return popup(*args, title=title, button_color=button_color, background_color=background_color, text_color=text_color,
                 button_type=button_type,
                 auto_close=auto_close, auto_close_duration=auto_close_duration, non_blocking=non_blocking, icon=icon,
                 line_width=line_width,
                 font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location, relative_location=relative_location, image=image, modal=modal)


# --------------------------- popup_quick - a NonBlocking, Self-closing Popup  ---------------------------
def popup_quick(*args, title=None, button_type=POPUP_BUTTONS_OK, button_color=None, background_color=None,
                text_color=None, auto_close=True, auto_close_duration=2, non_blocking=True, icon=None, line_width=None,
                font=None, no_titlebar=False, grab_anywhere=False, keep_on_top=None, location=(None, None), relative_location=(None, None), image=None, modal=False):
    """
    Show Popup box that doesn't block and closes itself

    :param *args:               Variable number of items to display
    :type *args:                (Any)
    :param title:               Title to display in the window.
    :type title:                (str)
    :param button_type:         Determines which pre-defined buttons will be shown (Default value = POPUP_BUTTONS_OK).
    :type button_type:          (int)
    :param button_color:        button color (foreground, background)
    :type button_color:         (str, str) | str
    :param background_color:    color of background
    :type background_color:     (str)
    :param text_color:          color of the text
    :type text_color:           (str)
    :param auto_close:          if True window will close itself
    :type auto_close:           (bool)
    :param auto_close_duration: Older versions only accept int. Time in seconds until window will close
    :type auto_close_duration:  int | float
    :param non_blocking:        if True the call will immediately return rather than waiting on user input
    :type non_blocking:         (bool)
    :param icon:                filename or base64 string to be used for the window's icon
    :type icon:                 bytes | str
    :param line_width:          Width of lines in characters
    :type line_width:           (int)
    :param font:                specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
    :type font:                 (str or (str, int[, str]) or None)
    :param no_titlebar:         If True no titlebar will be shown
    :type no_titlebar:          (bool)
    :param grab_anywhere:       If True: can grab anywhere to move the window (Default = False)
    :type grab_anywhere:        (bool)
    :param keep_on_top:         If True the window will remain above all current windows
    :type keep_on_top:          (bool)
    :param location:            Location of upper left corner of the window
    :type location:             (int, int)
    :param relative_location:   (x,y) location relative to the default location of the window, in pixels. Normally the window centers.  This location is relative to the location the window would be created. Note they can be negative.
    :type relative_location:    (int, int)
    :param image:               Image to include at the top of the popup window
    :type image:                (str) or (bytes)
    :param modal:               If True then makes the popup will behave like a Modal window... all other windows are non-operational until this one is closed. Default = False
    :type modal:                bool
    :return:                    Returns text of the button that was pressed.  None will be returned if user closed window with X
    :rtype:                     str | None | TIMEOUT_KEY
    """

    return popup(*args, title=title, button_color=button_color, background_color=background_color, text_color=text_color,
                 button_type=button_type,
                 auto_close=auto_close, auto_close_duration=auto_close_duration, non_blocking=non_blocking, icon=icon,
                 line_width=line_width,
                 font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location, relative_location=relative_location, image=image, modal=modal)


# --------------------------- popup_quick_message - a NonBlocking, Self-closing Popup with no titlebar and no buttons ---------------------------
def popup_quick_message(*args, title=None, button_type=POPUP_BUTTONS_NO_BUTTONS, button_color=None, background_color=None,
                        text_color=None, auto_close=True, auto_close_duration=2, non_blocking=True, icon=None, line_width=None,
                        font=None, no_titlebar=True, grab_anywhere=False, keep_on_top=True, location=(None, None), relative_location=(None, None), image=None, modal=False):
    """
    Show Popup window with no titlebar, doesn't block, and auto closes itself.

    :param *args:               Variable number of items to display
    :type *args:                (Any)
    :param title:               Title to display in the window.
    :type title:                (str)
    :param button_type:         Determines which pre-defined buttons will be shown (Default value = POPUP_BUTTONS_OK).
    :type button_type:          (int)
    :param button_color:        button color (foreground, background)
    :type button_color:         (str, str) | str
    :param keep_on_top:         If True the window will remain above all current windows
    :type keep_on_top:          (bool)
    :param background_color:    color of background
    :type background_color:     (str)
    :param text_color:          color of the text
    :type text_color:           (str)
    :param auto_close:          if True window will close itself
    :type auto_close:           (bool)
    :param auto_close_duration: Older versions only accept int. Time in seconds until window will close
    :type auto_close_duration:  int | float
    :param non_blocking:        if True the call will immediately return rather than waiting on user input
    :type non_blocking:         (bool)
    :param icon:                filename or base64 string to be used for the window's icon
    :type icon:                 bytes | str
    :param line_width:          Width of lines in characters
    :type line_width:           (int)
    :param font:                specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
    :type font:                 (str or (str, int[, str]) or None)
    :param no_titlebar:         If True no titlebar will be shown
    :type no_titlebar:          (bool)
    :param grab_anywhere:       If True: can grab anywhere to move the window (Default = False)
    :type grab_anywhere:        (bool)
    :param location:            Location of upper left corner of the window
    :type location:             (int, int)
    :param relative_location:   (x,y) location relative to the default location of the window, in pixels. Normally the window centers.  This location is relative to the location the window would be created. Note they can be negative.
    :type relative_location:    (int, int)
    :param image:               Image to include at the top of the popup window
    :type image:                (str) or (bytes)
    :param modal:               If True then makes the popup will behave like a Modal window... all other windows are non-operational until this one is closed. Default = False
    :type modal:                bool
    :return:                    Returns text of the button that was pressed.  None will be returned if user closed window with X
    :rtype:                     str | None | TIMEOUT_KEY
    """
    return popup(*args, title=title, button_color=button_color, background_color=background_color, text_color=text_color,
                 button_type=button_type,
                 auto_close=auto_close, auto_close_duration=auto_close_duration, non_blocking=non_blocking, icon=icon,
                 line_width=line_width,
                 font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location, relative_location=relative_location, image=image, modal=modal)


# --------------------------- PopupNoTitlebar ---------------------------
def popup_no_titlebar(*args, title=None, button_type=POPUP_BUTTONS_OK, button_color=None, background_color=None,
                      text_color=None, auto_close=False, auto_close_duration=None, non_blocking=False, icon=None,
                      line_width=None, font=None, grab_anywhere=True, keep_on_top=None, location=(None, None), relative_location=(None, None), image=None, modal=True):
    """
    Display a Popup without a titlebar.   Enables grab anywhere so you can move it

    :param *args:               Variable number of items to display
    :type *args:                (Any)
    :param title:               Title to display in the window.
    :type title:                (str)
    :param button_type:         Determines which pre-defined buttons will be shown (Default value = POPUP_BUTTONS_OK).
    :type button_type:          (int)
    :param button_color:        button color (foreground, background)
    :type button_color:         (str, str) | str
    :param background_color:    color of background
    :type background_color:     (str)
    :param text_color:          color of the text
    :type text_color:           (str)
    :param auto_close:          if True window will close itself
    :type auto_close:           (bool)
    :param auto_close_duration: Older versions only accept int. Time in seconds until window will close
    :type auto_close_duration:  int | float
    :param non_blocking:        if True the call will immediately return rather than waiting on user input
    :type non_blocking:         (bool)
    :param icon:                filename or base64 string to be used for the window's icon
    :type icon:                 bytes | str
    :param line_width:          Width of lines in characters
    :type line_width:           (int)
    :param font:                specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
    :type font:                 (str or (str, int[, str]) or None)
    :param grab_anywhere:       If True: can grab anywhere to move the window (Default = False)
    :type grab_anywhere:        (bool)
    :param keep_on_top:         If True the window will remain above all current windows
    :type keep_on_top:          (bool)
    :param location:            Location of upper left corner of the window
    :type location:             (int, int)
    :param relative_location:   (x,y) location relative to the default location of the window, in pixels. Normally the window centers.  This location is relative to the location the window would be created. Note they can be negative.
    :type relative_location:    (int, int)
    :param image:               Image to include at the top of the popup window
    :type image:                (str) or (bytes)
    :param modal:               If True then makes the popup will behave like a Modal window... all other windows are non-operational until this one is closed. Default = True
    :type modal:                bool
    :return:                    Returns text of the button that was pressed.  None will be returned if user closed window with X
    :rtype:                     str | None | TIMEOUT_KEY
    """
    return popup(*args, title=title, button_color=button_color, background_color=background_color, text_color=text_color,
                 button_type=button_type,
                 auto_close=auto_close, auto_close_duration=auto_close_duration, non_blocking=non_blocking, icon=icon,
                 line_width=line_width,
                 font=font, no_titlebar=True, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location, relative_location=relative_location, image=image, modal=modal)


# --------------------------- PopupAutoClose ---------------------------
def popup_auto_close(*args, title=None, button_type=POPUP_BUTTONS_OK, button_color=None, background_color=None, text_color=None,
                     auto_close=True, auto_close_duration=None, non_blocking=False, icon=None,
                     line_width=None, font=None, no_titlebar=False, grab_anywhere=False, keep_on_top=None,
                     location=(None, None), relative_location=(None, None), image=None, modal=True):
    """Popup that closes itself after some time period

    :param *args:               Variable number of items to display
    :type *args:                (Any)
    :param title:               Title to display in the window.
    :type title:                (str)
    :param button_type:         Determines which pre-defined buttons will be shown (Default value = POPUP_BUTTONS_OK).
    :type button_type:          (int)
    :param button_color:        button color (foreground, background)
    :type button_color:         (str, str) | str
    :param background_color:    color of background
    :type background_color:     (str)
    :param text_color:          color of the text
    :type text_color:           (str)
    :param auto_close:          if True window will close itself
    :type auto_close:           (bool)
    :param auto_close_duration: Older versions only accept int. Time in seconds until window will close
    :type auto_close_duration:  int | float
    :param non_blocking:        if True the call will immediately return rather than waiting on user input
    :type non_blocking:         (bool)
    :param icon:                filename or base64 string to be used for the window's icon
    :type icon:                 bytes | str
    :param line_width:          Width of lines in characters
    :type line_width:           (int)
    :param font:                specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
    :type font:                 (str or (str, int[, str]) or None)
    :param no_titlebar:         If True no titlebar will be shown
    :type no_titlebar:          (bool)
    :param grab_anywhere:       If True: can grab anywhere to move the window (Default = False)
    :type grab_anywhere:        (bool)
    :param keep_on_top:         If True the window will remain above all current windows
    :type keep_on_top:          (bool)
    :param location:            Location of upper left corner of the window
    :type location:             (int, int)
    :param relative_location:   (x,y) location relative to the default location of the window, in pixels. Normally the window centers.  This location is relative to the location the window would be created. Note they can be negative.
    :type relative_location:    (int, int)
    :param image:               Image to include at the top of the popup window
    :type image:                (str) or (bytes)
    :param modal:               If True then makes the popup will behave like a Modal window... all other windows are non-operational until this one is closed. Default = True
    :type modal:                bool
    :return:                    Returns text of the button that was pressed.  None will be returned if user closed window with X
    :rtype:                     str | None | TIMEOUT_KEY
    """

    return popup(*args, title=title, button_color=button_color, background_color=background_color, text_color=text_color,
                 button_type=button_type,
                 auto_close=auto_close, auto_close_duration=auto_close_duration, non_blocking=non_blocking, icon=icon,
                 line_width=line_width,
                 font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location, relative_location=relative_location, image=image, modal=modal)


# --------------------------- popup_error ---------------------------
def popup_error(*args, title=None, button_color=(None, None), background_color=None, text_color=None, auto_close=False,
                auto_close_duration=None, non_blocking=False, icon=None, line_width=None, font=None,
                no_titlebar=False, grab_anywhere=False, keep_on_top=None, location=(None, None), relative_location=(None, None), image=None, modal=True):
    """
    Popup with colored button and 'Error' as button text

    :param *args:               Variable number of items to display
    :type *args:                (Any)
    :param title:               Title to display in the window.
    :type title:                (str)
    :param button_color:        button color (foreground, background)
    :type button_color:         (str, str) | str
    :param background_color:    color of background
    :type background_color:     (str)
    :param text_color:          color of the text
    :type text_color:           (str)
    :param auto_close:          if True window will close itself
    :type auto_close:           (bool)
    :param auto_close_duration: Older versions only accept int. Time in seconds until window will close
    :type auto_close_duration:  int | float
    :param non_blocking:        if True the call will immediately return rather than waiting on user input
    :type non_blocking:         (bool)
    :param icon:                filename or base64 string to be used for the window's icon
    :type icon:                 bytes | str
    :param line_width:          Width of lines in characters
    :type line_width:           (int)
    :param font:                specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
    :type font:                 (str or (str, int[, str]) or None)
    :param no_titlebar:         If True no titlebar will be shown
    :type no_titlebar:          (bool)
    :param grab_anywhere:       If True: can grab anywhere to move the window (Default = False)
    :type grab_anywhere:        (bool)
    :param keep_on_top:         If True the window will remain above all current windows
    :type keep_on_top:          (bool)
    :param location:            Location of upper left corner of the window
    :type location:             (int, int)
    :param relative_location:   (x,y) location relative to the default location of the window, in pixels. Normally the window centers.  This location is relative to the location the window would be created. Note they can be negative.
    :type relative_location:    (int, int)
    :param image:               Image to include at the top of the popup window
    :type image:                (str) or (bytes)
    :param modal:               If True then makes the popup will behave like a Modal window... all other windows are non-operational until this one is closed. Default = True
    :type modal:                bool
    :return:                    Returns text of the button that was pressed.  None will be returned if user closed window with X
    :rtype:                     str | None | TIMEOUT_KEY
    """
    tbutton_color = DEFAULTS.ERROR_BUTTON_COLOR if button_color == (None, None) else button_color
    return popup(*args, title=title, button_type=POPUP_BUTTONS_ERROR, background_color=background_color, text_color=text_color,
                 non_blocking=non_blocking, icon=icon, line_width=line_width, button_color=tbutton_color,
                 auto_close=auto_close,
                 auto_close_duration=auto_close_duration, font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere,
                 keep_on_top=keep_on_top, location=location, relative_location=relative_location, image=image, modal=modal)


# --------------------------- popup_cancel ---------------------------
def popup_cancel(*args, title=None, button_color=None, background_color=None, text_color=None, auto_close=False,
                 auto_close_duration=None, non_blocking=False, icon=None, line_width=None, font=None,
                 no_titlebar=False, grab_anywhere=False, keep_on_top=None, location=(None, None), relative_location=(None, None), image=None, modal=True):
    """
    Display Popup with "cancelled" button text

    :param *args:               Variable number of items to display
    :type *args:                (Any)
    :param title:               Title to display in the window.
    :type title:                (str)
    :param button_color:        button color (foreground, background)
    :type button_color:         (str, str) | str
    :param background_color:    color of background
    :type background_color:     (str)
    :param text_color:          color of the text
    :type text_color:           (str)
    :param auto_close:          if True window will close itself
    :type auto_close:           (bool)
    :param auto_close_duration: Older versions only accept int. Time in seconds until window will close
    :type auto_close_duration:  int | float
    :param non_blocking:        if True the call will immediately return rather than waiting on user input
    :type non_blocking:         (bool)
    :param icon:                filename or base64 string to be used for the window's icon
    :type icon:                 bytes | str
    :param line_width:          Width of lines in characters
    :type line_width:           (int)
    :param font:                specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
    :type font:                 (str or (str, int[, str]) or None)
    :param no_titlebar:         If True no titlebar will be shown
    :type no_titlebar:          (bool)
    :param grab_anywhere:       If True: can grab anywhere to move the window (Default = False)
    :type grab_anywhere:        (bool)
    :param keep_on_top:         If True the window will remain above all current windows
    :type keep_on_top:          (bool)
    :param location:            Location of upper left corner of the window
    :type location:             (int, int)
    :param relative_location:   (x,y) location relative to the default location of the window, in pixels. Normally the window centers.  This location is relative to the location the window would be created. Note they can be negative.
    :type relative_location:    (int, int)
    :param image:               Image to include at the top of the popup window
    :type image:                (str) or (bytes)
    :param modal:               If True then makes the popup will behave like a Modal window... all other windows are non-operational until this one is closed. Default = True
    :type modal:                bool
    :return:                    Returns text of the button that was pressed.  None will be returned if user closed window with X
    :rtype:                     str | None | TIMEOUT_KEY
    """
    return popup(*args, title=title, button_type=POPUP_BUTTONS_CANCELLED, background_color=background_color,
                 text_color=text_color,
                 non_blocking=non_blocking, icon=icon, line_width=line_width, button_color=button_color, auto_close=auto_close,
                 auto_close_duration=auto_close_duration, font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere,
                 keep_on_top=keep_on_top, location=location, relative_location=relative_location, image=image, modal=modal)


# --------------------------- popup_ok ---------------------------
def popup_ok(*args, title=None, button_color=None, background_color=None, text_color=None, auto_close=False,
             auto_close_duration=None, non_blocking=False, icon=None, line_width=None, font=None,
             no_titlebar=False, grab_anywhere=False, keep_on_top=None, location=(None, None), relative_location=(None, None), image=None, modal=True):
    """
    Display Popup with OK button only

    :param *args:               Variable number of items to display
    :type *args:                (Any)
    :param title:               Title to display in the window.
    :type title:                (str)
    :param button_color:        button color (foreground, background)
    :type button_color:         (str, str) | str
    :param background_color:    color of background
    :type background_color:     (str)
    :param text_color:          color of the text
    :type text_color:           (str)
    :param auto_close:          if True window will close itself
    :type auto_close:           (bool)
    :param auto_close_duration: Older versions only accept int. Time in seconds until window will close
    :type auto_close_duration:  int | float
    :param non_blocking:        if True the call will immediately return rather than waiting on user input
    :type non_blocking:         (bool)
    :param icon:                filename or base64 string to be used for the window's icon
    :type icon:                 bytes | str
    :param line_width:          Width of lines in characters
    :type line_width:           (int)
    :param font:                specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
    :type font:                 (str or (str, int[, str]) or None)
    :param no_titlebar:         If True no titlebar will be shown
    :type no_titlebar:          (bool)
    :param grab_anywhere:       If True: can grab anywhere to move the window (Default = False)
    :type grab_anywhere:        (bool)
    :param keep_on_top:         If True the window will remain above all current windows
    :type keep_on_top:          (bool)
    :param location:            Location of upper left corner of the window
    :type location:             (int, int)
    :param relative_location:   (x,y) location relative to the default location of the window, in pixels. Normally the window centers.  This location is relative to the location the window would be created. Note they can be negative.
    :type relative_location:    (int, int)
    :param image:               Image to include at the top of the popup window
    :type image:                (str) or (bytes)
    :param modal:               If True then makes the popup will behave like a Modal window... all other windows are non-operational until this one is closed. Default = True
    :type modal:                bool
    :return:                    Returns text of the button that was pressed.  None will be returned if user closed window with X
    :rtype:                     str | None | TIMEOUT_KEY
    """
    return popup(*args, title=title, button_type=POPUP_BUTTONS_OK, background_color=background_color, text_color=text_color,
                 non_blocking=non_blocking, icon=icon, line_width=line_width, button_color=button_color, auto_close=auto_close,
                 auto_close_duration=auto_close_duration, font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere,
                 keep_on_top=keep_on_top, location=location, relative_location=relative_location, image=image, modal=modal)


# --------------------------- popup_ok_cancel ---------------------------
def popup_ok_cancel(*args, title=None, button_color=None, background_color=None, text_color=None, auto_close=False,
                    auto_close_duration=None, non_blocking=False, icon=DEFAULTS.WINDOW_ICON, line_width=None, font=None,
                    no_titlebar=False, grab_anywhere=False, keep_on_top=None, location=(None, None), relative_location=(None, None), image=None, modal=True):
    """
    Display popup with OK and Cancel buttons

    :param *args:               Variable number of items to display
    :type *args:                (Any)
    :param title:               Title to display in the window.
    :type title:                (str)
    :param button_color:        button color (foreground, background)
    :type button_color:         (str, str) | str
    :param background_color:    color of background
    :type background_color:     (str)
    :param text_color:          color of the text
    :type text_color:           (str)
    :param auto_close:          if True window will close itself
    :type auto_close:           (bool)
    :param auto_close_duration: Older versions only accept int. Time in seconds until window will close
    :type auto_close_duration:  int | float
    :param non_blocking:        if True the call will immediately return rather than waiting on user input
    :type non_blocking:         (bool)
    :param icon:                filename or base64 string to be used for the window's icon
    :type icon:                 bytes | str
    :param line_width:          Width of lines in characters
    :type line_width:           (int)
    :param font:                specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
    :type font:                 (str or (str, int[, str]) or None)
    :param no_titlebar:         If True no titlebar will be shown
    :type no_titlebar:          (bool)
    :param grab_anywhere:       If True: can grab anywhere to move the window (Default = False)
    :type grab_anywhere:        (bool)
    :param keep_on_top:         If True the window will remain above all current windows
    :type keep_on_top:          (bool)
    :param location:            Location of upper left corner of the window
    :type location:             (int, int)
    :param relative_location:   (x,y) location relative to the default location of the window, in pixels. Normally the window centers.  This location is relative to the location the window would be created. Note they can be negative.
    :type relative_location:    (int, int)
    :param image:               Image to include at the top of the popup window
    :type image:                (str) or (bytes)
    :param modal:               If True then makes the popup will behave like a Modal window... all other windows are non-operational until this one is closed. Default = True
    :type modal:                bool
    :return:                    clicked button
    :rtype:                     "OK" | "Cancel" | None
    """
    return popup(*args, title=title, button_type=POPUP_BUTTONS_OK_CANCEL, background_color=background_color,
                 text_color=text_color,
                 non_blocking=non_blocking, icon=icon, line_width=line_width, button_color=button_color,
                 auto_close=auto_close, auto_close_duration=auto_close_duration, font=font, no_titlebar=no_titlebar,
                 grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location, relative_location=relative_location, image=image, modal=modal)


# --------------------------- popup_yes_no ---------------------------
def popup_yes_no(*args, title=None, button_color=None, background_color=None, text_color=None, auto_close=False,
                 auto_close_duration=None, non_blocking=False, icon=None, line_width=None, font=None,
                 no_titlebar=False, grab_anywhere=False, keep_on_top=None, location=(None, None), relative_location=(None, None), image=None, modal=True):
    """
    Display Popup with Yes and No buttons

    :param *args:               Variable number of items to display
    :type *args:                (Any)
    :param title:               Title to display in the window.
    :type title:                (str)
    :param button_color:        button color (foreground, background)
    :type button_color:         (str, str) | str
    :param background_color:    color of background
    :type background_color:     (str)
    :param text_color:          color of the text
    :type text_color:           (str)
    :param auto_close:          if True window will close itself
    :type auto_close:           (bool)
    :param auto_close_duration: Older versions only accept int. Time in seconds until window will close
    :type auto_close_duration:  int | float
    :param non_blocking:        if True the call will immediately return rather than waiting on user input
    :type non_blocking:         (bool)
    :param icon:                filename or base64 string to be used for the window's icon
    :type icon:                 bytes | str
    :param line_width:          Width of lines in characters
    :type line_width:           (int)
    :param font:                specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
    :type font:                 (str or (str, int[, str]) or None)
    :param no_titlebar:         If True no titlebar will be shown
    :type no_titlebar:          (bool)
    :param grab_anywhere:       If True: can grab anywhere to move the window (Default = False)
    :type grab_anywhere:        (bool)
    :param keep_on_top:         If True the window will remain above all current windows
    :type keep_on_top:          (bool)
    :param location:            Location of upper left corner of the window
    :type location:             (int, int)
    :param relative_location:   (x,y) location relative to the default location of the window, in pixels. Normally the window centers.  This location is relative to the location the window would be created. Note they can be negative.
    :type relative_location:    (int, int)
    :param image:               Image to include at the top of the popup window
    :type image:                (str) or (bytes)
    :param modal:               If True then makes the popup will behave like a Modal window... all other windows are non-operational until this one is closed. Default = True
    :type modal:                bool
    :return:                    clicked button
    :rtype:                     "Yes" | "No" | None
    """
    return popup(*args, title=title, button_type=POPUP_BUTTONS_YES_NO, background_color=background_color,
                 text_color=text_color,
                 non_blocking=non_blocking, icon=icon, line_width=line_width, button_color=button_color,
                 auto_close=auto_close, auto_close_duration=auto_close_duration, font=font, no_titlebar=no_titlebar,
                 grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location, relative_location=relative_location, image=image, modal=modal)
