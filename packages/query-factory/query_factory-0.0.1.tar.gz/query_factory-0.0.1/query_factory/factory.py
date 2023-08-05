import yaml

from . import exceptions


class SQLQueryFactory:
    def __init__(self, template_path):
        self._template_path = template_path
        self._query = None
        self._variables = None
        self._load_template(template_path)

    def __call__(self, **kwargs):
        return self.get_query_with(**kwargs)

    def get_query_with(self, **kwargs):
        self._check_kwargs(**kwargs)
        return self._query.format(**kwargs)

    def _load_template(self, path):
        with open(path) as _f:
            template = yaml.load(_f, Loader=yaml.FullLoader)
        try:
            self._query = template["query_template"]
            self._variables = template["variables"]
        except KeyError as err:
            raise exceptions.MalformedTemplate(f"Missing {err}")
        if not self._query:
            raise exceptions.NoOrEmptyQueryException(f"Invalid query: '{self._query}'")

    def _check_kwargs(self, **kwargs):
        if set(kwargs) != set(self._variables):
            missing = set(self._variables) - set(kwargs)
            extra = set(kwargs) - set(self._variables)
            raise exceptions.MissingOrExtraVariableException(
                f"Wrong varibales passed. MISSING: {missing}, EXTRA: {extra}."
            )
