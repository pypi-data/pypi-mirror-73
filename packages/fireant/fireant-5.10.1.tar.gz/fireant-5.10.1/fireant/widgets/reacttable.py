import re
from collections import OrderedDict, defaultdict
from functools import partial

import pandas as pd

from fireant.dataset.fields import (
    DataType,
    Field,
)
from fireant.dataset.filters import ComparisonOperator
from fireant.dataset.totals import (
    DATE_TOTALS,
    NUMBER_TOTALS,
    TEXT_TOTALS,
    TOTALS_MARKERS,
)
from fireant.formats import (
    RAW_VALUE,
    TOTALS_VALUE,
    display_value,
    json_value,
    raw_value,
    return_none,
    safe_value,
)
from fireant.reference_helpers import reference_alias
from fireant.utils import (
    alias_for_alias_selector,
    alias_selector,
    getdeepattr,
    setdeepattr,
    wrap_list,
)
from .base import ReferenceItem
from .pandas import Pandas

TOTALS_LABEL = "Totals"
METRICS_DIMENSION_ALIAS = "metrics"
F_METRICS_DIMENSION_ALIAS = alias_selector(METRICS_DIMENSION_ALIAS)
_display_value = partial(display_value, nan_value="", null_value="")


class FormattingField:
    def __init__(self, metric=None, reference=None, operation=None):
        self.metric = metric
        self.reference = reference
        self.operation = operation

    def get_alias(self):
        if self.reference:
            if self.operation:
                return reference_alias(self.operation, self.reference)
            else:
                return reference_alias(self.metric, self.reference)

        if self.operation:
            return self.operation.alias

        return self.metric.alias


class FormattingConditionRule:
    def __init__(self, field, operator, value, color, covers_row=False):
        self.field = field
        self.operator = operator
        self.value = value
        self.color = color
        self.covers_row = covers_row

    def applies(self, value):
        return ComparisonOperator.eval(value, self.operator, self.value)


def find_rule_to_apply(rules, value):
    for rule in rules:
        if rule.applies(value):
            return rule

    return None


def map_index_level(index, level, func):
    # If the index is empty, do not do anything
    if 0 == index.size:
        return index

    if isinstance(index, pd.MultiIndex):
        values = index.levels[level]
        return index.set_levels(values.map(func), level)

    assert level == 0

    return index.map(func)


class TotalsItem:
    alias = TOTALS_VALUE
    label = TOTALS_LABEL
    prefix = suffix = precision = None


class ReactTable(Pandas):
    """
    This component does not work with react-table out of the box, some customization is needed in order to work with
    the transformed data.

    .. code-block:: jsx

        // A Custom TdComponent implementation is required by Fireant in order to render display values
        const TdComponent = ({
                               toggleSort,
                               className,
                               children,
                               ...rest
                             }) =>
            <div className={classNames('rt-td', className)} role="gridcell" {...rest}>
                {_.get(children, 'display', children.raw) || <span>&nbsp;</span>}
            </div>;

        const FireantReactTable = ({
                                config, // The payload from fireant
                              }) =>
            <ReactTable columns={config.columns}
                        data={config.data}
                        minRows={0}

                        TdComponent={ DashmoreTdComponent}
                        defaultSortMethod={(a, b, desc) => ReactTableDefaults.defaultSortMethod(a.raw, b.raw, desc)}>
            </ReactTable>;
    """
    def __init__(
        self,
        metric,
        *metrics: Field,
        pivot=(),
        hide=(),
        transpose=False,
        sort=None,
        ascending=None,
        max_columns=None,
        formatting_rules=(),
    ):
        super(ReactTable, self).__init__(
            metric,
            *metrics,
            pivot=pivot,
            hide=hide,
            transpose=transpose,
            sort=sort,
            ascending=ascending,
            max_columns=max_columns
        )
        self.formatting_rules_map = defaultdict(list)
        for formatting_rule in formatting_rules:
            field_selector = alias_selector(formatting_rule.field.get_alias())
            self.formatting_rules_map[field_selector].append(formatting_rule)

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__, ",".join(str(m) for m in self.items)
        )

    @staticmethod
    def map_hyperlink_templates(df, dimensions):
        """
        Creates a mapping for each dimension to it's hyperlink template if it is possible to create the hyperlink
        template for it.

        The hyperlink template is a URL-like string containing curley braces enclosing dimension keys: `{dimension}`.
        While rendering this widget, the dimension key placeholders need to be replaced with the dimension values for
        that row.

        :param df:
            The result data set that is being transformed. The data frame SHOULD be pivoted/transposed if that step is
            required, before calling this function, in order to prevent the template from being included for the
            dimension if one of the required dimensions is pivoted.
        :param dimensions:
            The list of dimensions included in the query that created the result data set df.
        :return:
            A dict with the dimension key as the key and the hyperlink template as the value. Templates will only be
            included if it will be possible to fill in the required parameters.
        """
        hyperlink_templates = {}
        pattern = re.compile(r"{[^{}]+}")

        for dimension in dimensions:
            hyperlink_template = dimension.hyperlink_template
            if hyperlink_template is None:
                continue

            required_hyperlink_parameters = [
                alias_selector(argument[1:-1])
                for argument in pattern.findall(hyperlink_template)
            ]

            # Check that all of the required dimensions are in the result data set. Only include the hyperlink template
            # in the return value of this function if all are present.
            unavailable_hyperlink_parameters = set(required_hyperlink_parameters) & set(
                df.index.names
            )
            if not unavailable_hyperlink_parameters:
                continue

            # replace the dimension keys with the formatted values. This will come in handy later when replacing the
            # actual values
            hyperlink_template = hyperlink_template.format(
                **{
                    alias_for_alias_selector(argument): "{" + argument + "}"
                    for argument in required_hyperlink_parameters
                }
            )

            f_dimension_alias = alias_selector(dimension.alias)
            hyperlink_templates[f_dimension_alias] = hyperlink_template

        return hyperlink_templates

    @staticmethod
    def format_data_frame(data_frame):
        """
        This function prepares the raw data frame for transformation by formatting dates in the index and removing any
        remaining NaN/NaT values. It also names the column as metrics so that it can be treated like a dimension level.

        :param data_frame:
            The result set data frame
        :param dimensions:
        :return:
        """
        data_frame = data_frame.copy()
        data_frame.columns.name = F_METRICS_DIMENSION_ALIAS
        return data_frame

    @staticmethod
    def transform_index_column_headers(data_frame, field_map, hide_dimension_aliases):
        """
        Convert the un-pivoted dimensions into ReactTable column header definitions.

        :param data_frame:
            The result set data frame.
        :param field_map:
            A map to find metrics/operations based on their keys found in the data frame.
        :param hide_dimension_aliases:
            A set with hide dimension aliases.
        :return:
            A list of column header definitions with the following structure.

        .. code-block:: jsx

            columns = [{
              Header: 'Column A',
              accessor: 'a',
            }, {
              Header: 'Column B',
              accessor: 'b',
            }]
        """
        columns = []
        if (
            not isinstance(data_frame.index, pd.MultiIndex)
            and data_frame.index.name is None
        ):
            return columns

        for f_dimension_alias in data_frame.index.names:
            if f_dimension_alias not in field_map or f_dimension_alias in hide_dimension_aliases:
                continue

            dimension = field_map[f_dimension_alias]
            header = getattr(dimension, "label", dimension.alias)

            columns.append(
                {
                    "Header": json_value(header),
                    "accessor": safe_value(f_dimension_alias),
                }
            )

        return columns

    @staticmethod
    def transform_data_column_headers(data_frame, field_map):
        """
        Convert the metrics into ReactTable column header definitions. This includes any pivoted dimensions, which will
        result in multiple rows of headers.

        :return:
        :param data_frame:
            The result set data frame.
        :param field_map:
            A map to find metrics/operations based on their keys found in the data frame.
        :return:
            A list of column header definitions with the following structure.

        .. code-block:: jsx

            columns = [{
              Header: 'Column A',
              columns: [{
                Header: 'SubColumn A.0',
                accessor: 'a.0',
              }, {
                Header: 'SubColumn A.1',
                accessor: 'a.1',
              }]
            }, {
              Header: 'Column B',
              columns: [
                ...
              ]
            }]
        """

        def get_header(column_value, f_dimension_alias, is_totals):
            if f_dimension_alias == F_METRICS_DIMENSION_ALIAS or is_totals:
                item = field_map[column_value]
                return getattr(item, "label", item.alias)

            if f_dimension_alias in field_map:
                field = field_map[f_dimension_alias]
                return _display_value(column_value, field) or safe_value(column_value)

            if f_dimension_alias is None:
                return ""

            return safe_value(column_value)

        def _make_columns(columns_frame, previous_level_values=()):
            """
            This function recursively creates the individual column definitions for React Table with the above tree
            structure depending on how many index levels there are in the columns.

            :param columns_frame:
                A data frame representing the columns of the result set data frame.
            :param previous_level_values:
                A tuple containing the higher level index level values used for building the data accessor path
            """
            f_dimension_alias = columns_frame.index.names[0]

            # Group the columns if they are multi-index so we can get the proper sub-column values. This will yield
            # one group per dimension value with the group data frame containing only the relevant sub-columns
            groups = (
                columns_frame.groupby(level=0)
                if isinstance(columns_frame.index, pd.MultiIndex)
                else [(level, None) for level in columns_frame.index]
            )

            columns = []
            for column_value, group in groups:
                is_totals = column_value in TOTALS_MARKERS | {TOTALS_LABEL}

                # All column definitions have a header
                column = {
                    "Header": get_header(column_value, f_dimension_alias, is_totals)
                }

                level_values = previous_level_values + (column_value,)
                if group is not None:
                    # If there is a group, then drop this index level from the group data frame and recurse to build
                    # sub column definitions
                    next_level_df = group.reset_index(level=0, drop=True)
                    column["columns"] = _make_columns(next_level_df, level_values)

                else:
                    column["accessor"] = ".".join(
                        safe_value(value) for value in level_values
                    )

                if is_totals:
                    column["className"] = "fireant-totals"

                columns.append(column)

            return columns

        # If the query only has a single metric, that level will be dropped, and set as data_frame.name
        dropped_metric_level_name = (
            (data_frame.name,) if hasattr(data_frame, "name") else ()
        )

        return _make_columns(data_frame.columns.to_frame(), dropped_metric_level_name)

    @staticmethod
    def transform_row_index(index_values, field_map, dimension_hyperlink_templates, hide_dimension_aliases, row_color):
        # Add the index to the row
        row = {}
        for key, value in index_values.items():
            if key is None or key not in field_map:
                continue

            field_alias = key
            field = field_map[field_alias]

            data = {RAW_VALUE: raw_value(value, field)}
            display = _display_value(value, field)
            if display is not None:
                data["display"] = display
            if row_color is not None:
                data["color"] = row_color

            # If the dimension has a hyperlink template, then apply the template by formatting it with the dimension
            # values for this row. The values contained in `index_values` will always contain all of the required values
            # at this point, otherwise the hyperlink template will not be included.
            if key in dimension_hyperlink_templates:
                try:
                    data["hyperlink"] = dimension_hyperlink_templates[key].format(
                        **index_values
                    )
                except KeyError:
                    pass

            safe_key = safe_value(key)
            row[safe_key] = data

        for dimension_alias in hide_dimension_aliases:
            del row[dimension_alias]

        return row

    @staticmethod
    def _get_row_value_accessor(series, fields, key):
        index_names = series.index.names or []

        accessor_fields = [
            fields[field_alias]
            for field_alias in index_names
            if field_alias is not None
        ]
        accessor = [
            safe_value(value) for value, field in zip(key, accessor_fields)
        ] or key

        return accessor

    def transform_row_values(self, series, fields, is_transposed, is_pivoted):
        row = {}
        row_color = None

        for key, value in series.items():
            key = wrap_list(key)

            # Get the field for the metric
            metric_alias = wrap_list(series.name)[0] if is_transposed else key[0]
            field = fields[metric_alias]
            data = {
                RAW_VALUE: raw_value(value, field),
            }
            if not row_color:
                # No color for this field yet
                rule = find_rule_to_apply(self.formatting_rules_map[metric_alias], value)
                if rule is not None:
                    data["color"] = rule.color
                    if not is_transposed and not is_pivoted and rule.covers_row:
                        # No transposing or pivoting going on so set as row color if it's specified for the rule
                        row_color = rule.color

            display = _display_value(value, field, date_as=return_none)
            if display is not None:
                data["display"] = display

            accessor = self._get_row_value_accessor(series, fields, key)
            setdeepattr(row, accessor, data)

        # Assign the row color to fields that don't have a color yet
        if row_color:
            for key in series.keys():
                accessor = self._get_row_value_accessor(series, fields, wrap_list(key))
                data = getdeepattr(row, accessor)
                if "color" not in data:
                    data["color"] = row_color

        return row, row_color

    def transform_data(
        self, data_frame, field_map, hide_dimensions, dimension_hyperlink_templates, is_transposed, is_pivoted,
    ):
        """
        Builds a list of dicts containing the data for ReactTable. This aligns with the accessors set by
        #transform_dimension_column_headers and #transform_metric_column_headers

        :param data_frame:
            The result set data frame.
        :param field_map:
            A mapping to all the fields in the dataset used for this query.
        :param hide_dimensions:
            A set with hide dimension aliases.
        :param dimension_hyperlink_templates:
            A mapping to fields and its hyperlink dimension, if any.
        :param is_transposed:
            Whether the table is transposed or not.
        :param is_pivoted:
            Whether the table is pivoted or not.
        """
        index_names = data_frame.index.names

        def _get_field_label(alias):
            if alias not in field_map:
                return alias

            field = field_map[alias]
            return getattr(field, "label", field.alias)

        # If the metric column was dropped due to only having a single metric, add it back here so the
        # formatting can be applied.
        if hasattr(data_frame, "name"):
            metric_alias = data_frame.name
            data_frame = pd.concat(
                [data_frame],
                keys=[metric_alias],
                names=[F_METRICS_DIMENSION_ALIAS],
                axis=1,
            )

        rows = []
        for index, series in data_frame.iterrows():
            index = wrap_list(index)

            # Get a list of values from the index. These can be metrics or dimensions so it checks in the item map if
            # there is a display value for the value
            index_values = (
                [_get_field_label(value) for value in index] if is_transposed else index
            )
            index_display_values = OrderedDict(zip(index_names, index_values))

            row_values, row_color = self.transform_row_values(series, field_map, is_transposed, is_pivoted)
            row_index = self.transform_row_index(
                index_display_values, field_map, dimension_hyperlink_templates, hide_dimensions, row_color
            )
            rows.append(
                {
                    **row_index,
                    **row_values,
                }
            )

        return rows

    def transform(
        self,
        data_frame,
        dimensions,
        references,
        annotation_frame=None,
        use_raw_values=False,
    ):
        """
        Transforms a data frame into a format for ReactTable. This is an object containing attributes `columns` and
        `data` which align with the props in ReactTable with the same name.

        :param data_frame:
            The result set data frame.
        :param dimensions:
            A list of dimensions that were selected in the data query.
        :param references:
            A list of references that were selected in the data query.
        :param annotation_frame:
            A data frame containing the annotation data.
        :param use_raw_values:
            Don't add prefix or postfix to values.
        :return:
            An dict containing attributes `columns` and `data` which align with the props in ReactTable with the same
            names.
        """
        result_df = data_frame.copy()

        dimension_map = {
            alias_selector(dimension.alias): dimension for dimension in dimensions
        }

        metric_map = OrderedDict(
            [
                (
                    alias_selector(reference_alias(item, ref)),
                    ReferenceItem(item, ref) if ref is not None else item,
                )
                for item in self.items
                for ref in [None] + references
            ]
        )

        field_map = {
            **metric_map,
            **dimension_map,
            # Add an extra item to map the totals markers to it's label
            NUMBER_TOTALS: TotalsItem,
            TEXT_TOTALS: TotalsItem,
            DATE_TOTALS: TotalsItem,
            TOTALS_LABEL: TotalsItem,
            alias_selector(METRICS_DIMENSION_ALIAS): Field(
                METRICS_DIMENSION_ALIAS, None, data_type=DataType.text, label=""
            ),
        }
        metric_aliases = list(metric_map.keys())

        hide_dimensions = {
            alias_selector(dimension.alias) for dimension in self.hide
        }

        pivot_dimensions = [
            alias_selector(dimension.alias)
            for dimension in self.pivot
            if alias_selector(dimension.alias) not in hide_dimensions
        ]

        result_df = self.format_data_frame(result_df[metric_aliases])
        result_df, is_pivoted, is_transposed = self.pivot_data_frame(result_df, pivot_dimensions, self.transpose)
        dimension_columns = self.transform_index_column_headers(result_df, field_map, hide_dimensions)
        metric_columns = self.transform_data_column_headers(result_df, field_map)

        data = self.transform_data(
            result_df,
            field_map,
            hide_dimensions=hide_dimensions,
            dimension_hyperlink_templates=self.map_hyperlink_templates(result_df, dimensions),
            is_transposed=is_transposed,
            is_pivoted=is_pivoted,
        )

        return {"columns": dimension_columns + metric_columns, "data": data}
