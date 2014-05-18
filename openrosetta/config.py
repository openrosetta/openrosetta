from cornice import Service

default_cors_policy = {'origins': ('*', )}


class RService(Service):
    def __init__(self, name, path, description=None, cors_policy=default_cors_policy, **kw):
        # To work properly with venusian, we have to specify the number of
        # frames between the call to venusian.attach and the definition of
        # the attached function. Cornice defaults to 1, and we add another.
        depth = 2
        super(RService, self).__init__(name, path, description=description, cors_policy=cors_policy,
                                       depth=depth, **kw)
