class NullIdentifiers(Exception):
    def __init__(self):
        super(NullIdentifiers, self).__init__('None Identifier has sent to service.')
