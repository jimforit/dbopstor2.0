CREATE TABLE `User` (
`id` int(4) NOT NULL COMMENT '用户ID',
`username` varchar(64) NOT NULL COMMENT '用户名',
`pwd` varchar(64) NOT NULL COMMENT '密码',
`email` varchar(64) NOT NULL COMMENT '邮箱',
`phone` varchar(20) NOT NULL COMMENT '手机号',
`status` tinyint(1) NOT NULL DEFAULT 0 COMMENT '用户状态',
`role_id` tinyint(1) NOT NULL COMMENT '角色ID',
`department_id` int(4) NOT NULL COMMENT '部门编号'
);

CREATE TABLE `Role` (
`id` int(4) NOT NULL COMMENT '角色ID',
`role_name` varchar(64) NOT NULL COMMENT '角色名',
PRIMARY KEY (`id`) 
);

CREATE TABLE `Order` (
`id` int(4) NOT NULL COMMENT '订单编号',
`order_name` varchar(64) NOT NULL COMMENT '项目名称',
`order_type` tinyint(2) NOT NULL COMMENT '工单类型',
`order_owner_id` int(4) NOT NULL COMMENT '责任人',
`order_config_type` tinyint(2) NULL COMMENT '申请架构类型',
`order_dead_line` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '期望解决日期',
`order_node_num` tinyint(4) NULL COMMENT '申请节点数量',
`order_cpu_cores` tinyint(2) NULL COMMENT 'CPU核心数量',
`order_mem_volmn` tinyint(2) NULL COMMENT '单节点内存容量',
`order_disk_type` tinyint(2) NULL COMMENT '服务器磁盘类型',
`order_disk_volmn` tinyint(2) NULL COMMENT '服务器磁盘容量',
`order_disk_array` tinyint(2) NULL COMMENT '磁盘阵列类型',
`order_apply_id` int(4) NOT NULL COMMENT '申请人ID',
`order_comment` text NOT NULL COMMENT '申请备注信息',
`order_project_id` int(4) NOT NULL COMMENT '项目名称',
PRIMARY KEY (`id`) 
);

CREATE TABLE `Oplog` (
`id` bigint(10) NOT NULL DEFAULT 操作ID,
`user_id` int(11) NOT NULL COMMENT '操作用户ID',
`ip` int(10) NOT NULL,
`content` varchar(256) NOT NULL,
`addtime` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '操作时间',
PRIMARY KEY (`id`) 
);

CREATE TABLE `DataCenter` (
`id` int(4) NOT NULL COMMENT '数据中心ID',
`data_center_name` varchar(64) NOT NULL COMMENT '数据中心名称',
`data_center_type` tinyint(2) NOT NULL COMMENT '数据中心类型',
`data_center_address` varchar(100) NOT NULL COMMENT '数据中心地址',
`ip_addr_range` varchar(64) NOT NULL COMMENT '网段',
`data_center_status` tinyint(2) NOT NULL COMMENT '状态',
PRIMARY KEY (`id`) 
);

CREATE TABLE `Host` (
`id` int(4) NOT NULL COMMENT '主机ID',
`host_name` varchar(64) NOT NULL COMMENT '主机名',
`host_type` tinyint(2) NOT NULL COMMENT '主机类型',
`ip_addr` int(10) NOT NULL COMMENT 'IP地址',
`host_status` tinyint(2) NOT NULL COMMENT '主机状态',
`host_admin_id` int(4) NOT NULL COMMENT '主机管理员',
`data_center_id` int(4) NOT NULL COMMENT '所属数据中心ID',
`addtime` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '添加时间',
`order_id` int(4) NOT NULL COMMENT '工单编号',
PRIMARY KEY (`id`) 
);

CREATE TABLE `Userlog` (
`id` int(4) NOT NULL COMMENT '登录日志ID',
`user_id` int(4) NOT NULL COMMENT '用户ID',
`ip` int(10) NOT NULL,
`addtime` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '操作时间',
PRIMARY KEY (`id`) 
);

CREATE TABLE `Instance` (
`id` int(4) NOT NULL COMMENT '实例ID',
`instance_name` varchar(64) NOT NULL COMMENT '实例名',
`host_id` int(4) NOT NULL COMMENT '主机ID',
`addtime` datetime NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '新增时间',
`instance_status` tinyint(2) NOT NULL COMMENT '实例状态',
`instance_monitor_url` varchar(100) NOT NULL COMMENT '实例监控链接',
`project_id` int(4) NOT NULL,
PRIMARY KEY (`id`) 
);

CREATE TABLE `Task` (
`id` int(4) NOT NULL COMMENT '作业ID',
`task_name` varchar(100) NOT NULL COMMENT '作业名',
`task_command` varchar(100) NOT NULL COMMENT '任务命令',
`task_type` tinyint(2) NOT NULL COMMENT '作业类型',
`task_status` tinyint(2) NOT NULL COMMENT '作业状态',
`host_id` int(4) NOT NULL COMMENT '主机ID',
PRIMARY KEY (`id`) 
);

CREATE TABLE `Script` (
`id` int(4) NOT NULL COMMENT '脚本ID',
`script_name` varchar(64) NOT NULL COMMENT '脚本名称',
`version` varchar(10) NOT NULL COMMENT '版本号',
`function_discription` text NOT NULL COMMENT '功能描述',
`auther_id` int(4) NOT NULL COMMENT '作者',
PRIMARY KEY (`id`) 
);

CREATE TABLE `Project` (
`id` int(4) NOT NULL COMMENT '项目ID',
`project_name` varchar(100) NOT NULL COMMENT '项目名称',
`project_manager_id` int(4) NOT NULL COMMENT '项目经理ID',
`addtime` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '上线时间',
PRIMARY KEY (`id`) 
);

CREATE TABLE `Department` (
`id` int(4) NOT NULL COMMENT '部门ID',
`department_name` varchar(64) NOT NULL COMMENT '部门名称',
PRIMARY KEY (`id`) 
);

CREATE TABLE `DbLogs` (
`id` int(4) NOT NULL COMMENT '日志ID',
`log_name` varchar(64) NOT NULL COMMENT '日志名',
`path` varchar(64) NOT NULL COMMENT '路径',
`log_type` tinyint(2) NOT NULL COMMENT '日志类型',
`instance_id` int(4) NOT NULL COMMENT '实例ID',
PRIMARY KEY (`id`) 
);


ALTER TABLE `User` ADD CONSTRAINT `role_id` FOREIGN KEY (`role_id`) REFERENCES `Role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `Order` ADD CONSTRAINT `order_apply_id` FOREIGN KEY (`order_apply_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `Order` ADD CONSTRAINT `order_hander_id` FOREIGN KEY (`order_owner_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `Oplog` ADD CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE;
ALTER TABLE `Host` ADD CONSTRAINT `admin_id` FOREIGN KEY (`host_admin_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `Host` ADD CONSTRAINT `data_center_id` FOREIGN KEY (`data_center_id`) REFERENCES `DataCenter` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `Host` ADD CONSTRAINT `order_id` FOREIGN KEY (`order_id`) REFERENCES `Order` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `Userlog` ADD CONSTRAINT `users` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `Instance` ADD CONSTRAINT `host_id` FOREIGN KEY (`host_id`) REFERENCES `Host` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `Task` ADD CONSTRAINT `task_host_id` FOREIGN KEY (`host_id`) REFERENCES `Host` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `Script` ADD CONSTRAINT `auther` FOREIGN KEY (`auther_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `Instance` ADD CONSTRAINT `project_id` FOREIGN KEY (`project_id`) REFERENCES `Project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `Order` ADD CONSTRAINT `order_project_id` FOREIGN KEY (`order_project_id`) REFERENCES `Project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `User` ADD CONSTRAINT `department_id` FOREIGN KEY (`department_id`) REFERENCES `Department` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `DbLogs` ADD CONSTRAINT `instance_log` FOREIGN KEY (`instance_id`) REFERENCES `Instance` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

