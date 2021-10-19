# simple-issue-creator
`simple-issue-creator` is a python library for open issue-reporter gui (based on [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)) in any python project.

## Installing
To install with pip
type in terminal:
```
(sudo) pip install "https://github.com/matan-h/simple-issue-creator/archive/main.zip"
```
## Example
```python
import sys
# init the IssueReporter with url and versions dictionary
iss = IssueReporter("https://github.com/matan-h/simple-issue-creator", {"python": sys.version, "my-library": "0.3dev"})
# build the issue creator window
iss.open_reporter()  
```

## error reporter
`simple-issue-creator` can automatically report your errors:
using `try\\except`:
```python
try:
    1/0 # raise ZeroDivisionError
except ZeroDivisionError:
    iss.error(*sys.exc_info()) # open github issue
```
or using sys.excepthook (place this at the top of the file and this will automatically report for all exceptions after that):
```python
sys.excepthook = iss.error
1/0 # do not copy this line - its example for raising error
```

## Author
matan h

## License
This project is licensed under the MIT License.
