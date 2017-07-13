/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : PostgreSQL
 Source Server Version : 90603
 Source Host           : localhost
 Source Database       : ctf
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 90603
 File Encoding         : utf-8

 Date: 07/13/2017 19:46:10 PM
*/

-- ----------------------------
--  Table structure for flags_stolen
-- ----------------------------
DROP TABLE IF EXISTS "public"."flags_stolen";
CREATE TABLE "public"."flags_stolen" (
	"flag_id" int4 NOT NULL,
	"timestamp" timestamp(6) NOT NULL DEFAULT now(),
	"team_id" int2 NOT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."flags_stolen" OWNER TO "ctf";

-- ----------------------------
--  Table structure for logs
-- ----------------------------
DROP TABLE IF EXISTS "public"."logs";
CREATE TABLE "public"."logs" (
	"id" int4 NOT NULL DEFAULT nextval('log_id_seq'::regclass),
	"team_id" int2 NOT NULL,
	"service_id" int2 NOT NULL,
	"timestamp" varchar(20) NOT NULL COLLATE "default",
	"code" int2 NOT NULL DEFAULT 110,
	"message" varchar NOT NULL COLLATE "default",
	"type" int2 NOT NULL DEFAULT 1,
	"flag" varchar(100) DEFAULT NULL::character varying COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."logs" OWNER TO "ctf";

-- ----------------------------
--  Table structure for round_total
-- ----------------------------
DROP TABLE IF EXISTS "public"."round_total";
CREATE TABLE "public"."round_total" (
	"team_id" int2 NOT NULL,
	"service_id" int2 NOT NULL,
	"round" int2 NOT NULL,
	"a_points" int4 NOT NULL,
	"d_points" int4 NOT NULL,
	"place" int2 NOT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."round_total" OWNER TO "ctf";

-- ----------------------------
--  Table structure for services
-- ----------------------------
DROP TABLE IF EXISTS "public"."services";
CREATE TABLE "public"."services" (
	"id" int2 NOT NULL DEFAULT nextval('services_id_seq'::regclass),
	"name" varchar(40) NOT NULL DEFAULT 'Test service'::character varying COLLATE "default",
	"info" varchar NOT NULL DEFAULT 'Test description'::character varying COLLATE "default",
	"exploit" text COLLATE "default",
	"interval" int2,
	"hash" varchar NOT NULL COLLATE "default",
	"multiplier" float4 NOT NULL DEFAULT 1.0
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."services" OWNER TO "ctf";

-- ----------------------------
--  Table structure for teams
-- ----------------------------
DROP TABLE IF EXISTS "public"."teams";
CREATE TABLE "public"."teams" (
	"id" int2 NOT NULL DEFAULT nextval('teams_id_seq'::regclass),
	"name" varchar(40) NOT NULL DEFAULT 'Noname'::character varying COLLATE "default",
	"logo" varchar NOT NULL DEFAULT 'http://web.vmc3.com/projects/bufs2016/branch/army/logos/NoLogo.jpg'::character varying COLLATE "default",
	"network" varchar NOT NULL DEFAULT '10.60.0.0/24'::character varying COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."teams" OWNER TO "ctf";

-- ----------------------------
--  Primary key structure for table flags_stolen
-- ----------------------------
ALTER TABLE "public"."flags_stolen" ADD PRIMARY KEY ("flag_id", "team_id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table logs
-- ----------------------------
ALTER TABLE "public"."logs" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Indexes structure for table logs
-- ----------------------------
CREATE INDEX  "service" ON "public"."logs" USING btree(service_id "pg_catalog"."int2_ops" ASC NULLS LAST);
CREATE INDEX  "team" ON "public"."logs" USING btree(team_id "pg_catalog"."int2_ops" ASC NULLS LAST);

-- ----------------------------
--  Primary key structure for table round_total
-- ----------------------------
ALTER TABLE "public"."round_total" ADD PRIMARY KEY ("team_id", "service_id", "round") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table services
-- ----------------------------
ALTER TABLE "public"."services" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table teams
-- ----------------------------
ALTER TABLE "public"."teams" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

