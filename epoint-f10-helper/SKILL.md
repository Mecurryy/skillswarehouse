---
name: epoint-f10-helper
description: |
  Complete scaffolding helper for Epoint F10 web framework development. Use this whenever working with Epoint F10 framework - creating Actions, Services, DSL database scripts, or fui frontend pages. Automatically handles proper project structure, naming conventions, and framework-specific patterns. Trigger on: "create action", "create service", "add database table", "create fui page", "epoint development", "F10 framework", or any request to build CRUD functionality in the Epoint ecosystem.
---

# Epoint F10 Framework Helper

Quick scaffolding for Epoint F10 web framework development. This skill generates the basic structure and common patterns for Actions, Services, DSL database scripts, and fui frontend pages following Epoint framework conventions.

## Framework Overview

Epoint F10 is an enterprise Java web application framework built on Spring Boot with:
- **Action Controllers**: RESTful endpoints using `@RequestMapping` annotations
- **Service Layer**: Business logic with `@Service` and `@Transactional` annotations
- **DSL Database Scripts**: Database-agnostic schema definitions (NOT native SQL!)
- **fui Frontend**: Epoint UI Framework for page development

## Project Structure

```
epoint-web/
├── src/main/
│   ├── java/              # Java source code
│   ├── resources/         # Configuration files
│   │   ├── spring/        # Spring context configuration
│   │   ├── *.properties   # Application properties
│   │   └── log4j2.xml     # Logging configuration
│   └── webapp/            # Web resources
│       ├── frame/fui/     # FUI framework resources
│       ├── {module}/      # Module-specific pages
│       └── WEB-INF/       # Web configuration
└── docs/                  # Documentation
```

## Quick Scaffolding Workflows

### 1. Creating an Action Controller

When the user wants to create a new Action:

1. **Identify the module name** from the context or ask the user
2. **Determine the Action type**:
   - List Action: `{Entity}ListAction` - queries and displays data
   - Add Action: `{Entity}AddAction` - handles new record creation
   - Edit Action: `{Entity}EditAction` - handles record updates
   - Detail Action: `{Entity}DetailAction` - displays single record details
3. **Generate the Action class** following this template:

```java
package com.epoint.{module}.action;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import com.epoint.core.BaseAction;

/**
 * {Entity}列表控制器
 */
@Controller
@RequestMapping("/{module}/{entity}list")
public class {Entity}ListAction extends BaseAction {

    /**
     * 查询列表数据
     */
    public void list() {
        // Implementation here
        // Use service layer to fetch data
    }

    /**
     * 删除记录
     */
    public void delete() {
        // Implementation here
    }
}
```

**Key Points:**
- Extend `BaseAction` or appropriate Epoint base class
- Use `@Controller` and `@RequestMapping` annotations
- Methods return void or ResponseData/DTO
- Action2REST automatically converts action methods to REST endpoints

### 2. Creating a Service Layer

When the user wants to create a new Service:

1. **Create the Service Interface** `I{Entity}Service.java`:

```java
package com.epoint.{module}.service;

import java.util.List;
import com.epoint.{module}.domain.{Entity};

/**
 * {Entity}服务接口
 */
public interface I{Entity}Service {

    /**
     * 查询所有记录
     */
    List<{Entity}> findAll();

    /**
     * 根据ID查询
     */
    {Entity} findById(String id);

    /**
     * 新增记录
     */
    void insert({Entity} entity);

    /**
     * 更新记录
     */
    void update({Entity} entity);

    /**
     * 删除记录
     */
    void delete(String id);
}
```

2. **Create the Service Implementation** `{Entity}ServiceImpl.java`:

```java
package com.epoint.{module}.service.impl;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.epoint.{module}.service.I{Entity}Service;
import com.epoint.{module}.domain.{Entity};

/**
 * {Entity}服务实现
 */
@Service
@Transactional
public class {Entity}ServiceImpl implements I{Entity}Service {

    @Override
    public List<{Entity}> findAll() {
        // Implementation using DAO/Repository
        return null;
    }

    @Override
    public {Entity} findById(String id) {
        // Implementation
        return null;
    }

    @Override
    public void insert({Entity} entity) {
        // Implementation
    }

    @Override
    public void update({Entity} entity) {
        // Implementation
    }

    @Override
    public void delete(String id) {
        // Implementation
    }
}
```

**Key Points:**
- Interface name uses `I` prefix (e.g., `IUserService`)
- Implementation class uses `Impl` suffix (e.g., `UserServiceImpl`)
- Use `@Service` annotation on implementation class
- Use `@Transactional` for transaction management
- Place interface in `service/` package, implementation in `service/impl/`

### 3. Creating DSL Database Scripts

**CRITICAL: Database scripts MUST use DSL format, NOT native SQL!**

DSL scripts provide database abstraction for cross-database compatibility (MySQL, Oracle, SQL Server, DaMeng).

#### DSL Script Location

Place DSL scripts in:
```
{web_project_path}/{module_name}/DB.DSL
```

For example: `src/main/webapp/example/DB.DSL`

#### DSL Format

```json
[
  {
    "tableId": "example_table",
    "tableName": "示例表",
    "description": "示例表描述信息",
    "codeGroups": [
      {
        "codeGroupName": "状态",
        "codes": [
          {"codeLabel": "启用", "codeValue": "01", "order": 1},
          {"codeLabel": "禁用", "codeValue": "02", "order": 2}
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
        "formConfig": {
          "colSpan": false,
          "show": false,
          "widgetType": "textbox",
          "widgetProps": {"disabled": false},
          "order": 980
        },
        "listConfig": {
          "show": true,
          "sortable": true,
          "searchable": false
        }
      },
      {
        "fieldId": "name",
        "fieldName": "名称",
        "fieldType": "nvarchar",
        "length": 128,
        "required": true,
        "formConfig": {
          "colSpan": false,
          "show": true,
          "widgetType": "textbox",
          "widgetProps": {"disabled": false},
          "order": 981
        },
        "listConfig": {
          "show": true,
          "sortable": true,
          "searchable": true
        }
      },
      {
        "fieldId": "status",
        "fieldName": "状态",
        "fieldType": "nvarchar",
        "length": 2,
        "required": false,
        "formConfig": {
          "colSpan": false,
          "show": true,
          "widgetType": "combobox",
          "widgetProps": {"disabled": false},
          "order": 982
        },
        "listConfig": {
          "show": true,
          "sortable": true,
          "searchable": true
        }
      }
    ]
  }
]
```

#### Common Field Types

| DSL Type | Description | Length |
|----------|-------------|--------|
| `nvarchar` | Variable length string | 1-4000 |
| `nchar` | Fixed length string | 1-255 |
| `int` | Integer | - |
| `bigint` | Long integer | - |
| `decimal` | Decimal number | precision,scale |
| `datetime` | Date and time | - |
| `text` | Long text | - |
| `blob` | Binary data | - |

#### Standard Audit Fields

Include these standard fields in most tables:

```json
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
```

### 4. Creating fui Frontend Pages

When the user wants to create a frontend page:

1. **Identify the page type**:
   - List page: `list.html` - displays data in a grid
   - Add page: `add.html` - form for creating new records
   - Edit page: `edit.html` - form for updating records
   - Detail page: `detail.html` - read-only view of a record

2. **Determine the module path** based on context or ask user

3. **Generate the HTML page** using fui components:

#### List Page Template (`list.html`)

```html
<!DOCTYPE html>
<html>
<head>
    <title>{Entity}列表</title>
    <script type="text/javascript">
        // Page initialization
        function onLoad() {
            // Initialize datagrid
        }

        // Query button click
        function query() {
            var grid = mini.get("datagrid1");
            grid.load();
        }

        // Add button click
        function add() {
            mini.open({
                url: "add.html",
                title: "新增{Entity}",
                width: 600,
                height: 400,
                ondestroy: function(action) {
                    if (action == "ok") {
                        query();
                    }
                }
            });
        }

        // Edit button click
        function edit() {
            var grid = mini.get("datagrid1");
            var row = grid.getSelected();
            if (!row) {
                mini.alert("请选择一条记录");
                return;
            }
            mini.open({
                url: "edit.html?id=" + row.id,
                title: "编辑{Entity}",
                width: 600,
                height: 400,
                ondestroy: function(action) {
                    if (action == "ok") {
                        query();
                    }
                }
            });
        }

        // Delete button click
        function del() {
            var grid = mini.get("datagrid1");
            var row = grid.getSelected();
            if (!row) {
                mini.alert("请选择一条记录");
                return;
            }
            mini.confirm("确定删除选中记录？", "确定", function(action) {
                if (action == "ok") {
                    // Call delete action
                    query();
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
            </tr>
        </table>
    </div>
    <div id="datagrid1" class="mini-datagrid"
         action="{module}/{entity}list.action"
         idField="id"
         allowResize="true"
         multiSelect="false"
         pageSize="20"
         sizeList="[10,20,50,100]">
        <div property="columns">
            <div type="indexcolumn" width="30"></div>
            <div field="name" width="120" headerAlign="center" allowSort="true">名称</div>
            <div field="status" width="80" headerAlign="center">状态</div>
            <div field="create_time" width="150" headerAlign="center" allowSort="true" dateFormat="yyyy-MM-dd HH:mm:ss">创建时间</div>
        </div>
    </div>
</body>
</html>
```

#### Add/Edit Page Template (`add.html` / `edit.html`)

```html
<!DOCTYPE html>
<html>
<head>
    <title>{Entity}维护</title>
    <script type="text/javascript">
        function SaveData() {
            var form = new mini.Form("#form1");
            form.validate();
            if (form.isValid() == false) return;

            var data = form.getData();
            var json = mini.encode(data);

            // Submit to action
            $.ajax({
                url: "{module}/{entity}add.action",
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
            <tr>
                <td>状态：</td>
                <td>
                    <input name="status" class="mini-combobox"
                           action="{module}/{entity}list.getStatusData"
                           textField="text" valueField="id" />
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

**Key Points:**
- Use fui components from `frame/fui/`
- Pages go in `src/main/webapp/{module}/` directory
- Use `mini.js` for JavaScript interactions
- Forms submit JSON data to actions
- Use mini-open for popup windows

## Naming Conventions

### Java Classes
- **Package**: `com.epoint.{module}` (all lowercase)
- **Interface**: `I{Entity}Service` (I prefix + PascalCase)
- **Implementation**: `{Entity}ServiceImpl` (PascalCase + Impl suffix)
- **Action**: `{Entity}ListAction`, `{Entity}AddAction`, etc.
- **Entity**: `{Entity}` (PascalCase, single word usually)

### Database (DSL)
- **Table ID**: `snake_case` (e.g., `example_table`)
- **Field ID**: `snake_case` (e.g., `create_time`)
- **Field Name**: Chinese description

### Frontend
- **Pages**: `list.html`, `add.html`, `edit.html`, `detail.html`
- **Actions**: Lowercase (e.g., `{entity}list.action`)
- **JavaScript**: camelCase (e.g., `query()`, `SaveData()`)

## Common Patterns

### Handling Combobox Dropdowns

For dropdown selects, create a data method in the Action:

```java
/**
 * 获取状态下拉数据
 */
public List<SelectItem> getStatusData() {
    List<SelectItem> list = new ArrayList<>();
    list.add(new SelectItem("01", "启用"));
    list.add(new SelectItem("02", "禁用"));
    return list;
}
```

Frontend configuration:
```html
<input name="status" class="mini-combobox"
       action="{module}/{entity}list.getStatusData"
       textField="text" valueField="id" />
```

### Standard CRUD Operations

1. **Create**: Add Action receives POST, validates, calls Service.insert()
2. **Read**: List Action queries data, returns JSON grid
3. **Update**: Edit Action loads record by ID, saves changes via Service.update()
4. **Delete**: Delete Action receives ID, calls Service.delete()

## Common Utilities

- **StringUtil**: String manipulation
- **DateUtil**: Date formatting and parsing
- **JsonUtil**: JSON serialization/deserialization
- **FileUtil**: File operations

## Configuration Files

- `src/main/resources/application.properties`: Main Spring Boot configuration
- `src/main/resources/jdbc.properties`: Database connection (supports encrypted values)
- `src/main/resources/epointframe.properties`: Framework-specific settings
- `src/main/resources/log4j2.xml`: Logging configuration

## Development Commands

```bash
# Build and run
mvn clean tomcat7:run

# Build without tests
mvn clean package -DskipTests

# Run specific tests
mvn test -Dtest=TestClassName
```

## Access URLs

- Main application: `http://localhost:8088/epoint-web/rest`
- Druid monitoring: `http://localhost:8088/epoint-web/druid`
- System check: `http://localhost:8088/epoint-web/autocheck/*`

## Important Reminders

1. **Database scripts MUST use DSL format** - never native SQL CREATE TABLE statements
2. **Use fui components** for all frontend pages
3. **Follow naming conventions** strictly
4. **Use @Transactional** for service methods that modify data
5. **Extend BaseAction** for all controllers
6. **Place DSL scripts** in `{webapp}/{module}/DB.DSL`

## Examples and References

- Demo code: `src/main/webapp/demo/`
- fui framework: `src/main/webapp/frame/fui/`
- Project documentation: `docs/project-context.md`
