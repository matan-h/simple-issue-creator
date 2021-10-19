import sys

from simple_issue_creator import IssueReporter
import PySimpleGUI as sg
sg.theme("lightblue7")
iss = IssueReporter("https://github.com/matan-h/simple-issue-creator", {"python": sys.version, "my-library": "0.3dev"})
sys.excepthook = iss.error
1/0