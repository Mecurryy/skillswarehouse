# FUI Components Reference

Complete reference for Epoint FUI framework components used in frontend page development.

## Page Structure Template

```html
<!DOCTYPE html>
<html>
<head>
    <title>Page Title</title>
    <meta charset="utf-8" />
    <script type="text/javascript">
        // Page initialization and functions
    </script>
</head>
<body>
    <!-- Page content -->
</body>
</html>
```

## Core Components

### Mini-Toolbar

Button toolbar for page actions.

```html
<div class="mini-toolbar">
    <table style="width:100%;">
        <tr>
            <td style="width:100%;">
                <a class="mini-button" onclick="add()">新增</a>
                <a class="mini-button" onclick="edit()">编辑</a>
                <a class="mini-button" onclick="del()">删除</a>
                <span class="separator"></span>
                <a class="mini-button" onclick="export()">导出</a>
            </td>
            <td style="white-space:nowrap;">
                <input id="key" class="mini-textbox" emptyText="请输入关键字" style="width:150px;" />
                <a class="mini-button" onclick="search()">查询</a>
            </td>
        </tr>
    </table>
</div>
```

### Mini-Datagrid

Data grid for displaying tabular data.

```html
<div id="datagrid1" class="mini-datagrid"
     action="{module}/{entity}list.action"
     idField="id"
     allowResize="true"
     multiSelect="false"
     pageSize="20"
     sizeList="[10,20,50,100]"
     showPager="true">
    <div property="columns">
        <div type="indexcolumn" width="30"></div>
        <div type="checkcolumn" width="30"></div>
        <div field="name" width="120" headerAlign="center">名称</div>
        <div field="code" width="100" headerAlign="center">编码</div>
        <div field="status" width="80" headerAlign="center" renderer="onStatusRenderer">状态</div>
        <div field="create_time" width="150" headerAlign="center" dateFormat="yyyy-MM-dd HH:mm:ss">创建时间</div>
    </div>
</div>
```

**Common Properties:**
- `action`: Backend action URL for data loading
- `idField`: Primary key field name
- `allowResize`: Allow column resize
- `multiSelect`: Enable multiple row selection
- `pageSize`: Rows per page
- `sizeList`: Available page size options
- `showPager`: Show pagination control

**Column Types:**
- `indexcolumn`: Row number column
- `checkcolumn`: Checkbox selection column
- Regular columns use `field`, `width`, `headerAlign`

**Column Properties:**
- `field`: Data field name
- `width`: Column width in pixels
- `headerAlign`: `center|left|right`
- `allowSort`: Enable sorting
- `dateFormat`: Date format string
- `renderer`: Custom render function name

### Mini-Form

Form for data input.

```html
<form id="form1" method="post">
    <input name="id" class="mini-hidden" />
    <table style="width:100%;">
        <tr>
            <td style="width:80px;">名称：</td>
            <td>
                <input name="name" class="mini-textbox"
                       required="true"
                       requiredErrorText="名称不能为空"
                       vtype="maxLength:128" />
            </td>
        </tr>
        <tr>
            <td>编码：</td>
            <td>
                <input name="code" class="mini-textbox"
                       required="true" />
            </td>
        </tr>
    </table>
</form>
```

### Input Components

#### Mini-Textbox

Single line text input.

```html
<input name="field_name" class="mini-textbox"
       required="true"
       requiredErrorText="不能为空"
       vtype="maxLength:128;email"
       emptyText="请输入..."
       enabled="true"
       readonly="false"
       style="width:200px;" />
```

**Common Properties:**
- `required`: Required field
- `requiredErrorText`: Required error message
- `vtype`: Validation type (`email`, `url`, `maxLength:N`, `minLength:N`)
- `emptyText`: Placeholder text
- `enabled`: Enable/disable
- `readonly`: Read-only

#### Mini-Textarea

Multi-line text input.

```html
<input name="description" class="mini-textarea"
       required="false"
       emptyText="请输入描述"
       style="width:300px;height:100px;" />
```

#### Mini-Combobox

Dropdown select.

```html
<input name="status" class="mini-combobox"
       action="{module}/{entity}list.getStatusData"
       textField="text"
       valueField="id"
       emptyText="请选择"
       allowInput="false"
       required="true"
       style="width:150px;" />
```

**Properties:**
- `action`: Action URL for loading options
- `textField`: Display field name
- `valueField`: Value field name
- `allowInput`: Allow typing to filter
- `emptyText`: Placeholder text

#### Mini-Datepicker

Date picker.

```html
<input name="create_time" class="mini-datepicker"
       format="yyyy-MM-dd HH:mm:ss"
       showTime="true"
       showOkButton="true"
       style="width:180px;" />
```

**Properties:**
- `format`: Date format string
- `showTime`: Show time selection
- `showOkButton`: Show OK button

#### Mini-Spinner

Number input.

```html
<input name="price" class="mini-spinner"
       minValue="0"
       maxValue="999999"
       decimalPlaces="2"
       incrementValue="0.01"
       style="width:150px;" />
```

**Properties:**
- `minValue`: Minimum value
- `maxValue`: Maximum value
- `decimalPlaces`: Decimal precision
- `incrementValue`: Step value

#### Mini-Checkbox

Single checkbox.

```html
<input name="enabled" class="mini-checkbox"
       text="启用"
       trueValue="1"
       falseValue="0" />
```

#### Mini-Radiolist

Radio button group.

```html
<input name="type" class="mini-radiobuttonlist"
       data="[{'id':'1','text':'类型1'},{'id':'2','text':'类型2'}]"
       textField="text"
       valueField="id" />
```

### Mini-Window

Popup window.

```html
<script>
function openAddWindow() {
    mini.open({
        url: "add.html",
        title: "新增",
        width: 600,
        height: 400,
        onload: function() {
            var iframe = this.getIFrameEl();
            var data = { action: "new" };
            iframe.contentWindow.SetData(data);
        },
        ondestroy: function(action) {
            if (action == "ok") {
                // Refresh grid
                var grid = mini.get("datagrid1");
                grid.reload();
            }
        }
    });
}
</script>
```

### Mini-Panel

Container panel.

```html
<div class="mini-panel" title="查询条件"
     showCollapseButton="true"
     style="width:100%;height:100px;">
    <table style="width:100%;">
        <tr>
            <td>名称：<input name="name" class="mini-textbox" style="width:150px;" /></td>
            <td>状态：<input name="status" class="mini-combobox" style="width:150px;" /></td>
        </tr>
    </table>
</div>
```

## Common JavaScript Patterns

### Grid Operations

```javascript
// Get grid
var grid = mini.get("datagrid1");

// Get selected row
var row = grid.getSelected();

// Get selected rows
var rows = grid.getSelecteds();

// Get row by ID
var row = grid.getRow(id);

// Reload data
grid.reload();

// Load with parameters
grid.load({ name: "test" });

// Add row
grid.addRow(row, index);

// Update row
grid.updateRow(row, data);

// Remove row
grid.removeRow(row);

// Clear selection
grid.clearSelect();

// Select row
grid.select(row);

```

### Form Operations

```javascript
// Get form
var form = new mini.Form("#form1");

// Validate form
form.validate();
if (form.isValid() == false) return;

// Get form data
var data = form.getData();

// Set form data
form.setData(row);

// Clear form
form.clear();

// Reset form
form.reset();

// Get field
var field = mini.get("fieldName");

// Set field value
field.setValue("value");

// Get field value
var value = field.getValue();
```

### AJAX Calls

```javascript
$.ajax({
    url: "{module}/{entity}add.action",
    type: "post",
    data: { data: mini.encode(data) },
    success: function(text) {
        mini.alert("保存成功");
        CloseWindow("ok");
    },
    error: function(jqXHR, textStatus, errorThrown) {
        mini.alert("操作失败：" + errorThrown);
    }
});
```

### Message Boxes

```javascript
// Alert
mini.alert("消息内容");

// Confirm
mini.confirm("确定要删除吗？", "确认", function(action) {
    if (action == "ok") {
        // User clicked OK
    }
});

// Prompt
mini.prompt("请输入原因：", "输入", function(action, value) {
    if (action == "ok") {
        // User entered value
    }
});

// Loading
mini.loading("加载中...");
mini.unmask();
```

### Window Operations

```javascript
// Close window and return result
function CloseWindow(action) {
    if (window.CloseOwnerWindow) {
        window.CloseOwnerWindow(action);
    } else {
        window.close();
    }
}

// Close with OK
CloseWindow("ok");

// Close with Cancel
CloseWindow("cancel");

// Get data from parent window
var data = window.GetData();
```

### Custom Renderers

```javascript
// Status renderer
function onStatusRenderer(e) {
    var value = e.value;
    if (value == "01") return "<span style='color:green;'>启用</span>";
    if (value == "02") return "<span style='color:red;'>禁用</span>";
    return value;
}

// Date renderer
function onDateRenderer(e) {
    if (!e.value) return "";
    return mini.formatDate(e.value, "yyyy-MM-dd");
}

// Use in column definition
<div field="status" renderer="onStatusRenderer">状态</div>
```

## Complete Page Examples

### List Page Template

```html
<!DOCTYPE html>
<html>
<head>
    <title>列表页面</title>
    <meta charset="utf-8" />
    <script type="text/javascript">
        function onLoad() {
            var grid = mini.get("datagrid1");
            grid.load();
        }

        function search() {
            var key = mini.get("key").getValue();
            var grid = mini.get("datagrid1");
            grid.load({ key: key });
        }

        function add() {
            mini.open({
                url: "add.html",
                title: "新增",
                width: 600,
                height: 400,
                ondestroy: function(action) {
                    if (action == "ok") {
                        search();
                    }
                }
            });
        }

        function edit() {
            var grid = mini.get("datagrid1");
            var row = grid.getSelected();
            if (!row) {
                mini.alert("请选择一条记录");
                return;
            }
            mini.open({
                url: "edit.html?id=" + row.id,
                title: "编辑",
                width: 600,
                height: 400,
                ondestroy: function(action) {
                    if (action == "ok") {
                        search();
                    }
                }
            });
        }

        function del() {
            var grid = mini.get("datagrid1");
            var row = grid.getSelected();
            if (!row) {
                mini.alert("请选择一条记录");
                return;
            }
            mini.confirm("确定删除选中记录？", "确认", function(action) {
                if (action == "ok") {
                    $.ajax({
                        url: "{module}/{entity}delete.action",
                        type: "post",
                        data: { id: row.id },
                        success: function(text) {
                            mini.alert("删除成功");
                            search();
                        }
                    });
                }
            });
        }
    </script>
</head>
<body>
    <div class="mini-toolbar">
        <table style="width:100%;">
            <tr>
                <td style="width:100%;">
                    <a class="mini-button" onclick="add()">新增</a>
                    <a class="mini-button" onclick="edit()">编辑</a>
                    <a class="mini-button" onclick="del()">删除</a>
                </td>
                <td style="white-space:nowrap;">
                    <input id="key" class="mini-textbox" emptyText="请输入关键字" style="width:150px;" />
                    <a class="mini-button" onclick="search()">查询</a>
                </td>
            </tr>
        </table>
    </div>
    <div id="datagrid1" class="mini-datagrid"
         action="{module}/{entity}list.action"
         idField="id"
         allowResize="true"
         pageSize="20">
        <div property="columns">
            <div type="indexcolumn" width="30"></div>
            <div field="name" width="120" headerAlign="center">名称</div>
            <div field="create_time" width="150" headerAlign="center" dateFormat="yyyy-MM-dd HH:mm:ss">创建时间</div>
        </div>
    </div>
</body>
</html>
```

### Form Page Template

```html
<!DOCTYPE html>
<html>
<head>
    <title>表单页面</title>
    <meta charset="utf-8" />
    <script type="text/javascript">
        function SaveData() {
            var form = new mini.Form("#form1");
            form.validate();
            if (form.isValid() == false) return;

            var data = form.getData();
            var json = mini.encode(data);

            $.ajax({
                url: "{module}/{entity}save.action",
                type: "post",
                data: { data: json },
                success: function(text) {
                    mini.alert("保存成功");
                    CloseWindow("ok");
                }
            });
        }

        function CloseWindow(action) {
            if (window.CloseOwnerWindow) {
                window.CloseOwnerWindow(action);
            } else {
                window.close();
            }
        }

        function onLoad() {
            var data = window.GetData();
            if (data.action == "edit") {
                // Load data for edit
                $.ajax({
                    url: "{module}/{entity}get.action",
                    type: "post",
                    data: { id: data.id },
                    success: function(text) {
                        var form = new mini.Form("#form1");
                        form.setData(text);
                    }
                });
            }
        }
    </script>
</head>
<body>
    <form id="form1">
        <input name="id" class="mini-hidden" />
        <table style="width:100%;">
            <tr>
                <td style="width:80px;">名称：</td>
                <td>
                    <input name="name" class="mini-textbox"
                           required="true"
                           requiredErrorText="名称不能为空" />
                </td>
            </tr>
        </table>
    </form>
    <div style="text-align:center;padding:10px;">
        <a class="mini-button" onclick="SaveData()">保存</a>
        <a class="mini-button" onclick="CloseWindow()">取消</a>
    </div>
</body>
</html>
```

## Important Notes

1. **Always use fui components** - don't use raw HTML elements
2. **Initialize components** using `mini.get()` or `new mini.Form()`
3. **Use mini.encode()** for JSON serialization
4. **Handle errors** in AJAX calls
5. **Validate forms** before submission
6. **Close windows** properly with `CloseOwnerWindow()`
7. **Follow naming conventions** - lowercase for actions, camelCase for JavaScript
