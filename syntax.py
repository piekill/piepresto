# syntax.py

from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter


def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages
STYLES = {
    'keyword': format('blue'),
    'operator': format('red'),
    'brace': format('darkGray'),
    'constant': format('black', 'bold'),
    'string': format('magenta'),
    'string2': format('darkMagenta'),
    'comment': format('darkGreen', 'italic'),
    'function': format('darkCyan', 'italic'),
    'numbers': format('brown'),
}


class PrestoHighlighter (QSyntaxHighlighter):
    """Syntax highlighter for Presto SQL.
    """
    # keywords
    keywords = [
        'alter', 'as', 'by', 'case', 'constraint', 'create', 'cross', 'cube',
        'deallocate', 'delete', 'describe', 'distinct', 'drop', 'else', 'end',
        'escape', 'except', 'execute', 'exists', 'extract', 'for', 'from',
        'full', 'group', 'grouping', 'having', 'inner', 'insert', 'intersect',
        'into', 'join', 'left', 'natural', 'normalize', 'on', 'order', 'outer',
        'prepare', 'recursive', 'right', 'rollup', 'select', 'show', 'table',
        'then', 'uescape', 'union', 'using', 'values', 'when', 'where', 'with']

    # functions
    functions = [
        'abs', 'acos', 'approx_distinct', 'approx_percentile', 'approx_set',
        'arbitrary', 'array_agg', 'array_distinct', 'array_except',
        'array_intersect', 'array_join', 'array_max', 'array_min',
        'array_position', 'array_remove', 'array_sort', 'array_union',
        'arrays_overlap', 'asin', 'atan', 'atan2', 'avg', 'bar', 'beta_cdf',
        'cardinality', 'cast', 'cbrt', 'ceil', 'ceiling', 'char2hexint',
        'checksum', 'chr', 'classify', 'coalesce', 'codepoint', 'color',
        'concat', 'contains', 'convex_hull_agg', 'corr', 'cos', 'cosh',
        'cosine_similarity', 'count', 'count_if', 'covar_pop', 'covar_samp',
        'crc32', 'cume_dist', 'current_date', 'current_path', 'current_time',
        'current_timestamp', 'current_timezone', 'current_user', 'date',
        'date_add', 'date_diff', 'date_format', 'date_parse', 'date_trunc',
        'day', 'day_of_month', 'day_of_week', 'day_of_year', 'degrees',
        'dense_rank', 'dow', 'doy', 'e', 'element_at', 'empty_approx_set',
        'evaluate_classifier_predictions', 'every', 'exp', 'features',
        'filter', 'first_value', 'flatten', 'floor', 'great_circle_distance',
        'greatest', 'hamming_distance', 'hash_counts', 'histogram', 'hmac_md5',
        'hmac_sha1', 'hmac_sha256', 'hmac_sha512', 'hour', 'index', 'infinity',
        'intersection_cardinality', 'inverse_beta_cdf', 'inverse_normal_cdf',
        'is_finite', 'is_infinite', 'is_json_scalar', 'is_nan',
        'jaccard_index', 'json_array_contains', 'json_array_get',
        'json_array_length', 'json_extract', 'json_extract_scalar',
        'json_format', 'json_parse', 'json_size', 'kurtosis', 'lag',
        'last_value', 'lead', 'learn_classifier', 'learn_libsvm_classifier',
        'learn_libsvm_regressor', 'learn_regressor', 'least', 'length',
        'levenshtein_distance', 'like_pattern', 'line_locate_point', 'ln',
        'localtime', 'localtimestamp', 'log10', 'log2', 'lower', 'lpad',
        'ltrim', 'make_set_digest', 'map', 'map_agg', 'map_concat',
        'map_entries', 'map_filter', 'map_from_entries', 'map_keys',
        'map_union', 'map_values', 'map_zip_with', 'max', 'max_by', 'md5',
        'merge', 'merge_set_digest', 'millisecond', 'min', 'min_by', 'minute',
        'mod', 'nullif', 'parse_presto_data_size', 'qdigest_agg', 'quarter',
        'radians', 'rand', 'random', 'rank', 'reduce', 'reduce_agg',
        'regexp_extract', 'regexp_extract_all', 'regexp_like',
        'regexp_replace', 'regexp_split', 'regr_intercept', 'regr_slope',
        'regress', 'render', 'repeat', 'replace', 'reverse', 'rgb', 'round',
        'row_number', 'rpad', 'rtrim', 'second', 'sequence', 'sha1', 'sha256',
        'sha512', 'shuffle', 'sign', 'simplify_geometry', 'sin', 'skewness',
        'slice', 'spatial_partitioning', 'spatial_partitions', 'split',
        'split_part', 'split_to_map', 'split_to_multimap', 'spooky_hash_v2_32',
        'spooky_hash_v2_64', 'sqrt', 'ST_Area', 'ST_AsBinary', 'ST_AsText',
        'ST_Boundary', 'ST_Buffer', 'ST_Centroid', 'ST_Contains',
        'ST_ConvexHull', 'ST_CoordDim', 'ST_Crosses', 'ST_Difference',
        'ST_Dimension', 'ST_Disjoint', 'ST_Distance', 'ST_EndPoint',
        'ST_Envelope', 'ST_EnvelopeAsPts', 'ST_Equals', 'ST_SymDifference',
        'ST_Touches', 'ST_Union', 'ST_Within', 'ST_X', 'ST_XMax', 'ST_XMin',
        'ST_Y', 'ST_YMax', 'ST_YMin', 'stddev', 'stddev_pop', 'stddev_samp',
        'strpos', 'substr', 'substring', 'sum', 'tan', 'tanh', 'timezone_hour',
        'timezone_minute', 'to_base', 'to_base64', 'to_base64url',
        'to_big_endian_32', 'to_big_endian_64', 'to_char', 'to_date',
        'to_geometry', 'to_hex', 'to_ieee754_32', 'to_ieee754_64',
        'to_iso8601', 'to_milliseconds', 'to_spherical_geography',
        'to_timestamp', 'to_unixtime', 'to_utf8', 'transform',
        'transform_keys', 'transform_values', 'trim', 'truncate', 'try',
        'try_cast', 'typeof', 'unnest', 'upper', 'url_decode', 'url_encode',
        'url_extract_fragment', 'url_extract_host', 'url_extract_parameter',
        'url_extract_path', 'url_extract_port', 'url_extract_protocol',
        'url_extract_query', 'uuid', 'value_at_quantile',
        'values_at_quantiles', 'var_pop', 'var_samp', 'variance', 'week',
        'week_of_year', 'width_bucket', 'wilson_interval_lower',
        'wilson_interval_upper', 'word_stem', 'xxhash64', 'year_of_week',
        'yearcast', 'yow', 'zip', 'zip_with']

    # constants
    constants = [
        'false', 'null', 'true'
    ]

    # operators
    operators = [
        '=', '->'
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        r'\+', '-', r'\*', '/', '//', r'\%', r'\*\*',
        # In-place
        r'\+=', '-=', r'\*=', '/=', r'\%=',
        # Bitwise
        r'\^', r'\|', r'\&', r'\~', '>>', '<<',
        ' and ', ' between ', ' in ', ' is ', ' like ', ' not ', ' or '
    ]

    # braces
    braces = [
        r'\{', r'\}', r'\(', r'\)', r'\[', r'\]',
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])

        rules = []

        # Keyword, function, constant, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in PrestoHighlighter.keywords]
        rules += [(r'\b%s\b' % f, 0, STYLES['function'])
                  for f in PrestoHighlighter.functions]
        rules += [(r'\b%s\b' % c, 0, STYLES['constant'])
                  for c in PrestoHighlighter.constants]
        rules += [(r'%s' % o, 0, STYLES['operator'])
                  for o in PrestoHighlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
                  for b in PrestoHighlighter.braces]

        # All other rules
        rules += [
            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # From '--' until a newline
            (r'--[^\n]*', 0, STYLES['comment']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b',
             0, STYLES['numbers']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat, Qt.CaseInsensitive), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = text.length() - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False
