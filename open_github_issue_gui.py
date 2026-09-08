

import platform
import sys
import urllib
import webbrowser

from quick_tkinter import (
    EMOJI_BASE64,
    SYMBOLS,
    WIN_CLOSED,
    WINDOW_CLOSE_ATTEMPTED_EVENT,
    Button,
    Checkbox,
    Column,
    Frame,
    HorizontalSeparator,
    Input,
    Multiline,
    Pane,
    Radio,
    Tab,
    TabGroup,
    Text,
    Window,
    pin,
    popup,
    popup_error,
    popup_yes_no,
    running_linux,
    running_mac,
    running_windows,
    tclversion_detailed,
    ver,
    vtop,
)


def main_open_github_issue():
    font_frame = '_ 14'
    issue_types = ('Question', 'Bug', 'Enhancement', 'Error Message')
    frame_type = [[Radio(t, 1, size=(10, 1), enable_events=True, key=t)] for t in issue_types]

    v_size = (15, 1)
    frame_versions = [[Text('Python', size=v_size), Input(sys.version, size=(20, 1), key='-VER PYTHON-')],
                      [Text('PySimpleGUI', size=v_size), Input(ver, size=(20, 1), key='-VER PSG-')],
                      [Text('tkinter', size=v_size), Input(tclversion_detailed, size=(20, 1), key='-VER TK-')]]

    frame_platforms = [[Text('OS                 '), Text('Details')],
                       [Radio('Windows', 2, default_value=running_windows, size=(8, 1), key='-OS WIN-'), Input(size=(8, 1), key='-OS WIN VER-')],
                       [Radio('Linux', 2, default_value=running_linux, size=(8, 1), key='-OS LINUX-'), Input(size=(8, 1), key='-OS LINUX VER-')],
                       [Radio('Mac', 2, default_value=running_mac, size=(8, 1), key='-OS MAC-'), Input(size=(8, 1), key='-OS MAC VER-')],
                       [Radio('Other', 2, size=(8, 1), key='-OS OTHER-'), Input(size=(8, 1), key='-OS OTHER VER-')]]

    col_experience = [[Text('Optional Experience Info')],
                      [Input(size=(4, 1), key='-EXP PROG-'), Text('Years Programming')],
                      [Input(size=(4, 1), key='-EXP PYTHON-'), Text('Years Writing Python')],
                      [Checkbox('Previously programmed a GUI', key='-CB PRIOR GUI-')],
                      [Text('Share more if you want....')],
                      [Input(size=(25, 1), key='-EXP NOTES-', expand_x=True)]]

    checklist = (('Searched main docs for your problem', 'www.PySimpleGUI.org'),
                 ('Looked for Demo Programs that are similar to your goal.\nIt is recommend you use the Demo Browser!', 'https://Demos.PySimpleGUI.org'),
                 ('If not tkinter - looked for Demo Programs for specific port', ''),
                 ('For non tkinter - Looked at readme for your specific port if not PySimpleGUI (Qt, WX, Remi)', ''),
                 ('Run your program outside of your debugger (from a command line)', ''),
                 ('Searched through Issues (open and closed) to see if already reported', 'https://Issues.PySimpleGUI.org'),
                 ('Upgraded to the latest official release of PySimpleGUI on PyPI', 'https://Upgrading.PySimpleGUI.org'),
                 ('Tried using the PySimpleGUI.py file on GitHub. Your problem may have already been fixed but not released.', ''))

    checklist_col1 = Column([[Checkbox(c, key=('-CB-', i)), Text(t, key=f"-T{i}-", enable_events=True)] for i, (c, t) in enumerate(checklist[:4])], key='-C FRAME CBs1-')
    checklist_col2 = Column([[Checkbox(c, key=('-CB-', i + 4)), Text(t, key=f"-T{i + 4}-", enable_events=True)] for i, (c, t) in enumerate(checklist[4:])], pad=(0, 0),
                         key='-C FRAME CBs2-')
    checklist_tabgropup = TabGroup(
        [[Tab('Checklist 1 *', [[checklist_col1]], expand_x=True, expand_y=True), Tab('Checklist 2  *', [[checklist_col2]]), Tab('Experience', col_experience, key='-Tab Exp-', pad=(0, 0))]], expand_x=True, expand_y=True)

    frame_details = [[Multiline(size=(65, 10), font='Courier 10', key='-ML DETAILS-', expand_x=True, expand_y=True)]]

    tooltip_project_details = 'If you care to share a little about your project,\nthen by all means tell us what you are making!'
    frame_project_details = [[Multiline(size=(65, 10), font='Courier 10', key='-ML PROJECT DETAILS-', expand_x=True, expand_y=True, tooltip=tooltip_project_details)]]

    tooltip_where_find_psg = 'Where did you learn about PySimpleGUI?'
    frame_where_you_found_psg = [[Multiline(size=(65, 10), font='Courier 10', key='-ML FOUND PSG-', expand_x=True, expand_y=True, tooltip=tooltip_where_find_psg)]]

    tooltip_code = 'A short program that can be immediately run will considerably speed up getting you quality help.'
    frame_code = [[Multiline(size=(80, 10), font='Courier 8', key='-ML CODE-', expand_x=True, expand_y=True, tooltip=tooltip_code)]]

    frame_markdown = [[Multiline(size=(80, 10), font='Courier 8', key='-ML MARKDOWN-', expand_x=True, expand_y=True)]]

    top_layout = [[Column([[Text('Open A GitHub Issue (* = Required Info)', font='_ 15')]], expand_x=True),
                   Column([[Button('Help')]])
                   ],
                  [Frame('Title *', [[Input(key='-TITLE-', size=(50, 1), font='_ 14', focus=True)]], font=font_frame)],
                  # Image(data=EMOJI_BASE64_WEARY)],
                  vtop([
                      Frame('Platform *', frame_platforms, font=font_frame),
                      Frame('Type of Issue *', frame_type, font=font_frame),
                      Frame('Versions *', frame_versions, font=font_frame),
                  ])]

    middle_layout = [
        [Frame('Checklist * (note that you can click the links)', [[checklist_tabgropup]], font=font_frame, key='-CLIST FRAME-', expand_x=True, expand_y=True)],
        [HorizontalSeparator()],
        [Text(SYMBOLS.DOWN + ' If you need more room for details grab the dot and drag to expand', background_color='red', text_color='white')]]

    bottom_layout = [[TabGroup([[Tab('Details *\n', frame_details, pad=(0, 0)),
                                 Tab('SHORT Program\nto duplicate problem *', frame_code, pad=(0, 0)),
                                 Tab('Your Project Details\n(optional)', frame_project_details, pad=(0, 0)),
                                 Tab('Where you found us?\n(optional)', frame_where_you_found_psg, pad=(0, 0)),
                                 Tab('Markdown Output\n', frame_markdown, pad=(0, 0)),
                                 ]], key='-TABGROUP-', expand_x=True, expand_y=True),
                      ]]


    layout_pane = Pane([Column(middle_layout), Column(bottom_layout)], key='-PANE-', expand_x=True, expand_y=True)

    layout = [
        [pin(Button(SYMBOLS.DOWN, pad=(0, 0), key='-HIDE CLIST-', tooltip='Hide/show upper sections of window')), pin(Column(top_layout, key='-TOP COL-'))],
        [layout_pane],
        [Column([[Button('Post Issue'), Button('Create Markdown Only'), Button('Quit')]])]]

    window = Window('Open A GitHub Issue', layout, finalize=True, resizable=True, enable_close_attempted_event=True, margins=(0, 0))



    # for i in range(len(checklist)):
    [window[f"-T{i}-"].set_cursor('hand1') for i in range(len(checklist))]
    # window['-TABGROUP-'].expand(True, True, True)
    # window['-ML CODE-'].expand(True, True, True)
    # window['-ML DETAILS-'].expand(True, True, True)
    # window['-ML MARKDOWN-'].expand(True, True, True)
    # window['-PANE-'].expand(True, True, True)

    if running_mac:
        window['-OS MAC VER-'].update(platform.mac_ver())
    elif running_windows:
        window['-OS WIN VER-'].update(platform.win32_ver())
    elif running_linux:
        window['-OS LINUX VER-'].update(platform.libc_ver())


    window.bring_to_front()
    while True:  # Event Loop
        event, values = window.read()
        # print(event, values)
        if event in (WINDOW_CLOSE_ATTEMPTED_EVENT, 'Quit'):
            if popup_yes_no('Do you really want to exit?',
                            'If you have not clicked Post Issue button and then clicked "Submit New Issue" button '
                            'then your issue will not have been submitted to GitHub.\n'
                            'If you are having trouble with PySimpleGUI opening your browser, consider generating '
                            'the markdown, copying it to a text file, and then using it later to manually paste into a new issue '
                            '\n'
                            'Are you sure you want to quit?',
                            image=EMOJI_BASE64.PONDER, keep_on_top=True
                            ) == 'Yes':
                break
        if event == WIN_CLOSED:
            break
        if event in [f"-T{i}-" for i in range(len(checklist))]:
            webbrowser.open_new_tab(window[event].get())
        if event in issue_types:
            title = str(values['-TITLE-'])
            if len(title) != 0:
                if title[0] == '[' and title.find(']'):
                    title = title[title.find(']') + 1:]
                    title = title.strip()
            window['-TITLE-'].update(f"[{event}] {title}")
        if event == '-HIDE CLIST-':
            window['-TOP COL-'].update(visible=not window['-TOP COL-'].visible)
            window['-HIDE CLIST-'].update(text=SYMBOLS.UP if window['-HIDE CLIST-'].get_text() == SYMBOLS.DOWN else SYMBOLS.DOWN)
        if event == 'Help':
            _github_issue_help()
        elif event in ('Post Issue', 'Create Markdown Only'):
            issue_type = None
            for itype in issue_types:
                if values[itype]:
                    issue_type = itype
                    break
            if issue_type is None:
                popup_error('Must choose issue type', keep_on_top=True)
                continue
            if values['-OS WIN-']:
                operating_system = 'Windows'
                os_ver = values['-OS WIN VER-']
            elif values['-OS LINUX-']:
                operating_system = 'Linux'
                os_ver = values['-OS LINUX VER-']
            elif values['-OS MAC-']:
                operating_system = 'Mac'
                os_ver = values['-OS MAC VER-']
            elif values['-OS OTHER-']:
                operating_system = 'Other'
                os_ver = values['-OS OTHER VER-']
            else:
                popup_error('Must choose Operating System', keep_on_top=True)
                continue
            checkboxes = ['X' if values[('-CB-', i)] else ' ' for i in range(len(checklist))]

            if not _github_issue_post_validate(values, checklist, issue_types):
                continue

            cb_dict = {'cb_docs': checkboxes[0], 'cb_demos': checkboxes[1], 'cb_demo_port': checkboxes[2], 'cb_readme_other': checkboxes[3],
                       'cb_command_line': checkboxes[4], 'cb_issues': checkboxes[5], 'cb_latest_pypi': checkboxes[6], 'cb_github': checkboxes[7], 'detailed_desc': values['-ML DETAILS-'],
                       'code': values['-ML CODE-'],
                       'project_details': values['-ML PROJECT DETAILS-'].rstrip(),
                       'where_found': values['-ML FOUND PSG-']}

            markdown = _github_issue_post_make_markdown(issue_type, operating_system, os_ver, 'tkinter', values['-VER PSG-'], values['-VER TK-'],
                                                        values['-VER PYTHON-'],
                                                        values['-EXP PYTHON-'],values['-EXP PROG-'], 'Yes' if values['-CB PRIOR GUI-'] else 'No',
                                                        values['-EXP NOTES-'],
                                                        **cb_dict)
            window['-ML MARKDOWN-'].update(markdown)
            link = _github_issue_post_make_github_link(values['-TITLE-'], window['-ML MARKDOWN-'].get())
            if event == 'Post Issue':
                webbrowser.open_new_tab(link)
            else:
                popup('Your markdown code is in the Markdown tab', keep_on_top=True)

    window.close()


def _github_issue_post_make_github_link(title, body):
    pysimplegui_url = "https://github.com/PySimpleGUI/PySimpleGUI"
    pysimplegui_issues = f"{pysimplegui_url}/issues/new?"

    # Fix body cuz urllib can't do it smfh
    get_vars = {'title': str(title), 'body': str(body)}
    return (pysimplegui_issues + urllib.parse.urlencode(get_vars).replace("%5Cn", "%0D"))


def _github_issue_help():
    text_font = '_ 10'

    def HelpText(text):
        return Text(text, size=(80, None), font=text_font)

    help_why = \
""" Let's start with a review of the Goals of the PySimpleGUI project
1. To have fun
2. For you to be successful

This form is as important as the documentation and the demo programs to meeting those goals.

The GitHub Issue GUI is here to help you more easily log issues on the PySimpleGUI GitHub Repo. """

    help_goals = \
""" The goals of using GitHub Issues for PySimpleGUI question, problems and suggestions are:
* Give you direct access to engineers with the most knowledge of PySimpleGUI
* Answer your questions in the most precise and correct way possible
* Provide the highest quality solutions possible
* Give you a checklist of things to try that may solve the problem
* A single, searchable database of known problems and their workarounds
* Provide a place for the PySimpleGUI project to directly provide support to users
* A list of requested enhancements
* An easy to use interface to post code and images
* A way to track the status and have converstaions about issues
* Enable multiple people to help users """

    help_explain = \
""" GitHub does not provide a "form" that normal bug-tracking-databases provide. As a result, a form was created specifically for the PySimpleGUI project.

The most obvious questions about this form are
* Why is there a form? Other projects don't have one?
* My question is an easy one, why does it still need a form?

The answer is:
I want you to get your question answered with the highest quality answer possible as quickly as possible.

The longer answer - For quite a while there was no form. It resulted the same back and forth, multiple questions comversation.  "What version are you running?"  "What OS are you using?"  These waste precious time.

If asking nicely helps... PLEASE ... please fill out the form.

I can assure you that this form is not here to punish you. It doesn't exist to make you angry and frustrated.  It's not here for any purpose than to try and get you support and make PySimpleGUI better. """

    help_experience = \
""" Not many Bug-tracking systems ask about you as a user. Your experience in programming, programming in Python and programming a GUI are asked to provide you with the best possible answer.  Here's why it's helpful.  You're a human being, with a past, and a some amount of experience.  Being able to taylor the reply to your issue in a way that fits you and your experience will result in a reply that's efficient and clear.  It's not something normally done but perhaps it should be. It's meant to provide you with a personal response.

If you've been programming for a month, the person answering your question can answer your question in a way that's understandable to you.  Similarly, if you've been programming for 20 years and have used multiple Python GUI frameworks, then you are unlikely to need as much explanation.  You'll also have a richer GUI vocabularly. It's meant to try and give you a peronally crafted response that's on your wavelength. Fun & success... Remember those are our shared goals"""

    help_steps = \
""" The steps to log an issue are:
1. Fill in the form
2. Click Post Issue """

    t_goals = Tab('Goals', [[HelpText(help_goals)]])
    t_why = Tab('Why', [[HelpText(help_why)]])
    t_faq = Tab('FAQ', [[HelpText(help_explain)]])
    t_exp = Tab('Experience', [[HelpText(help_experience)]])
    t_steps = Tab('Steps', [[HelpText(help_steps)]])

    layout = [[TabGroup([[t_goals, t_why, t_faq, t_exp, t_steps]])],
              [Button('Close')]]

    Window('GitHub Issue GUI Help', layout, keep_on_top=True).read(close=True)


def _github_issue_post_validate(values, checklist, issue_types):
    issue_type = None
    for itype in issue_types:
        if values[itype]:
            issue_type = itype
            break
    if issue_type is None:
        popup_error('Must choose issue type', keep_on_top=True)
        return False
    if values['-OS WIN-']:
        os_ver = values['-OS WIN VER-']
    elif values['-OS LINUX-']:
        os_ver = values['-OS LINUX VER-']
    elif values['-OS MAC-']:
        os_ver = values['-OS MAC VER-']
    elif values['-OS OTHER-']:
        os_ver = values['-OS OTHER VER-']
    else:
        popup_error('Must choose Operating System', keep_on_top=True)
        return False

    if os_ver == '':
        popup_error('Must fill in an OS Version', keep_on_top=True)
        return False

    checkboxes = any(values[('-CB-', i)] for i in range(len(checklist)))
    if not checkboxes:
        popup_error('None of the checkboxes were checked.... you need to have tried something...anything...', keep_on_top=True)
        return False

    title = values['-TITLE-'].strip()
    if len(title) == 0:
        popup_error("Title can't be blank", keep_on_top=True)
        return False
    if title[1:len(title) - 1] == issue_type:
        popup_error("Title can't be blank (only the type of issue isn't enough)", keep_on_top=True)
        return False

    if len(values['-ML DETAILS-']) < 4:
        popup_error("A little more details would be awesome", keep_on_top=True)
        return False

    return True


def _github_issue_post_make_markdown(issue_type, operating_system, os_ver, psg_port, psg_ver, gui_ver, python_ver,
                                     python_exp, prog_exp, used_gui, gui_notes,
                                     cb_docs, cb_demos, cb_demo_port, cb_readme_other, cb_command_line, cb_issues, cb_latest_pypi, cb_github,
                                     detailed_desc, code, project_details, where_found):
    body = \
f"""
## Type of Issue (Enhancement, Error, Bug, Question)

{issue_type}

----------------------------------------

## Environment 

#### Operating System

{operating_system}  version {os_ver}

#### PySimpleGUI Port (tkinter, Qt, Wx, Web)

{psg_port}

----------------------------------------

## Versions


#### Python version (`sg.sys.version`)

{python_ver}

#### PySimpleGUI Version (`sg.__version__`)

{gui_ver}

#### GUI Version  (tkinter (`sg.tclversion_detailed`), PySide2, WxPython, Remi)

{project_details}
"""

    body2 = \
f"""


---------------------

## Your Experience In Months or Years (optional)

{python_exp} Years Python programming experience
{prog_exp } Years Programming experience overall
{used_gui } Have used another Python GUI Framework? (tkinter, Qt, etc) (yes/no is fine)
{gui_notes}

---------------------

## Troubleshooting

These items may solve your problem. Please check those you've done by changing - [ ] to - [X]

- [{cb_docs        }] Searched main docs for your problem  www.PySimpleGUI.org
- [{cb_demos       }] Looked for Demo Programs that are similar to your goal. It is recommend you use the Demo Browser! Demos.PySimpleGUI.org
- [{cb_demo_port   }] If not tkinter - looked for Demo Programs for specific port
- [{cb_readme_other}] For non tkinter - Looked at readme for your specific port if not PySimpleGUI (Qt, WX, Remi)
- [{cb_command_line}] Run your program outside of your debugger (from a command line)
- [{cb_issues      }] Searched through Issues (open and closed) to see if already reported Issues.PySimpleGUI.org
- [{cb_latest_pypi }] Upgraded to the latest official release of PySimpleGUI on PyPI
- [{cb_github      }] Tried using the PySimpleGUI.py file on GitHub. Your problem may have already been fixed but not released

## Detailed Description

{detailed_desc}

#### Code To Duplicate


```python
{code if len(code) > 10 else '# Paste your code here'}


```

#### Screenshot, Sketch, or Drawing



"""


    if project_details or where_found:
        body2 +=  '------------------------'

    if project_details:
        body2 +=  \
f"""
## Watcha Makin?
{project_details}
"""

    if where_found:
        body2 += \
f"""
## How did you find PySimpleGUI?
{where_found}
"""
    return body + body2
