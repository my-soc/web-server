def core_print(args):
    return args['value']


class Connector:
    def __init__(self, params=None):
        self.params = params

    def execute(self, command, args):
        print(self.params)
        if command == "Print":
            return core_print(args)
