import inspect
import inquirer


def function_argument_panel(func, use_default=False, func_arg_parent=None):
    """use inquirer panel to let user input function parameter or just use default value"""

    if len(inspect.getfullargspec(func).args) > 0:
        print("Input function parameter")
        arg_len = len(inspect.getfullargspec(func).args)
        def_len = len(inspect.getfullargspec(func).defaults)
        arg_w_def = zip(inspect.getfullargspec(func).args[arg_len - def_len:],
                        inspect.getfullargspec(func).defaults)
        if use_default:
            return dict(arg_w_def)

        inquirer_list = []
        for k, v in arg_w_def:
            if v is not None:
                if callable(v):
                    msg = k
                    inquirer_list.append(inquirer.List(k, message=msg, choices=v(func_arg_parent)))
                elif isinstance(v, list):
                    msg = k
                    inquirer_list.append(inquirer.List(k, message=msg, choices=v))
                elif isinstance(v, bool):
                    msg = k
                    inquirer_list.append(inquirer.List(k, message=msg, choices=[True, False]))
                else:
                    if isinstance(v, float) and 0 < v < 1:  # probability
                        msg = k + " (between 0-1)"
                    elif isinstance(v, float) or isinstance(v, int):  # number
                        msg = k + " (number)"
                    else:
                        msg = k
                    inquirer_list.append(inquirer.Text(k, message=msg, default=v))
        predict_parameter = inquirer.prompt(inquirer_list)
        return predict_parameter
    else:
        return dict()
