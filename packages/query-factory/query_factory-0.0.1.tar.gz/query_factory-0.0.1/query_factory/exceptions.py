class MalformedTemplate(Exception):
    """Raise when yaml template does not meet requirements."""


class NoOrEmptyQueryException(Exception):
    """Raise when templator has no query or empty query."""


class MissingOrExtraVariableException(Exception):
    """Raise when templator is given more or less variables than explicitly specified in template."""
