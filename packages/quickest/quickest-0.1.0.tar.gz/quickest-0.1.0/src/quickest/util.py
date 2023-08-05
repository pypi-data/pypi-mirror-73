import logging 
import numpy as np


def get_change_logger(LOGFILE):

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)03d %(name)-16s %(levelname)-8s %(message)s',
                        datefmt='%d-%m-%y %H:%M:%S',
                        filename=LOGFILE,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger('change.app')
    return logger

def print_progress_bar(current_step, total_steps, width=100):
    progress_bar_ticks = int(np.floor((current_step / total_steps) * width))
    progress_bar_spaces = width - progress_bar_ticks - 1
    percentage = int(np.ceil(float(current_step) / float(total_steps) * 100))

    if current_step == total_steps - 1:
        endchar = "\n"
    else:
        endchar = "\r"
    percentage_spacing = 3 - len(str(percentage))

    print(
        "|{}>{}| [{}{}%]".format(
            progress_bar_ticks * "-",
            progress_bar_spaces * " ",
            percentage_spacing * " ",
            percentage,
        ),
        end=endchar, flush=True
    )
