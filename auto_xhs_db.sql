CREATE DATABASE IF NOT EXISTS `auto_xhs_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE `auto_xhs_db`;


SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `uname` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名',
  `upwd` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '哈希后的密码',
  `max_limit` int(11) NULL DEFAULT NULL COMMENT '爬虫数量限制',
  `is_admin` tinyint(1) NULL DEFAULT NULL COMMENT '是否为管理员',
  `is_disabled` tinyint(1) NULL DEFAULT NULL COMMENT '是否禁用',
  `is_wait` tinyint(1) NULL DEFAULT NULL COMMENT '登录是否等待',
  `wait_time` timestamp NULL DEFAULT NULL COMMENT '等待时间',
  `error` int(11) NULL DEFAULT NULL COMMENT '错误次数',
  `token` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '登录令牌',
  `salt` varbinary(128) NULL DEFAULT NULL COMMENT '盐值',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`uname`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
