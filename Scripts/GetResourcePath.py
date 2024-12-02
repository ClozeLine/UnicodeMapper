import os
import sys


def get_resource_path(filename):
    """
    Gets the correct for bundles/non-bundled environments
    :param filename: name of desired file
    :return: filepath
    """

    def get_meipass():
        return getattr(sys, "_MEIPASS", None)

    if hasattr(sys, '_MEIPASS'):  # noqa: E1101
        return os.path.join(get_meipass(), filename)
    else:
        return os.path.join(os.path.dirname(__file__), filename)
