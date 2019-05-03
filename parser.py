from lark import Lark

type_syntax = '''data_type: primitive_type
  | array_type
  | map_type
  | row_type

!primitive_type: "tinyint"
  | "smallint"
  | "integer"
  | "bigint"
  | "boolean"
  | "real"
  | "double"
  | "date"
  | "time"
  | "timestamp"
  | "varchar"
  | "char"
  | "varbinary"
  | "json"
  | DECIMAL

array_type: "array(" data_type ")"

map_type: "map(" data_type ", " data_type ")"
  | "map(" data_type "," data_type ")"

row_type: "row(" (CNAME " " data_type ", ")* CNAME" "data_type")"
  | "row(" (CNAME " " data_type ",")* CNAME" "data_type")"

DECIMAL: "decimal("INT","INT")"

INT: /[0-9]+/
CNAME: /[^\s`]+/  // column name: any non-whitespace char or anything between "`"
  | /`[^`]*`/
'''

type_parser = Lark(type_syntax, start='data_type')

# from lark.tree import pydot__tree_to_png
