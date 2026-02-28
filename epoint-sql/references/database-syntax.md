# EPoint Database Syntax Reference

Complete syntax reference for generating SQL scripts across all supported databases.

## Table of Contents

- [Data Type Mappings](#data-type-mappings)
- [MySQL Syntax](#mysql-syntax)
- [Oracle Syntax](#oracle-syntax)
- [DM (Dameng) Syntax](#dm-dameng-syntax)
- [SQL Server Syntax](#sql-server-syntax)
- [Index Syntax](#index-syntax)
- [Common Patterns](#common-patterns)

---

## Data Type Mappings

### Character Types

| Description | MySQL | Oracle | DM | SQL Server |
|-------------|-------|--------|-----|------------|
| Short string | `varchar(50)` | `VARCHAR2(150)` | `VARCHAR(200 char)` | `VARCHAR(50)` |
| Medium string | `varchar(255)` | `VARCHAR2(765)` | `VARCHAR(1020 char)` | `VARCHAR(255)` |
| Long string | `varchar(500)` | `VARCHAR2(1500)` | `VARCHAR(2000 char)` | `VARCHAR(500)` |
| Very long string | `text` | `CLOB` | `TEXT` | `text` |

**Conversion Rules:**
- MySQL varchar(n) → Oracle VARCHAR2(n×3)
- MySQL varchar(n) → DM VARCHAR(n×4 char)
- MySQL varchar(n) → SQL Server VARCHAR(n) (same)

### Numeric Types

| Description | MySQL | Oracle | DM | SQL Server |
|-------------|-------|--------|-----|------------|
| Integer | `int(11)` | `INT` | `INT` | `INT` |
| Small int | `int(1)` | `INT` | `INT` | `INT` |
| Big integer | `bigint(13)` | `NUMBER(13)` | `BIGINT` | `BIGINT` |
| Decimal | `decimal(10,2)` | `NUMBER(10,2)` | `DECIMAL(10,2)` | `DECIMAL(10,2)` |

### Date/Time Types

| Description | MySQL | Oracle | DM | SQL Server |
|-------------|-------|--------|-----|------------|
| DateTime | `datetime(0)` | `DATE` | `TIMESTAMP` | `datetime` |
| Timestamp | `timestamp` | `DATE` | `TIMESTAMP` | `datetime` |

---

## MySQL Syntax

### Table Creation Template

```sql
-- DELIMITER GO --
-- YYYY/MM/DD
-- author_name
-- 创建xxx表（table_name）

CREATE TABLE if NOT EXISTS `table_name`
(
    `rowguid`         varchar(50)  NOT NULL COMMENT '表主键',
    `field_name`      varchar(255) NULL     DEFAULT NULL COMMENT '字段说明',
    `text_field`      text         NULL COMMENT '大文本字段',
    `date_field`      datetime(0)  NULL DEFAULT NULL COMMENT '日期字段',
    `int_field`       int(11)      NULL DEFAULT NULL COMMENT '整数字段',
    `big_int_field`   bigint(13)   NULL DEFAULT NULL COMMENT '大整数字段',
    `decimal_field`   decimal(10,2) NULL DEFAULT NULL COMMENT '小数字段',
    `bool_field`      int(1)       NOT NULL DEFAULT 0 COMMENT '布尔字段(0-否,1-是)',
    PRIMARY KEY (`rowguid`),
    KEY `IDX_TABLE_FIELD` (`field_name`),
    KEY `IDX_TABLE_DATE` (`date_field`)
) DEFAULT CHARSET = utf8mb4 COMMENT ='xxx表';
GO
```

### ALTER TABLE (Incremental)

```sql
-- DELIMITER GO --
-- YYYY/MM/DD
-- author_name
-- 添加xxx字段到table_name表

drop procedure if exists `epoint_proc_alter`;
GO
create procedure `epoint_proc_alter`()
begin
if not exists (SELECT null FROM INFORMATION_SCHEMA.COLUMNS
    where table_schema = database() and table_name='table_name'
    and column_name='new_column') then
    alter table table_name add column `new_column` varchar(255) NULL DEFAULT NULL COMMENT '新字段';
end if;
end;
GO
call epoint_proc_alter();
GO
drop procedure if exists `epoint_proc_alter`;
GO
```

### Modify Column

```sql
drop procedure if exists `epoint_proc_alter`;
GO
create procedure `epoint_proc_alter`()
begin
    -- Modify column type
    alter table table_name modify column `column_name` varchar(500) NULL DEFAULT NULL;
end;
GO
call epoint_proc_alter();
GO
drop procedure if exists `epoint_proc_alter`;
GO
```

### Add Index

```sql
-- Normal index
ALTER TABLE table_name ADD INDEX IDX_TABLE_FIELD(field_name);

-- Unique index
ALTER TABLE table_name ADD UNIQUE INDEX UK_TABLE_FIELD(field_name);

-- Composite index
ALTER TABLE table_name ADD INDEX IDX_TABLE_FIELDS(field1, field2);
```

---

## Oracle Syntax

### Table Creation Template

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
	"BIG_INT_FIELD" NUMBER(13) DEFAULT NULL,
	"DECIMAL_FIELD" NUMBER(10,2) DEFAULT NULL,
	"BOOL_FIELD" INT NOT NULL DEFAULT 0,
	PRIMARY KEY ("ROWGUID")
)';
end if;
end;
end;
/* GO */
```

### ALTER TABLE (Incremental)

```sql
-- BEGIN

begin
  declare
isexist number;
begin
select count(1)
into isexist
from user_tab_columns
where table_name = upper('table_name') and column_name = upper('new_column');
if
(isexist = 0) then
    execute immediate 'ALTER TABLE "TABLE_NAME" ADD ("NEW_COLUMN" VARCHAR2(765) DEFAULT NULL)';
end if;
end;
end;
/* GO */
```

### Add Index

```sql
-- Normal index
CREATE INDEX IDX_TABLE_FIELD ON table_name(field_name);

-- Unique index
CREATE UNIQUE INDEX UK_TABLE_FIELD ON table_name(field_name);

-- Composite index
CREATE INDEX IDX_TABLE_FIELDS ON table_name(field1, field2);
```

---

## DM (Dameng) Syntax

### Table Creation Template

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
	"BIG_INT_FIELD" BIGINT DEFAULT NULL,
	"DECIMAL_FIELD" DECIMAL(10,2) DEFAULT NULL,
	"BOOL_FIELD" INT NOT NULL DEFAULT 0,
	PRIMARY KEY ("ROWGUID")
)';
end if;
end;
end;
/* GO */
```

### ALTER TABLE (Incremental)

```sql
-- BEGIN

begin
  declare
isexist number;
begin
select count(1)
into isexist
from user_tab_columns
where table_name = upper('table_name') and column_name = upper('new_column');
if
(isexist = 0) then
    execute immediate 'ALTER TABLE "TABLE_NAME" ADD ("NEW_COLUMN" VARCHAR(1020 char) DEFAULT NULL)';
end if;
end;
end;
/* GO */
```

### Add Index

```sql
-- Normal index
create index IDX_TABLE_FIELD on table_name(field_name);

-- Unique index
create unique index UK_TABLE_FIELD on table_name(field_name);

-- Composite index
create index IDX_TABLE_FIELDS on table_name(field1, field2);
```

---

## SQL Server Syntax

### Table Creation Template

```sql
-- DELIMITER GO --
-- YYYY/MM/DD
-- author_name
-- 创建xxx表（table_name）

IF NOT EXISTS (select * from dbo.sysobjects where id = object_id('table_name'))
CREATE TABLE table_name
(
    rowguid         VARCHAR(50) NOT NULL,
    field_name      VARCHAR(255) NULL DEFAULT NULL,
    text_field      text NULL,
    date_field      datetime NULL DEFAULT NULL,
    int_field       INT NULL DEFAULT NULL,
    big_int_field   BIGINT NULL DEFAULT NULL,
    decimal_field   DECIMAL(10,2) NULL DEFAULT NULL,
    bool_field      INT NOT NULL DEFAULT 0,
    PRIMARY KEY (rowguid)
);
GO
```

### ALTER TABLE (Incremental)

```sql
-- DELIMITER GO --
-- YYYY/MM/DD
-- author_name
-- 添加xxx字段到table_name表

IF NOT EXISTS (
    SELECT * FROM syscolumns
    WHERE id = object_id('table_name') AND name = 'new_column'
)
BEGIN
    ALTER TABLE table_name ADD new_column VARCHAR(255) NULL DEFAULT NULL;
END
GO
```

### Add Index

```sql
-- Normal index
CREATE INDEX IDX_TABLE_FIELD ON table_name(field_name);

-- Unique index
CREATE UNIQUE INDEX UK_TABLE_FIELD ON table_name(field_name);

-- Composite index
CREATE INDEX IDX_TABLE_FIELDS ON table_name(field1, field2);
```

---

## Index Syntax

### Index File Format

Each database has its own index file in `index/` directory:

**mysql_index.txt**:
```
-- table_name
-- primary;rowguid
ALTER TABLE table_name ADD PRIMARY KEY (rowguid);
-- Normal;field1,field2;IDX_TABLE_FIELDS
ALTER TABLE table_name ADD INDEX IDX_TABLE_FIELDS(field1, field2);
-- Unique;field3;UK_TABLE_FIELD
ALTER TABLE table_name ADD UNIQUE INDEX UK_TABLE_FIELD(field3);
```

**oracle_index.txt**:
```
-- table_name
-- primary;rowguid
ALTER TABLE table_name ADD PRIMARY KEY (rowguid);
-- Normal;field1,field2;IDX_TABLE_FIELDS
CREATE INDEX IDX_TABLE_FIELDS ON table_name(field1, field2);
-- Unique;field3;UK_TABLE_FIELD
CREATE UNIQUE INDEX UK_TABLE_FIELD ON table_name(field3);
```

**dm_index.txt**: Same as Oracle

**sqlserver_index.txt**: Same as Oracle (CREATE INDEX syntax)

### Index Comment Format

Each index definition is preceded by a comment:
```
-- table_name
-- index_type;column_list;index_name
```

- **index_type**: `primary`, `Normal`, `Unique`
- **column_list**: comma-separated column names
- **index_name**: name of the index

---

## Common Patterns

### Standard Primary Key

Always use `rowguid` as the primary key:

```sql
-- MySQL
`rowguid` varchar(50) NOT NULL,
PRIMARY KEY (`rowguid`)

-- Oracle
"ROWGUID" VARCHAR2(150) NOT NULL,
PRIMARY KEY ("ROWGUID")

-- DM
"ROWGUID" VARCHAR(200 char) NOT NULL,
PRIMARY KEY ("ROWGUID")

-- SQL Server
rowguid VARCHAR(50) NOT NULL,
PRIMARY KEY (rowguid)
```

### Standard Audit Fields

```sql
-- Operation tracking fields
operatedate      datetime/timestamp - 操作时间
operateusername  varchar(150/200)   - 操作人姓名
operateuserguid  varchar(150/200)   - 操作人GUID

-- Creation tracking
creator          varchar(100)        - 创建人
createtime       datetime/timestamp  - 创建时间

-- Update tracking
updater          varchar(100)        - 更新人
updatetime       datetime/timestamp  - 更新时间
```

### Boolean Convention

Use `int(1)` / `INT` with 0/1 values for boolean:

```sql
-- Example: server status field
serverstatus int(1) NOT NULL DEFAULT 0 COMMENT '服务器状态（0-未激活，1-激活，2-停用）'

-- Example: enabled flag
isenabled int(1) NOT NULL DEFAULT 1 COMMENT '是否启用（0-禁用，1-启用）'
```

### Comment Format

Always include descriptive comments:

```sql
-- MySQL: inline COMMENT
field_name varchar(255) NULL DEFAULT NULL COMMENT '字段说明'

-- Table comment
) DEFAULT CHARSET = utf8mb4 COMMENT ='xxx表';

-- Oracle/DM/SQL Server: block comment before table
-- 创建xxx表（table_name）
```

---

## Check Scripts

**IMPORTANT**: The Check script is used by the system during startup to determine whether the table creation script should be executed. **Always update the Check script when adding or modifying tables.**

### Check Script Location

Check scripts are located in the same directory as Frame scripts:
```
{module}/table/init/
├── mysql_Frame.sql
├── mysql_Check_Frame.sql    # MySQL check script
├── oracle_Frame.sql
├── oracle_Check_Frame.sql   # Oracle check script
├── dm_Frame.sql
├── dm_Check_Frame.sql       # DM check script
├── sqlserver_Frame.sql
└── sqlserver_Check_Frame.sql # SQL Server check script
```

### Check Script Format

Each Check script contains **only one line** - the check for the **last table** in the corresponding Frame script.

**MySQL Check Script** (`mysql_Check_Frame.sql`):
```sql
select count(*) from information_schema.columns where table_schema = database() and table_name ='table_name'
```

**Oracle Check Script** (`oracle_Check_Frame.sql`):
```sql
select count(*) from user_tab_columns where table_name = upper('table_name')
```

**DM Check Script** (`dm_Check_Frame.sql`):
```sql
select count(*) from user_tab_columns where table_name = upper('table_name')
```

**SQL Server Check Script** (`sqlserver_Check_Frame.sql`):
```sql
select count(*) from information_schema.tables where table_name = 'table_name'
```

### Check Script Syntax Comparison

| Database | System Table/View | Table Name Handling |
|----------|-------------------|---------------------|
| MySQL | `information_schema.columns` | lowercase with backticks |
| Oracle | `user_tab_columns` | `upper('table_name')` |
| DM | `user_tab_columns` | `upper('table_name')` |
| SQL Server | `information_schema.tables` | exact case with single quotes |

### When to Update Check Scripts

**Add new table**: Replace the existing check with the new table's check
```sql
-- Before: checking for api_script_category
select count(*) from information_schema.columns where table_schema = database() and table_name ='api_script_category'

-- After: checking for new table api_test_basic
select count(*) from information_schema.columns where table_schema = database() and table_name ='api_test_basic'
```

**Note**: The Check script should always contain the check for the **last table** defined in the Frame script. The system executes scripts sequentially, and the check determines if all tables in the script need to be created.

### Check Script vs Existence Check in Frame Script

- **Check Script**: Used by the system at startup to decide if the entire Frame script should run
- **Existence Check in Frame**: Used within the Frame script to safely handle script re-execution (e.g., `if NOT EXISTS`, `CREATE TABLE IF NOT EXISTS`)

Both serve different purposes:
- Check Script: System-level control before script execution
- Frame Script Existence Check: Script-level safety during execution

---

## Incremental Script Patterns

**IMPORTANT**: Incremental modifications should always be added to the **latest existing version**, NOT a new version.

### Version Management Rule

```
✅ CORRECT:  Modify existing version 3.5.0/
❌ WRONG:    Create new version 3.6.0/ for modifications
```

**Rationale**: Scripts are executed sequentially in version order. Incremental modifications belong to the current development version, not a new version.

### Incremental Script Structure

For each database type, incremental scripts use stored procedures (MySQL) or PL/SQL blocks (Oracle/DM) or IF EXISTS checks (SQL Server) to ensure safe re-execution.

**MySQL Incremental Pattern** (modify column type):
```sql
drop procedure if exists `epoint_proc_alter`;
GO
create procedure `epoint_proc_alter`()
begin
if exists (SELECT null FROM INFORMATION_SCHEMA.COLUMNS
    where table_schema = database() and table_name='table_name'
    and column_name='column_name' and data_type = 'varchar') then
    -- Add temp column, copy data, drop old, rename
    ALTER TABLE table_name ADD COLUMN column_temp INT NULL DEFAULT NULL;
    UPDATE table_name SET column_temp = CAST(column_name AS SIGNED)
        WHERE column_name IS NOT NULL AND column_name REGEXP '^[0-9]+$';
    ALTER TABLE table_name DROP COLUMN column_name;
    ALTER TABLE table_name CHANGE COLUMN column_temp column_name INT NULL DEFAULT NULL;
end if;
end;
GO
call `epoint_proc_alter`();
GO
drop procedure if exists `epoint_proc_alter`;
GO
```

**Oracle/DM Incremental Pattern**:
```sql
begin
  declare
isexist number;
begin
select count(1)
into isexist
from user_tab_columns
where table_name = upper('table_name')
  and column_name = upper('column_name')
  and DATA_TYPE in ('VARCHAR2', 'CHAR');
if
(isexist > 0) then
    execute immediate 'ALTER TABLE TABLE_NAME ADD COLUMN_TEMP INT DEFAULT NULL';
    execute immediate 'UPDATE TABLE_NAME SET COLUMN_TEMP = TO_NUMBER(COLUMN_NAME)
        WHERE COLUMN_NAME IS NOT NULL AND REGEXP_LIKE(COLUMN_NAME, ''^[0-9]+$'')';
    execute immediate 'ALTER TABLE TABLE_NAME DROP COLUMN COLUMN_NAME';
    execute immediate 'ALTER TABLE TABLE_NAME RENAME COLUMN COLUMN_TEMP TO COLUMN_NAME';
end if;
end;
end;
/* GO */
```

**SQL Server Incremental Pattern**:
```sql
IF EXISTS (
    SELECT * FROM syscolumns
    WHERE id = object_id('table_name') AND name = 'column_name'
    AND xtype IN ('167', '175') -- varchar/char types
)
BEGIN
    ALTER TABLE table_name ADD column_temp INT NULL;
    UPDATE table_name SET column_temp = CAST(column_name AS INT)
        WHERE column_name IS NOT NULL AND ISNUMERIC(column_name) = 1;
    ALTER TABLE table_name DROP COLUMN column_name;
    EXEC sp_rename 'table_name.column_temp', 'column_name', 'COLUMN';
END
GO
```

### Common Incremental Operations

**Add new column**:
```sql
-- MySQL
if not exists (SELECT null FROM INFORMATION_SCHEMA.COLUMNS
    where table_schema = database() and table_name='table_name'
    and column_name='new_column') then
    ALTER TABLE table_name ADD COLUMN `new_column` varchar(255) NULL DEFAULT NULL;
end if;

-- Oracle/DM
if not exists (select count(1) from user_tab_columns
    where table_name = upper('table_name') and column_name = upper('new_column')) then
    execute immediate 'ALTER TABLE TABLE_NAME ADD "NEW_COLUMN" VARCHAR2(765) DEFAULT NULL';
end if;
```

**Drop column**:
```sql
-- MySQL
if exists (SELECT null FROM INFORMATION_SCHEMA.COLUMNS
    where table_schema = database() and table_name='table_name'
    and column_name='old_column') then
    ALTER TABLE table_name DROP COLUMN `old_column`;
end if;

-- Oracle/DM
if exists (select count(1) from user_tab_columns
    where table_name = upper('table_name') and column_name = upper('OLD_COLUMN')) then
    execute immediate 'ALTER TABLE TABLE_NAME DROP COLUMN OLD_COLUMN';
end if;
```

**Modify column length**:
```sql
-- MySQL
if not exists (SELECT null FROM INFORMATION_SCHEMA.COLUMNS
    where table_schema = database() and table_name='table_name'
    and column_name='column_name' and character_maximum_length >= 500) then
    ALTER TABLE table_name MODIFY COLUMN `column_name` varchar(500) NULL DEFAULT NULL;
end if;

-- Oracle/DM
if not exists (select count(1) from user_tab_columns
    where table_name = upper('table_name')
    and column_name = upper('column_name')
    and DATA_LENGTH >= 500) then
    execute immediate 'ALTER TABLE TABLE_NAME MODIFY COLUMN_NAME VARCHAR2(500 char)';
end if;
```

**Drop index**:
```sql
-- MySQL
if exists (SELECT null FROM INFORMATION_SCHEMA.STATISTICS
    where table_schema = database() and table_name='table_name'
    and index_name='index_name') then
    ALTER TABLE table_name DROP INDEX index_name;
end if;

-- Oracle/DM
if exists (select count(1) from user_indexes
    where table_name = upper('TABLE_NAME')
    and index_name = upper('INDEX_NAME')) then
    execute immediate 'DROP INDEX INDEX_NAME';
end if;

-- SQL Server
IF EXISTS (SELECT name FROM sysindexes WHERE name = 'index_name')
BEGIN
    DROP INDEX index_name ON table_name;
END
```

---

## Statement Delimiters

| Database | Delimiter |
|----------|-----------|
| MySQL | `GO` |
| Oracle | `/* GO */` |
| DM | `/* GO */` |
| SQL Server | `GO` |

Always end each table creation or major statement with the appropriate delimiter.
