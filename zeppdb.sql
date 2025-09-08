/*
 Navicat Premium Data Transfer

 Source Server         : zeppdb
 Source Server Type    : MySQL
 Source Server Version : 50744 (5.7.44-log)
 Source Host           : 192.140.176.128:3306
 Source Schema         : zeppdb

 Target Server Type    : MySQL
 Target Server Version : 50744 (5.7.44-log)
 File Encoding         : 65001

 Date: 01/08/2025 22:37:26
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admins
-- ----------------------------
DROP TABLE IF EXISTS `admins`;
CREATE TABLE `admins`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `openid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '管理员openid',
  `nickname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '管理员昵称',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `openid`(`openid`) USING BTREE,
  INDEX `idx_openid`(`openid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '管理员表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admins
-- ----------------------------
INSERT INTO `admins` VALUES (1, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '管理员1', '2025-08-01 06:46:21');
INSERT INTO `admins` VALUES (2, 'opJ5I6wKtvTZ6CV2H3O5Xr20IVgA', '管理员2', '2025-08-01 06:46:21');

-- ----------------------------
-- Table structure for card_keys
-- ----------------------------
DROP TABLE IF EXISTS `card_keys`;
CREATE TABLE `card_keys`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `key_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '卡密码',
  `days` int(11) NOT NULL COMMENT '增加天数',
  `is_used` tinyint(1) NULL DEFAULT 0 COMMENT '是否已使用',
  `is_active` tinyint(1) NULL DEFAULT 1 COMMENT '是否有效',
  `used_by_openid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '使用者openid',
  `used_by_nickname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '使用者昵称',
  `used_at` datetime NULL DEFAULT NULL COMMENT '使用时间',
  `expires_at` datetime NULL DEFAULT NULL COMMENT '过期时间，NULL表示永久有效',
  `created_by` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '创建者openid',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `key_code`(`key_code`) USING BTREE,
  INDEX `idx_key_code`(`key_code`) USING BTREE,
  INDEX `idx_used_by_openid`(`used_by_openid`) USING BTREE,
  INDEX `idx_created_by`(`created_by`) USING BTREE,
  INDEX `idx_created_at`(`created_at`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '卡密表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of card_keys
-- ----------------------------
INSERT INTO `card_keys` VALUES (2, 'fmol87a2y8vn', 7, 1, 1, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '蕉太兔', '2025-08-01 04:56:04', NULL, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '2025-08-01 12:55:44', '2025-08-01 12:56:04');
INSERT INTO `card_keys` VALUES (3, 'optjkgy5gi2o', 7, 1, 1, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '蕉太兔', '2025-08-01 04:56:14', NULL, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '2025-08-01 12:55:44', '2025-08-01 12:56:13');
INSERT INTO `card_keys` VALUES (4, '99hfxvsq7mzj', 7, 0, 1, NULL, NULL, NULL, NULL, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '2025-08-01 12:55:44', '2025-08-01 12:55:44');
INSERT INTO `card_keys` VALUES (5, '1l6nfze07aed', 7, 0, 1, NULL, NULL, NULL, NULL, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '2025-08-01 12:55:44', '2025-08-01 12:55:44');
INSERT INTO `card_keys` VALUES (6, 'p2b4mn9fddku', 7, 0, 1, NULL, NULL, NULL, NULL, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '2025-08-01 12:55:44', '2025-08-01 12:55:44');
INSERT INTO `card_keys` VALUES (7, 'y1ylhyuq9id6', 7, 0, 1, NULL, NULL, NULL, NULL, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '2025-08-01 12:55:44', '2025-08-01 12:55:44');
INSERT INTO `card_keys` VALUES (8, 'o5euz4ii5i4c', 7, 0, 1, NULL, NULL, NULL, NULL, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '2025-08-01 12:55:44', '2025-08-01 12:55:44');
INSERT INTO `card_keys` VALUES (9, 'vu6ok08r3mve', 7, 0, 1, NULL, NULL, NULL, NULL, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '2025-08-01 12:55:44', '2025-08-01 12:55:44');
INSERT INTO `card_keys` VALUES (10, 'oleopmfoc7m9', 7, 0, 1, NULL, NULL, NULL, NULL, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '2025-08-01 12:55:44', '2025-08-01 12:55:44');
INSERT INTO `card_keys` VALUES (11, 't0jdfq7tbbi2', 7, 0, 1, NULL, NULL, NULL, NULL, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '2025-08-01 12:55:44', '2025-08-01 12:55:44');

-- ----------------------------
-- Table structure for donation_configs
-- ----------------------------
DROP TABLE IF EXISTS `donation_configs`;
CREATE TABLE `donation_configs`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '配置名称',
  `price` float NOT NULL COMMENT '捐赠价格（元）',
  `days` int(11) NOT NULL COMMENT '获得天数',
  `is_active` tinyint(1) NULL DEFAULT NULL COMMENT '是否启用',
  `created_by` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '创建者openid',
  `created_at` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of donation_configs
-- ----------------------------
INSERT INTO `donation_configs` VALUES (1, '捐赠方案1', 0.1, 7, 1, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '2025-08-01 15:22:00', '2025-08-01 15:22:00');
INSERT INTO `donation_configs` VALUES (2, '捐赠方案2', 0.2, 30, 1, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '2025-08-01 15:22:00', '2025-08-01 15:22:00');
INSERT INTO `donation_configs` VALUES (3, '捐赠方案3', 0.3, 10000, 1, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '2025-08-01 15:22:00', '2025-08-01 15:22:00');

-- ----------------------------
-- Table structure for donation_orders
-- ----------------------------
DROP TABLE IF EXISTS `donation_orders`;
CREATE TABLE `donation_orders`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_no` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '订单号',
  `user_openid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户openid',
  `user_nickname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户昵称',
  `amount` float NOT NULL COMMENT '捐赠金额（元）',
  `days` int(11) NOT NULL COMMENT '获得天数',
  `description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '订单描述',
  `prepay_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '微信预支付ID',
  `transaction_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '微信交易号',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '订单状态：pending/paid/failed/cancelled',
  `created_at` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `paid_at` datetime NULL DEFAULT NULL COMMENT '支付时间',
  `updated_at` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `order_no`(`order_no`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of donation_orders
-- ----------------------------
INSERT INTO `donation_orders` VALUES (1, 'DN1754032960191092', 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '蕉太兔', 0.1, 7, '捐赠0.1元获得7天体验时间', NULL, 'mock_transaction_1754032960', 'paid', '2025-08-01 15:22:40', '2025-08-01 07:22:40', '2025-08-01 15:22:40');
INSERT INTO `donation_orders` VALUES (2, 'DN1754032962815477', 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '蕉太兔', 0.2, 30, '捐赠0.2元获得30天体验时间', NULL, 'mock_transaction_1754032962', 'paid', '2025-08-01 15:22:42', '2025-08-01 07:22:43', '2025-08-01 15:22:43');
INSERT INTO `donation_orders` VALUES (3, 'DN1754032965904535', 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '蕉太兔', 0.3, 10000, '捐赠0.3元获得10000天体验时间', NULL, 'mock_transaction_1754032965', 'paid', '2025-08-01 15:22:45', '2025-08-01 07:22:45', '2025-08-01 15:22:45');
INSERT INTO `donation_orders` VALUES (4, 'DN1754035230856416', 'opJ5I61JOtrTFN648cybHU21TbhI', '入坤', 0.1, 7, '捐赠0.1元获得7天体验时间', NULL, NULL, 'failed', '2025-08-01 16:00:30', NULL, '2025-08-01 16:00:30');
INSERT INTO `donation_orders` VALUES (5, 'DN1754035259479564', 'opJ5I61JOtrTFN648cybHU21TbhI', '入坤', 0.1, 7, '捐赠0.1元获得7天体验时间', NULL, NULL, 'failed', '2025-08-01 16:00:59', NULL, '2025-08-01 16:00:59');
INSERT INTO `donation_orders` VALUES (6, 'DN1754036690277874', 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '蕉太兔', 0.1, 7, '捐赠0.1元获得7天体验时间', NULL, NULL, 'failed', '2025-08-01 16:24:50', NULL, '2025-08-01 16:24:51');
INSERT INTO `donation_orders` VALUES (7, 'DN1754045306933548', 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '蕉太兔', 0.1, 7, '捐赠0.1元获得7天体验时间', NULL, NULL, 'pending', '2025-08-01 18:48:26', NULL, '2025-08-01 18:48:26');
INSERT INTO `donation_orders` VALUES (8, 'DN1754045307563261', 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '蕉太兔', 0.1, 7, '捐赠0.1元获得7天体验时间', NULL, NULL, 'pending', '2025-08-01 18:48:27', NULL, '2025-08-01 18:48:27');
INSERT INTO `donation_orders` VALUES (9, 'DN1754045313524371', 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '蕉太兔', 0.1, 7, '捐赠0.1元获得7天体验时间', NULL, NULL, 'pending', '2025-08-01 18:48:33', NULL, '2025-08-01 18:48:33');
INSERT INTO `donation_orders` VALUES (10, 'DN1754045314615026', 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '蕉太兔', 0.2, 30, '捐赠0.2元获得30天体验时间', NULL, NULL, 'pending', '2025-08-01 18:48:34', NULL, '2025-08-01 18:48:34');
INSERT INTO `donation_orders` VALUES (11, 'DN1754045315626935', 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '蕉太兔', 0.3, 10000, '捐赠0.3元获得10000天体验时间', NULL, NULL, 'pending', '2025-08-01 18:48:35', NULL, '2025-08-01 18:48:35');
INSERT INTO `donation_orders` VALUES (12, 'DN1754053466122580', 'opJ5I6wUg4mU80ds4gMsXvRfEkz8', '蕉太猫', 0.1, 7, '捐赠0.1元获得7天体验时间', 'wx0121042688049685a3265348382c360000', '4200002842202508010934940979', 'paid', '2025-08-01 21:04:26', '2025-08-01 13:04:36', '2025-08-01 21:04:35');
INSERT INTO `donation_orders` VALUES (13, 'DN1754053483849764', 'opJ5I6wUg4mU80ds4gMsXvRfEkz8', '蕉太猫', 0.3, 10000, '捐赠0.3元获得10000天体验时间', 'wx012104439832052f5a76cefd710bbd0000', '4200002841202508012690202652', 'paid', '2025-08-01 21:04:43', '2025-08-01 13:04:51', '2025-08-01 21:04:50');

-- ----------------------------
-- Table structure for invite_records
-- ----------------------------
DROP TABLE IF EXISTS `invite_records`;
CREATE TABLE `invite_records`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inviter_openid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邀请人openid',
  `invitee_openid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '被邀请人openid',
  `invitee_nickname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '被邀请人昵称',
  `reward_days` int(11) NULL DEFAULT 3 COMMENT '奖励天数',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_inviter`(`inviter_openid`) USING BTREE,
  INDEX `idx_invitee`(`invitee_openid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '邀请记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of invite_records
-- ----------------------------
INSERT INTO `invite_records` VALUES (1, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 'opJ5I61JOtrTFN648cybHU21TbhI', '入坤', 3, '2025-08-01 03:51:47');
INSERT INTO `invite_records` VALUES (2, 'opJ5I6wKtvTZ6CV2H3O5Xr20IVgA', 'opJ5I6_QYaa8UdHIW8OQ0lo1FHiA', '七嘻小子', 3, '2025-08-01 08:33:31');
INSERT INTO `invite_records` VALUES (3, 'opJ5I6wKtvTZ6CV2H3O5Xr20IVgA', 'opJ5I6w_7SnLbJOPRK1wzLx6hIBM', '微信用户', 3, '2025-08-01 08:40:19');
INSERT INTO `invite_records` VALUES (4, 'opJ5I6wKtvTZ6CV2H3O5Xr20IVgA', 'opJ5I6-RYi-m9RAj96GzHUg-qZX4', '李白¹', 3, '2025-08-01 08:40:23');

-- ----------------------------
-- Table structure for step_records
-- ----------------------------
DROP TABLE IF EXISTS `step_records`;
CREATE TABLE `step_records`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `openid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户openid',
  `steps` int(11) NOT NULL COMMENT '修改的步数',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '修改状态：success/failure',
  `error_message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '错误信息',
  `zepp_username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '使用的Zepp账号',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_openid`(`openid`) USING BTREE,
  INDEX `idx_created_at`(`created_at`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 44 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '步数修改记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of step_records
-- ----------------------------
INSERT INTO `step_records` VALUES (4, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 10000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 01:22:04');
INSERT INTO `step_records` VALUES (5, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 10000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 01:22:10');
INSERT INTO `step_records` VALUES (6, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 12000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 01:22:14');
INSERT INTO `step_records` VALUES (7, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 10000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 01:22:27');
INSERT INTO `step_records` VALUES (8, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 01:22:55');
INSERT INTO `step_records` VALUES (9, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 01:23:15');
INSERT INTO `step_records` VALUES (10, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 01:24:21');
INSERT INTO `step_records` VALUES (11, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'network_error', 'Expecting value: line 1 column 1 (char 0)', 'dt4dsq97m5@163.com', '2025-08-01 02:37:01');
INSERT INTO `step_records` VALUES (12, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'network_error', 'Expecting value: line 1 column 1 (char 0)', 'dt4dsq97m5@163.com', '2025-08-01 02:43:33');
INSERT INTO `step_records` VALUES (13, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'network_error', 'Expecting value: line 1 column 1 (char 0)', 'dt4dsq97m5@163.com', '2025-08-01 02:43:36');
INSERT INTO `step_records` VALUES (14, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'network_error', 'Expecting value: line 1 column 1 (char 0)', 'dt4dsq97m5@163.com', '2025-08-01 02:43:52');
INSERT INTO `step_records` VALUES (15, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'network_error', 'Expecting value: line 1 column 1 (char 0)', 'dt4dsq97m5@163.com', '2025-08-01 02:44:00');
INSERT INTO `step_records` VALUES (16, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'network_error', 'Expecting value: line 1 column 1 (char 0)', 'dt4dsq97m5@163.com', '2025-08-01 02:44:06');
INSERT INTO `step_records` VALUES (17, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'network_error', 'Expecting value: line 1 column 1 (char 0)', 'dt4dsq97m5@163.com', '2025-08-01 02:44:29');
INSERT INTO `step_records` VALUES (18, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'network_error', 'Expecting value: line 1 column 1 (char 0)', 'dt4dsq97m5@163.com', '2025-08-01 02:44:32');
INSERT INTO `step_records` VALUES (19, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 02:46:11');
INSERT INTO `step_records` VALUES (20, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 02:46:24');
INSERT INTO `step_records` VALUES (21, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 02:53:24');
INSERT INTO `step_records` VALUES (22, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 02:53:33');
INSERT INTO `step_records` VALUES (23, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 03:03:54');
INSERT INTO `step_records` VALUES (24, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 12300, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 03:28:29');
INSERT INTO `step_records` VALUES (25, 'opJ5I61JOtrTFN648cybHU21TbhI', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 03:47:30');
INSERT INTO `step_records` VALUES (26, 'opJ5I61JOtrTFN648cybHU21TbhI', 18000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 03:48:08');
INSERT INTO `step_records` VALUES (27, 'opJ5I61JOtrTFN648cybHU21TbhI', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 03:52:37');
INSERT INTO `step_records` VALUES (28, 'opJ5I61JOtrTFN648cybHU21TbhI', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 03:52:39');
INSERT INTO `step_records` VALUES (29, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 03:53:13');
INSERT INTO `step_records` VALUES (30, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 18222, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 03:53:53');
INSERT INTO `step_records` VALUES (31, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 03:54:39');
INSERT INTO `step_records` VALUES (32, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'network_error', 'Expecting value: line 1 column 1 (char 0)', 'dt4dsq97m5@163.com', '2025-08-01 04:55:03');
INSERT INTO `step_records` VALUES (33, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 04:55:30');
INSERT INTO `step_records` VALUES (34, 'opJ5I6wKtvTZ6CV2H3O5Xr20IVgA', 8000, 'success', NULL, 'a6qic03cwh@163.com', '2025-08-01 08:29:42');
INSERT INTO `step_records` VALUES (35, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 08:30:13');
INSERT INTO `step_records` VALUES (36, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 08:30:23');
INSERT INTO `step_records` VALUES (37, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 25000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 08:30:30');
INSERT INTO `step_records` VALUES (38, 'opJ5I6wKtvTZ6CV2H3O5Xr20IVgA', 30000, 'success', NULL, 'a6qic03cwh@163.com', '2025-08-01 08:32:24');
INSERT INTO `step_records` VALUES (39, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 08:35:22');
INSERT INTO `step_records` VALUES (40, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'network_error', '(\'Connection aborted.\', RemoteDisconnected(\'Remote end closed connection without response\'))', 'dt4dsq97m5@163.com', '2025-08-01 08:37:02');
INSERT INTO `step_records` VALUES (41, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 08:37:08');
INSERT INTO `step_records` VALUES (42, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 8000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 10:28:52');
INSERT INTO `step_records` VALUES (43, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 12000, 'success', NULL, 'dt4dsq97m5@163.com', '2025-08-01 10:42:58');

-- ----------------------------
-- Table structure for system_config
-- ----------------------------
DROP TABLE IF EXISTS `system_config`;
CREATE TABLE `system_config`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `config_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '配置键',
  `config_value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '配置值',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '配置描述',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `config_key`(`config_key`) USING BTREE,
  INDEX `idx_config_key`(`config_key`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '系统配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_config
-- ----------------------------
INSERT INTO `system_config` VALUES (1, 'free_trial_days', '5', '免费体验天数', '2025-08-01 06:46:21', '2025-08-01 06:46:21');
INSERT INTO `system_config` VALUES (2, 'invite_reward_days', '3', '邀请奖励天数', '2025-08-01 06:46:21', '2025-08-01 06:46:21');
INSERT INTO `system_config` VALUES (3, 'max_steps', '98800', '最大步数限制', '2025-08-01 06:46:21', '2025-08-01 06:46:21');
INSERT INTO `system_config` VALUES (4, 'min_steps', '1', '最小步数限制', '2025-08-01 06:46:21', '2025-08-01 06:46:21');

-- ----------------------------
-- Table structure for system_settings
-- ----------------------------
DROP TABLE IF EXISTS `system_settings`;
CREATE TABLE `system_settings`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_system_settings_key`(`key`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_settings
-- ----------------------------
INSERT INTO `system_settings` VALUES (1, 'contact_content', '你好，不欢迎你联系客服，我们一定会解决提出问题的人！', '联系客服弹窗显示内容', '2025-08-01 13:03:58', '2025-08-01 13:04:11');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `openid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '微信用户唯一标识',
  `nickname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '微信昵称',
  `headimgurl` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '微信头像URL',
  `expire_time` datetime NOT NULL COMMENT '授权到期时间',
  `total_days` int(11) NULL DEFAULT 5 COMMENT '总授权天数',
  `used_days` int(11) NULL DEFAULT 0 COMMENT '已使用天数',
  `invite_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户专属邀请码',
  `invited_by` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '邀请人openid',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `openid`(`openid`) USING BTREE,
  UNIQUE INDEX `invite_code`(`invite_code`) USING BTREE,
  INDEX `idx_openid`(`openid`) USING BTREE,
  INDEX `idx_invite_code`(`invite_code`) USING BTREE,
  INDEX `idx_invited_by`(`invited_by`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '用户信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '蕉太兔', 'https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJjfbwk5Hf8n4Cbks5bIHcmHQxB97uuj1dFA8qtoOKXW8sNInEa3za35KT4QREgux6CHqiaBxWBO8iaPxJeUboxFdjjdyjbaVpcZpgbWFuqpUfA/132', '2053-02-13 23:44:28', 10059, 0, 'Qrk4A321', NULL, '2025-07-31 23:44:28', '2025-08-01 07:22:45');
INSERT INTO `users` VALUES (2, 'opJ5I6y_irdoI62Lif2Llzt4zUIY', '微信用户', 'https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM4Rv7nYYRvbQVEONuJ0LwLbKeesh5YMZs4aRfGzoCXfTJet5zoWGiby8wG08toVx7H1OqCtmKqiaiaKA/132', '2025-08-06 00:59:53', 5, 0, 'XiRJ0QGz', NULL, '2025-08-01 00:59:53', '2025-08-01 00:59:53');
INSERT INTO `users` VALUES (3, 'opJ5I6wUg4mU80ds4gMsXvRfEkz8', '蕉太猫', 'https://thirdwx.qlogo.cn/mmopen/vi_32/qAvccJ7WZGwq81fTvVqcWq1gLYJ1LVyVohFxFsA2F1Zpysp7Jzia3jFGMtajohc3F61TDkibED1PasUEKyqGU0TICqVyvtbiaxuLtJDTAmnglo/132', '2052-12-29 00:59:58', 10012, 0, 'j5pSqaeK', NULL, '2025-08-01 00:59:58', '2025-08-01 13:04:51');
INSERT INTO `users` VALUES (4, 'opJ5I6xcxg0PAYV_NHpnWFJq5iJ0', '微信用户', 'https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM5AcsibNTTNy3Fiad9vIgSkLmYKCq0ico69Ww04YgxicC8X8B0qrudXiccbg76TNPiaxatRne5TuibpcVMHQ/132', '2025-08-06 01:31:18', 5, 0, 'DRkHN8eL', NULL, '2025-08-01 01:31:18', '2025-08-01 01:31:18');
INSERT INTO `users` VALUES (8, 'opJ5I61JOtrTFN648cybHU21TbhI', '入坤', 'https://thirdwx.qlogo.cn/mmopen/vi_32/x0pq7ibInn5b91FhtRhdRnJibZoPSQib7tPNE6ibvY72HqibGtDYzIvrcXxjicZ5gsDmDjGdiauS9raM6icC36aBZgb4QkwLmrhP5UCunEA78aI5hxQ/132', '2025-08-06 03:49:34', 5, 0, 'EObOVa9A', 'opJ5I68MQNLPGHjL4v-ySEdebjX8', '2025-08-01 03:49:34', '2025-08-01 03:51:47');
INSERT INTO `users` VALUES (9, 'opJ5I6wKtvTZ6CV2H3O5Xr20IVgA', '李白', 'https://thirdwx.qlogo.cn/mmopen/vi_32/pxpJg0r6lmkKaibWp0Lag1U3nZfObe4LwnNkvSdftNEYIgffKtBI6rnJRF8fwp4Z4dy5Lt3hCVv0ZzchSUSXTUQ/132', '2025-08-15 08:28:26', 14, 0, '5hnXFU8s', NULL, '2025-08-01 08:28:26', '2025-08-01 08:40:23');
INSERT INTO `users` VALUES (10, 'opJ5I60a9gVqaXKJZThY55tEqRcc', '微信用户', 'https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7Neohjs6Ue4O6FP55TxSwqKCj6CibDwVGkbZpzgj4P4rhYjBxl4XibUvYzQpN39XJEeF1YiblwREavQ/132', '2025-08-06 08:32:46', 5, 0, 'MqTzrRHu', NULL, '2025-08-01 08:32:46', '2025-08-01 08:32:46');
INSERT INTO `users` VALUES (11, 'opJ5I6_QYaa8UdHIW8OQ0lo1FHiA', '七嘻小子', 'https://thirdwx.qlogo.cn/mmopen/vi_32/QNEbUA9ibCRX2YXh41LmnyqXpUggic3xZM4xDIGVia9YpxH67P89M6nrsDCTr9BgabgMOAqAfScETY8J59JVsgPfw/132', '2025-08-06 08:32:54', 5, 0, 'ZFEvXOQl', 'opJ5I6wKtvTZ6CV2H3O5Xr20IVgA', '2025-08-01 08:32:54', '2025-08-01 08:33:31');
INSERT INTO `users` VALUES (12, 'opJ5I6w_7SnLbJOPRK1wzLx6hIBM', '微信用户', 'https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7Xv3QqyArlPC1F7CnffJwvibiaAYYcENx4rAJcdjUL6chdd6GtmqYiaogMiaEKWRGiadVnCEdCp67GnNw/132', '2025-08-06 08:40:19', 5, 0, 'WWplmRKf', 'opJ5I6wKtvTZ6CV2H3O5Xr20IVgA', '2025-08-01 08:40:19', '2025-08-01 08:40:19');
INSERT INTO `users` VALUES (13, 'opJ5I6-RYi-m9RAj96GzHUg-qZX4', '李白¹', 'https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEK45DdS1ZDj7UiaGAHMkMu0EGFSY3yS1NAzvxQaDKveNvsOk6UfMj9vtDDictk5nIfgicQUybIFSrUtVtUYfSeX5Qe2JcsyMbnGSdx0kjeLcWdnQ/132', '2025-08-06 08:40:23', 5, 0, 'ntswujY0', 'opJ5I6wKtvTZ6CV2H3O5Xr20IVgA', '2025-08-01 08:40:23', '2025-08-01 08:40:23');

-- ----------------------------
-- Table structure for zepp_accounts
-- ----------------------------
DROP TABLE IF EXISTS `zepp_accounts`;
CREATE TABLE `zepp_accounts`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Zepp账号用户名',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Zepp账号密码',
  `userid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Zepp账户userid',
  `qr_code_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '绑定微信的二维码链接',
  `bound_openid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `is_active` tinyint(1) NULL DEFAULT 1 COMMENT '账号是否可用',
  `bind_status` tinyint(1) NULL DEFAULT 0 COMMENT '绑定状态：0未绑定，1已绑定',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_username`(`username`) USING BTREE,
  UNIQUE INDEX `unique_bound_openid`(`bound_openid`) USING BTREE,
  INDEX `idx_bound_openid`(`bound_openid`) USING BTREE,
  INDEX `idx_bind_status`(`bind_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'Zepp账号信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of zepp_accounts
-- ----------------------------
INSERT INTO `zepp_accounts` VALUES (18, 'dt4dsq97m5@163.com', 'aa123456', '1134822148', 'http://we.qq.com/d/AQBG9yW38dXGKQwhbmoQ3Y0DHGxdxvnfJ7efwo6o', 'opJ5I68MQNLPGHjL4v-ySEdebjX8', 1, 1, '2025-08-01 09:53:42', '2025-08-01 10:42:55');
INSERT INTO `zepp_accounts` VALUES (19, 'a6qic03cwh@163.com', 'aa123456', '1134822171', 'http://we.qq.com/d/AQBG9yW3oeNQ8pmE0HLvm5Bp4vmlHXxQA5pm0abh', NULL, 1, 0, '2025-08-01 09:53:43', '2025-08-01 09:53:43');
INSERT INTO `zepp_accounts` VALUES (20, 'q5ijkocbwi@163.com', 'aa123456', '1134822143', 'http://we.qq.com/d/AQBG9yW3a5bAqcBa6ssguzOFOBqvzM5TVjyTRp13', NULL, 1, 0, '2025-08-01 09:53:44', '2025-08-01 09:53:44');
INSERT INTO `zepp_accounts` VALUES (21, 'zru1eb0wos@163.com', 'aa123456', '1134822170', 'http://we.qq.com/d/AQBG9yW3SgM3YADFD4KH6VmdJrH_I_wgHECHenaR', NULL, 1, 0, '2025-08-01 09:53:45', '2025-08-01 09:53:45');
INSERT INTO `zepp_accounts` VALUES (22, 'bsu4kocxz0@163.com', 'aa123456', '1134822173', 'http://we.qq.com/d/AQBG9yW3v7ycB_RKv23_YazZOgXjpeplorneksM3', NULL, 1, 0, '2025-08-01 09:53:47', '2025-08-01 09:53:47');

SET FOREIGN_KEY_CHECKS = 1;
