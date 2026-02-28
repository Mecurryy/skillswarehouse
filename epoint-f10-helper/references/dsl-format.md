# DSL Format Reference

Complete reference for Epoint F10 DSL database schema definitions.

## DSL File Location

```
{web_project_path}/{module_name}/DB.DSL
```

Example: `src/main/webapp/example/DB.DSL`

## DSL Structure

```json
[
  {
    "tableId": "table_name_in_snake_case",
    "tableName": "表的中文名称",
    "description": "表的描述信息",
    "codeGroups": [
      {
        "codeGroupName": "代码组名称",
        "codes": [
          {
            "codeLabel": "显示文本",
            "codeValue": "代码值",
            "order": 排序号
          }
        ]
      }
    ],
    "fields": [
      {
        "fieldId": "field_id",
        "fieldName": "字段中文名",
        "fieldType": "nvarchar|nchar|int|bigint|decimal|datetime|text|blob",
        "length": 字段长度(字符串类型),
        "precision": 数字精度,
        "scale": 小数位数,
        "required": true|false,
        "defaultValue": "默认值",
        "formConfig": {
          "colSpan": true|false,
          "show": true|false,
          "widgetType": "textbox|textarea|combobox|datepicker|spinner|checkbox|radio",
          "widgetProps": {},
          "order": 显示顺序,
          "readonly": true|false,
          "disabled": true|false,
          "vtype": "验证类型",
          "maxLength": 最大长度
        },
        "listConfig": {
          "show": true|false,
          "sortable": true|false,
          "searchable": true|false,
          "width": 列宽度,
          "headerAlign": "center|left|right"
        }
      }
    ]
  }
]
```

## Field Types

| fieldType | Description | Length Required | Example |
|-----------|-------------|-----------------|---------|
| `nvarchar` | Variable length string | Yes | `"length": 128` |
| `nchar` | Fixed length string | Yes | `"length": 32` |
| `int` | Integer | No | - |
| `bigint` | Long integer | No | - |
| `decimal` | Decimal number | precision, scale | `"precision": 10, "scale": 2` |
| `datetime` | Date and time | No | - |
| `text` | Long text | No | - |
| `blob` | Binary data | No | - |

## Widget Types (formConfig)

| widgetType | Description | Use For |
|------------|-------------|---------|
| `textbox` | Single line text input | Short strings, codes |
| `textarea` | Multi-line text input | Descriptions, comments |
| `combobox` | Dropdown select | Fixed value options, foreign keys |
| `datepicker` | Date picker | Date fields |
| `spinner` | Number input | Integer, decimal numbers |
| `checkbox` | Checkbox | Boolean values |
| `radio` | Radio buttons | Mutually exclusive options |

## Standard Audit Fields Template

```json
{
  "fieldId": "create_time",
  "fieldName": "创建时间",
  "fieldType": "datetime",
  "required": false,
  "formConfig": {
    "show": false
  },
  "listConfig": {
    "show": true,
    "sortable": true
  }
},
{
  "fieldId": "create_user",
  "fieldName": "创建人",
  "fieldType": "nvarchar",
  "length": 64,
  "required": false,
  "formConfig": {
    "show": false
  },
  "listConfig": {
    "show": true
  }
},
{
  "fieldId": "update_time",
  "fieldName": "更新时间",
  "fieldType": "datetime",
  "required": false,
  "formConfig": {
    "show": false
  },
  "listConfig": {
    "show": true,
    "sortable": true
  }
},
{
  "fieldId": "update_user",
  "fieldName": "更新人",
  "fieldType": "nvarchar",
  "length": 64,
  "required": false,
  "formConfig": {
    "show": false
  },
  "listConfig": {
    "show": true
  }
}
```

## Common Field Patterns

### Primary Key (UUID)

```json
{
  "fieldId": "id",
  "fieldName": "主键ID",
  "fieldType": "nvarchar",
  "length": 32,
  "required": true,
  "formConfig": {
    "show": false,
    "widgetType": "textbox"
  },
  "listConfig": {
    "show": false
  }
}
```

### Status Field (with codeGroups)

```json
{
  "fieldId": "status",
  "fieldName": "状态",
  "fieldType": "nvarchar",
  "length": 2,
  "required": false,
  "formConfig": {
    "show": true,
    "widgetType": "combobox"
  },
  "listConfig": {
    "show": true,
    "sortable": true
  }
}
```

With corresponding codeGroups:

```json
"codeGroups": [
  {
    "codeGroupName": "状态",
    "codes": [
      {"codeLabel": "启用", "codeValue": "01", "order": 1},
      {"codeLabel": "禁用", "codeValue": "02", "order": 2},
      {"codeLabel": "草稿", "codeValue": "03", "order": 3}
    ]
  }
]
```

### Name/Description Fields

```json
{
  "fieldId": "name",
  "fieldName": "名称",
  "fieldType": "nvarchar",
  "length": 128,
  "required": true,
  "formConfig": {
    "show": true,
    "widgetType": "textbox",
    "vtype": "maxLength:128",
    "maxLength": 128
  },
  "listConfig": {
    "show": true,
    "sortable": true,
    "searchable": true,
    "width": 150
  }
},
{
  "fieldId": "description",
  "fieldName": "描述",
  "fieldType": "text",
  "required": false,
  "formConfig": {
    "show": true,
    "widgetType": "textarea"
  },
  "listConfig": {
    "show": false
  }
}
```

### Numeric Fields

```json
{
  "fieldId": "price",
  "fieldName": "价格",
  "fieldType": "decimal",
  "precision": 10,
  "scale": 2,
  "required": false,
  "formConfig": {
    "show": true,
    "widgetType": "spinner",
    "widgetProps": {
      "decimalPlaces": 2,
      "minValue": 0
    }
  },
  "listConfig": {
    "show": true,
    "sortable": true,
    "width": 100
  }
},
{
  "fieldId": "quantity",
  "fieldName": "数量",
  "fieldType": "int",
  "required": false,
  "formConfig": {
    "show": true,
    "widgetType": "spinner",
    "widgetProps": {
      "minValue": 0
    }
  },
  "listConfig": {
    "show": true,
    "sortable": true,
    "width": 80
  }
}
```

## Complete Example

```json
[
  {
    "tableId": "product_info",
    "tableName": "产品信息表",
    "description": "用于存储产品基本信息",
    "codeGroups": [
      {
        "codeGroupName": "状态",
        "codes": [
          {"codeLabel": "上架", "codeValue": "01", "order": 1},
          {"codeLabel": "下架", "codeValue": "02", "order": 2}
        ]
      },
      {
        "codeGroupName": "产品类型",
        "codes": [
          {"codeLabel": "实物", "codeValue": "01", "order": 1},
          {"codeLabel": "服务", "codeValue": "02", "order": 2},
          {"codeLabel": "虚拟", "codeValue": "03", "order": 3}
        ]
      }
    ],
    "fields": [
      {
        "fieldId": "id",
        "fieldName": "主键ID",
        "fieldType": "nvarchar",
        "length": 32,
        "required": true,
        "formConfig": {"show": false, "widgetType": "textbox"},
        "listConfig": {"show": false}
      },
      {
        "fieldId": "product_name",
        "fieldName": "产品名称",
        "fieldType": "nvarchar",
        "length": 128,
        "required": true,
        "formConfig": {
          "show": true,
          "widgetType": "textbox",
          "vtype": "maxLength:128",
          "maxLength": 128,
          "order": 1
        },
        "listConfig": {
          "show": true,
          "sortable": true,
          "searchable": true,
          "width": 200
        }
      },
      {
        "fieldId": "product_code",
        "fieldName": "产品编码",
        "fieldType": "nvarchar",
        "length": 32,
        "required": true,
        "formConfig": {
          "show": true,
          "widgetType": "textbox",
          "vtype": "maxLength:32",
          "maxLength": 32,
          "order": 2
        },
        "listConfig": {
          "show": true,
          "sortable": true,
          "searchable": true,
          "width": 120
        }
      },
      {
        "fieldId": "product_type",
        "fieldName": "产品类型",
        "fieldType": "nvarchar",
        "length": 2,
        "required": false,
        "formConfig": {
          "show": true,
          "widgetType": "combobox",
          "order": 3
        },
        "listConfig": {
          "show": true,
          "sortable": true,
          "width": 100
        }
      },
      {
        "fieldId": "price",
        "fieldName": "价格",
        "fieldType": "decimal",
        "precision": 10,
        "scale": 2,
        "required": false,
        "formConfig": {
          "show": true,
          "widgetType": "spinner",
          "widgetProps": {"decimalPlaces": 2, "minValue": 0},
          "order": 4
        },
        "listConfig": {
          "show": true,
          "sortable": true,
          "width": 100
        }
      },
      {
        "fieldId": "status",
        "fieldName": "状态",
        "fieldType": "nvarchar",
        "length": 2,
        "required": false,
        "formConfig": {
          "show": true,
          "widgetType": "combobox",
          "order": 5
        },
        "listConfig": {
          "show": true,
          "sortable": true,
          "width": 80
        }
      },
      {
        "fieldId": "description",
        "fieldName": "产品描述",
        "fieldType": "text",
        "required": false,
        "formConfig": {
          "show": true,
          "widgetType": "textarea",
          "order": 6
        },
        "listConfig": {
          "show": false
        }
      },
      {
        "fieldId": "create_time",
        "fieldName": "创建时间",
        "fieldType": "datetime",
        "required": false,
        "formConfig": {"show": false},
        "listConfig": {"show": true, "sortable": true}
      },
      {
        "fieldId": "create_user",
        "fieldName": "创建人",
        "fieldType": "nvarchar",
        "length": 64,
        "required": false,
        "formConfig": {"show": false},
        "listConfig": {"show": true}
      },
      {
        "fieldId": "update_time",
        "fieldName": "更新时间",
        "fieldType": "datetime",
        "required": false,
        "formConfig": {"show": false},
        "listConfig": {"show": true, "sortable": true}
      },
      {
        "fieldId": "update_user",
        "fieldName": "更新人",
        "fieldType": "nvarchar",
        "length": 64,
        "required": false,
        "formConfig": {"show": false},
        "listConfig": {"show": true}
      }
    ]
  }
]
```

## Important Notes

1. **NEVER use native SQL CREATE TABLE statements** - always use DSL format
2. **tableId** must be lowercase with underscores (snake_case)
3. **fieldId** must be lowercase with underscores (snake_case)
4. **String types (nvarchar, nchar) require length** property
5. **Decimal type requires precision and scale** properties
6. **formConfig.show = false** hides field from add/edit forms
7. **listConfig.show = false** hides field from list grid
8. **codeGroups** defines dropdown options that can be referenced by combobox widgets
9. The framework automatically handles database compatibility (MySQL, Oracle, SQL Server, DaMeng)
