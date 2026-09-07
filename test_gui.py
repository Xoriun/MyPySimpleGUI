
import tkinter as tk
from tkinter import ttk
import random
import webbrowser
import json
import os
import sys
import copy

from quick_tkinter import Window, Text, Spin, Column, Combo, Tab, TabGroup, Frame, Multiline, Input, Listbox, Checkbox, Radio, Button, ButtonMenu, Menu, MenubarCustom, ProgressBar, Image, Graph, VerticalPush, Tree, TreeData, Table, Slider, pin, HorizontalSeparator, Push, OptionMenu, typed
from quick_tkinter import DEFAULT_MODAL_WINDOWS_FORCED, TIMEOUT_KEY, WIN_CLOSED, WINDOW_CLOSE_ATTEMPTED_EVENT, SYMBOLS, DEFAULTS, RELIEFS, DEFAULT_TTK_PART_MAPPING_DICT
from quick_tkinter import TTK_SCROLLBAR_PART_LIST, TTK_SCROLLBAR_PART_THEME_BASED_LIST, PSG_THEME_PART_LIST, TTK_SCROLLBAR_PART_ARROW_WIDTH, TTK_SCROLLBAR_PART_SCROLL_WIDTH, TTK_SCROLLBAR_PART_RELIEF
from quick_tkinter import DEFAULT_BASE64_LOADING_GIF, DEFAULT_BASE64_ICON, EMOJI_BASE64, UDEMY_ICON, PYTHON_COLORED_HEARTS_BASE64, HEART_3D_BASE64, ICON_BUY_ME_A_COFFEE
from quick_tkinter import set_options, FileBrowse, FolderBrowse
from quick_tkinter import popup, popup_scrolled, popup_get_file, popup_get_folder, popup_get_date, popup_get_text, popup_non_blocking, popup_auto_close, popup_no_titlebar, popup_quick_message, popup_ok, popup_cancel, popup_ok_cancel, popup_yes_no, popup_error
from quick_tkinter import theme_background_color, theme, theme_use_custom_titlebar, theme_text_color, OFFICIAL_PYSIMPLEGUI_THEME, _theme_preview_window_swatches, list_of_look_and_feel_values, theme_list, theme_button_color, _change_ttk_theme
from quick_tkinter import ver, version, pysimplegui_user_settings, get_versions
from quick_tkinter import running_trinket, execute_editor, vtop
from quick_tkinter import clipboard_set, ttk_part_mapping_dict
from quick_tkinter import Print, tkinter_keysyms, main_mac_feature_control, _global_settings_get_watermark_info, _global_settings_get_ttk_scrollbar_info, _read_mac_global_settings
import help_gui
import upgrade_gui
import open_github_issue_gui
import psg_debugger


upgrade_gui.__perform_upgrade_check()

def main():
    """
    The PySimpleGUI "Test Harness".  This is meant to be a super-quick test of the Elements.
    """
    forced_modal = DEFAULT_MODAL_WINDOWS_FORCED
    # set_options(force_modal_windows=True)
    window = _create_main_window()
    set_options(keep_on_top=True)
    graph_elem = window['+GRAPH+']
    i = 0
    graph_figures = []
    # Don't use the debug window
    # Print('', location=(0, 0), font='Courier 10', size=(100, 20), grab_anywhere=True)
    # print(window.element_list())
    while True:  # Event Loop
        event, values = window.read(timeout=5)
        if event != TIMEOUT_KEY:
            print(event, values)
            # Print(event, text_color='white', background_color='red', end='')
            # Print(values)
        if event in {WIN_CLOSED, WINDOW_CLOSE_ATTEMPTED_EVENT, 'Exit'} or (event == '-BMENU-' and values['-BMENU-'] == 'Exit'):
            break
        if i < graph_elem.CanvasSize[0]:
            x = i % graph_elem.CanvasSize[0]
            fig = graph_elem.draw_line((x, 0), (x, random.randint(0, graph_elem.CanvasSize[1])), width=1, color=f"#{random.randint(0, 0xffffff):06x}")
            graph_figures.append(fig)
        else:
            x = graph_elem.CanvasSize[0]
            graph_elem.move(-1, 0)
            fig = graph_elem.draw_line((x, 0), (x, random.randint(0, graph_elem.CanvasSize[1])), width=1, color=f"#{random.randint(0, 0xffffff):06x}")
            graph_figures.append(fig)
            graph_elem.delete_figure(graph_figures[0])
            del graph_figures[0]
        window[typed('+PROGRESS+', ProgressBar)].update(i % 800)
        window.find_element('-IMAGE-').update_animation(DEFAULT_BASE64_LOADING_GIF, time_between_frames=50)
        if event == 'Button':
            window.find_element('-TEXT1-').set_tooltip('NEW TEXT')
            window.find_element('-MENU-').update(visible=True)
        elif event == 'Popout':
            psg_debugger.show_debugger_popout_window()
        elif event == 'Launch Debugger':
            psg_debugger.show_debugger_window()
        elif event == 'About...':
            popup('About this program...', 'You are looking at the test harness for the PySimpleGUI program', version, keep_on_top=True, image=DEFAULT_BASE64_ICON)
        elif event.startswith('See'):
            window._see_through = not window._see_through
            window.set_transparent_color(theme_background_color() if window._see_through else '')
        elif event in ('-INSTALL-', '-UPGRADE FROM GITHUB-'):
            upgrade_gui._upgrade_gui()
        elif event == 'Popup':
            popup('This is your basic popup', keep_on_top=True)
        elif event == 'Get File':
            popup_scrolled('Returned:', popup_get_file('Get File', keep_on_top=True))
        elif event == 'Get Folder':
            popup_scrolled('Returned:', popup_get_folder('Get Folder', keep_on_top=True))
        elif event == 'Get Date':
            popup_scrolled('Returned:', popup_get_date(keep_on_top=True))
        elif event == 'Get Text':
            popup_scrolled('Returned:', popup_get_text('Enter some text', keep_on_top=True))
        elif event.startswith('-UDEMY-'):
                webbrowser.open_new_tab(r'https://www.udemy.com/course/pysimplegui/?couponCode=62A4C02AB0A3DAB34388')
        elif event.startswith('-SPONSOR-'):
            webbrowser.open_new_tab(r'https://www.paypal.me/pythongui')
        elif event == '-COFFEE-':
            webbrowser.open_new_tab(r'https://www.buymeacoffee.com/PySimpleGUI')
        elif event in  ('-EMOJI-HEARTS-', '-HEART-', '-PYTHON HEARTS-'):
            popup_scrolled("Oh look!  It's a Udemy discount coupon!", '62A4C02AB0A3DAB34388',
                           'A personal message from Mike -- thank you so very much for supporting PySimpleGUI!', title='Udemy Coupon', image=EMOJI_BASE64.MIKE, keep_on_top=True)
        elif event == 'Themes':
            search_string = popup_get_text('Enter a search term or leave blank for all themes', 'Show Available Themes', keep_on_top=True)
            if search_string is not None:
                theme_previewer(search_string=search_string)
        elif event == 'Theme Swatches':
            theme_previewer_swatches()
        elif event == 'Switch Themes':
            window.close()
            _main_switch_theme()
            window = _create_main_window()
            graph_elem = window['+GRAPH+']
        elif event == '-HIDE TABS-':
            window['-TAB GROUP COL-'].update(visible=window['-TAB GROUP COL-'].metadata is True)
            window['-TAB GROUP COL-'].metadata = not window['-TAB GROUP COL-'].metadata
            window['-HIDE TABS-'].update(text=SYMBOLS.UP if window['-TAB GROUP COL-'].metadata else SYMBOLS.DOWN)
        elif event == 'SDK Reference':
            help_gui.main_sdk_help()
        elif event == 'Global Settings':
            if main_global_pysimplegui_settings():
                theme(pysimplegui_user_settings.get('-theme-', OFFICIAL_PYSIMPLEGUI_THEME))
                window.close()
                window = _create_main_window()
                graph_elem = window['+GRAPH+']
            else:
                Window('', layout=[[Multiline()]], alpha_channel=0).read(timeout=1, close=True)
        elif event.startswith('P '):
            if event == 'P ':
                popup('Normal Popup - Modal', keep_on_top=True)
                # popup('this', 'is', 'a', 'popup', 'with', 'a', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'large', 'amount', 'of', 'lines', '!!!')
            elif event == 'P Scrolled':
                popup_scrolled('this', 'is', 'a', 'popup', 'with', 'a', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'very', 'large', 'amont', 'of', 'lines', '!!!')
            elif event == 'P NoTitle':
                popup_no_titlebar('No titlebar', keep_on_top=True)
            elif event == 'P NoModal':
                set_options(force_modal_windows=False)
                popup('Normal Popup - Not Modal', 'You can interact with main window menubar ',
                      'but will have no effect immediately', 'button clicks will happen after you close this popup', modal=False, keep_on_top=True)
                set_options(force_modal_windows=forced_modal)
            elif event == 'P NoBlock':
                popup_non_blocking('Non-blocking', 'The background window should still be running', keep_on_top=True)
            elif event == 'P AutoClose':
                popup_auto_close('Will autoclose in 3 seconds', auto_close_duration=3, keep_on_top=True)
            elif event == 'P ok':
                popup_ok('Popup with OK button', keep_on_top=True)
            elif event == 'P cancel':
                popup_cancel('Popup with Cancel button', keep_on_top=True)
            elif event == 'P ok cancel':
                popup_ok_cancel('Popup with OK Cancel buttons', keep_on_top=True)
            elif event == 'P yes no':
                popup_yes_no('Popup with Yes No buttons', keep_on_top=True)
            elif event == 'P error':
                popup_error('Popup with Error button', keep_on_top=True)
            elif event == 'P custom':
                buttons = popup_get_text("Enter the text of the buttons, seperated by ','")
                popup('Popup with custom buttons', button_text=[button.strip() for button in buttons.split(',')])
        elif event == 'Versions for GitHub':
            main_get_debug_data()
        elif event == 'Edit Me':
            execute_editor(__file__)
        elif event == 'Open GitHub Issue':
            window.minimize()
            open_github_issue_gui.main_open_github_issue()
            window.normal()
        elif event == 'Show Notification Again':
            if not running_trinket:
                pysimplegui_user_settings.set('-upgrade info seen-', value=False)
            upgrade_gui.__show_previous_upgrade_information()
        elif event == '-UPGRADE SHOW ONLY CRITICAL-':
            if not running_trinket:
                pysimplegui_user_settings.set('-upgrade show only critical-', values['-UPGRADE SHOW ONLY CRITICAL-'])


        i += 1
        # _refresh_debugger()
    print('event = ', event)
    window.close()
    set_options(force_modal_windows=forced_modal)

def _create_main_window():
    """
    Creates the main test harness window.

    :return: The test window
    :rtype:  Window
    """

    # theme('dark blue 3')
    # theme('dark brown 2')
    # theme('dark')
    # theme('dark red')
    # theme('Light Green 6')
    # theme('Dark Grey 8')

    tkversion = tk.TkVersion
    tclversion = tk.TclVersion
    tclversion_detailed = tk.Tcl().eval('info patchlevel')

    print('Starting up PySimpleGUI Diagnostic & Help System')
    print('PySimpleGUI long version = ', version)
    print('PySimpleGUI Version ', ver, '\ntcl ver = ', tclversion, 'tkinter version = ', tkversion, '\nPython Version ', sys.version)
    print('tcl detailed version = ', tclversion_detailed)
    print('PySimpleGUI.py location', __file__)
    # ------ Menu Definition ------ #
    menu_def = [['&File', ['!&Open', '&Save::savekey', '---', '&Properties', 'E&xit']],
                ['&Edit', ['&Paste', ['Special', 'Normal', '!Disabled'], 'Undo'] ],
                ['&Debugger', ['Popout', 'Launch Debugger']],
                ['!&Disabled', ['Popout', 'Launch Debugger']],
                ['&Toolbar', ['Command &1', 'Command &2', 'Command &3', 'Command &4']],
                ['&Help', '&About...'] ]

    button_menu_def = ['unused', ['&Paste', ['Special', 'Normal', '!Disabled'], 'Undo', 'Exit'] ]
    treedata = TreeData()

    treedata.Insert("", '_A_', 'Tree Item 1', [1, 2, 3] )
    treedata.Insert("", '_B_', 'B', [4, 5, 6] )
    treedata.Insert("_A_", '_A1_', 'Sub Item 1', ['can', 'be', 'anything'] )
    treedata.Insert("", '_C_', 'C', [] )
    treedata.Insert("_C_", '_C1_', 'C1', ['or'] )
    treedata.Insert("_A_", '_A2_', 'Sub Item 2', [None, None])
    treedata.Insert("_A1_", '_A3_', 'A30', ['getting deep'])
    treedata.Insert("_C_", '_C2_', 'C2', ['nothing', 'at', 'all'])

    for i in range(100):
        treedata.Insert('_C_', i, i, [])

    frame1 = [
        [Input('Input Text', size=(25, 1)) ],
        [Multiline(size=(30, 5), default_value='Multiline Input', key='MulitLIne+!+!+')],
    ]

    frame2 = [
        # [ProgressBar(100, bar_color=('red', 'green'), orientation='h')],

        [Listbox([f'Listbox {i}' for i in range(1, 10)], select_mode=Listbox.SELECT_MODE_EXTENDED, size=(20, 5)),
         Spin([1, 2, 3, 'a', 'b', 'c'], default_value='a', size=(4, 3), wrap=True)],
        [Combo([f"Combo item {i}" for i in range(5)], size=(20, 3), default_value='Combo item 2', key='-COMBO1-' )],
        [Combo([f"Combo item {i}" for i in range(5)], size=(20, 3), font='Courier 14', default_value='Combo item 2', key='-COMBO2-' )],
        [OptionMenu([f"Option {i}" for i in range(7)], default_value='Option 2', key='-OPTIONMENU-', enable_events=False)],

    ]

    frame3 = [
        [Checkbox('Checkbox1', default_value=True, key='-CB1-'), Checkbox('Checkbox2', key='-CB2-', enable_events=True)],
        [Radio('Radio Button1', 1, key='-R1-'), Radio('Radio Button2', 1, default_value=True, key='-R2-', tooltip='Radio 2')],
        [Text('', size=(1, 4))]
    ]

    frame4 = [
        [Slider(range=(0, 100), orientation='v', size=(7, 15), default_value=40, key='-SLIDER1-'),
         Slider(range=(0, 100), orientation='h', size=(11, 15), default_value=40, key='-SLIDER2-') ]
    ]
    matrix = [[str(x * y) for x in range(1, 5)] for y in range(1, 8)]

    frame5 = [vtop([
        Table(values=matrix, headings=matrix[0],
              auto_size_columns=False, display_row_numbers=True, enable_events=False, justification='right',  header_border_width=4,
              # header_relief=RELIEF_GROOVE,
              num_rows=10, alternating_row_color='lightblue', key='-TABLE-',
              col_widths=[5, 5, 5, 5]),
        Tree(data=treedata, headings=['col1', 'col2', 'col3'], col_widths=[5, 5, 5, 5], enable_events=True, auto_size_columns=False, header_border_width=4,
             # header_relief=RELIEF_GROOVE,
             num_rows=8, col0_width=8, key='-TREE-', show_expanded=True )])]
    frame7 = [[Image(data=EMOJI_BASE64.HAPPY_HEARTS, enable_events=True, key='-EMOJI-HEARTS-'), Text('Do you'), Image(data=HEART_3D_BASE64, subsample=3, enable_events=True, key='-HEART-'), Text('so far?')],
              [Text('Want to be taught PySimpleGUI?\nThen maybe the "Official PySimpleGUI Course" on Udemy is for you.')],
              [Button(image_data=UDEMY_ICON, enable_events=True, key='-UDEMY-'),Text('Check docs, announcements, easter eggs on this page for coupons.')],
              [Button(image_data=ICON_BUY_ME_A_COFFEE, enable_events=True, key='-COFFEE-'), Text('It is financially draining to operate a project this huge. $1 helps')]]


    pop_test_tab_layout = [
        [Image(data=EMOJI_BASE64.HAPPY_IDEA), Text('Popup tests? Good idea!', col_span=3)],
        [Button('Popup', key='P '), Button('Scrolled', key='P Scrolled'), Button('No Titlebar', key='P NoTitle'), Button('Not Modal', key='P NoModal'), Button('Non Blocking', key='P NoBlock'), Button('Auto Close', key='P AutoClose')],
        [Text('Button Popups')],
        [Button('OK', key='P ok'), Button('Cancel', key='P cancel'), Button('OK Cancel', key='P ok cancel'), Button('Yes No', key='P yes no'), Button('Error', key='P error'), Button('Custom', key='P custom')],
        [Text('"Get" popups too!', col_span=5)],
        [Button('Get File'), Button('Get Folder'), Button('Get Date'), Button('Get Text')]
    ]
    pop_test_tab_layout = [[Frame(title='test', layout=pop_test_tab_layout)]]

    GRAPH_SIZE=(500, 200)
    graph_elem = Graph(canvas_size=GRAPH_SIZE, graph_bottom_left=(0, 0), graph_top_right=GRAPH_SIZE, key='+GRAPH+')

    frame6 = [[VerticalPush()],[graph_elem]]

    themes_tab_layout = [[Text('You can see a preview of the themes, the color swatches, or switch themes for this window')],
                         [Text('If you want to change the default theme for PySimpleGUI, use the Global Settings')],
                         [Button('Themes'), Button('Theme Swatches'), Button('Switch Themes')]]


    upgrade_recommendation_tab_layout = [[Text('Latest Recommendation and Announcements For You', font='_ 14')],
                                         [Text('Severity Level of Update:'), Text(pysimplegui_user_settings.get('-severity level-',''))],
                                         [Text('Recommended Version To Upgrade To:'), Text(pysimplegui_user_settings.get('-upgrade recommendation-',''))],
                                         [Text(pysimplegui_user_settings.get('-upgrade message 1-',''))],
                                         [Text(pysimplegui_user_settings.get('-upgrade message 2-',''))],
                                         [Checkbox('Show Only Critical Messages', default_value=pysimplegui_user_settings.get('-upgrade show only critical-', False), key='-UPGRADE SHOW ONLY CRITICAL-', enable_events=True)],
                                         [Button('Show Notification Again'),
],
                                         ]
    tab_upgrade = Tab('Upgrade\n', upgrade_recommendation_tab_layout,  expand_x=True)


    tab1 = Tab('Graph\n', frame6, tooltip='Graph is in here', title_color='red')
    tab2 = Tab('CB, Radio\nList, Combo',
               [[Frame('Multiple Choice Group', frame2, title_color='#FFFFFF', tooltip='Checkboxes, radio buttons, etc', vertical_alignment='t'),
                 Frame('Binary Choice Group', frame3, title_color='#FFFFFF', tooltip='Binary Choice', vertical_alignment='t' ) ]])
    # tab3 = Tab('Table and Tree', [[Frame('Structured Data Group', frame5, title_color='red', element_justification='l')]], tooltip='tab 3', title_color='red', )
    tab3 = Tab('Table &\nTree', [[Column(frame5, element_justification='l', vertical_alignment='t')]], tooltip='tab 3', title_color='red', key='-TAB TABLE-')
    tab4 = Tab('Sliders\n', [[Frame('Variable Choice Group', frame4, title_color='blue')]], tooltip='tab 4', title_color='red', key='-TAB VAR-')
    tab5 = Tab('Input\nMultiline', [[Frame('TextInput', frame1, title_color='blue')]], tooltip='tab 5', title_color='red', key='-TAB TEXT-')
    tab6 = Tab('Course or\nSponsor', frame7, key='-TAB SPONSOR-')
    tab7 = Tab('Popups\n', pop_test_tab_layout, key='-TAB POPUP-')
    tab8 = Tab('Themes\n', themes_tab_layout, key='-TAB THEMES-')
    tab9 = Tab('Images\n', [[Image(data=EMOJI_BASE64.HAPPY_IDEA, zoom=2)]], key='-TAB IMAGE-', image_source=EMOJI_BASE64.HAPPY_IDEA, image_subsample=2)

    def VerLine(version, description, justification='r', size=(40, 1)):
        return [Text(version, justification=justification, font='Any 12', text_color='yellow', size=size, pad=(0,0)), Text(description, font='Any 12', pad=(0,0))]

    layout_top = Column(
    [
        [
            Image(data=EMOJI_BASE64.HAPPY_BIG_SMILE, enable_events=True, key='-LOGO-', tooltip='This is PySimpleGUI logo'),
            Image(data=DEFAULT_BASE64_LOADING_GIF, enable_events=True, key='-IMAGE-'),
            Text('PySimpleGUI Test Harness', font='ANY 14', tooltip='My tooltip', key='-TEXT1-')
        ],
        [
            *VerLine(ver, 'PySimpleGUI Version'),
            Image(data=HEART_3D_BASE64, subsample=4)
        ],
        # VerLine('{}/{}'.format(tkversion, tclversion), 'TK/TCL Versions'),
        VerLine(tclversion_detailed, 'detailed tkinter version'),
        VerLine(os.path.dirname(os.path.abspath(__file__)), 'PySimpleGUI Location', size=(40, None)),
        VerLine(sys.executable, 'Python Executable'),
        [
            *VerLine(sys.version, 'Python Version', size=(40,2)),
            Image(data=PYTHON_COLORED_HEARTS_BASE64, subsample=3, key='-PYTHON HEARTS-', enable_events=True)
        ]
    ], pad=0)

    layout_bottom = [
        [Button(SYMBOLS.DOWN, pad=(0, 0), key='-HIDE TABS-'),
         pin(Column(layout=[[TabGroup(layout=[[tab1, tab2, tab3, tab6, tab4, tab5, tab7, tab8, tab9, tab_upgrade]], key='-TAB_GROUP-')]], key='-TAB GROUP COL-'))],
        [Button('Button', highlight_colors=('yellow', 'red'),pad=(1, 0)),
         Button('ttk Button', use_ttk_buttons=True, tooltip='This is a TTK Button',pad=(1, 0)),
         Button('See-through Mode', tooltip='Make the background transparent',pad=(1, 0)),
         Button('Upgrade PySimpleGUI from GitHub', button_color='white on red', key='-INSTALL-',pad=(1, 0)),
         Button('Global Settings', tooltip='Settings across all PySimpleGUI programs',pad=(1, 0)),
         Button('Exit', tooltip='Exit button',pad=(1, 0))],
        # [B(image_data=ICON_BUY_ME_A_COFFEE,pad=(1, 0), key='-COFFEE-'),
        [Button(image_data=UDEMY_ICON,pad=(1, 0), key='-UDEMY-'),
         Button('SDK Reference', pad=(1, 0)), Button('Open GitHub Issue',pad=(1, 0)), Button('Versions for GitHub',pad=(1, 0)),
         ButtonMenu('ButtonMenu', button_menu_def, pad=(1, 0),key='-BMENU-', tearoff=True,  disabled_text_color='yellow')
         ]]

    layout = [[]]

    if not theme_use_custom_titlebar():
        layout += [[Menu(menu_def, key='-MENU-', font='Courier 15', background_color='red', text_color='white', disabled_text_color='yellow', tearoff=True)]]
    else:
        layout += [[MenubarCustom(menu_def, key='-MENU-', font='Courier 15', bar_background_color=theme_background_color(), bar_text_color=theme_text_color(),
                                  background_color='red', text_color='white', disabled_text_color='yellow')]]

    layout += [[layout_top, ProgressBar(max_value=800, size=(20, 25), orientation='v', key='+PROGRESS+')]]
    layout += layout_bottom

    window = Window('PySimpleGUI Main Test Harness', layout, #layout_type=Window.GRID,
                    # font=('Helvetica', 18),
                    # background_color='black',
                    right_click_menu=['&Right', ['Right', 'Edit Me', '!&Click', '&Menu', 'E&xit', 'Properties']],
                    # transparent_color= '#9FB8AD',
                    resizable=True,
                    keep_on_top=False,
                    element_justification='left',  # justify contents to the left
                    metadata='My window metadata',
                    finalize=True,
                    # grab_anywhere=True,
                    enable_close_attempted_event=True,
                    modal=False,
                    # ttk_theme=THEME_CLASSIC,
                    # scaling=2,
                    # icon=PSG_DEBUGGER_LOGO,
                    # icon=PSGDebugLogo,
                    )
    # window['-SPONSOR-'].set_cursor(cursor='hand2')
    window._see_through = False
    return window

def theme_previewer_swatches():
    """
    Display themes in a window as color swatches.
    Click on a color swatch to see the hex value printed on the console.
    If you hover over a color or right click it you'll also see the hext value.
    """
    current_theme = theme()
    popup_quick_message('This is going to take a minute...', text_color='white', background_color='red', font='Default 20', keep_on_top=True)
    window = _theme_preview_window_swatches()
    theme(OFFICIAL_PYSIMPLEGUI_THEME)
    # col_height = window.get_screen_size()[1]-200
    # if window.size[1] > 100:
    #     window.size = (window.size[0], col_height)
    # window.move(window.get_screen_size()[0] // 2 - window.size[0] // 2, 0)

    while True:  # Event Loop
        event, _ = window.read()
        if event in {WIN_CLOSED, 'Exit'}:
            break
        if isinstance(event, tuple):  # someone clicked a swatch
            chosen_color = event[1]
        else:
            chosen_color = event if event[0] == '#' else ''  # someone right clicked
        print('Copied to clipboard color = ', chosen_color)
        clipboard_set(chosen_color)
        # window.TKroot.clipboard_clear()
        # window.TKroot.clipboard_append(chosen_color)
    window.close()
    theme(current_theme)

def theme_previewer(*, columns=12, scrollable=False, scroll_area_size=(None, None), search_string=None, location=(None, None)):
    """
    Displays a "Quick Reference Window" showing all of the different Look and Feel settings that are available.
    They are sorted alphabetically.  The legacy color names are mixed in, but otherwise they are sorted into Dark and Light halves

    :param columns:          The number of themes to display per row
    :type columns:           int
    :param scrollable:       If True then scrollbars will be added
    :type scrollable:        bool
    :param scroll_area_size: Size of the scrollable area (The Column Element used to make scrollable)
    :type scroll_area_size:  (int, int)
    :param search_string:    If specified then only themes containing this string will be shown
    :type search_string:     str
    :param location:         Location on the screen to place the window. Defaults to the center like all windows
    :type location:          (int, int)
    """

    current_theme = theme()

    # Show a "splash" type message so the user doesn't give up waiting
    popup_quick_message('Hang on for a moment, this will take a bit to create....', keep_on_top=True, background_color='red', text_color='#FFFFFF',
                        auto_close=True, non_blocking=True)

    web = False

    win_bg = 'black'

    def sample_layout():
        return [[Text('Text element'), Input('Input data here', size=(10, 1))],
                [Button('Ok'), Button('Disabled', disabled=True), Slider((1, 10), orientation='h', size=(5, 15))]]

    names = list_of_look_and_feel_values()
    names.sort()
    if search_string not in (None, ''):
        names = [name for name in names if search_string.lower().replace(" ", "") in name.lower().replace(" ", "")]

    if search_string not in (None, ''):
        layout = [[Text(f"Themes containing '{search_string}'", font='Default 18', background_color=win_bg)]]
    else:
        layout = [[Text('List of all themes', font='Default 18', background_color=win_bg)]]

    col_layout = []
    row = []
    for count, theme_name in enumerate(names):
        theme(theme_name)
        if not count % columns:
            col_layout += [row]
            row = []
        row += [Frame(theme_name, sample_layout() if not web else [[Text(theme_name)], *sample_layout()], pad=(2, 2))]
    if row:
        col_layout += [row]

    layout += [[Column(col_layout, scrollable=scrollable, size=scroll_area_size, pad=(0, 0), background_color=win_bg, key='-COL-')]]
    window = Window('Preview of Themes', layout, background_color=win_bg, resizable=True, location=location, keep_on_top=True, finalize=True, modal=True)
    window['-COL-'].expand(expand_x=True, expand_y=True, expand_row=True)  # needed so that col will expand with the window
    window.read(close=True)
    theme(current_theme)

def _main_switch_theme():
    layout = [
        [Text('Click a look and feel color to see demo window')],
        [Listbox(values=theme_list(),
                 size=(20, 20), key='-LIST-')],
        [Button('Choose'), Button('Cancel')]]

    window = Window('Change Themes', layout)

    event, values = window.read(close=True)

    if event == 'Choose':
        theme_name = values['-LIST-'][0]
        theme(theme_name)

def main_global_pysimplegui_settings():
    """
    Window to set settings that will be used across all PySimpleGUI programs that choose to use them.
    Use set_options to set the path to the folder for all PySimpleGUI settings.

    :return: True if settings were changed
    :rtype:  (bool)
    """
    global DEFAULT_WINDOW_SNAPSHOT_KEY_CODE, ttk_part_mapping_dict, DEFAULT_TTK_THEME

    key_choices = tuple(sorted(tkinter_keysyms))

    settings = pysimplegui_user_settings.read()

    editor_format_dict = {
        'pycharm': '<editor> --line <line> <file>',
        'notepad++': '<editor> -n<line> <file>',
        'sublime': '<editor> <file>:<line>',
        'vim': '<editor> +<line> <file>',
        'wing': '<editor> <file>:<line>',
        'visual studio': '<editor> <file> /command "edit.goto <line>"',
        'atom': '<editor> <file>:<line>',
        'spyder': '<editor> <file>',
        'thonny': '<editor> <file>',
        'pydev': '<editor> <file>:<line>',
        'idle': '<editor> <file>'}

    tooltip = (
        "Format strings for some popular editors/IDEs:\n"
        "PyCharm - <editor> --line <line> <file>\n"
        "Notepad++ - <editor> -n<line> <file>\n"
        "Sublime - <editor> <file>:<line>\n"
        "vim -  <editor> +<line> <file>\n"
        "wing - <editor> <file>:<line>\n"
        "Visual Studio - <editor> <file> /command \"edit.goto <line>\"\n"
        "Atom - <editor> <file>:<line>\n"
        "Spyder - <editor> <file>\n"
        "Thonny - <editor> <file>\n"
        "PyDev - <editor> <file>:<line>\n"
        "IDLE - <editor> <file>\n"
    )

    tooltip_file_explorer = "This is the program you normally use to 'Browse' for files\n'For Windows this is normally 'explorer'. On Linux 'nemo' is sometimes used."

    tooltip_theme = (
        "The normal default theme for PySimpleGUI is 'Dark Blue 13'\n"
        "If you do not call theme('theme name') by your program to change the theme, then the default is used.\n"
        "This setting allows you to set the theme that PySimpleGUI will use for ALL of your programs that\n"
        "do not set a theme specifically."
    )

    # ------------------------- TTK Tab -------------------------
    ttk_scrollbar_tab_layout = [[Text('Default TTK Theme', font='_ 16'), Combo([], default_value=DEFAULTS.TTK_THEME, readonly=True, size=(20, 10), key='-TTK THEME-', font='_ 16')],
                                [HorizontalSeparator()],
                                [Text('TTK Scrollbar Settings', font='_ 16')]]

    t_len = max([len(l) for l in TTK_SCROLLBAR_PART_LIST])
    ttk_layout = [[]]
    for key, item in ttk_part_mapping_dict.items():
        if key in TTK_SCROLLBAR_PART_THEME_BASED_LIST:
            ttk_layout += [[Text(key, size=t_len, justification='r'), Combo(PSG_THEME_PART_LIST, default_value=settings.get(('-ttk scroll-', key), item), key=('-TTK SCROLL-', key))]]
        elif key in (TTK_SCROLLBAR_PART_ARROW_WIDTH, TTK_SCROLLBAR_PART_SCROLL_WIDTH):
            ttk_layout += [[Text(key, size=t_len, justification='r'), Combo(list(range(100)), default_value=settings.get(('-ttk scroll-', key), item), key=('-TTK SCROLL-', key))]]
        elif key == TTK_SCROLLBAR_PART_RELIEF:
            ttk_layout += [[Text(key, size=t_len, justification='r'), Combo(list(RELIEFS.values()), default_value=settings.get(('-ttk scroll-', key), item), readonly=True, key=('-TTK SCROLL-', key))]]

    ttk_scrollbar_tab_layout += ttk_layout
    ttk_scrollbar_tab_layout += [[Button('Reset Scrollbar Settings'), Button('Test Scrollbar Settings')]]
    ttk_tab = Tab('TTK', ttk_scrollbar_tab_layout)

    layout = [[Text('Global PySimpleGUI Settings', text_color=theme_button_color()[0], background_color=theme_button_color()[1],font='_ 18', expand_x=True, justification='c')]]

    # ------------------------- Interpreter Tab -------------------------


    interpreter_tab = Tab('Python Interpreter',
              [[Text('Normally leave this blank')],
                [Text('Command to run a python program:'), Input(settings.get('-python command-', ''), key='-PYTHON COMMAND-', enable_events=True), FileBrowse()]], font='_ 16', expand_x=True)

    # ------------------------- Editor Tab -------------------------

    editor_tab = Tab('Editor Settings',
              [[Text('Command to invoke your editor:'), Input(settings.get('-editor program-', ''), key='-EDITOR PROGRAM-', enable_events=True), FileBrowse()],
              [Text('String to launch your editor to edit at a particular line #.')],
              [Text('Use tags <editor> <file> <line> to specify the string')],
              [Text('that will be executed to edit python files using your editor')],
              [Text('Edit Format String (hover for tooltip)', tooltip=tooltip),
               Input(settings.get('-editor format string-', '<editor> <file>'), key='-EDITOR FORMAT-', tooltip=tooltip)]], font='_ 16', expand_x=True)

    # ------------------------- Explorer Tab -------------------------

    explorer_tab = Tab('Explorer Program',
              [[Input(settings.get('-explorer program-', ''), key='-EXPLORER PROGRAM-', tooltip=tooltip_file_explorer)]], font='_ 16', expand_x=True,  tooltip=tooltip_file_explorer)

    # ------------------------- Snapshots Tab -------------------------

    snapshots_tab = Tab('Window Snapshots',
              [[Combo(('',)+key_choices, default_value=settings.get(json.dumps(('-snapshot keysym-', i)), ''), readonly=True, key=('-SNAPSHOT KEYSYM-', i), size=(None, 30)) for i in range(4)],
              [Text('Manually Entered Bind String:'), Input(settings.get('-snapshot keysym manual-', ''),key='-SNAPSHOT KEYSYM MANUAL-')],
              [Text('Folder to store screenshots:'), Push(), Input(settings.get('-screenshots folder-', ''), key='-SCREENSHOTS FOLDER-'), FolderBrowse()],
              [Text('Screenshots Filename or Prefix:'), Push(), Input(settings.get('-screenshots filename-', ''), key='-SCREENSHOTS FILENAME-'), FileBrowse()],
              [Checkbox('Auto-number Images', key='-SCREENSHOTS AUTONUMBER-')]], font='_ 16', expand_x=True,)

    # ------------------------- Theme Tab -------------------------

    theme_tab = Tab('Theme',
              [[Text(f"Leave blank for 'official' PySimpleGUI default theme: {OFFICIAL_PYSIMPLEGUI_THEME}")],
              [Text('Default Theme For All Programs:'),
               Combo(['', *theme_list()], default_value=settings.get('-theme-', None), readonly=True, key='-THEME-', tooltip=tooltip_theme), Checkbox('Always use custom Titlebar', default_value=pysimplegui_user_settings.get('-custom titlebar-',False), key='-CUSTOM TITLEBAR-')],
               [Frame('Window Watermarking',
                       [[Checkbox('Enable Window Watermarking', default_value=pysimplegui_user_settings.get('-watermark-', False), key='-WATERMARK-')],
                       [Text('Prefix Text String:'), Input(pysimplegui_user_settings.get('-watermark text-', ''), key='-WATERMARK TEXT-')],
                       [Checkbox('PySimpleGUI Version', default_value=pysimplegui_user_settings.get('-watermark ver-', False), key='-WATERMARK VER-')],
                       [Checkbox('Framework Version', default_value=pysimplegui_user_settings.get('-watermark framework ver-', False), key='-WATERMARK FRAMEWORK VER-')],
                       [Text('Font:'), Input(pysimplegui_user_settings.get('-watermark font-', '_ 9 bold'), key='-WATERMARK FONT-')],
                       # [T('Background Color:'), Input(pysimplegui_user_settings.get('-watermark bg color-', 'window.BackgroundColor'), key='-WATERMARK BG COLOR-')],
                        ],
                font='_ 16', expand_x=True)]])



    settings_tab_group = TabGroup(layout=[[theme_tab, ttk_tab, interpreter_tab, explorer_tab, editor_tab, snapshots_tab,  ]])
    layout += [[settings_tab_group]]
              # [T('Buttons (Leave Unchecked To Use Default) NOT YET IMPLEMENTED!',  font='_ 16')],
              #      [Checkbox('Always use TTK buttons'), CBox('Always use TK Buttons')],
    layout += [[Button('Ok', bind_return_key=True), Button('Cancel'), Button('Mac Patch Control')]]

    window = Window('Settings', layout, keep_on_top=True, modal=False, finalize=True)

    # fill in the theme list into the Combo element - must do this AFTER the window is created or a tkinter temp window is auto created by tkinter
    ttk_theme_list = ttk.Style().theme_names()

    window['-TTK THEME-'].update(value=DEFAULTS.TTK_THEME, values=ttk_theme_list)

    while True:
        event, values = window.read()
        if event in ('Cancel', WIN_CLOSED):
            break
        if event == 'Ok':
            new_theme = OFFICIAL_PYSIMPLEGUI_THEME if values['-THEME-'] == '' else values['-THEME-']
            pysimplegui_user_settings.set('-editor program-', values['-EDITOR PROGRAM-'])
            pysimplegui_user_settings.set('-explorer program-', values['-EXPLORER PROGRAM-'])
            pysimplegui_user_settings.set('-editor format string-', values['-EDITOR FORMAT-'])
            pysimplegui_user_settings.set('-python command-', values['-PYTHON COMMAND-'])
            pysimplegui_user_settings.set('-custom titlebar-', values['-CUSTOM TITLEBAR-'])
            pysimplegui_user_settings.set('-theme-', new_theme)
            pysimplegui_user_settings.set('-watermark-', values['-WATERMARK-'])
            pysimplegui_user_settings.set('-watermark text-', values['-WATERMARK TEXT-'])
            pysimplegui_user_settings.set('-watermark ver-', values['-WATERMARK VER-'])
            pysimplegui_user_settings.set('-watermark framework ver-', values['-WATERMARK FRAMEWORK VER-'])
            pysimplegui_user_settings.set('-watermark font-', values['-WATERMARK FONT-'])
            # pysimplegui_user_settings.set('-watermark bg color-', values['-WATERMARK BG COLOR-'])

            # TTK SETTINGS
            pysimplegui_user_settings.set('-ttk theme-', values['-TTK THEME-'])
            DEFAULT_TTK_THEME = values['-TTK THEME-']

            # Snapshots portion
            screenshot_keysym_manual = values['-SNAPSHOT KEYSYM MANUAL-']
            pysimplegui_user_settings.set('-snapshot keysym manual-', values['-SNAPSHOT KEYSYM MANUAL-'])
            screenshot_keysym = ''
            for i in range(4):
                pysimplegui_user_settings.set(json.dumps(('-snapshot keysym-',i)), values[('-SNAPSHOT KEYSYM-', i)])
                if values[('-SNAPSHOT KEYSYM-', i)]:
                    screenshot_keysym += f"<{values[('-SNAPSHOT KEYSYM-', i)]}>"
            if screenshot_keysym_manual:
                DEFAULT_WINDOW_SNAPSHOT_KEY_CODE = screenshot_keysym_manual
            elif screenshot_keysym:
                DEFAULT_WINDOW_SNAPSHOT_KEY_CODE = screenshot_keysym

            pysimplegui_user_settings.set('-screenshots folder-', values['-SCREENSHOTS FOLDER-'])
            pysimplegui_user_settings.set('-screenshots filename-', values['-SCREENSHOTS FILENAME-'])

            # TTK Scrollbar portion
            for key, value in values.items():
                if isinstance(key, tuple):
                    if key[0] == '-TTK SCROLL-':
                        pysimplegui_user_settings.set(json.dumps(('-ttk scroll-', key[1])), value)

            theme(new_theme)

            _global_settings_get_ttk_scrollbar_info()
            _global_settings_get_watermark_info()

            window.close()
            return True
        if event == '-EDITOR PROGRAM-':
            for key, value in editor_format_dict.items():
                if key in values['-EDITOR PROGRAM-'].lower():
                    window['-EDITOR FORMAT-'].update(value=value)
        elif event == 'Mac Patch Control':
            main_mac_feature_control()
            # re-read the settings in case they changed
            _read_mac_global_settings()
        elif event == 'Reset Scrollbar Settings':
            ttk_part_mapping_dict = copy.copy(DEFAULT_TTK_PART_MAPPING_DICT)
            for key, item in ttk_part_mapping_dict.items():
                window[('-TTK SCROLL-', key)].update(item)
        elif event == 'Test Scrollbar Settings':
            for ttk_part in TTK_SCROLLBAR_PART_LIST:
                value = values[('-TTK SCROLL-', ttk_part)]
                ttk_part_mapping_dict[ttk_part] = value
            DEFAULT_TTK_THEME = values['-TTK THEME-']
            for i in range(100):
                Print(i, keep_on_top=True)
            Print('Close this window to continue...', keep_on_top=True)

    window.close()
    # In case some of the settings were modified and tried out, reset the ttk info to be what's in the config file
    style = ttk.Style(Window.hidden_master_root)
    _change_ttk_theme(style, DEFAULTS.TTK_THEME)
    _global_settings_get_ttk_scrollbar_info()

    return False

def main_get_debug_data(*, suppress_popup=False):
    """
    Collect up and display the data needed to file GitHub issues.
    This function will place the information on the clipboard.
    You MUST paste the information from the clipboard prior to existing your application (except on Windows).
    :param suppress_popup: If True no popup window will be shown. The string will be only returned, not displayed
    :type suppress_popup:  (bool)
    :returns:              String containing the information to place into the GitHub Issue
    :rtype:                (str)
    """
    message = get_versions()
    clipboard_set(message)

    if not suppress_popup:
        popup_scrolled('*** Version information copied to your clipboard. Paste into your GitHub Issue. ***\n',
                       message, title='Select and copy this info to your GitHub Issue', keep_on_top=True, size=(100, 10))

    return message
