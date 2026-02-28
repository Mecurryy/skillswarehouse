---
name: epoint-sql
description: Generate and manage EPoint platform SQL scripts and Java entity objects for MySQL, Oracle, DM (Dameng), and SQL Server databases. Use when creating new tables, modifying existing tables, or managing database schema changes in the EPoint API management platform. Automatically handles full scripts (init/), incremental scripts (version/), entity object generation, including proper type conversions, existence checks, and index management for all four database types.
---

# EPoint SQL Script Generator

## Overview

This skill generates SQL scripts and Java entity objects for the EPoint API management platform, supporting MySQL, Oracle, DM (Dameng), and SQL Server databases. It handles both full table creation scripts (in `init/` directory) and incremental update scripts (in versioned directories like `1.0.0/`, `3.5.0/`), plus optionally generates corresponding Java entity classes.

## Directory Structure

Each module's SQL scripts are located at:
```
{module}-action/src/main/resources/META-INF/script/{module-name}/
├── table/
│   ├── init/           # Full table creation scripts
│   │   ├── mysql_Frame.sql
│   │   ├── oracle_Frame.sql
│   │   ├── dm_Frame.sql
│   │   └── sqlserver_Frame.sql
│   ├── 1.0.0/          # Version-specific incremental scripts
│   │   ├── mysql_Frame.sql
│   │   ├── oracle_Frame.sql
│   │   ├── dm_Frame.sql
│   │   ├── sqlserver_Frame.sql
│   │   └── 脚本更新.txt
│   └── {version}/      # More versions...
├── data/               # Data initialization scripts
└── index/              # Index definitions
    ├── mysql_index.txt
    ├── oracle_index.txt
    ├── dm_index.txt
    └── sqlserver_index.txt
```

## Module Mapping

| Module Name | Component Name | Script Directory |
|-------------|----------------|------------------|
| epoint-apimanager-action | apimanager | `apimanager/table/` |
| epoint-frame-action | mmc | `mmc/table/` |
| epoint-frame-api | mmci | `mmci/table/` |
| epoint-mis-api | misi | `misi/table/` |
| epoint-gateway-action | apigateway | `apigateway/table/` |
| epoint-workflow-action | workflow | `workflow/table/` |
| epoint-workflow-service | workflowi | `workflowi/table/` |
| epoint-rule-action | rule | `rule/table/` |
| epoint-shell-international | international | `international/table/` |

## Script Generation Workflow

### Step 1: Identify Target Module and Version

Ask the user to specify:
1. **Module name** (e.g., apimanager, mmc, misi)
2. **Script type**: Full (init/) or Incremental (version/)
3. **Version** (for incremental): **Use the latest existing version**, do NOT create a new version
4. **Operation**: CREATE TABLE, ALTER TABLE, ADD COLUMN, etc.

**IMPORTANT - Version Management Rule**:
- **Always use the latest existing version** for incremental modifications
- **NEVER create a new version** for table modifications
- Examples:
  - apimanager module's latest version is `3.5.0` → use `3.5.0/` for modifications
  - mmc module's latest version is `9.5.7` → use `9.5.7/` for modifications
  - misi module's latest version is `9.5.3` → use `9.5.3/` for modifications

**Rationale**: Incremental scripts follow the current component version. Creating a new version would break the sequential execution order of scripts.

### Step 2: Generate Scripts for All Databases

Generate 4 database variants with proper syntax:

#### Type Mappings

| MySQL | Oracle | DM (Dameng) | SQL Server |
|-------|--------|-------------|------------|
| `varchar(n)` | `VARCHAR2(n*3)` | `VARCHAR(n*4 char)` | `VARCHAR(n)` |
| `text` | `CLOB` | `TEXT` | `text` |
| `datetime` | `DATE` | `TIMESTAMP` | `datetime` |
| `int(11)` | `INT` / `NUMBER` | `INT` | `INT` |
| `bigint(13)` | `NUMBER(13)` | `BIGINT` | `BIGINT` |

#### Syntax Patterns

**MySQL**:
```sql
-- DELIMITER GO --
-- YYYY/MM/DD
-- author
-- description

CREATE TABLE if NOT EXISTS `table_name`
(
    `rowguid` varchar(50) NOT NULL,
    `field_name` varchar(255) NULL DEFAULT NULL,
    `text_field` text NULL,
    `date_field` datetime(0) NULL DEFAULT NULL,
    `int_field` int(11) NULL DEFAULT NULL,
    PRIMARY KEY (`rowguid`),
    KEY `IDX_TABLE_FIELD` (`field_name`)
);
GO
```

**Oracle**:
```sql
-- 如需手工在PL/SQL中执行，把语句拷贝到查询设计器，然后将下一行BEGIN和最后一行的END;前的注释去除即可
-- BEGIN

begin
  declare
isexist number;
begin
select count(1)
into isexist
from user_tab_columns
where table_name = upper('table_name');
if
(isexist = 0) then
    execute immediate 'CREATE TABLE "TABLE_NAME" (
	"ROWGUID" VARCHAR2(150) NOT NULL,
	"FIELD_NAME" VARCHAR2(765) DEFAULT NULL,
	"TEXT_FIELD" CLOB,
	"DATE_FIELD" DATE DEFAULT NULL,
	"INT_FIELD" INT DEFAULT NULL,
	PRIMARY KEY ("ROWGUID")
)';
end if;
end;
end;
/* GO */
```

**DM (Dameng)**:
```sql
-- 如需手工在dm管理工具中执行，把语句拷贝到查询设计器，然后将下一行BEGIN和最后一行的END;前的注释去除即可
-- BEGIN

begin
  declare
isexist number;
begin
select count(1)
into isexist
from user_tab_columns
where table_name = upper('table_name');
if
(isexist = 0) then
    execute immediate 'CREATE TABLE "TABLE_NAME" (
	"ROWGUID" VARCHAR(200 char) NOT NULL,
	"FIELD_NAME" VARCHAR(1020 char) DEFAULT NULL,
	"TEXT_FIELD" TEXT,
	"DATE_FIELD" TIMESTAMP DEFAULT NULL,
	"INT_FIELD" INT DEFAULT NULL,
	PRIMARY KEY ("ROWGUID")
)';
end if;
end;
end;
/* GO */
```

**SQL Server**:
```sql
-- DELIMITER GO --
-- YYYY/MM/DD
-- author
-- description

IF NOT EXISTS (select * from dbo.sysobjects where id = object_id('table_name'))
CREATE TABLE table_name
(
    rowguid         VARCHAR(50) NOT NULL,
    field_name      VARCHAR(255) NULL DEFAULT NULL,
    text_field      text NULL,
    date_field      datetime NULL DEFAULT NULL,
    int_field       INT NULL DEFAULT NULL,
    PRIMARY KEY (rowguid)
);
GO
```

### Step 3: Handle Incremental Scripts

For incremental scripts (ALTER TABLE, ADD COLUMN, etc.):

**MySQL** (use stored procedure):
```sql
-- DELIMITER GO --
-- YYYY/MM/DD
-- author
-- description

drop procedure if exists `epoint_proc_alter`;
GO
create procedure `epoint_proc_alter`()
begin
if not exists (SELECT null FROM INFORMATION_SCHEMA.COLUMNS
    where table_schema = database() and table_name='table_name'
    and column_name='new_column') then
    alter table table_name add column `new_column` varchar(255) NULL DEFAULT NULL;
end if;
end;
GO
call epoint_proc_alter();
GO
drop procedure if exists `epoint_proc_alter`;
GO
```

**Oracle/DM/SQL Server**: Use similar existence check patterns per database.

### Step 4: Update Check Scripts

**IMPORTANT**: The Check script determines whether the table creation script should be executed during system startup. **Always update the Check script when adding/modifying tables.**

Each database has its own Check script in the same directory as Frame scripts:
- `mysql_Check_Frame.sql` - MySQL table existence check
- `oracle_Check_Frame.sql` - Oracle table existence check
- `dm_Check_Frame.sql` - DM table existence check
- `sqlserver_Check_Frame.sql` - SQL Server table existence check

**Check Script Format** (one line per last table):

**MySQL**:
```sql
select count(*) from information_schema.columns where table_schema = database() and table_name ='table_name'
```

**Oracle/DM**:
```sql
select count(*) from user_tab_columns where table_name = upper('table_name')
```

**SQL Server**:
```sql
select count(*) from information_schema.tables where table_name = 'table_name'
```

**Note**: The Check script typically contains only the check for the **last table** in the Frame script. When adding a new table, replace the existing check with the new table's check.

### Step 5: Update Index Scripts

For new indexes, add entries to the appropriate `index/{database}_index.txt` file:

```
-- table_name
-- primary;rowguid
ALTER TABLE table_name ADD PRIMARY KEY (rowguid);
-- Normal;field1,field2;IDX_TABLE_FIELDS
ALTER TABLE table_name ADD INDEX IDX_TABLE_FIELDS(field1, field2);
-- Unique;field3;UK_TABLE_FIELD
ALTER TABLE table_name ADD UNIQUE INDEX UK_TABLE_FIELD(field3);
```

### Step 6: Verify Scripts

After generating scripts, verify:
1. All 4 database Frame scripts are updated
2. All 4 database Check scripts are updated
3. Init scripts reflect the new structure (if applicable)
4. Index scripts are updated (if applicable)

### Step 7: Create Java Entity Objects (Optional)

After completing SQL script generation, ask the user if they want to create the corresponding Java entity objects.

**IMPORTANT**: This step requires user confirmation before executing.

#### Entity Object Location

Entity objects are typically located in the `*-api` module corresponding to the action module:

| Action Module | API Module | Entity Package Pattern |
|---------------|------------|----------------------|
| epoint-apimanager-action | epoint-apimanager-api | `com.epoint.{module}.entity` |
| epoint-frame-action | epoint-frame-api | `com.epoint.{module}.entity` |
| epoint-gateway-action | epoint-gateway-api | `com.epoint.gateway.entity` |

#### Entity Class Template

```java
package com.epoint.{module}.entity;

import com.epoint.core.BaseEntity;
import com.epoint.core.annotation.Entity;
import java.util.Date;

/**
 * {表名称中文描述}
 * @author {author}
 * @version {date}
 */
@Entity(table = "{table_name}", id = {"rowguid"})
public class {ClassName} extends BaseEntity implements Cloneable
{
    private static final long serialVersionUID = 1L;

    /**
     * 默认主键字段
     */
    public String getRowguid() {
        return super.get("rowguid");
    }

    public void setRowguid(String rowguid) {
        super.set("rowguid", rowguid);
    }

    /**
     * {字段中文描述}
     */
    public String getField() {
        return super.get("field");
    }

    public void setField(String field) {
        super.set("field", field);
    }

    /**
     * {字段中文描述}
     */
    public Integer getIntField() {
        return super.getInt("intfield");
    }

    public void setIntField(Integer intField) {
        super.set("intfield", intField);
    }

    /**
     * {字段中文描述}
     */
    public Date getDateField() {
        return super.getDate("datefield");
    }

    public void setDateField(Date dateField) {
        super.set("datefield", dateField);
    }

    @Override
    public {ClassName} clone() {
        return ({ClassName}) super.clone();
    }
}
```

#### Type Mappings for Entity Getters

| Database Type | Java Type | Getter Method |
|---------------|-----------|---------------|
| `varchar(n)` | `String` | `super.get("field")` or `super.getStr("field")` |
| `int`, `int(11)` | `Integer` | `super.getInt("field")` |
| `bigint`, `bigint(13)` | `Long` | `super.getLong("field")` |
| `datetime`, `timestamp` | `Date` | `super.getDate("field")` |
| `text`, `clob` | `String` | `super.get("field")` |
| `double`, `decimal` | `Double` | `super.get("field")` |

#### Naming Conventions

- **Class name**: Convert table name from `snake_case` to `PascalCase`
  - `api_test_basic` → `ApiTestBasic`
  - `frame_rest_info` → `FrameRestInfo`
  - `api_environment` → `ApiEnvironment`

- **Property name**: Convert database column from `snake_case` to `camelCase`
  - `test_name` → `testName`
  - `operate_date` → `operateDate`
  - `user_guid` → `userGuid`

- **Getter/Setter name**: Standard JavaBean convention
  - `field` → `getField()`, `setField()`
  - `testName` → `getTestName()`, `setTestName()`

#### Package Structure Example

For `apimanager` module, entity files are located at:
```
D:\apimanage\epoint-api-parent\epoint-apimanager-api\src\main\java\com\epoint\{submodule}\entity\
```

## Key Conventions

1. **Primary Key**: Always use `rowguid` as VARCHAR(50) NOT NULL
2. **Common Fields**:
   - `operatedate` - datetime/timestamp for operation time
   - `operateusername` - operator name
   - `operateuserguid` - operator GUID
   - `creator/updater` - creator/updater name
   - `createtime/updatetime` - create/update time

3. **Naming Conventions**:
   - Tables: `module_entity_name` (snake_case)
   - Indexes: `IDX_{TABLE_ABBREV}_{FIELD_ABBREV}`
   - Unique keys: `uk_{purpose}_{field}`

4. **Version Numbers**: Follow semantic versioning (e.g., 1.0.0, 1.0.1, 2.0.0) or year-based (2017, 2018, 9.4, 9.5.0, f10.0.0)

## When to Use

Use this skill when:
- Creating new database tables in any EPoint module
- Modifying existing table structures (ADD COLUMN, MODIFY COLUMN, etc.)
- Adding or modifying indexes
- Managing database version migrations
- Ensuring cross-database compatibility (MySQL, Oracle, DM, SQL Server)
- Creating Java entity objects corresponding to database tables

## Resources

### Database Syntax Reference
See [references/database-syntax.md](references/database-syntax.md) for complete syntax patterns and type mappings.

### Module Directory Mapping
See [references/module-mapping.md](references/module-mapping.md) for complete module-to-directory mappings.

### Entity Object Template
See [references/entity-template.md](references/entity-template.md) for complete entity class templates and naming conventions.

### Script Templates
See [scripts/](scripts/) for helper utilities for script generation.
