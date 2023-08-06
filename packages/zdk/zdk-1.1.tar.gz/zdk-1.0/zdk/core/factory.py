class Factory:
    """
    dinamic instance creator
    """

    def __init__(self, instance=None, base=None):
        self.base = base
        self.instance = instance

    def get_instance(self):
        if not self.instance:
            raise ("Fail Factoryn, can't create intance")

        parts = f"{self.base}.{self.instance}".split('.')
        module_name = ".".join(parts[:-1])
        module = __import__(module_name)
        for comp in parts[1:]:
            module = getattr(module, comp)
        return module
