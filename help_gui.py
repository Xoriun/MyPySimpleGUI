
import inspect
import sys
import pydoc
import webbrowser
import itertools


from quick_tkinter import Window, Text, Column, Multiline, Checkbox, Button, MenubarCustom, Element, Titlebar, Sizegrip, Input, Menu
from quick_tkinter import WIN_CLOSED
from quick_tkinter import EMOJI_BASE64, popup_get_text, _error_popup_with_traceback
import quick_tkinter, psg_debugger, upgrade_gui, open_github_issue_gui, test_gui

_modules = (sys.modules[__name__], quick_tkinter, psg_debugger, upgrade_gui, open_github_issue_gui, test_gui)

def _all_subclasses(cls: type):
    return set(cls.__subclasses__()).union(
        (subsubcls for sub_cls in cls.__subclasses__() for subsubcls in _all_subclasses(sub_cls))
    )


def main_sdk_help():
    """
    Display a window that will display the docstrings for each PySimpleGUI Element and the Window object

    """
    online_help_links = {
        'Button': r'https://PySimpleGUI.org/en/latest/call%20reference/#button-element',
        'ButtonMenu': r'https://PySimpleGUI.org/en/latest/call%20reference/#buttonmenu-element',
        'Canvas': r'https://PySimpleGUI.org/en/latest/call%20reference/#canvas-element',
        'Checkbox': r'https://PySimpleGUI.org/en/latest/call%20reference/#checkbox-element',
        'Column': r'https://PySimpleGUI.org/en/latest/call%20reference/#column-element',
        'Combo': r'https://PySimpleGUI.org/en/latest/call%20reference/#combo-element',
        'Frame': r'https://PySimpleGUI.org/en/latest/call%20reference/#frame-element',
        'Graph': r'https://PySimpleGUI.org/en/latest/call%20reference/#graph-element',
        'HorizontalSeparator': r'https://PySimpleGUI.org/en/latest/call%20reference/#horizontalseparator-element',
        'Image': r'https://PySimpleGUI.org/en/latest/call%20reference/#image-element',
        'Input': r'https://PySimpleGUI.org/en/latest/call%20reference/#input-element',
        'Listbox': r'https://PySimpleGUI.org/en/latest/call%20reference/#listbox-element',
        'Menu': r'https://PySimpleGUI.org/en/latest/call%20reference/#menu-element',
        'MenubarCustom': r'https://PySimpleGUI.org/en/latest/call%20reference/#menubarcustom-element',
        'Multiline': r'https://PySimpleGUI.org/en/latest/call%20reference/#multiline-element',
        'OptionMenu': r'https://PySimpleGUI.org/en/latest/call%20reference/#optionmenu-element',
        'Output': r'https://PySimpleGUI.org/en/latest/call%20reference/#output-element',
        'Pane': r'https://PySimpleGUI.org/en/latest/call%20reference/#pane-element',
        'ProgressBar': r'https://PySimpleGUI.org/en/latest/call%20reference/#progressbar-element',
        'Radio': r'https://PySimpleGUI.org/en/latest/call%20reference/#radio-element',
        'Slider': r'https://PySimpleGUI.org/en/latest/call%20reference/#slider-element',
        'Spin': r'https://PySimpleGUI.org/en/latest/call%20reference/#spin-element',
        'StatusBar': r'https://PySimpleGUI.org/en/latest/call%20reference/#statusbar-element',
        'Tab': r'https://PySimpleGUI.org/en/latest/call%20reference/#tab-element',
        'TabGroup': r'https://PySimpleGUI.org/en/latest/call%20reference/#tabgroup-element',
        'Table': r'https://PySimpleGUI.org/en/latest/call%20reference/#table-element',
        'Text': r'https://PySimpleGUI.org/en/latest/call%20reference/#text-element',
        'Titlebar': r'https://PySimpleGUI.org/en/latest/call%20reference/#titlebar-element',
        'Tree': r'https://PySimpleGUI.org/en/latest/call%20reference/#tree-element',
        'VerticalSeparator': r'https://PySimpleGUI.org/en/latest/call%20reference/#verticalseparator-element',
        'Window': r'https://PySimpleGUI.org/en/latest/call%20reference/#window',
    }

    NOT_AN_ELEMENT = 'Not An Element'
    element_classes = list(_all_subclasses(Element))
    element_names = {element.__name__: element for element in element_classes if not element.__name__.startswith('_')}
    element_names['Window'] = Window
    element_classes.append(Window)
    element_arg_default_dict, element_arg_default_dict_update = {}, {}
    vars3 = list(itertools.chain(*(
        inspect.getmembers(module)
        for module in _modules
    )))

    functions = list(itertools.chain(*(
        inspect.getmembers(module, inspect.isfunction)
        for module in _modules
    )))
    functions_names_lower = [f for f in functions if f[0][0].islower()]
    functions_names_upper = [f for f in functions if f[0][0].isupper()]
    functions_names_rest = [f for f in functions if not (f[0][0].isupper() or f[0][0].islower())]
    functions_names = sorted(functions_names_lower) + sorted(functions_names_upper) + sorted(functions_names_rest)

    for element in element_classes:
        # Build info about init method
        specs = inspect.getfullargspec(element.__init__)
        args = specs.args[1:] + specs.kwonlyargs
        defaults = tuple(specs.kwonlydefaults[arg] for arg in specs.kwonlyargs if arg in specs.kwonlydefaults)
        if specs.defaults is not None:
            defaults = specs.defaults + defaults
        # print('------------- {element}----------')
        # print(args)
        # print(defaults)
        if len(args) != len(defaults):
            diff = len(args) - len(defaults)
            defaults = ('NO DEFAULT',) * diff + defaults
        args_defaults = []
        for i, a in enumerate(args):
            args_defaults.append((a, defaults[i]))
        element_arg_default_dict[element.__name__] = args_defaults

        # Build info about update method
        try:
            args = inspect.getfullargspec(element.update).args[1:]
            defaults = inspect.getfullargspec(element.update).defaults
            if args is None or defaults is None:
                element_arg_default_dict_update[element.__name__] = (('', ''),)
                continue
            if len(args) != len(defaults):
                diff = len(args) - len(defaults)
                defaults = ('NO DEFAULT',) * diff + defaults
            args_defaults = []
            for i, a in enumerate(args):
                args_defaults.append((a, defaults[i]))
            element_arg_default_dict_update[element.__name__] = args_defaults or (('', ''),)
        except Exception:
            pass

    # Add on the pseudo-elements
    element_names['MenubarCustom'] = MenubarCustom
    element_names['Titlebar'] = Titlebar

    buttons = [[Button(e, pad=(0, 0), size=(22, 1), font='Courier 10')] for e in sorted(element_names.keys())]
    buttons += [[Button('Func Search', pad=(0, 0), size=(22, 1), font='Courier 10')]]
    button_col = Column(buttons, vertical_alignment='t', scrollable=True, expand_y=True, vertical_scroll_only=True)
    mline_col = Column([[Multiline(size=(100, 46), key='-ML-', write_only=True, reroute_stdout=True, font='Courier 10', expand_x=True, expand_y=True)],
                        [Text(size=(80, 1), font='Courier 10 underline', key='-DOC LINK-', enable_events=True)]], pad=(0, 0), expand_x=True, expand_y=True, vertical_alignment='t')
    layout = [[button_col, mline_col]]
    layout += [[
        Checkbox('Summary Only', enable_events=True, key='-SUMMARY-'),
        Checkbox('Display Only PEP8 Functions', default_value=True, key='-PEP8-'),
        Text('Filter:', tooltip='Only show classes that caintain the given method.'),
        Input(size=20, key='filter', enable_events=True),
        Checkbox('exact match', key='filter_exact', default_value=True, enable_events=True),
        Button('Clear filter', key='filter_clear', enable_events=True)
    ]]
    # layout = [[Column(layout, scrollable=True, p=0, expand_x=True, expand_y=True, vertical_alignment='t'), Sizegrip()]]
    layout += [[Button('Exit', size=(15, 1)), Sizegrip()]]

    window = Window('SDK API Call Reference', layout=layout, resizable=True, use_default_focus=False, keep_on_top=True, icon=EMOJI_BASE64.THINK, finalize=True, right_click_menu=Menu.RIGHT_CLICK_EDITME_EXIT)
    window['-DOC LINK-'].set_cursor('hand1')
    online_help_link = ''
    ml = window['-ML-']
    current_element = ''
    try:
        while True:  # Event Loop
            event, values = window.read()
            if event in (WIN_CLOSED, 'Exit'):
                break
            if event == '-DOC LINK-':
                if online_help_link:
                    webbrowser.open_new_tab(online_help_link)
            if event == '-SUMMARY-':
                event = current_element

            if event in element_names:
                current_element = event
                window['-ML-'].update('')
                online_help_link = online_help_links.get(event, '')
                window['-DOC LINK-'].update(online_help_link)
                if not values['-SUMMARY-']:
                    elem = element_names[event]
                    ml.print(pydoc.help(elem))
                    # print the aliases for the class
                    ml.print('\n--- Shortcut Aliases for Class ---')
                    for v in vars3:
                        if elem == v[1] and elem.__name__ != v[0]:
                            print(v[0])
                    ml.print('\n--- Init Parms ---')
                else:
                    elem = element_names[event]
                    if inspect.isfunction(elem):
                        ml.print('Not a class...It is a function', background_color='red', text_color='white')
                    else:
                        element_methods = [m[0] for m in inspect.getmembers(Element, inspect.isfunction) if not m[0].startswith('_') and not m[0][0].isupper()]
                        methods = inspect.getmembers(elem, inspect.isfunction)
                        methods = [m[0] for m in methods if not m[0].startswith('_') and not m[0][0].isupper()]

                        unique_methods = [m for m in methods if m not in element_methods and not m[0][0].isupper()]

                        properties = inspect.getmembers(elem, lambda o: isinstance(o, property))
                        properties = [p[0] for p in properties if not p[0].startswith('_')]
                        ml.print('--- Methods ---', background_color='red', text_color='white')
                        ml.print('\n'.join(methods))
                        ml.print('--- Properties ---', background_color='red', text_color='white')
                        ml.print('\n'.join(properties))
                        if elem != NOT_AN_ELEMENT:
                            if issubclass(elem, Element):
                                ml.print('Methods Unique to This Element', background_color='red', text_color='white')
                                ml.print('\n'.join(unique_methods))
                        ml.print('========== Init Parms ==========', background_color='#FFFF00', text_color='black')
                        elem_text_name = event
                        for parm, default in element_arg_default_dict[elem_text_name]:
                            ml.print(f"{parm:18}", end=' = ')
                            ml.print(default, end=',\n')
                        if elem_text_name in element_arg_default_dict_update:
                            ml.print('========== Update Parms ==========', background_color='#FFFF00', text_color='black')
                            for parm, default in element_arg_default_dict_update[elem_text_name]:
                                ml.print(f"{parm:18}", end=' = ')
                                ml.print(default, end=',\n')
                ml.set_vscroll_position(0)  # scroll to top of multoline
            elif event == 'Func Search':
                search_string = popup_get_text('Search for this in function list:', keep_on_top=True)
                if search_string is not None:
                    online_help_link = ''
                    window['-DOC LINK-'].update('')
                    ml.update('')
                    for f_entry in functions_names:
                        f = f_entry[0]
                        if search_string in f.lower() and not f.startswith('_'):
                            if (values['-PEP8-'] and not f[0].isupper()) or not values['-PEP8-']:
                                if values['-SUMMARY-']:
                                    ml.print(f)
                                else:
                                    ml.print('=========== ' + f + '===========', background_color='#FFFF00', text_color='black')
                                    ml.print(pydoc.help(f_entry[1]))
                ml.set_vscroll_position(0)  # scroll to top of multoline
            elif 'filter' in event:
                if event == 'filter_clear':
                    window['filter'].update('')
                show_all = not values['filter'] or event == 'filter_clear'
                for button, in buttons[:-1]:
                    if show_all:
                        button.update_visible(visible=True)
                        continue

                    # get actual class of button and skip if a function
                    button_cls = element_names[button.key]
                    if not isinstance(button_cls, type):
                        button.update_visible(visible=False)
                        continue

                    # get member that are not inherited
                    members = (
                        mem[0]
                        for mem in inspect.getmembers(button_cls)
                        if not any(getattr(button_cls, mem[0]) == getattr(i, mem[0], None) for i in button_cls.mro()[1:])
                    )

                    # filter
                    if values['filter_exact']:
                        button.update_visible(visible = show_all or values['filter'] in members)
                    else:
                        visible = False
                        for attr_name in members:
                            if values['filter'] in attr_name and not attr_name.startswith('_'):
                                visible = True
                                break
                        button.update_visible(visible=visible)

    except Exception as e:
        _error_popup_with_traceback('Exception in SDK reference', e)
        raise
    window.close()