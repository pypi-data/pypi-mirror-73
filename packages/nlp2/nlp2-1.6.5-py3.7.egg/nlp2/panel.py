import inspect
import inquirer


def function_argument_panel(func, use_default=False, func_arg_parent=None, show_func_name=False):
    """use inquirer panel to let user input function parameter or just use default value"""
    fname = func.__name__
    if len(inspect.getfullargspec(func).args) > 0:
        arg_len = len(inspect.getfullargspec(func).args)
        def_len = len(inspect.getfullargspec(func).defaults)
        arg_w_def = zip(inspect.getfullargspec(func).args[arg_len - def_len:],
                        inspect.getfullargspec(func).defaults)
        if use_default:
            return dict(arg_w_def)

        inquirer_list = []
        for k, v in arg_w_def:
            if v is not None:
                msg = fname + " " + k if show_func_name else k
                if callable(v):
                    inquirer_list.append(inquirer.List(k, message=msg, choices=v(func_arg_parent)))
                elif isinstance(v, list):
                    inquirer_list.append(inquirer.List(k, message=msg, choices=v))
                elif isinstance(v, bool):
                    inquirer_list.append(inquirer.List(k, message=msg, choices=[True, False]))
                else:
                    if isinstance(v, float) and 0 < v < 1:  # probability
                        msg += " (between 0-1)"
                    elif isinstance(v, float) or isinstance(v, int):  # number
                        msg += " (number)"
                    inquirer_list.append(inquirer.Text(k, message=msg, default=v))
        predict_parameter = inquirer.prompt(inquirer_list)
        return predict_parameter
    else:
        return dict()
