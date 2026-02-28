# EPoint Module to Script Directory Mapping

Complete mapping of EPoint modules to their SQL script directories.

## Module Directory Structure

```
D:\apimanage\
├── epoint-api-parent/
│   └── epoint-apimanager-action/
│       └── src/main/resources/META-INF/script/apimanager/
├── epaas-mmc-parent/
│   ├── epoint-frame-action/
│   │   └── src/main/resources/META-INF/script/mmc/
│   └── epoint-frame-api/
│       └── src/main/resources/META-INF/script/mmci/
├── epoint-mis-parent/
│   └── epoint-mis-api/
│       └── src/main/resources/META-INF/script/misi/
├── epoint-gateway-parent/
│   └── epoint-gateway-action/
│       └── src/main/resources/META-INF/script/apigateway/
├── epoint-workflow-parent/
│   ├── epoint-workflow-action/
│   │   └── src/main/resources/META-INF/script/workflow/
│   └── epoint-workflow-service/
│       └── src/main/resources/META-INF/script/workflowi/
├── epoint-rule-parent/
│   └── epoint-rule-action/
│       └── src/main/resources/META-INF/script/rule/
└── epoint-international-parent/
    └── epoint-shell-international/
        └── src/main/resources/META-INF/script/international/
```

## Complete Module Mapping Table

| # | Module Project | Action/API Module | Component Name | Script Base Path |
|---|----------------|-------------------|----------------|------------------|
| 1 | epoint-api-parent | epoint-apimanager-action | **apimanager** | `epoint-api-parent/epoint-apimanager-action/src/main/resources/META-INF/script/apimanager/` |
| 2 | epaas-mmc-parent | epoint-frame-action | **mmc** | `epaas-mmc-parent/epoint-frame-action/src/main/resources/META-INF/script/mmc/` |
| 3 | epaas-mmc-parent | epoint-frame-api | **mmci** | `epaas-mmc-parent/epoint-frame-api/src/main/resources/META-INF/script/mmci/` |
| 4 | epoint-mis-parent | epoint-mis-api | **misi** | `epoint-mis-parent/epoint-mis-api/src/main/resources/META-INF/script/misi/` |
| 5 | epoint-gateway-parent | epoint-gateway-action | **apigateway** | `epoint-gateway-parent/epoint-gateway-action/src/main/resources/META-INF/script/apigateway/` |
| 6 | epoint-workflow-parent | epoint-workflow-action | **workflow** | `epoint-workflow-parent/epoint-workflow-action/src/main/resources/META-INF/script/workflow/` |
| 7 | epoint-workflow-parent | epoint-workflow-service | **workflowi** | `epoint-workflow-parent/epoint-workflow-service/src/main/resources/META-INF/script/workflowi/` |
| 8 | epoint-rule-parent | epoint-rule-action | **rule** | `epoint-rule-parent/epoint-rule-action/src/main/resources/META-INF/script/rule/` |
| 9 | epoint-international-parent | epoint-shell-international | **international** | `epoint-international-parent/epoint-shell-international/src/main/resources/META-INF/script/international/` |

## Script Directory Structure

Each component follows this structure:

```
{component}/
├── table/              # Table structure scripts
│   ├── init/           # Full initialization scripts
│   │   ├── mysql_Frame.sql
│   │   ├── oracle_Frame.sql
│   │   ├── dm_Frame.sql
│   │   ├── sqlserver_Frame.sql
│   │   └── 脚本更新.txt
│   ├── {version}/      # Version-specific incremental scripts
│   │   ├── mysql_Frame.sql
│   │   ├── oracle_Frame.sql
│   │   ├── dm_Frame.sql
│   │   ├── sqlserver_Frame.sql
│   │   └── 脚本更新.txt
│   └── ...
├── data/               # Data initialization scripts
│   ├── init/           # Initial data
│   │   ├── mysql_Data.sql
│   │   ├── oracle_Data.sql
│   │   ├── dm_Data.sql
│   │   ├── sqlserver_Data.sql
│   │   └── 脚本更新.txt
│   └── {version}/      # Version-specific data updates
├── index/              # Index definitions
│   ├── mysql_index.txt
│   ├── oracle_index.txt
│   ├── dm_index.txt
│   └── sqlserver_index.txt
└── tenant/             # Tenant-related scripts (optional)
```

## Version History by Module

### apimanager (API Management)
```
init/
1.0.0/
1.0.1/
1.1.0/
2.0.0/
3.3.0/
3.4.0/
3.5.0/
```

### mmc (Framework Management Console)
```
init/
2017/
2018/
9.4/
9.4.1/
9.4.2/
9.5.0/
9.5.2/
9.5.3/
9.5.4/
9.5.5/
9.5.6/
9.5.7/
9.5.7_auth/
f10.0.1/
```

### mmci (Framework API)
```
init/
2017/
2018/
9.4/
9.4.1/
9.4.2/
9.5.0/
9.5.2/
9.5.3/
9.5.4/
9.5.5/
9.5.6/
9.5.7/
f10.0.0/
```

### misi (MIS API)
```
init/
2018/
9.4/
9.4.1/
9.4.2/
9.5.0/
9.5.1/
9.5.2/
9.5.3/
f10.0.0/
```

### apigateway (API Gateway)
```
init/
```

### workflow (Workflow Action)
```
init/
2017/
2018/
9.4/
9.4.1/
9.4.2/
9.5.0/
9.5.1/
9.5.2/
9.5.3/
9.5.4/
9.5.5/
9.5.6/
9.5.7/
f10.0.0/
```

### workflowi (Workflow Service)
```
init/
2017/
2018/
9.4/
9.4.1/
9.4.2/
9.5.0/
9.5.1/
9.5.2/
9.5.3/
9.5.4/
9.5.5/
9.5.6/
9.5.7/
f10.0.0/
```

### rule (Rule Engine)
```
init/
1.0.0/
```

### international (Internationalization)
```
init/
1.0.0/
1.0.1/
1.1.0/
```

## Full Path Examples

### Example 1: API Manager - New Table in Init

For a new table in apimanager init:
```
D:\apimanage\epoint-api-parent\epoint-apimanager-action\src\main\resources\META-INF\script\apimanager\table\init\
├── mysql_Frame.sql
├── oracle_Frame.sql
├── dm_Frame.sql
└── sqlserver_Frame.sql
```

### Example 2: Framework - Incremental Update

For a version 9.5.8 update to mmc:
```
D:\apimanage\epaas-mmc-parent\epoint-frame-action\src\main\resources\META-INF\script\mmc\table\9.5.8\
├── mysql_Frame.sql
├── oracle_Frame.sql
├── dm_Frame.sql
├── sqlserver_Frame.sql
└── 脚本更新.txt
```

### Example 3: Gateway - Index Update

For updating apigateway indexes:
```
D:\apimanage\epoint-gateway-parent\epoint-gateway-action\src\main\resources\META-INF\script\apigateway\index\
├── mysql_index.txt
├── oracle_index.txt
├── dm_index.txt
└── sqlserver_index.txt
```

## Usage Notes

1. **Always verify the module name** before generating scripts. Different modules may have similar table names.

2. **Check existing versions** before creating a new incremental script directory.

3. **The component name** (apimanager, mmc, mmci, etc.) is the directory name under `script/`.

4. **Frame vs Check scripts**:
   - `{db}_Frame.sql` - Main table creation/update script
   - `{db}_Check_Frame.sql` - Table existence check script (optional)

5. **Action vs Service modules**:
   - Action modules typically contain table scripts
   - Service/API modules (with 'i' suffix like mmci, workflowi) may also contain table scripts
