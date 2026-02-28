# Java Entity Object Template Reference

## Overview

Each database table in the EPoint platform has a corresponding Java entity object. This document provides the template and conventions for creating entity classes.

## Entity Class Template

```java
package com.epoint.{module}.{submodule}.entity;

import com.epoint.core.BaseEntity;
import com.epoint.core.annotation.Entity;
import java.util.Date;

/**
 * {表名称中文描述}
 *
 * @author {author_name}
 * @version {create_date}
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
    public Long getLongField() {
        return super.getLong("longfield");
    }

    public void setLongField(Long longField) {
        super.set("longfield", longField);
    }

    /**
     * {字段中文描述}
     */
    public Double getDoubleField() {
        return super.get("doublefield");
    }

    public void setDoubleField(Double doubleField) {
        super.set("doublefield", doubleField);
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

    /**
     * 操作日期
     */
    public Date getOperateDate() {
        return super.getDate("operatedate");
    }

    public void setOperateDate(Date operateDate) {
        super.set("operatedate", operateDate);
    }

    /**
     * 操作人
     */
    public String getOperateUserName() {
        return super.get("operateusername");
    }

    public void setOperateUserName(String operateUserName) {
        super.set("operateusername", operateUserName);
    }

    /**
     * 操作人GUID
     */
    public String getOperateUserGuid() {
        return super.get("operateuserguid");
    }

    public void setOperateUserGuid(String operateUserGuid) {
        super.set("operateuserguid", operateUserGuid);
    }

    @Override
    public {ClassName} clone() {
        return ({ClassName}) super.clone();
    }
}
```

## Database Type to Java Type Mapping

| Database Type | Java Type | Getter Method |
|---------------|-----------|---------------|
| `varchar(n)` | `String` | `super.get("field")` or `super.getStr("field")` |
| `char(n)` | `String` | `super.get("field")` |
| `int`, `int(11)` | `Integer` | `super.getInt("field")` |
| `bigint`, `bigint(13)` | `Long` | `super.getLong("field")` |
| `tinyint` | `Integer` | `super.getInt("field")` |
| `smallint` | `Integer` | `super.getInt("field")` |
| `double` | `Double` | `super.get("field")` |
| `decimal(p,s)` | `Double` | `super.get("field")` |
| `datetime`, `timestamp` | `Date` | `super.getDate("field")` |
| `text` | `String` | `super.get("field")` |
| `clob` | `String` | `super.get("field")` |
| `blob` | `byte[]` | `super.get("field")` |

## Naming Conventions

### Table Name to Class Name

Convert table name from `snake_case` to `PascalCase`:

| Table Name | Class Name |
|------------|------------|
| `api_test_basic` | `ApiTestBasic` |
| `frame_rest_info` | `FrameRestInfo` |
| `api_environment` | `ApiEnvironment` |
| `api_manage_config` | `ApiManageConfig` |
| `sentinel_flow` | `EpointFlowRuleEntity` (special case) |
| `sentinel_degrade` | `EpointDegradeRuleEntity` (special case) |

### Column Name to Property Name

Convert database column from `snake_case` to `camelCase`:

| Column Name | Property Name | Getter Name | Setter Name |
|-------------|---------------|-------------|-------------|
| `field_name` | `fieldName` | `getFieldName()` | `setFieldName()` |
| `test_name` | `testName` | `getTestName()` | `setTestName()` |
| `operate_date` | `operateDate` | `getOperateDate()` | `setOperateDate()` |
| `user_guid` | `userGuid` | `getUserGuid()` | `setUserGuid()` |
| `rowguid` | `rowguid` | `getRowguid()` | `setRowguid()` |

**Note**: The `super.get()`, `super.set()` methods use the **lowercase snake_case** database column name, not the camelCase property name.

## Module Entity Location Mapping

| Module | Action Module | API Module | Entity Package Pattern | Example Path |
|--------|---------------|------------|------------------------|--------------|
| apimanager | epoint-apimanager-action | epoint-apimanager-api | `com.epoint.{submodule}.entity` | `com.epoint.apimanage.test.entity` |
| mmc | epoint-frame-action | epoint-frame-api | `com.epoint.{submodule}.entity` | `com.epoint.frame.user.entity` |
| apigateway | epoint-gateway-action | epoint-gateway-api | `com.epoint.gateway.entity` | `com.epoint.gateway.entity` |
| workflow | epoint-workflow-action | epoint-workflow-api | `com.epoint.workflow.entity` | `com.epoint.workflow.entity` |

**File Path Pattern**:
```
D:\apimanage\{api-module}\src\main\java\com\epoint\{submodule}\entity\{ClassName}.java
```

## Common Fields

Most entity classes include these common operation fields:

```java
/**
 * 操作日期
 */
public Date getOperateDate() {
    return super.getDate("operatedate");
}

public void setOperateDate(Date operateDate) {
    super.set("operatedate", operateDate);
}

/**
 * 操作人
 */
public String getOperateUserName() {
    return super.get("operateusername");
}

public void setOperateUserName(String operateUserName) {
    super.set("operateusername", operateUserName);
}

/**
 * 操作人GUID
 */
public String getOperateUserGuid() {
    return super.get("operateuserguid");
}

public void setOperateUserGuid(String operateUserGuid) {
    super.set("operateuserguid", operateUserGuid);
}
```

## Complete Example

```java
package com.epoint.apimanage.test.entity;

import com.epoint.core.BaseEntity;
import com.epoint.core.annotation.Entity;
import java.util.Date;

/**
 * 测试环境实体
 * @author wpxiang
 * @version 2023/12/27 17:35
 */
@Entity(table = "api_environment", id = {"rowguid"})
public class ApiEnvironment extends BaseEntity implements Cloneable
{

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
     * 环境名称
     */
    public String getEnvironmentName() {
        return super.getStr("environmentname");
    }

    public void setEnvironmentName(String environmentName) {
        super.set("environmentname", environmentName);
    }

    /**
     * 前置URL
     */
    public String getPreUrl() {
        return super.getStr("preurl");
    }

    public void setPreUrl(String preUrl) {
        super.set("preurl", preUrl);
    }

    /**
     * 认证配置
     */
    public String getAuthConfig() {
        return super.getStr("authconfig");
    }

    public void setAuthConfig(String authConfig) {
        super.set("authconfig", authConfig);
    }

    /**
     * 环境变量
     */
    public String getVariables() {
        return super.getStr("variables");
    }

    public void setVariable(String variables) {
        super.set("variables", variables);
    }

    /**
     * 项目guid
     */
    public String getProjectGuid() {
        return super.getStr("projectguid");
    }

    public void setProjectGuid(String projectGuid) {
        super.set("projectguid", projectGuid);
    }

    /**
     * 操作日期
     */
    public Date getOperateDate() {
        return super.getDate("operatedate");
    }

    public void setOperateDate(Date operateDate) {
        super.set("operatedate", operateDate);
    }

    /**
     * 操作人
     */
    public String getOperateUserName() {
        return super.getStr("operateusername");
    }

    public void setOperateUserName(String operateUserName) {
        super.set("operateusername", operateUserName);
    }

}
```
