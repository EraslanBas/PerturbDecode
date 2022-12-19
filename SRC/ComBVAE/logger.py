import logging
import os

def setup_logger(name, save_dir):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(os.path.join(save_dir, '%s_info.log' % name))
    fh.setLevel(logging.INFO)

    fh_debug = logging.FileHandler(os.path.join(save_dir, '%s_debug.log' % name))
    fh_debug.setLevel(logging.DEBUG)

    logger.addHandler(fh)
    logger.addHandler(fh_debug)

    return logger
