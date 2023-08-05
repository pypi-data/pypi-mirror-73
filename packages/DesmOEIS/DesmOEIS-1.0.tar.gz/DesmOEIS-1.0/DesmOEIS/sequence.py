class Sequence():

    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args):
        self._args = args

    @property
    def integers(self):
        return self._integers

    @integers.setter
    def integers(self, integers):
        self._integers = integers

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, results):
        self._results = results

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
