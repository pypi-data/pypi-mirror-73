import os


def _prepend_hydra_prefix(path):
    """Hydra creates a working directory depending on the time stamps.
       The format is:
            outputs/*-*-*/*-*-*/
       This makes it inconvenient to pass relative paths arguments as
       the relative paths will be evaluated from the working directory.

       This function prepends a prefix to the relative path to move out
       of the current working directory into the directory where the cli
       was initially executed. It then turns the relative path into an 
       absolute path and returns it.
    """
    path = os.path.join('../../../', path)
    return os.path.abspath(path)


def fix_input_path(path):
    """Fix broken relative paths.

    """
    if not os.path.isabs(path):
        path = _prepend_hydra_prefix(path)
    return path
