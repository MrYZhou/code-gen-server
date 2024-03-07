CREATE DATABASE IF NOT EXISTS study;

/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80025
 Source Host           : 127.0.0.1:3306
 Source Schema         : study

 Target Server Type    : MySQL
 Target Server Version : 80025
 File Encoding         : 65001

 Date: 07/03/2024 23:45:25
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for config
-- ----------------------------
DROP TABLE IF EXISTS `config`;
CREATE TABLE `config`  (
  `id` int NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `age` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of config
-- ----------------------------
INSERT INTO `config` VALUES (1, '123', NULL);
INSERT INTO `config` VALUES (2, '456', NULL);
INSERT INTO `config` VALUES (3, '22', 18);
INSERT INTO `config` VALUES (4, '22', 20);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `address` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `age` bigint NULL DEFAULT NULL,
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `score` bigint NULL DEFAULT NULL,
  `dept` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `created_at` datetime(3) NULL DEFAULT NULL,
  `updated_at` datetime(3) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 411 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (407, '张三', 'password1', '地址1', 25, '12345678901', 80, '部门1', '2024-02-03 03:14:13.000', '2024-02-03 03:14:13.000');
INSERT INTO `users` VALUES (408, '李四', 'password2', '地址2', 30, '12345678902', 90, '部门2', '2024-02-03 03:14:13.000', '2024-02-03 03:14:13.000');
INSERT INTO `users` VALUES (409, '王五', 'password3', '地址3', 35, '12345678903', 70, '部门1', '2024-02-03 03:14:13.000', '2024-02-03 03:14:13.000');
INSERT INTO `users` VALUES (410, '赵六', 'password4', '地址4', 28, '12345678904', 85, '部门2', '2024-02-03 03:14:13.000', '2024-02-03 03:14:13.000');
INSERT INTO `users` VALUES (411, '钱七', 'password5', '地址5', 32, '12345678905', 75, '部门1', '2024-02-03 03:14:13.000', '2024-02-03 03:14:13.000');

SET FOREIGN_KEY_CHECKS = 1;
