# from __future__ import annotations
# based on PySimpleGUI.main_open_github_issue
import platform
import random
import sys
import traceback
import webbrowser

PY2 = Py3 = False
if sys.version_info[0] < 3:
    PY2 = True
    import urllib as parse
    import PySimpleGUI27 as sg
else:
    Py3 = True
    import urllib.parse as parse
    import PySimpleGUI as sg


body = ("""
### Type of Issue 

{issue_type}

----------------------------------------
### platform

{platform}

----------------------------------------
## Versions
{versions}

----------------------------------------
#### Detailed Description

{detailed_description}
            """)

issue_types = (
    'Question',
    'Bug',
    'Enhancement',
)


class IssueReporter:
    def __init__(self, base_url, versions):
        """
        IssueReporter class

        Args:
            base_url (str): github repository url (https://github.com/user/repository)
            versions (dict): dictionary of versions ({"pySimpleGui version",sg.ver})
        """
        self.versions_dict = versions
        self.versions = self.make_versions()

        self.issues_url = "{}/issues/new?".format(base_url)

    def make_versions(self):
        """
        create markdown from versions dict

        Returns: markdown string

        """
        versions_list = []
        fmt = "`{}` : {}"
        for k, v in self.versions_dict.items():
            versions_list.append(fmt.format(k, v))

        return "\n".join(versions_list)

    def make_markdown(self, issue_type, detailed_description):
        """
        make markdown from issue_type and detailed_description

        Args:
            issue_type (str): one of the `issue_types` or Error
            detailed_description (str): description of the issue

        Returns:issue markdown string

        """
        return body.format(
            issue_type=issue_type,
            platform=platform.platform(),
            python_version=platform.python_version(),
            versions=self.versions,
            detailed_description=detailed_description,
        )

    @staticmethod
    def build_layout():
        """
        build the window layout
        Returns:
             list[list]:the layout
        """
        frame_types = [[sg.Radio(t, 1, size=(10, 1), enable_events=True, key=t)] for t in issue_types]
        frame_details = [[sg.Multiline(size=(65, 10), font='Courier 10', key='-details-')]]
        #######
        top_layout = [
            [sg.Text('Open A GitHub Issue')],
            [sg.T('Title'), sg.Input(key='-title-', size=(50, 1), focus=True)],
            [sg.Frame('Type of Issue', frame_types), ]
        ]
        bottom_layout = [[
            sg.Frame("Details", frame_details)
        ]]

        layout = [
            [sg.Col(top_layout, key='-TOP COL-')],
            [sg.Col(bottom_layout)],
            [sg.B('Post Issue')]
        ]

        return layout

    @staticmethod
    def github_issue_post_validate(values):
        """
        check if github issue us valid.

        Args:
            values (dict): sg.window values

        Returns
            bool: True if valid,else False

        """
        issue_type = None
        for itype in issue_types:
            if values[itype]:
                issue_type = itype
                break
        #
        if issue_type is None:
            sg.popup_error('Must choose issue type', )
            return False

        title = values['-title-'].strip()
        if len(title) == 0:
            sg.popup_error("Title can't be blank")
            return False
        if title.startswith("[") and title.endswith("]"):
            sg.popup_error("Title can't be only tag")
            return False

        if len(values['-details-'].split()) < 3:
            sg.popup_error("A little more details would be awesome")
            return False

        return True

    def post_issue(self, issue_type, title, details):
        """
        open web url to issue

        Args:
            issue_type (str): one of the issue_types or Error
            title (str): title of the issue
            details (str) :details for the issue

        """
        markdown = self.make_markdown(issue_type, details)

        # Fix body cuz urllib can't do it.
        getVars = {'title': title, 'body': markdown}
        link = (self.issues_url + parse.urlencode(getVars).replace("%5Cn", "%0D"))

        webbrowser.open_new_tab(link)

    def open_reporter(self):
        """
        open window for open issue with title,details and type inputs
        """
        layout = self.build_layout()
        window = sg.Window('Open A GitHub Issue', layout, finalize=True, resizable=True)
        if Py3:
            window['-details-'].expand(True, True, True)

        window.bring_to_front()
        while 1:
            event, values = window.read()
            if event is None:  # sg.WIN_CLOSED
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

                if not self.github_issue_post_validate(values):
                    continue

                self.post_issue(issue_type, values["-title-"], values["-details-"])

        window.close()

    def error(self, cls, value, tb):
        """
        ask the user for issue reporting. if user press Yes,post the issue

        arguments are from sys.excepthook
        """

        if sg.popup_yes_no(
                "an error has occurred: %s\n"% cls.__name__+
                "do you want to report the error to github issues?\n"
                "the program processed all automatically, and you only need to push the Submit button.",
                title="an error has occurred") == "Yes":
            trace = "".join(traceback.format_exception(cls, value, tb))
            self.post_issue("Error", "[Error] " + cls.__name__, "traceback:\n```pytb\n%s\n```" % trace)


def main():
    """
    main example of this library
    """
    theme = random.choice(list(sg.LOOK_AND_FEEL_TABLE.keys()))  # random theme
    print("use random theme:", theme)
    sg.change_look_and_feel(theme)
    iss = IssueReporter("https://github.com/matan-h/simple-issue-creator",
                        {"python": sys.version, "this": "3.8"})  # init IssueReporter
    iss.open_reporter()


if __name__ == '__main__':
    main()
