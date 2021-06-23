import contextlib
import threading
import traceback
import webbrowser
import os.path
import PySimpleGUI as sg
from howdoi.howdoi import SUPPORTED_SEARCH_ENGINES

import difflib
from . import reporter
from . import datalib
from .util import howdoi, check_for_howdoi_update
import sys


def exc(cls, value, tb):
    if issubclass(cls, KeyboardInterrupt):  # Ignore Ctrl + C.
        sys.__excepthook__(cls, value, tb)
        return
    f_name = os.path.join(os.path.dirname(__file__), 'error.txt')
    sg.popup('writing error to:', f_name)
    with open(f_name, 'w') as e_io:
        s = traceback.format_exception(cls, value, tb)
        e_io.writelines(s)
        print(''.join(s), file=sys.stderr)
        print(f"done writing error to {f_name}")
    try:
        reporter.error(cls, value, tb)
    except Exception:
        pass


sys.excepthook = exc
#
num_items_to_show = 4
input_width = 20
# sg.theme('DarkAmber')
sg.theme('LightBlue7')
sg.theme_input_background_color('#2b7088')


class Graphic:
    # noinspection PyTypeChecker
    def __init__(self):
        self.window: sg.Window = None
        self.choices = None
        self.data: dict = None

    def build_layout(self, pb_window):
        index = [0]
        tasks = ["get data ...", "building search layout ...", "building search results layout ...",
                 "building answer layout ...",
                 "building master layout ..."]

        @contextlib.contextmanager
        def write_case():
            pb_window.write_event_value("$start", tasks[index[0]])
            yield
            index[0] += 1
            pb_window.write_event_value("$pb", [index[0], len(tasks)])

        with write_case():
            self.data = datalib.get_data()
            self.choices = list(datalib.get_data().keys())

        with write_case():
            search_layout = [
                [sg.Input(size=(input_width, 1), enable_events=True, key='-inp-'),
                 sg.B('search', key='-search-', bind_return_key=True), sg.B('create', key='-create-'),
                 sg.B('Locals', key='-locals-')],
                [sg.pin(sg.Col(
                    [[sg.Listbox(values=[], size=(input_width, num_items_to_show), enable_events=True, key='-box-',
                                 select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, no_scrollbar=True)]],
                    key='-box-visible-', pad=(0, 0), visible=False))],
                [sg.T("Number Answers :"), sg.Spin(list(range(1, 11)), initial_value=3, key='-num_answers-')],
                [sg.Checkbox('All Answer', default=False, key='-all_answer-bool-')],
                [sg.Checkbox('Saved Answer', default=False, key='-save-answer-bool-')],
                [sg.T('Search Engine'),
                 sg.Combo(SUPPORTED_SEARCH_ENGINES, SUPPORTED_SEARCH_ENGINES[1], key='-search_engine-')],
            ]
        with write_case():
            search_results_layout = [
                [sg.Listbox(['search something for results !' + ' ' * 20], size=(60, 6), key='-search-results-',
                            enable_events=True)]
            ]
        with write_case():
            answer_layout = [
                [sg.B('open question', key='-open-question-'), sg.T('with link'), sg.In(key='-link-')],
                [sg.Multiline('', size=(70, 8), key='-answer-')],
                [sg.B('Save', key='-save-answer-'), sg.T('under the name:'), sg.Input(key='-answer-name-')]
            ]
        with write_case():
            layout = [[
                sg.TabGroup([
                    [sg.Tab('search', search_layout, key='-search-master-')],
                    [sg.Tab('search results', search_results_layout, key='-search-results-master-', visible=False)],
                    [sg.Tab('answer', answer_layout, key='-answer-master-', visible=False)]
                ], key='-master-')
            ],
                [sg.T("found bug? you have idea to new feature? click here to open issue !", enable_events=True,
                      font="Courier-New 12 underline", key="-open-issue-"), ],

                [sg.T("if you enjoy from this free software,it would be great if you could buy me a coffee:",
                      font='Courier-New 12'),
                 sg.B(image_data=sg.ICON_BUY_ME_A_COFFEE, key="-buy-me-coffee-")]
            ]
        pb_window.write_event_value("$done", layout)

    def loading_screen(self):
        layout = [
            [sg.T("loading ..." + " " * 50, key="-t-")],
            [sg.ProgressBar(1, orientation='h', size=(20, 20), key='-pb-')]
        ]
        window = sg.Window('Loading ...', layout, finalize=True)
        # start Thread
        building = threading.Thread(target=self.build_layout, args=[window])
        building.start()
        while 1:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                if building.is_alive():
                    ex = sg.popup_ok_cancel("do you want to exit while loading?")
                else:  # error
                    ex = True
                if ex:
                    window.close()
                    exit("user exit while loading")

            if event == "$start":
                window["-t-"].update(values["$start"])

            elif event == "$pb":
                pb: sg.ProgressBar = window["-pb-"]
                pb.update(values["$pb"])

            elif event == "$done":
                window.close()
                return values["$done"]

    def update_data(self, data):
        self.data.update(data)
        datalib.write_data(self.data)
        self.choices = list(self.data.keys())

    def main(self):
        check_for_howdoi_update()

        layout = self.loading_screen()
        window = sg.Window('CodeSnippets', layout, finalize=True, resizable=True, font=('Helvetica', 16))
        # setup:
        expand_elements = ['-master-', '-answer-', '-search-results-']
        for element in expand_elements:
            window[element].expand(True, True)
        # window['-search-results-'].expand(expand_x=True, expand_y=True, expand_row=True)
        answers_links = {}
        answers_links_full = {}
        input_text = ""

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break

            elif event == '-inp-':
                text = values['-inp-'].lower()
                if text == input_text:
                    continue
                else:
                    input_text = text
                # correct_choices = [c for c in choices if c.lower().startswith(text)]
                correct_choices = difflib.get_close_matches(text, self.choices)
                if not correct_choices:
                    correct_choices = [c for c in self.choices if c.lower().startswith(text)]
                    if not correct_choices:
                        correct_choices = [c for c in self.choices if text.split('\n') in c.lower().split('\n')]
                window['-box-'].update(values=correct_choices)
                window['-box-visible-'].update(visible=bool(correct_choices))
                window['-save-answer-bool-'].update(False)

            elif event == '-box-':
                window['-inp-'].update(value=values['-box-'][0])
                window['-box-visible-'].update(visible=False)
                window['-save-answer-bool-'].update(True)

            elif event == '-create-':
                answer_name = values['-inp-']
                window['-link-'].update('')
                window['-answer-'].update('# write here your answer')
                window['-answer-name-'].update(answer_name)
                window['-answer-master-'].update(visible=True).select()
                # answers = [ {'answer':answer,'link':link},{'answer':answer,'link':link} ]

            elif event == '-search-':
                text: str = values['-inp-']
                # answers = [ {'answer':answer,'link':link},{'answer':answer,'link':link} ]
                if text:
                    if (text.strip() in self.choices) or values['-save-answer-bool-']:
                        if text.strip() in self.choices:
                            q = [(text.strip(), self.data[text.strip()])]
                        else:
                            q = [(k, v) for k, v in self.data.items() if k.startswith(text.strip())]
                            if not q:
                                s = difflib.get_close_matches(text.strip(), self.choices)
                                if s:
                                    q = [(k, self.data[k]) for k in s]

                            if not q:
                                q = {'error': "Sorry, couldn't find any local answer with that topic"}
                        #
                        if 'error' in q:
                            sg.popup(q['error'])
                            continue
                        else:
                            answers_links = dict(
                                map(lambda x: (x[0], x[1]['answer']), q))
                            answers_links_full = dict(
                                map(lambda x: (x[0], x[1]['link'],), q))

                            # q = list(map(lambda x: x[1], q))
                    else:
                        q = howdoi(text, values["-num_answers-"], values["-search_engine-"],
                                   values["-all_answer-bool-"])

                        if 'error' in q:
                            sg.popup(q['error'])
                            continue
                        else:
                            basename = lambda x: os.path.basename(x) if x is not None else ''
                            answers_links = dict(
                                map(lambda x: (basename(x['link']).replace('-', ' '), x['answer']), q))
                            answers_links_full = dict(
                                map(lambda x: (basename(x['link']).replace('-', ' '), x['link'],), q))

                    # all
                    search_results = list(answers_links.keys())
                    window['-search-results-'].update(search_results, visible=True)
                    window['-search-results-master-'].update(visible=True)
                    if len(search_results) == 1:
                        r = search_results[0]
                        window['-link-'].update(answers_links_full[r])
                        window['-answer-'].update(answers_links[r])
                        window['-answer-name-'].update(r)
                        window['-answer-master-'].update(visible=True).select()
                    else:
                        window['-search-results-master-'].select()

            elif event == '-search-results-':  # choice from search results
                if answers_links:
                    answer_name = values['-search-results-'][0]
                    selected_answer: str = answers_links[answer_name]
                    window['-link-'].update(answers_links_full[answer_name])
                    window['-answer-'].update(selected_answer)
                    window['-answer-name-'].update(answer_name)
                    window['-answer-master-'].update(visible=True).select()

            elif event == '-open-question-':
                if values['-link-']:
                    webbrowser.open(values['-link-'])

            elif event == '-save-answer-':
                saved_answer = values['-answer-']
                answer_name = values['-answer-name-']
                self.update_data({answer_name: {"answer": saved_answer, 'link': values['-link-']}})
                window['-search-master-'].select()
                window['-inp-'].update('')

            elif event == '-locals-':
                answers_links = dict(
                    map(lambda x: (x[0], x[1]['answer']), self.data.items()))
                answers_links_full = dict(
                    map(lambda x: (x[0], x[1]['link'],), self.data.items()))
                if self.choices:
                    window['-search-results-'].update(self.choices, visible=True)
                else:
                    window['-search-results-'].update([self.choices], visible=True)

                window['-search-results-master-'].update(visible=True).select()
            elif event == '-open-issue-':
                window.disappear()
                reporter.open_github_issue()
                window.reappear()
            elif event == "-buy-me-coffee-":
                webbrowser.open('https://www.buymeacoffee.com/matanh')
            else:
                print("unknown event:", event)


if __name__ == '__main__':
    graphic = Graphic()
    graphic.main()
