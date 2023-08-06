import yaml

from jinjasql import JinjaSql

from . import exceptions


class SQLQueryFactory:
    """
    SQL query factory to variabilize some query with various parameters on the go.

    Args:
        template_path (path-like): Template location.
        param_style (str): Style to use depending on you SQL query engine.
            See https://github.com/hashedin/jinjasql#multiple-param-styles
    """

    def __init__(self, template_path, param_style="format"):
        self._template_path = template_path
        self._query = None
        self._variables = None
        self.required_variables = None
        self.optional_variables = None

        self._load_template(template_path)
        self._jinjasql = JinjaSql(param_style=param_style)

    def __call__(self, **kwargs):
        """Build query with kwargs as data."""
        return self.get_query_with(**kwargs)

    def get_query_with(self, **kwargs):
        """Build query with kwargs as data."""
        self._check_kwargs(**kwargs)
        query, params = self._jinjasql.prepare_query(self._query, data=kwargs)
        return query % tuple(params)

    def describe(self, varname):
        """
        Fetch description provided in template.

        Args:
            varname (str): Varible name available in template.

        Returns:
            str: Description string.
        """
        try:
            specs = self._variables[varname]
        except KeyError as key:
            raise exceptions.NoSpecsForVariable(key)
        return specs.get("description", f"No description for '{varname}'")

    def _load_template(self, path):
        with open(path) as _f:
            template = yaml.load(_f, Loader=yaml.FullLoader)
        try:
            self._query = template["query_template"]
            self._variables = template["variables"]
            self.required_variables = {name: specs for name, specs in self._variables.items()
                                       if specs.get("required", False)}
            self.optional_variables = {name: specs for name, specs in self._variables.items()
                                       if not specs.get("required", False)}
        except KeyError as err:
            raise exceptions.MalformedTemplate(f"Missing key {err}")
        if not self._query:
            raise exceptions.NoOrEmptyQueryException(f"Invalid query: '{self._query}'")

    def _check_kwargs(self, **kwargs):
        """Check completeness and compatibility of kwargs for the current template."""
        if not set(self.required_variables).issubset(kwargs):
            missing = set(self.required_variables) - set(kwargs)
            raise exceptions.MissingOrExtraVariableException(f"Wrong varibales passed. Missing required: {missing}")
        if not set(kwargs).issubset(set(self._variables)):
            extra = set(kwargs) - set(self._variables)
            raise exceptions.MissingOrExtraVariableException(f"Wrong varibales passed. Extras: {extra}")
