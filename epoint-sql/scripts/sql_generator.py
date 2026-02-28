#!/usr/bin/env python3
"""
EPoint SQL Script Generator Helper

This script helps generate SQL scripts for the EPoint platform
across multiple databases (MySQL, Oracle, DM, SQL Server).

It provides utility functions for:
- Type conversion between databases
- Table existence check generation
- Index statement generation
- Script template generation
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime


class DatabaseType:
    MYSQL = "mysql"
    ORACLE = "oracle"
    DM = "dm"
    SQLSERVER = "sqlserver"


class FieldType:
    """Field definition for table generation"""

    def __init__(self, name: str, mysql_type: str, nullable: bool = True,
                 default: Optional[str] = None, comment: str = ""):
        self.name = name
        self.mysql_type = mysql_type
        self.nullable = nullable
        self.default = default
        self.comment = comment


def convert_type(mysql_type: str, target_db: str) -> str:
    """
    Convert MySQL type to target database type.

    Args:
        mysql_type: MySQL type string (e.g., 'varchar(50)', 'int(11)', 'text')
        target_db: Target database (mysql, oracle, dm, sqlserver)

    Returns:
        Converted type string for target database
    """
    # Parse the base type and length
    base_type = mysql_type.lower()
    length = None

    if '(' in base_type:
        base_type, length_part = base_type.split('(', 1)
        length = length_part.rstrip(')')

    # Type conversion mapping
    conversions = {
        DatabaseType.MYSQL: lambda t, l: f"{t}({l})" if l else t,
        DatabaseType.ORACLE: _convert_to_oracle,
        DatabaseType.DM: _convert_to_dm,
        DatabaseType.SQLSERVER: _convert_to_sqlserver,
    }

    return conversions[target_db](base_type, length)


def _convert_to_oracle(base_type: str, length: Optional[str]) -> str:
    """Convert type to Oracle syntax"""
    if base_type == 'varchar':
        n = int(length) if length else 255
        return f"VARCHAR2({n * 3})"
    elif base_type == 'int':
        return "INT"
    elif base_type == 'bigint':
        return "NUMBER(13)"
    elif base_type == 'text':
        return "CLOB"
    elif base_type == 'datetime':
        return "DATE"
    elif base_type == 'timestamp':
        return "DATE"
    elif base_type == 'decimal':
        return f"NUMBER({length})" if length else "NUMBER"
    else:
        return f"{base_type.upper()}({length})" if length else base_type.upper()


def _convert_to_dm(base_type: str, length: Optional[str]) -> str:
    """Convert type to DM (Dameng) syntax"""
    if base_type == 'varchar':
        n = int(length) if length else 255
        return f"VARCHAR({n * 4} char)"
    elif base_type == 'int':
        return "INT"
    elif base_type == 'bigint':
        return "BIGINT"
    elif base_type == 'text':
        return "TEXT"
    elif base_type == 'datetime':
        return "TIMESTAMP"
    elif base_type == 'timestamp':
        return "TIMESTAMP"
    elif base_type == 'decimal':
        return f"DECIMAL({length})" if length else "DECIMAL"
    else:
        return f"{base_type.upper()}({length})" if length else base_type.upper()


def _convert_to_sqlserver(base_type: str, length: Optional[str]) -> str:
    """Convert type to SQL Server syntax"""
    if base_type == 'varchar':
        return f"VARCHAR({length})" if length else "VARCHAR(255)"
    elif base_type == 'int':
        return "INT"
    elif base_type == 'bigint':
        return "BIGINT"
    elif base_type == 'text':
        return "text"
    elif base_type == 'datetime':
        return "datetime"
    elif base_type == 'timestamp':
        return "datetime"
    elif base_type == 'decimal':
        return f"DECIMAL({length})" if length else "DECIMAL"
    else:
        return f"{base_type.upper()}({length})" if length else base_type.upper()


def quote_identifier(name: str, db_type: str) -> str:
    """
    Apply database-specific identifier quoting.

    Args:
        name: Identifier name (table name, column name, etc.)
        db_type: Target database type

    Returns:
        Quoted identifier
    """
    if db_type == DatabaseType.MYSQL:
        return f"`{name}`"
    elif db_type in (DatabaseType.ORACLE, DatabaseType.DM):
        return f'"{name.upper()}"'
    else:  # SQL Server
        return name


def generate_table_creation_sql(
    table_name: str,
    fields: List[FieldType],
    db_type: str,
    author: str = "",
    description: str = ""
) -> str:
    """
    Generate table creation SQL for a specific database.

    Args:
        table_name: Name of the table
        fields: List of field definitions
        db_type: Target database type
        author: Author name for comment
        description: Table description for comment

    Returns:
        Complete SQL script for table creation
    """
    today = datetime.now().strftime("%Y/%m/%d")

    if db_type == DatabaseType.MYSQL:
        return _generate_mysql_table(table_name, fields, today, author, description)
    elif db_type == DatabaseType.ORACLE:
        return _generate_oracle_table(table_name, fields, today, author, description)
    elif db_type == DatabaseType.DM:
        return _generate_dm_table(table_name, fields, today, author, description)
    else:  # SQL Server
        return _generate_sqlserver_table(table_name, fields, today, author, description)


def _generate_mysql_table(table_name: str, fields: List[FieldType],
                          today: str, author: str, description: str) -> str:
    """Generate MySQL table creation script"""
    lines = [
        "-- DELIMITER GO --",
        f"-- {today}",
        f"-- {author}" if author else "",
        f"-- 创建{description}表（{table_name}）" if description else "",
        "",
        f"CREATE TABLE if NOT EXISTS `{table_name}`",
        "("
    ]

    for i, field in enumerate(fields):
        nullable_str = "" if field.nullable else "NOT NULL"
        default_str = f"DEFAULT {field.default}" if field.default is not None else "DEFAULT NULL"
        if not field.nullable and field.default is not None:
            default_str = f"DEFAULT {field.default}"
        elif not field.nullable:
            default_str = ""

        comment_str = f"COMMENT '{field.comment}'" if field.comment else ""

        line = f"    `{field.name}` {field.mysql_type} {nullable_str} {default_str} {comment_str}"
        if i < len(fields) - 1:
            line += ","
        lines.append(line)

    # Add primary key
    lines.append(f"    PRIMARY KEY (`rowguid`)")
    lines.append(f") DEFAULT CHARSET = utf8mb4 COMMENT ='{description}';")
    lines.append("GO")
    lines.append("")

    return "\n".join(lines)


def _generate_oracle_table(table_name: str, fields: List[FieldType],
                           today: str, author: str, description: str) -> str:
    """Generate Oracle table creation script"""
    lines = [
        "-- 如需手工在PL/SQL中执行，把语句拷贝到查询设计器，然后将下一行BEGIN和最后一行的END;前的注释去除即可",
        "-- BEGIN",
        "",
        "begin",
        "  declare",
        "isexist number;",
        "begin",
        "select count(1)",
        "into isexist",
        "from user_tab_columns",
        f"where table_name = upper('{table_name}');",
        "if",
        "(isexist = 0) then",
        "    execute immediate 'CREATE TABLE \"" + table_name.upper() + "\" ("
    ]

    for i, field in enumerate(fields):
        oracle_type = convert_type(field.mysql_type, DatabaseType.ORACLE)
        nullable_str = "" if field.nullable else "NOT NULL"
        default_str = f"DEFAULT {field.default}" if field.default is not None else "DEFAULT NULL"
        if not field.nullable and field.default is not None:
            default_str = f"DEFAULT {field.default}"
        elif not field.nullable:
            default_str = ""

        line = f'\t"{field.name.upper()}" {oracle_type} {nullable_str} {default_str}'
        if i < len(fields) - 1:
            line += ","
        lines.append(line)

    lines.extend([
        "\tPRIMARY KEY (\"ROWGUID\")",
        ")';",
        "end if;",
        "end;",
        "end;",
        "/* GO */",
        ""
    ])

    return "\n".join(lines)


def _generate_dm_table(table_name: str, fields: List[FieldType],
                       today: str, author: str, description: str) -> str:
    """Generate DM (Dameng) table creation script"""
    lines = [
        "-- 如需手工在dm管理工具中执行，把语句拷贝到查询设计器，然后将下一行BEGIN和最后一行的END;前的注释去除即可",
        "-- BEGIN",
        "",
        "begin",
        "  declare",
        "isexist number;",
        "begin",
        "select count(1)",
        "into isexist",
        "from user_tab_columns",
        f"where table_name = upper('{table_name}');",
        "if",
        "(isexist = 0) then",
        "    execute immediate 'CREATE TABLE \"" + table_name.upper() + "\" ("
    ]

    for i, field in enumerate(fields):
        dm_type = convert_type(field.mysql_type, DatabaseType.DM)
        nullable_str = "" if field.nullable else "NOT NULL"
        default_str = f"DEFAULT {field.default}" if field.default is not None else "DEFAULT NULL"
        if not field.nullable and field.default is not None:
            default_str = f"DEFAULT {field.default}"
        elif not field.nullable:
            default_str = ""

        line = f'\t"{field.name.upper()}" {dm_type} {nullable_str} {default_str}'
        if i < len(fields) - 1:
            line += ","
        lines.append(line)

    lines.extend([
        "\tPRIMARY KEY (\"ROWGUID\")",
        ")';",
        "end if;",
        "end;",
        "end;",
        "/* GO */",
        ""
    ])

    return "\n".join(lines)


def _generate_sqlserver_table(table_name: str, fields: List[FieldType],
                              today: str, author: str, description: str) -> str:
    """Generate SQL Server table creation script"""
    lines = [
        "-- DELIMITER GO --",
        f"-- {today}",
        f"-- {author}" if author else "",
        f"-- 创建{description}表（{table_name}）" if description else "",
        "",
        "IF NOT EXISTS (select * from dbo.sysobjects where id = object_id('" + table_name + "'))",
        f"CREATE TABLE {table_name}",
        "("
    ]

    for i, field in enumerate(fields):
        sqlserver_type = convert_type(field.mysql_type, DatabaseType.SQLSERVER)
        nullable_str = "NULL" if field.nullable else "NOT NULL"
        default_str = f"DEFAULT {field.default}" if field.default is not None else "DEFAULT NULL"
        if not field.nullable and field.default is not None:
            default_str = f"DEFAULT {field.default}"
        elif not field.nullable:
            default_str = ""

        line = f"    {field.name} {sqlserver_type} {nullable_str} {default_str}"
        if i < len(fields) - 1:
            line += ","
        lines.append(line)

    lines.extend([
        "    PRIMARY KEY (rowguid)",
        ");",
        "GO",
        ""
    ])

    return "\n".join(lines)


def generate_index_sql(table_name: str, columns: List[str],
                       index_type: str, index_name: str, db_type: str) -> str:
    """
    Generate index creation SQL.

    Args:
        table_name: Name of the table
        columns: List of column names for the index
        index_type: Type of index (primary, Normal, Unique)
        index_name: Name of the index
        db_type: Target database type

    Returns:
        Index creation SQL statement
    """
    column_str = ", ".join(columns)

    if db_type == DatabaseType.MYSQL:
        if index_type == "primary":
            return f"ALTER TABLE {table_name} ADD PRIMARY KEY ({column_str});"
        elif index_type == "Normal":
            return f"ALTER TABLE {table_name} ADD INDEX {index_name}({column_str});"
        elif index_type == "Unique":
            return f"ALTER TABLE {table_name} ADD UNIQUE INDEX {index_name}({column_str});"

    elif db_type == DatabaseType.ORACLE:
        if index_type == "primary":
            return f"ALTER TABLE {table_name} ADD PRIMARY KEY ({column_str});"
        elif index_type == "Normal":
            return f"CREATE INDEX {index_name} ON {table_name}({column_str});"
        elif index_type == "Unique":
            return f"CREATE UNIQUE INDEX {index_name} ON {table_name}({column_str});"

    elif db_type == DatabaseType.DM:
        if index_type == "primary":
            return f"ALTER TABLE {table_name} ADD PRIMARY KEY ({column_str});"
        elif index_type == "Normal":
            return f"create index {index_name} on {table_name}({column_str});"
        elif index_type == "Unique":
            return f"create unique index {index_name} on {table_name}({column_str});"

    else:  # SQL Server - same as Oracle
        if index_type == "primary":
            return f"ALTER TABLE {table_name} ADD PRIMARY KEY ({column_str});"
        elif index_type == "Normal":
            return f"CREATE INDEX {index_name} ON {table_name}({column_str});"
        elif index_type == "Unique":
            return f"CREATE UNIQUE INDEX {index_name} ON {table_name}({column_str});"

    return ""


def generate_check_script_sql(table_name: str, db_type: str) -> str:
    """
    Generate Check script SQL for table existence check.

    The Check script is used by the system during startup to determine
    whether the table creation script should be executed.

    Args:
        table_name: Name of the table to check
        db_type: Target database type

    Returns:
        Check SQL statement (single line)
    """
    if db_type == DatabaseType.MYSQL:
        return f"select count(*) from information_schema.columns where table_schema = database() and table_name ='{table_name}'"
    elif db_type in (DatabaseType.ORACLE, DatabaseType.DM):
        return f"select count(*) from user_tab_columns where table_name = upper('{table_name}')"
    elif db_type == DatabaseType.SQLSERVER:
        return f"select count(*) from information_schema.tables where table_name = '{table_name}'"
    return ""


def generate_all_check_scripts(table_name: str) -> dict:
    """
    Generate Check scripts for all database types.

    Args:
        table_name: Name of the table to check

    Returns:
        Dictionary mapping database types to check SQL statements
    """
    return {
        DatabaseType.MYSQL: generate_check_script_sql(table_name, DatabaseType.MYSQL),
        DatabaseType.ORACLE: generate_check_script_sql(table_name, DatabaseType.ORACLE),
        DatabaseType.DM: generate_check_script_sql(table_name, DatabaseType.DM),
        DatabaseType.SQLSERVER: generate_check_script_sql(table_name, DatabaseType.SQLSERVER),
    }


# Standard field definitions for common patterns
STANDARD_FIELDS = {
    "rowguid": FieldType("rowguid", "varchar(50)", nullable=False, comment="表主键"),
    "operatedate": FieldType("operatedate", "datetime", nullable=True, comment="操作时间"),
    "operateusername": FieldType("operateusername", "varchar(50)", nullable=True, comment="操作人姓名"),
    "operateuserguid": FieldType("operateuserguid", "varchar(50)", nullable=True, comment="操作人GUID"),
    "creator": FieldType("creator", "varchar(100)", nullable=True, comment="创建人"),
    "updater": FieldType("updater", "varchar(100)", nullable=True, comment="更新人"),
    "createtime": FieldType("createtime", "datetime", nullable=False,
                           default="CURRENT_TIMESTAMP", comment="创建时间"),
    "updatetime": FieldType("updatetime", "datetime", nullable=False,
                           default="CURRENT_TIMESTAMP", comment="更新时间"),
}


def main():
    """Example usage of the SQL generator"""
    print("EPoint SQL Script Generator Helper")
    print("This module provides utility functions for generating SQL scripts")
    print("across MySQL, Oracle, DM, and SQL Server databases.")
    print()
    print("Usage examples:")
    print("- convert_type('varchar(50)', 'oracle')  # Returns: VARCHAR2(150)")
    print("- convert_type('text', 'oracle')         # Returns: CLOB")
    print("- generate_table_creation_sql(...)       # Generate full table script")
    print("- generate_index_sql(...)                # Generate index statement")


if __name__ == "__main__":
    main()
