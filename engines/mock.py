import logging


def params():
    return {}


def args():
    return {}


def command():
    return "ok"


def results(result):
    return result


def info(msg, *args):
    logging.getLogger().info(msg, *args)


def error(msg, *args):
    # print to stdout so pytest fail if not mocked
    print(msg, *args)


def debug(msg, *args):
    logging.getLogger().info(msg, *args)