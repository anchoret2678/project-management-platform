-- 企业级项目管理平台数据库表结构设计
-- 版本：1.0
-- 创建时间：2026-05-10

-- 创建数据库
CREATE DATABASE IF NOT EXISTS project_management_platform DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE project_management_platform;

-- 用户表（用于权限管理）
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
    full_name VARCHAR(100) NOT NULL COMMENT '姓名',
    role ENUM('admin', 'user') DEFAULT 'user' COMMENT '角色：admin-管理员，user-普通用户',
    department VARCHAR(100) COMMENT '所属部门',
    phone VARCHAR(20) COMMENT '联系电话',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 项目基础信息表
CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_code VARCHAR(50) NOT NULL UNIQUE COMMENT '项目编号',
    project_name VARCHAR(200) NOT NULL COMMENT '项目名称',
    application_name VARCHAR(200) NOT NULL COMMENT '应用名称',
    department VARCHAR(100) NOT NULL COMMENT '所属部门',
    manager_id INT NOT NULL COMMENT '负责人ID',
    status ENUM('planning', 'in_progress', 'testing', 'online', 'maintenance', 'archived') DEFAULT 'planning' COMMENT '项目状态',
    launch_date DATE COMMENT '上线时间',
    description TEXT COMMENT '项目描述',
    remark TEXT COMMENT '备注',
    created_by INT NOT NULL COMMENT '创建人ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE RESTRICT,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT,
    INDEX idx_project_code (project_code),
    INDEX idx_project_name (project_name),
    INDEX idx_status (status),
    INDEX idx_department (department),
    INDEX idx_launch_date (launch_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目基础信息表';

-- 云平台资产表
CREATE TABLE cloud_assets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL COMMENT '关联项目ID',
    cloud_provider ENUM('aliyun', 'huawei', 'tencent', 'self_built') NOT NULL COMMENT '云厂商类型',
    resource_type VARCHAR(100) NOT NULL COMMENT '资源类型',
    instance_spec VARCHAR(100) COMMENT '实例规格',
    region VARCHAR(50) NOT NULL COMMENT '地域',
    zone VARCHAR(50) COMMENT '可用区',
    account_info VARCHAR(200) COMMENT '账号信息',
    lifecycle ENUM('creating', 'running', 'stopped', 'deleting', 'deleted') DEFAULT 'running' COMMENT '资源生命周期',
    ip_address VARCHAR(50) COMMENT 'IP地址',
    config_json JSON COMMENT '配置信息JSON',
    created_by INT NOT NULL COMMENT '创建人ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT,
    INDEX idx_project_id (project_id),
    INDEX idx_cloud_provider (cloud_provider),
    INDEX idx_resource_type (resource_type),
    INDEX idx_lifecycle (lifecycle),
    INDEX idx_region (region)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='云平台资产表';

-- SOW（工作说明书）管理表
CREATE TABLE sows (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL COMMENT '关联项目ID',
    sow_number VARCHAR(50) NOT NULL UNIQUE COMMENT 'SOW编号',
    title VARCHAR(200) NOT NULL COMMENT 'SOW标题',
    version VARCHAR(20) NOT NULL COMMENT '版本号',
    file_path VARCHAR(500) NOT NULL COMMENT '文件存储路径',
    file_size BIGINT COMMENT '文件大小（字节）',
    file_type VARCHAR(50) COMMENT '文件类型',
    description TEXT COMMENT '描述',
    status ENUM('draft', 'reviewing', 'approved', 'rejected') DEFAULT 'draft' COMMENT '状态',
    effective_date DATE COMMENT '生效日期',
    expiry_date DATE COMMENT '失效日期',
    created_by INT NOT NULL COMMENT '创建人ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT,
    INDEX idx_project_id (project_id),
    INDEX idx_sow_number (sow_number),
    INDEX idx_status (status),
    INDEX idx_version (version),
    INDEX idx_effective_date (effective_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='SOW（工作说明书）管理表';

-- SLA（服务等级协议）管理表
CREATE TABLE slas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL COMMENT '关联项目ID',
    sla_number VARCHAR(50) NOT NULL UNIQUE COMMENT 'SLA编号',
    title VARCHAR(200) NOT NULL COMMENT 'SLA标题',
    availability_rate DECIMAL(5,2) NOT NULL COMMENT '服务可用率（%）',
    response_time VARCHAR(50) NOT NULL COMMENT '响应时效',
    fault_handling_time VARCHAR(50) NOT NULL COMMENT '故障处理时限',
    maintenance_window VARCHAR(200) COMMENT '维护窗口',
    penalty_terms TEXT COMMENT '违约条款',
    description TEXT COMMENT '描述',
    status ENUM('active', 'inactive', 'expired') DEFAULT 'active' COMMENT '状态',
    effective_date DATE COMMENT '生效日期',
    expiry_date DATE COMMENT '失效日期',
    created_by INT NOT NULL COMMENT '创建人ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT,
    INDEX idx_project_id (project_id),
    INDEX idx_sla_number (sla_number),
    INDEX idx_status (status),
    INDEX idx_effective_date (effective_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='SLA（服务等级协议）管理表';

-- 知识库分类表
CREATE TABLE knowledge_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE COMMENT '分类名称',
    description TEXT COMMENT '分类描述',
    parent_id INT DEFAULT NULL COMMENT '父分类ID',
    sort_order INT DEFAULT 0 COMMENT '排序',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (parent_id) REFERENCES knowledge_categories(id) ON DELETE CASCADE,
    INDEX idx_parent_id (parent_id),
    INDEX idx_sort_order (sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='知识库分类表';

-- 知识库文档表
CREATE TABLE knowledge_documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL COMMENT '关联项目ID',
    category_id INT NOT NULL COMMENT '分类ID',
    title VARCHAR(200) NOT NULL COMMENT '文档标题',
    content LONGTEXT COMMENT '文档内容（支持富文本）',
    file_path VARCHAR(500) COMMENT '文件存储路径（如果有附件）',
    file_type VARCHAR(50) COMMENT '文件类型',
    file_size BIGINT COMMENT '文件大小（字节）',
    tags JSON COMMENT '标签JSON数组',
    view_count INT DEFAULT 0 COMMENT '查看次数',
    is_published BOOLEAN DEFAULT TRUE COMMENT '是否发布',
    access_level ENUM('public', 'internal', 'confidential') DEFAULT 'internal' COMMENT '访问级别',
    created_by INT NOT NULL COMMENT '创建人ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES knowledge_categories(id) ON DELETE RESTRICT,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT,
    INDEX idx_project_id (project_id),
    INDEX idx_category_id (category_id),
    INDEX idx_title (title),
    INDEX idx_is_published (is_published),
    INDEX idx_access_level (access_level),
    INDEX idx_created_at (created_at),
    FULLTEXT idx_fulltext_search (title, content) WITH PARSER ngram
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='知识库文档表';

-- 初始化数据：知识库分类
INSERT INTO knowledge_categories (name, description, sort_order) VALUES
('技术文档', '技术架构、API文档、开发规范等', 1),
('运维手册', '部署指南、监控配置、故障处理等', 2),
('架构文档', '系统架构设计、技术选型等', 3),
('需求文档', '业务需求、功能规格等', 4),
('会议纪要', '项目会议记录、决策记录等', 5);

-- 初始化数据：管理员用户（密码：admin123）
INSERT INTO users (username, password_hash, email, full_name, role, department, phone, is_active) VALUES
('admin', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'admin@company.com', '系统管理员', 'admin', 'IT部', '13800138000', TRUE),
('user1', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'user1@company.com', '张三', 'user', '研发部', '13800138001', TRUE);

-- 创建数据库用户（用于应用连接）
CREATE USER IF NOT EXISTS 'pmp_user'@'localhost' IDENTIFIED BY 'Pmp@123456';
GRANT ALL PRIVILEGES ON project_management_platform.* TO 'pmp_user'@'localhost';
FLUSH PRIVILEGES;