from django.shortcuts import render
from code_rate import forms
from pycodestyle import Checker
import os
import io
from contextlib import redirect_stdout


def format_output(issues):
    strip_length_at_beginning = len('source_code.py:')
    issues = '\n'.join(line[strip_length_at_beginning:] for line in issues.split('\n'))
    issues_list = []
    for line in issues.split('\n'):
        if line:
            line_elements = line.split(':')
            issues_list.append({"line": line_elements[0], "column": line_elements[1], "error": line_elements[2]})
    response_string = [
        "Line:{} Column:{}: Error: {}".format(issue["line"], issue["column"], issue["error"]) for issue in issues_list
    ]
    response_string = "\n".join(response_string)
    return response_string


def rate(request):
    if request.method == 'POST':
        form = forms.CodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        with open("source_code.py", "w") as file:
            file.write(data["code"])
        checker = Checker('source_code.py')
        output = io.StringIO()
        with redirect_stdout(output):
            checker.check_all()
        os.remove("source_code.py")
        issues = output.getvalue()
        response_string = format_output(issues)
        return render(request, 'rate_form.html', {
            'form': form,
            'message': 'Checking done!',
            'code': data["code"],
            'response_string': response_string,
        })
    else:
        form = forms.CodeForm

    return render(request, 'rate_form.html', {'form': form, 'message': "Let's rate your code."})
