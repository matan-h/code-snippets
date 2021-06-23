# based on PySimpleGUI.main_open_github_issue
# todo: add a button to post github issue
import platform
import traceback
import urllib.parse
import webbrowser

import PySimpleGUI as sg
from .version import __version__
import howdoi
base_url = "https://github.com/matan-h/code-snippets"
issues_url = "{}/issues/new?".format(base_url)

body = ("""
### Type of Issue 

{issue_type}

----------------------------------------
### platform

{platform}

----------------------------------------
## Versions

python : {python_version}
code_snippets : {snippets_version}
PySimpleGUI : {sg_version}
howdoi: {howdoi_version}
tkinter : {tclversion}

----------------------------------------
#### Detailed Description

{detailed_description}
""")

issue_types = (
    'Question',
    'Bug',
    'Enhancement',
)


def make_markdown(issue_type, detailed_description):
    return body.format(
        issue_type=issue_type,
        platform=platform.platform(),
        python_version=platform.python_version(),
        snippets_version=__version__,
        sg_version=sg.ver,
        howdoi_version=howdoi.__version__,
        tclversion=sg.tclversion_detailed,
        detailed_description=detailed_description,
    )


def build_layout():
    frame_types = [[sg.Radio(t, 1, size=(10, 1), enable_events=True, key=t)] for t in issue_types]
    frame_details = [[sg.Multiline(size=(65, 10), font='Courier 10', k='-details-')]]
    #######
    top_layout = [
        [sg.Text('Open A GitHub Issue')],
        [sg.T('Title'), sg.Input(k='-title-', size=(50, 1), focus=True)],
        [sg.Frame('Type of Issue', frame_types), ]
    ]
    bottom_layout = [[
        sg.Frame("Details", frame_details)
    ]]

    layout = [
        [sg.pin(sg.Col(top_layout, k='-TOP COL-'))],
        [sg.Col(bottom_layout)],
        [sg.B('Post Issue')]
    ]

    return layout


def github_issue_post_validate(values, issue_types):
    issue_type = None
    for itype in issue_types:
        if values[itype]:
            issue_type = itype
            break
    #
    if issue_type is None:
        sg.popup_error('Must choose issue type',)
        return False

    title: str = values['-title-'].strip()
    if len(title) == 0:
        sg.popup_error("Title can't be blank")
        return False
    elif title.startswith("[") and title.endswith("]"):
        sg.popup_error("Title can't be only tag")
        return False

    if len(values['-details-'].split()) < 3:
        sg.popup_error("A little more details would be awesome")
        return False

    return True


def post_issue(issue_type, title, details):
    markdown = make_markdown(issue_type, details)

    # Fix body cuz urllib can't do it.
    getVars = {'title': title, 'body': markdown}
    link = (issues_url + urllib.parse.urlencode(getVars).replace("%5Cn", "%0D"))

    webbrowser.open_new_tab(link)


def error(cls, value, tb):
    if sg.popup_yes_no(
            f"an error has occurred: {cls.__name__}\n"
            "do you want to report the error to github issues?\n"
            "the program processed all automatically, and you only need to push the Submit button.",
            title="an error has occurred") == "Yes":
        trace = "".join(traceback.format_exception(cls, value, tb))
        post_issue("Error",f"[Error] {cls.__name__}",f"traceback:\n```pytb\n{trace}\n```")


def open_github_issue():
    layout = build_layout()
    window = sg.Window('Open A GitHub Issue', layout, finalize=True, resizable=True)

    window['-details-'].expand(True, True, True)
    window.bring_to_front()
    while 1:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event in issue_types:
            title = str(values['-title-'])
            if len(title) != 0:
                if title.startswith('[') and ']' in title:
                    title = title[title.find(']') + 1:].strip()

            window['-title-'].update('[{}] {}'.format(event, title))

        elif event == 'Post Issue':
            issue_type = None
            for itype in issue_types:
                if values[itype]:
                    issue_type = itype
                    break

            if not github_issue_post_validate(values, issue_types):
                continue

            post_issue(issue_type, values["-title-"], values["-details-"])

    window.close()


if __name__ == '__main__':
    open_github_issue()