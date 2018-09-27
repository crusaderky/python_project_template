"""TODO

A module that lets you say Hello world
"""


def hello(french=False):
    """Say hello world!

    :param bool french:
        If True, speak in French. If False, speak in English.
    :return:
        A string greeting the user
    :rtype:
        str
    """
    if french:
        return "Bonjour, Monde!"
    return "Hello, World!"
