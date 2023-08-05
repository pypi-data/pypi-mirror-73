import inspect
import inquirer
import sys


class Panel:
    def __init__(self):
        in_jupyter = sys.argv[-1].endswith('json')
        self.in_jupyter = in_jupyter
        self.element_list = []
        self.key_list = []
        self.result_dict = {}

    def add_element(self, k, v, msg):
        if isinstance(v, float) and 0 < v < 1:  # probability
            msg += " (between 0-1)"
        elif isinstance(v, float) or isinstance(v, int):  # number
            msg += " (number)"

        if not self.in_jupyter:
            if isinstance(v, list):
                self.element_list.append(inquirer.List(k, message=msg, choices=v))
            else:
                self.element_list.append(inquirer.Text(k, message=msg, default=v))
        else:
            if isinstance(v, list):
                selected = ''
                while selected not in [str(e) for e in v]:
                    selected = input(msg + ", input an item in the list " + str(v) + ": ")
                self.element_list.append(selected)
            else:
                self.element_list.append(input(msg + ", [default=" + str(v) + "]: "))
        self.key_list.append(k)

    def show_panel(self):
        if not self.in_jupyter:
            self.result_dict = inquirer.prompt(self.element_list)

    def get_result_dict(self):
        if not self.in_jupyter:
            return self.result_dict
        else:
            return dict(zip(self.key_list, self.element_list))


def function_get_all_arg(func):
    if len(inspect.getfullargspec(func).args) > 0:
        arg_len = len(inspect.getfullargspec(func).args)
        def_len = len(inspect.getfullargspec(func).defaults)
        return inspect.getfullargspec(func).args[arg_len - def_len:]
    else:
        return []


def function_check_wrong_arg(func, input_arg):
    all_arg = function_get_all_arg(func)
    return [arg for arg in input_arg if arg not in all_arg]


def function_check_missing_arg(func, input_arg):
    all_arg = function_get_all_arg(func)
    return [arg for arg in all_arg if arg not in input_arg]


def function_argument_panel(func, inputted_arg={}, disable_input_panel=False, ignore_empty=False,
                            func_parent=None, show_func_name=False):
    """use inquirer panel to let user input function parameter or just use default value"""
    fname = func.__name__
    if len(inspect.getfullargspec(func).args) > 0 and inspect.getfullargspec(func).defaults is not None:
        arg_len = len(inspect.getfullargspec(func).args)
        def_len = len(inspect.getfullargspec(func).defaults)
        arg_w_def = zip(inspect.getfullargspec(func).args[arg_len - def_len:],
                        inspect.getfullargspec(func).defaults)
        # merge two dict
        def_arg = dict(arg_w_def)
        function_def_arg = {**def_arg, **inputted_arg}
        # panel
        panel = Panel()
        for k, v in def_arg.items():
            if v is not None and (isinstance(v, bool) or len(v) > 0 or not ignore_empty):
                msg = fname + " " + k if show_func_name else k
                if callable(v):
                    v = v(func_parent)
                    function_def_arg[k] = v(func_parent)[0]  # set default value
                elif isinstance(v, bool):
                    v = [True, False]
                elif isinstance(v, float) and 0 < v < 1:  # probability
                    msg += " (between 0-1)"
                elif isinstance(v, float) or isinstance(v, int):  # number
                    msg += " (number)"
                panel.add_element(k, v, msg)

        if not disable_input_panel:
            panel.show_panel()
            function_def_arg.update(panel.get_result_dict())
        return function_def_arg
    else:
        return inputted_arg
