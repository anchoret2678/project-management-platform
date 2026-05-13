# 企业项目管理平台 - ER关系说明

## 实体关系图概览

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   用户表    │      │   项目表    │      │ 知识库分类  │
│   (users)   │◄─────┤  (projects) ├─────►│ (categories)│
└─────────────┘      └─────────────┘      └─────────────┘
       │                    │                    │
       │                    │                    │
       ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  云平台资产  │      │   SOW文档   │      │ 知识库文档  │
│ (cloud_assets)│    │   (sows)    │      │ (documents) │
└─────────────┘      └─────────────┘      └─────────────┘
                              │
                              │
                              ▼
                       ┌─────────────┐
                       │   SLA协议   │
                       │   (slas)    │
                       └─────────────┘
```

## 详细关系说明

### 1. 核心实体关系

#### 用户表 (users) → 项目表 (projects)
- **一对多关系**：一个用户可以管理多个项目
- **外键约束**：
  - `projects.manager_id` → `users.id` (负责人)
  - `projects.created_by` → `users.id` (创建人)
- **删除策略**：RESTRICT（有项目关联时不能删除用户）

#### 项目表 (projects) → 所有子表
- **一对多关系**：一个项目可以有多个关联资产
- **外键约束**：
  - `cloud_assets.project_id` → `projects.id`
  - `sows.project_id` → `projects.id`
  - `slas.project_id` → `projects.id`
  - `knowledge_documents.project_id` → `projects.id`
- **删除策略**：CASCADE（删除项目时自动删除所有关联资产）

### 2. 具体关系说明

#### 2.1 项目基础信息 (projects)
- **主键**：`id` (自增)
- **唯一约束**：`project_code` (项目编号)
- **关联实体**：
  - 负责人：`manager_id` → `users.id`
  - 创建人：`created_by` → `users.id`
- **状态枚举**：planning, in_progress, testing, online, maintenance, archived

#### 2.2 云平台资产 (cloud_assets)
- **主键**：`id` (自增)
- **关联项目**：`project_id` → `projects.id`
- **创建人**：`created_by` → `users.id`
- **云厂商枚举**：aliyun, huawei, tencent, self_built
- **生命周期枚举**：creating, running, stopped, deleting, deleted

#### 2.3 SOW文档 (sows)
- **主键**：`id` (自增)
- **唯一约束**：`sow_number` (SOW编号)
- **关联项目**：`project_id` → `projects.id`
- **创建人**：`created_by` → `users.id`
- **状态枚举**：draft, reviewing, approved, rejected

#### 2.4 SLA协议 (slas)
- **主键**：`id` (自增)
- **唯一约束**：`sla_number` (SLA编号)
- **关联项目**：`project_id` → `projects.id`
- **创建人**：`created_by` → `users.id`
- **状态枚举**：active, inactive, expired

#### 2.5 知识库分类 (knowledge_categories)
- **主键**：`id` (自增)
- **自引用**：`parent_id` → `knowledge_categories.id` (支持多级分类)
- **唯一约束**：`name` (分类名称)

#### 2.6 知识库文档 (knowledge_documents)
- **主键**：`id` (自增)
- **多对一关系**：
  - `project_id` → `projects.id`
  - `category_id` → `knowledge_categories.id`
  - `created_by` → `users.id`
- **访问级别枚举**：public, internal, confidential

### 3. 索引设计说明

#### 3.1 主键索引
- 所有表都有自增主键 `id` 作为聚集索引

#### 3.2 外键索引
- 所有外键字段都建立了索引，优化关联查询性能

#### 3.3 业务查询索引
- **项目表**：按项目编号、名称、状态、部门、上线时间查询
- **云资产表**：按云厂商、资源类型、地域、生命周期查询
- **SOW/SLA表**：按编号、状态、生效日期查询
- **知识库文档**：全文索引支持标题和内容搜索

#### 3.4 全文索引
- `knowledge_documents` 表建立了中文全文索引，支持 `ngram` 分词

### 4. 数据完整性约束

#### 4.1 外键约束
- 确保所有关联数据的一致性
- 防止孤儿记录（无父记录的子记录）

#### 4.2 唯一约束
- 用户：`username`, `email`
- 项目：`project_code`
- SOW：`sow_number`
- SLA：`sla_number`
- 知识库分类：`name`

#### 4.3 枚举约束
- 使用ENUM类型限制字段取值范围，保证数据一致性

### 5. 性能优化设计

#### 5.1 查询优化
- 为常用查询字段建立组合索引
- 使用覆盖索引减少回表查询
- 合理设置索引顺序（高选择性字段在前）

#### 5.2 存储优化
- 使用 `utf8mb4` 字符集支持完整Unicode
- 使用 `JSON` 类型存储灵活数据（标签、配置）
- 大文本字段使用 `LONGTEXT` 类型

#### 5.3 分区考虑
- 对于大数据量表（如知识库文档），可按 `created_at` 进行时间分区

### 6. 扩展性考虑

#### 6.1 字段扩展
- 使用 `JSON` 类型存储动态配置信息
- 预留 `remark`、`description` 等备注字段

#### 6.2 表结构扩展
- 支持多级知识库分类（`parent_id` 自引用）
- 支持文档版本管理（可扩展版本表）
- 支持文件附件管理（可扩展附件表）

#### 6.3 权限扩展
- 用户角色支持扩展更多类型
- 知识库文档支持多级访问控制

### 7. 数据初始化

#### 7.1 默认数据
- 知识库分类：技术文档、运维手册、架构文档、需求文档、会议纪要
- 用户账户：管理员（admin）、普通用户（user1, user2）

#### 7.2 测试数据
- 可根据需要添加测试项目和相关资产数据

## 总结

本数据库设计具有以下特点：

1. **完整性**：通过外键约束保证数据一致性
2. **性能**：合理的索引设计优化查询性能
3. **扩展性**：支持业务功能扩展
4. **安全性**：用户权限控制和数据访问级别
5. **实用性**：符合企业项目管理实际需求

所有表结构都支持完整的CRUD操作、搜索、分页和导出功能。