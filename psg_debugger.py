

import inspect
import sys
import traceback

from quick_tkinter import (
    SYMBOLS,
    Button,
    Cancel,
    Checkbox,
    Column,
    Frame,
    Input,
    Multiline,
    Ok,
    Tab,
    TabGroup,
    Text,
    VerticalSeparator,
    Window,
    obj_to_string_single_obj,
    popup_quick_message,
    popup_scrolled,
    popup_yes_no,
    theme,
    theme_button_color,
)


class _Debugger:
    debugger: _Debugger | None = None
    DEBUGGER_MAIN_WINDOW_THEME = 'dark grey 13'
    DEBUGGER_POPOUT_THEME = 'dark grey 13'
    WIDTH_VARIABLES = 23
    WIDTH_RESULTS = 46

    WIDTH_WATCHER_VARIABLES = 20
    WIDTH_WATCHER_RESULTS = 60

    WIDTH_LOCALS = 80
    NUM_AUTO_WATCH = 9

    MAX_LINES_PER_RESULT_FLOATING = 4
    MAX_LINES_PER_RESULT_MAIN = 3

    DEBUGGER_POPOUT_WINDOW_FONT = 'Sans 8'
    DEBUGGER_VARIABLE_DETAILS_FONT = 'Courier 10'

    
    def __init__(self):
        self.watcher_window = None  # type: Window
        self.popout_window = None  # type: Window
        self.local_choices = {}
        self.myrc = ''
        self.custom_watch = ''
        self.locals = {}
        self.globals = {}
        self.popout_choices = {}

    # Includes the DUAL PANE (now 2 tabs)!  Don't forget REPL is there too!
    def _build_main_debugger_window(self, location=(None, None)):
        old_theme = theme()
        theme(_Debugger.DEBUGGER_MAIN_WINDOW_THEME)

        def _in_var(key1):
            return [
                Text('    '),
                Input(key=key1, size=(_Debugger.WIDTH_VARIABLES, 1)),
                Text('', key=key1 + 'CHANGED_', size=(_Debugger.WIDTH_RESULTS, 1)),
                Button('Detail', key=key1 + 'DETAIL_'),
                Button('Obj', key=key1 + 'OBJ_')
            ]

        variables_frame = [_in_var(f'_VAR{i}_') for i in range(3)]

        interactive_frame = [
            [
                Text('>>> '),
                Input(size=(83, 1), key='-REPL-', tooltip='Type in any "expression" or "statement"\n and it will be disaplayed below.\nPress RETURN KEY instead of "Go"\nbutton for faster use'),
                Button('Go', bind_return_key=True, visible=True)
            ],
            [Multiline(size=(93, 26), key='-OUTPUT-', autoscroll=True, do_not_clear=True)]
        ]

        autowatch_frame = [[
            Button('Choose Variables To Auto Watch', key='-LOCALS-'),
            Button('Clear All Auto Watches'),
            Button('Show All Variables', key='-SHOW_ALL-'),
            Button('Locals', key='-ALL_LOCALS-'),
            Button('Globals', key='-GLOBALS-'),
            Button('Popout', key='-POPOUT-')
        ]]

        var_layout = [
            [
                Text('', size=(_Debugger.WIDTH_WATCHER_VARIABLES, 1), key=f"_WATCH{i}_"),
                Text('', size=(_Debugger.WIDTH_WATCHER_RESULTS, _Debugger.MAX_LINES_PER_RESULT_MAIN), key=f"_WATCH{i}_RESULT_")
            ]
            for i in range(_Debugger.NUM_AUTO_WATCH)
        ]

        col1 = [
            # [Frame('Auto Watches', autowatch_frame+variable_values, title_color='blue')]
            [Frame('Auto Watches', autowatch_frame + var_layout, title_color=theme_button_color()[0])]
        ]

        col2 = [
            [Frame('Variables or Expressions to Watch', variables_frame, title_color=theme_button_color()[0])],
            [Frame('REPL-Light - Press Enter To Execute Commands', interactive_frame, title_color=theme_button_color()[0]) ]
        ]

        # Tab based layout
        layout = [
            [Text('Debugging: ' + self._find_users_code())],
            [TabGroup([[
                Tab('Variables', col1),
                Tab('REPL & Watches', col2)
            ]])]
        ]

        # ------------------------------- Create main window -------------------------------
        window = Window("PySimpleGUI Debugger", layout, icon=PSG_DEBUGGER_LOGO, margins=(0, 0), location=location, keep_on_top=True, right_click_menu=[[''], ['Exit']])

        Window._read_call_from_debugger = True
        window.finalize()
        Window._read_call_from_debugger = False

        window.find_element('_VAR1_').set_focus()
        self.watcher_window = window
        theme(old_theme)
        return window

    def _refresh_main_debugger_window(self, mylocals, myglobals):
        if not self.watcher_window:  # if there is no window setup, nothing to do
            return False
        event, values = self.watcher_window.read(timeout=1)
        if event in (None, 'Exit', '_EXIT_', '-EXIT-'):  # EXIT BUTTON / X BUTTON
            try:
                self.watcher_window.close()
            except Exception:
                pass
            self.watcher_window = None
            return False
        # ------------------------------- Process events from REPL Tab -------------------------------
        cmd = values['-REPL-']  # get the REPL entered
        # BUTTON - GO (NOTE - This button is invisible!!)
        if event == 'Go':  # GO BUTTON
            self.watcher_window.find_element('-REPL-').update('')
            self.watcher_window.find_element('-OUTPUT-').update(f">>> {cmd}\n", append=True, autoscroll=True)

            try:
                result = eval(f"{cmd}", myglobals, mylocals)
            except Exception:
                if sys.version_info[0] < 3:
                    result = 'Not available in Python 2'
                else:
                    try:
                        result = exec(f"{cmd}", myglobals, mylocals)
                    except Exception as e:
                        result = f"Exception {e}\n"

            self.watcher_window.find_element('-OUTPUT-').update(f"{result}\n", append=True, autoscroll=True)
        # BUTTON - DETAIL
        elif event.endswith('_DETAIL_'):  # DETAIL BUTTON
            var = values[f"_VAR{event[4]}_"]
            try:
                result = str(eval(str(var), myglobals, mylocals))
            except Exception:
                result = ''
            old_theme = theme()
            theme(_Debugger.DEBUGGER_MAIN_WINDOW_THEME)
            popup_scrolled(str(values[f"_VAR{event[4]}_"]) + '\n' + result, title=var, non_blocking=True, font=_Debugger.DEBUGGER_VARIABLE_DETAILS_FONT)
            theme(old_theme)
        # BUTTON - OBJ
        elif event.endswith('_OBJ_'):  # OBJECT BUTTON
            var = values[f"_VAR{event[4]}_"]
            try:
                result = obj_to_string_single_obj(mylocals[var])
            except Exception:
                try:
                    result = eval(f"{var}", myglobals, mylocals)
                    result = obj_to_string_single_obj(result)
                except Exception as e:
                    result = f"{e}\nError showing object {var}"
            old_theme = theme()
            theme(_Debugger.DEBUGGER_MAIN_WINDOW_THEME)
            popup_scrolled(str(var) + '\n' + str(result), title=var, non_blocking=True, font=_Debugger.DEBUGGER_VARIABLE_DETAILS_FONT)
            theme(old_theme)
        # ------------------------------- Process Watch Tab -------------------------------
        # BUTTON - Choose Locals to see
        elif event == '-LOCALS-':  # Show all locals BUTTON
            self._choose_auto_watches(mylocals)
        # BUTTON - Locals (quick popup)
        elif event == '-ALL_LOCALS-':
            self._display_all_vars('All Locals', mylocals)
        # BUTTON - Globals (quick popup)
        elif event == '-GLOBALS-':
            self._display_all_vars('All Globals', myglobals)
        # BUTTON - clear all
        elif event == 'Clear All Auto Watches':
            if popup_yes_no('Do you really want to clear all Auto-Watches?', 'Really Clear??') == 'Yes':
                self.local_choices = {}
                self.custom_watch = ''
        # BUTTON - Popout
        elif event == '-POPOUT-':
            if not self.popout_window:
                self._build_floating_window()
        # BUTTON - Show All
        elif event == '-SHOW_ALL-':
            for key in self.locals:
                self.local_choices[key] = not key.startswith('_')

        # -------------------- Process the manual "watch list" ------------------
        for i in range(3):
            key = f"_VAR{i}_"
            out_key = f"_VAR{i}_CHANGED_"
            self.myrc = ''
            if self.watcher_window.find_element(key):
                var = values[key]
                try:
                    result = eval(str(var), myglobals, mylocals)
                except Exception:
                    result = ''
                self.watcher_window.find_element(out_key).update(str(result))
            else:
                self.watcher_window.find_element(out_key).update('')

        # -------------------- Process the automatic "watch list" ------------------
        slot = 0
        for key in self.local_choices:
            if key == '-CUSTOM_WATCH-':
                continue
            if self.local_choices[key]:
                self.watcher_window.find_element(f"_WATCH{slot}_").update(key)
                try:
                    self.watcher_window.find_element(f"_WATCH{slot}_RESULT_", silent_on_error=True).update(mylocals[key])
                except Exception:
                    self.watcher_window.find_element(f"_WATCH{slot}_RESULT_").update('')
                slot += 1

            if slot + int(self.custom_watch not in (None, '')) >= _Debugger.NUM_AUTO_WATCH:
                break
        # If a custom watch was set, display that value in the window
        if self.custom_watch:
            self.watcher_window.find_element(f"_WATCH{slot}_").update(self.custom_watch)
            try:
                self.myrc = eval(self.custom_watch, myglobals, mylocals)
            except Exception:
                self.myrc = ''
            self.watcher_window.find_element(f"_WATCH{slot}_RESULT_").update(self.myrc)
            slot += 1
        # blank out all of the slots not used (blank)
        for i in range(slot, _Debugger.NUM_AUTO_WATCH):
            self.watcher_window.find_element(f"_WATCH{i}_").update('')
            self.watcher_window.find_element(f"_WATCH{i}_RESULT_").update('')

        return True  # return indicating the window stayed open

    def _find_users_code(self):
        try:  # lots can go wrong so wrapping the entire thing
            trace_details = traceback.format_stack()
            file_info_pysimplegui, error_message = None, ''
            for line in reversed(trace_details):
                if __file__ not in line:
                    file_info_pysimplegui = line.split(",")[0]
                    error_message = line
                    break
            if file_info_pysimplegui is None:
                return ''
            error_parts = None
            if error_message != '':
                error_parts = error_message.split(', ')
                if len(error_parts) < 4:
                    error_message = error_parts[0] + '\n' + error_parts[1] + '\n' + ''.join(error_parts[2:])
            if error_parts is None:
                print('*** Error popup attempted but unable to parse error details ***')
                print(trace_details)
                return ''
            return error_parts[0][error_parts[0].index('File ') + 5:]
        except Exception:
            return None

    
    # displays them into a single text box

    def _display_all_vars(self, title, _dict):
        # num_cols = 3
        # output_text = ''
        # num_lines = 2
        # cur_col = 0
        out_text = title + '\n'
        # longest_line = max([len(key) for key in dict])
        # line = []
        sorted_dict = {}
        for key in sorted(_dict.keys()):
            sorted_dict[key] = _dict[key]
        for key in sorted_dict:
            value = _dict[key]
            # wrapped_list = textwrap.wrap(str(value), 60)
            # wrapped_text = '\n'.join(wrapped_list)
            wrapped_text = str(value)
            out_text += f"{key} - {wrapped_text}\n"
            # if cur_col + 1 == num_cols:
            #     cur_col = 0
            #     num_lines += len(wrapped_list)
            # else:
            #     cur_col += 1
        old_theme = theme()
        theme(_Debugger.DEBUGGER_MAIN_WINDOW_THEME)
        popup_scrolled(out_text, title=title, non_blocking=True, font=_Debugger.DEBUGGER_VARIABLE_DETAILS_FONT, keep_on_top=True, icon=PSG_DEBUGGER_LOGO)
        theme(old_theme)


    def _choose_auto_watches(self, my_locals):
        old_theme = theme()
        theme(_Debugger.DEBUGGER_MAIN_WINDOW_THEME)
        num_cols = 3
        # output_text = ''
        # num_lines = 2
        cur_col = 0
        layout = [[Text('Choose your "Auto Watch" variables', font='ANY 14', text_color='red')]]
        longest_line = max([len(key) for key in my_locals])
        line = []
        sorted_dict = {}
        for key in sorted(my_locals.keys()):
            sorted_dict[key] = my_locals[key]
        for key in sorted_dict:
            line.append(Checkbox(key, key=key, size=(longest_line, 1),
                           default_value=self.local_choices.get(key, False)))
            if cur_col + 1 == num_cols:
                cur_col = 0
                layout.append(line)
                line = []
            else:
                cur_col += 1
        if cur_col:
            layout.append(line)

        layout += [
            [Text('Custom Watch (any expression)'), Input(default_value=self.custom_watch, size=(40, 1), key='-CUSTOM_WATCH-')]]
        layout += [
            [Ok(), Cancel(), Button('Clear All'), Button('Select [almost] All', key='-AUTO_SELECT-')]]

        window = Window('Choose Watches', layout, icon=PSG_DEBUGGER_LOGO, finalize=True, keep_on_top=True)

        while True:  # event loop
            event, values = window.read()
            if event in (None, 'Cancel', '-EXIT-'):
                break
            if event == 'Ok':
                self.local_choices = values
                self.custom_watch = values['-CUSTOM_WATCH-']
                break
            if event == 'Clear All':
                popup_quick_message('Cleared Auto Watches', auto_close=True, auto_close_duration=3, non_blocking=True, text_color='red', font='ANY 18')
                for key in sorted_dict:
                    window.find_element(key).update(False)
                window.find_element('-CUSTOM_WATCH-').update('')
            elif event == 'Select All':
                for key in sorted_dict:
                    window.find_element(key).update(False)
            elif event == '-AUTO_SELECT-':
                for key in sorted_dict:
                    window.find_element(key).update(not key.startswith('_'))

        # exited event loop
        window.close()
        theme(old_theme)



    def _build_floating_window(self, location=(None, None)):
        """

        :param location:
        :type location:

        """
        if self.popout_window:  # if floating window already exists, close it first
            self.popout_window.close()
        old_theme = theme()
        theme(_Debugger.DEBUGGER_POPOUT_THEME)
        num_cols = 2
        width_var = 15
        width_value = 30
        layout = []
        line = []
        col = 0
        # self.popout_choices = self.local_choices
        self.popout_choices = {}
        if self.popout_choices == {}:  # if nothing chosen, then choose all non-_ variables
            for key in sorted(self.locals.keys()):
                self.popout_choices[key] = not key.startswith("_")

        width_var = max([len(key) for key in self.popout_choices])
        for key in self.popout_choices:
            if self.popout_choices[key] is True:
                value = str(self.locals.get(key))
                h = min(len(value) // width_value + 1, _Debugger.MAX_LINES_PER_RESULT_FLOATING)
                line += [Text(f"{key}", size=(width_var, 1), font=_Debugger.DEBUGGER_POPOUT_WINDOW_FONT),
                         Text(" = ", font=_Debugger.DEBUGGER_POPOUT_WINDOW_FONT),
                         Text(value, key=key, size=(width_value, h), font=_Debugger.DEBUGGER_POPOUT_WINDOW_FONT)]
                if col + 1 < num_cols:
                    line += [VerticalSeparator(), Text(' ')]
                col += 1
            if col >= num_cols:
                layout.append(line)
                line = []
                col = 0
        if col != 0:
            layout.append(line)
        layout = [[Text(SYMBOLS.X, enable_events=True, key='-EXIT-', font='_ 7')], [Column(layout)]]

        Window._read_call_from_debugger = True
        self.popout_window = Window('Floating', layout, alpha_channel=0, no_titlebar=True, grab_anywhere=True,
                                    element_padding=(0, 0), margins=(0, 0), keep_on_top=True,
                                    right_click_menu=['&Right', ['Debugger::RightClick', 'Exit::RightClick']], location=location, finalize=True)
        Window._read_call_from_debugger = False

        if location == (None, None):
            screen_size = self.popout_window.get_screen_dimensions()
            self.popout_window.move(screen_size[0] - self.popout_window.size[0], 0)
        self.popout_window.set_alpha(1)
        theme(old_theme)
        return True


    def _refresh_floating_window(self):
        if not self.popout_window:
            return
        for key in self.popout_choices:
            if self.popout_choices[key] is True and key in self.locals:
                if key is not None and self.popout_window is not None:
                    self.popout_window.find_element(key, silent_on_error=True).update(self.locals.get(key))
        event, _ = self.popout_window.read(timeout=5)
        if event in (None, '_EXIT_', 'Exit::RightClick', '-EXIT-'):
            self.popout_window.close()
            self.popout_window = None
        elif event == 'Debugger::RightClick':
            show_debugger_window()


def show_debugger_window(location=(None, None), *args):
    """
    Shows the large main debugger window
    :param location: Locations (x,y) on the screen to place upper left corner of the window
    :type location:  (int, int)
    :return:         None
    :rtype:          None
    """
    if _Debugger.debugger is None:
        _Debugger.debugger = _Debugger()
    debugger = _Debugger.debugger
    frame = inspect.currentframe()
    # prev_frame = inspect.currentframe().f_back
    # frame, *others = inspect.stack()[1]
    try:
        debugger.locals = frame.f_back.f_locals
        debugger.globals = frame.f_back.f_globals
    finally:
        del frame

    if not debugger.watcher_window:
        debugger.watcher_window = debugger._build_main_debugger_window(location=location)
    return True


def show_debugger_popout_window(location=(None, None), *args):
    """
    Shows the smaller "popout" window.  Default location is the upper right corner of your screen

    :param location: Locations (x,y) on the screen to place upper left corner of the window
    :type location:  (int, int)
    :return:         None
    :rtype:          None
    """
    if _Debugger.debugger is None:
        _Debugger.debugger = _Debugger()
    debugger = _Debugger.debugger
    frame = inspect.currentframe()
    # prev_frame = inspect.currentframe().f_back
    # frame = inspect.getframeinfo(prev_frame)
    # frame, *others = inspect.stack()[1]
    try:
        debugger.locals = frame.f_back.f_locals
        debugger.globals = frame.f_back.f_globals
    finally:
        del frame
    if debugger.popout_window:
        debugger.popout_window.Close()
        debugger.popout_window = None
    debugger._build_floating_window(location=location)


def _refresh_debugger():
    """
    Refreshes the debugger windows. USERS should NOT be calling this function. Within PySimpleGUI it is called for the USER every time the Window.Read function is called.

    :return: return code False if user closed the main debugger window.
    :rtype:  (bool)
    """
    if _Debugger.debugger is None:
        _Debugger.debugger = _Debugger()
    debugger = _Debugger.debugger
    Window._read_call_from_debugger = True
    rc = None
    # frame = inspect.currentframe()
    # frame = inspect.currentframe().f_back

    frame, *_ = inspect.stack()[1]
    try:
        debugger.locals = frame.f_back.f_locals
        debugger.globals = frame.f_back.f_globals
    finally:
        del frame
    if debugger.popout_window:
        rc = debugger._refresh_floating_window()
    if debugger.watcher_window:
        rc = debugger._refresh_main_debugger_window(debugger.locals, debugger.globals)
    Window._read_call_from_debugger = False
    return rc


def _debugger_window_is_open():
    """
    Determines if one of the debugger window is currently open
    :return: returns True if the popout window or the main debug window is open
    :rtype: (bool)
    """

    if _Debugger.debugger is None:
        return False
    debugger = _Debugger.debugger
    return debugger.popout_window or debugger.watcher_window


# -------------------------  NO BUTTON Element lazy function  ------------------------- #
def Debug(button_text='', *, size=(None, None), auto_size_button=None, button_color=None, disabled=False, font=None,
          tooltip=None, bind_return_key=False, focus=False, pad=None, key=None, visible=True, metadata=None, expand_x=False, expand_y=False):
    """
    This Button has been changed in how it works!!
    Your button has been replaced with a normal button that has the PySimpleGUI Debugger buggon logo on it.
    In your event loop, you will need to check for the event of this button and then call:
            show_debugger_popout_window()
    :param button_text:      text in the button (Default value = '')
    :type button_text:       (str)
    :param size:             (w,h) w=characters-wide, h=rows-high
    :type size:              (int, int)
    :param auto_size_button: True if button size is determined by button text
    :type auto_size_button:  (bool)
    :param button_color:     button color (foreground, background)
    :type button_color:      (str, str) | str
    :param disabled:         set disable state for element (Default = False)
    :type disabled:          (bool)
    :param font:             specifies the  font family, size, etc. Tuple or Single string format 'name size styles'. Styles: italic * roman bold normal underline overstrike
    :type font:              (str or (str, int[, str]) or None)
    :param tooltip:          text, that will appear when mouse hovers over the element
    :type tooltip:           (str)
    :param bind_return_key:  (Default = False) If True, this button will appear to be clicked when return key is pressed in other elements such as Input and elements with return key options
    :type bind_return_key:   (bool)
    :param focus:            if focus should be set to this
    :type focus:
    :param pad:              Amount of padding to put around element in pixels (left/right, top/bottom) or ((left, right), (top, bottom)) or an int. If an int, then it's converted into a tuple (int, int)
    :type pad:               (int, int) or ((int, int),(int,int)) or (int,(int,int)) or  ((int, int),int) | int
    :param key:              key for uniquely identify this element (for window.find_element)
    :type key:               str | int | tuple | object
    :param visible:          set initial visibility state of the Button
    :type visible:           (bool)
    :param metadata:         Anything you want to store along with this button
    :type metadata:          (Any)
    :param expand_x:         If True Element will expand in the Horizontal directions
    :type expand_x:          (bool)
    :param expand_y:         If True Element will expand in the Vertical directions
    :type expand_y:          (bool)
    :return:                 returns a button
    :rtype:                  (Button)
    """
    user_key = key if key is not None else button_text

    return Button(button_text='', button_type=Button.TYPE.READ_FORM, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=theme_button_color(), font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=user_key, visible=visible, image_data=PSG_DEBUGGER_LOGO,
                  image_subsample=2, border_width=0, metadata=metadata, expand_x=expand_x, expand_y=expand_y)

PSG_DEBUGGER_LOGO = b'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'
