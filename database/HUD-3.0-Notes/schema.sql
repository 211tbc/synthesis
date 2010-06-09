/*
 Navicat Premium Data Transfer

 Source Server         : dev-synthesis-01
 Source Server Type    : PostgreSQL
 Source Server Version : 80309
 Source Host           : 127.0.0.1
 Source Database       : synthesis
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 80309
 File Encoding         : utf-8

 Date: 06/09/2010 03:03:47 AM
*/

-- ----------------------------
--  Sequence structure for "age_requirements_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "age_requirements_id_seq";
CREATE SEQUENCE "age_requirements_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "age_requirements_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "agency_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "agency_2010_id_seq";
CREATE SEQUENCE "agency_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "agency_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "agency_child_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "agency_child_2010_id_seq";
CREATE SEQUENCE "agency_child_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "agency_child_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "agency_service_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "agency_service_2010_id_seq";
CREATE SEQUENCE "agency_service_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "agency_service_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "aid_requirements_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "aid_requirements_id_seq";
CREATE SEQUENCE "aid_requirements_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "aid_requirements_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "aka_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "aka_2010_id_seq";
CREATE SEQUENCE "aka_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "aka_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "application_process_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "application_process_2010_id_seq";
CREATE SEQUENCE "application_process_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "application_process_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "assignment_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "assignment_2010_id_seq";
CREATE SEQUENCE "assignment_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "assignment_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "assignment_period_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "assignment_period_2010_id_seq";
CREATE SEQUENCE "assignment_period_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "assignment_period_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "child_enrollment_status_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "child_enrollment_status_2010_id_seq";
CREATE SEQUENCE "child_enrollment_status_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "child_enrollment_status_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "child_enrollment_status_barrier_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "child_enrollment_status_barrier_2010_id_seq";
CREATE SEQUENCE "child_enrollment_status_barrier_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "child_enrollment_status_barrier_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "chronic_health_condition_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "chronic_health_condition_2010_id_seq";
CREATE SEQUENCE "chronic_health_condition_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "chronic_health_condition_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "contact_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "contact_2010_id_seq";
CREATE SEQUENCE "contact_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "contact_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "contact_made_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "contact_made_2010_id_seq";
CREATE SEQUENCE "contact_made_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "contact_made_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "cross_street_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "cross_street_2010_id_seq";
CREATE SEQUENCE "cross_street_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "cross_street_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "currently_in_school_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "currently_in_school_2010_id_seq";
CREATE SEQUENCE "currently_in_school_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "currently_in_school_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "degree_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "degree_2010_id_seq";
CREATE SEQUENCE "degree_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "degree_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "degree_code_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "degree_code_2010_id_seq";
CREATE SEQUENCE "degree_code_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "degree_code_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "destinations_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "destinations_2010_id_seq";
CREATE SEQUENCE "destinations_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "destinations_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "developmental_disability_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "developmental_disability_2010_id_seq";
CREATE SEQUENCE "developmental_disability_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "developmental_disability_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "disabling_condition_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "disabling_condition_2010_id_seq";
CREATE SEQUENCE "disabling_condition_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "disabling_condition_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "documents_required_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "documents_required_2010_id_seq";
CREATE SEQUENCE "documents_required_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "documents_required_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "domestic_violence_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "domestic_violence_2010_id_seq";
CREATE SEQUENCE "domestic_violence_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "domestic_violence_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "drug_history_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "drug_history_id_seq";
CREATE SEQUENCE "drug_history_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "drug_history_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "email_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "email_2010_id_seq";
CREATE SEQUENCE "email_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "email_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "emergency_contact_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "emergency_contact_id_seq";
CREATE SEQUENCE "emergency_contact_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "emergency_contact_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "employment_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "employment_2010_id_seq";
CREATE SEQUENCE "employment_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "employment_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "engaged_date_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "engaged_date_2010_id_seq";
CREATE SEQUENCE "engaged_date_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "engaged_date_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "family_requirements_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "family_requirements_2010_id_seq";
CREATE SEQUENCE "family_requirements_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "family_requirements_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "funding_source_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "funding_source_2010_id_seq";
CREATE SEQUENCE "funding_source_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "funding_source_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "geographic_area_served_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "geographic_area_served_2010_id_seq";
CREATE SEQUENCE "geographic_area_served_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "geographic_area_served_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "health_status_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "health_status_2010_id_seq";
CREATE SEQUENCE "health_status_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "health_status_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "highest_school_level_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "highest_school_level_2010_id_seq";
CREATE SEQUENCE "highest_school_level_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "highest_school_level_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "hiv_aids_status_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "hiv_aids_status_2010_id_seq";
CREATE SEQUENCE "hiv_aids_status_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "hiv_aids_status_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "hmis_asset_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "hmis_asset_2010_id_seq";
CREATE SEQUENCE "hmis_asset_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "hmis_asset_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "household_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "household_id_seq";
CREATE SEQUENCE "household_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "household_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "housing_status_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "housing_status_2010_id_seq";
CREATE SEQUENCE "housing_status_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "housing_status_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "hud_chronic_homeless_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "hud_chronic_homeless_2010_id_seq";
CREATE SEQUENCE "hud_chronic_homeless_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "hud_chronic_homeless_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "hud_homeless_episodes_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "hud_homeless_episodes_id_seq";
CREATE SEQUENCE "hud_homeless_episodes_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "hud_homeless_episodes_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "income_and_sources_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "income_and_sources_id_seq";
CREATE SEQUENCE "income_and_sources_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "income_and_sources_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "income_last_30_days_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "income_last_30_days_2010_id_seq";
CREATE SEQUENCE "income_last_30_days_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "income_last_30_days_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "income_requirements_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "income_requirements_2010_id_seq";
CREATE SEQUENCE "income_requirements_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "income_requirements_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "income_total_monthly_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "income_total_monthly_2010_id_seq";
CREATE SEQUENCE "income_total_monthly_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "income_total_monthly_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "inventory_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "inventory_2010_id_seq";
CREATE SEQUENCE "inventory_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "inventory_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "languages_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "languages_2010_id_seq";
CREATE SEQUENCE "languages_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "languages_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "length_of_stay_at_prior_residence_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "length_of_stay_at_prior_residence_2010_id_seq";
CREATE SEQUENCE "length_of_stay_at_prior_residence_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "length_of_stay_at_prior_residence_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "license_accreditation_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "license_accreditation_2010_id_seq";
CREATE SEQUENCE "license_accreditation_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "license_accreditation_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "members_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "members_id_seq";
CREATE SEQUENCE "members_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "members_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "mental_health_problem_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "mental_health_problem_2010_id_seq";
CREATE SEQUENCE "mental_health_problem_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "mental_health_problem_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "need_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "need_id_seq";
CREATE SEQUENCE "need_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "need_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "non_cash_benefits_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "non_cash_benefits_2010_id_seq";
CREATE SEQUENCE "non_cash_benefits_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "non_cash_benefits_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "non_cash_benefits_last_30_days_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "non_cash_benefits_last_30_days_2010_id_seq";
CREATE SEQUENCE "non_cash_benefits_last_30_days_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "non_cash_benefits_last_30_days_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "other_address_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "other_address_2010_id_seq";
CREATE SEQUENCE "other_address_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "other_address_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "other_names_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "other_names_id_seq";
CREATE SEQUENCE "other_names_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "other_names_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "other_requirements_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "other_requirements_2010_id_seq";
CREATE SEQUENCE "other_requirements_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "other_requirements_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "person_address_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "person_address_id_seq";
CREATE SEQUENCE "person_address_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "person_address_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "person_historical_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "person_historical_id_seq";
CREATE SEQUENCE "person_historical_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "person_historical_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "person_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "person_id_seq";
CREATE SEQUENCE "person_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "person_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "phone_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "phone_2010_id_seq";
CREATE SEQUENCE "phone_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "phone_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "physical_disability_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "physical_disability_2010_id_seq";
CREATE SEQUENCE "physical_disability_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "physical_disability_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "pit_count_set_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "pit_count_set_2010_id_seq";
CREATE SEQUENCE "pit_count_set_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "pit_count_set_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "pit_counts_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "pit_counts_2010_id_seq";
CREATE SEQUENCE "pit_counts_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "pit_counts_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "pregnancy_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "pregnancy_2010_id_seq";
CREATE SEQUENCE "pregnancy_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "pregnancy_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "prior_residence_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "prior_residence_2010_id_seq";
CREATE SEQUENCE "prior_residence_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "prior_residence_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "races_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "races_id_seq";
CREATE SEQUENCE "races_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "races_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "reasons_for_leaving_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "reasons_for_leaving_2010_id_seq";
CREATE SEQUENCE "reasons_for_leaving_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "reasons_for_leaving_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "region_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "region_2010_id_seq";
CREATE SEQUENCE "region_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "region_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "release_of_information_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "release_of_information_id_seq";
CREATE SEQUENCE "release_of_information_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "release_of_information_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "residency_requirements_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "residency_requirements_2010_id_seq";
CREATE SEQUENCE "residency_requirements_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "residency_requirements_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "resource_info_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "resource_info_2010_id_seq";
CREATE SEQUENCE "resource_info_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "resource_info_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "seasonal_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "seasonal_2010_id_seq";
CREATE SEQUENCE "seasonal_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "seasonal_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "sender_system_configuration_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "sender_system_configuration_id_seq";
CREATE SEQUENCE "sender_system_configuration_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "sender_system_configuration_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "service_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "service_2010_id_seq";
CREATE SEQUENCE "service_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "service_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "service_event_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "service_event_id_seq";
CREATE SEQUENCE "service_event_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "service_event_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "service_event_notes_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "service_event_notes_2010_id_seq";
CREATE SEQUENCE "service_event_notes_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "service_event_notes_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "service_group_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "service_group_2010_id_seq";
CREATE SEQUENCE "service_group_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "service_group_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "site_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "site_2010_id_seq";
CREATE SEQUENCE "site_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "site_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "site_service_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "site_service_2010_id_seq";
CREATE SEQUENCE "site_service_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "site_service_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "site_service_participation_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "site_service_participation_id_seq";
CREATE SEQUENCE "site_service_participation_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "site_service_participation_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "source_export_link_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "source_export_link_2010_id_seq";
CREATE SEQUENCE "source_export_link_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "source_export_link_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "source_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "source_id_seq";
CREATE SEQUENCE "source_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "source_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "spatial_location_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "spatial_location_2010_id_seq";
CREATE SEQUENCE "spatial_location_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "spatial_location_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "substance_abuse_problem_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "substance_abuse_problem_2010_id_seq";
CREATE SEQUENCE "substance_abuse_problem_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "substance_abuse_problem_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "taxonomy_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "taxonomy_2010_id_seq";
CREATE SEQUENCE "taxonomy_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "taxonomy_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "time_open_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "time_open_2010_id_seq";
CREATE SEQUENCE "time_open_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "time_open_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "time_open_days_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "time_open_days_2010_id_seq";
CREATE SEQUENCE "time_open_days_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "time_open_days_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "url_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "url_id_seq";
CREATE SEQUENCE "url_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "url_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "veteran_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "veteran_id_seq";
CREATE SEQUENCE "veteran_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "veteran_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "veteran_military_branches_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "veteran_military_branches_2010_id_seq";
CREATE SEQUENCE "veteran_military_branches_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "veteran_military_branches_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "veteran_military_service_duration_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "veteran_military_service_duration_2010_id_seq";
CREATE SEQUENCE "veteran_military_service_duration_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "veteran_military_service_duration_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "veteran_served_in_war_zone_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "veteran_served_in_war_zone_2010_id_seq";
CREATE SEQUENCE "veteran_served_in_war_zone_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "veteran_served_in_war_zone_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "veteran_service_era_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "veteran_service_era_2010_id_seq";
CREATE SEQUENCE "veteran_service_era_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "veteran_service_era_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "veteran_veteran_status_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "veteran_veteran_status_2010_id_seq";
CREATE SEQUENCE "veteran_veteran_status_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "veteran_veteran_status_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "veteran_warzones_served_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "veteran_warzones_served_2010_id_seq";
CREATE SEQUENCE "veteran_warzones_served_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "veteran_warzones_served_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for "vocational_training_2010_id_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "vocational_training_2010_id_seq";
CREATE SEQUENCE "vocational_training_2010_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "vocational_training_2010_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "contact_2010"
-- ----------------------------
DROP TABLE IF EXISTS "contact_2010";
CREATE TABLE "contact_2010" (
	"id" int4 NOT NULL DEFAULT nextval('contact_2010_id_seq'::regclass),
	"agency_index_id" int4 DEFAULT NULL,
	"resource_info_index_id" int4 DEFAULT NULL,
	"site_index_id" int4 DEFAULT NULL,
	"title" varchar(50) DEFAULT NULL,
	"name" varchar(50) DEFAULT NULL,
	"type" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "contact_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "phone_2010"
-- ----------------------------
DROP TABLE IF EXISTS "phone_2010";
CREATE TABLE "phone_2010" (
	"id" int4 NOT NULL DEFAULT nextval('phone_2010_id_seq'::regclass),
	"agency_index_id" int4 DEFAULT NULL,
	"contact_index_id" int4 DEFAULT NULL,
	"resource_info_index_id" int4 DEFAULT NULL,
	"site_index_id" int4 DEFAULT NULL,
	"site_service_index_id" int4 DEFAULT NULL,
	"person_historical_index_id" int4 DEFAULT NULL,
	"phone_number" varchar(50) DEFAULT NULL,
	"reason_withheld" varchar(50) DEFAULT NULL,
	"extension" varchar(50) DEFAULT NULL,
	"description" varchar(50) DEFAULT NULL,
	"type" varchar(50) DEFAULT NULL,
	"function" varchar(50) DEFAULT NULL,
	"toll_free" varchar(50) DEFAULT NULL,
	"confidential" varchar(50) DEFAULT NULL,
	"person_phone_number" varchar(50) DEFAULT NULL,
	"person_phone_number_date_collected" timestamptz DEFAULT NULL,
	"person_phone_number_date_effective" timestamptz DEFAULT NULL,
	"person_phone_number_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "phone_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "dedup_link"
-- ----------------------------
DROP TABLE IF EXISTS "dedup_link";
CREATE TABLE "dedup_link" (
	"source_rec_id" varchar(50) NOT NULL DEFAULT NULL,
	"destination_rec_id" varchar(50) DEFAULT NULL,
	"weight_factor" int4 DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "dedup_link" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "sender_system_configuration"
-- ----------------------------
DROP TABLE IF EXISTS "sender_system_configuration";
CREATE TABLE "sender_system_configuration" (
	"id" int4 NOT NULL DEFAULT nextval('sender_system_configuration_id_seq'::regclass),
	"vendor_name" varchar(50) DEFAULT NULL,
	"processing_mode" varchar(4) DEFAULT NULL,
	"source_id" varchar(50) DEFAULT NULL,
	"odbid" int4 DEFAULT NULL,
	"providerid" int4 DEFAULT NULL,
	"userid" int4 DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "sender_system_configuration" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "email_2010"
-- ----------------------------
DROP TABLE IF EXISTS "email_2010";
CREATE TABLE "email_2010" (
	"id" int4 NOT NULL DEFAULT nextval('email_2010_id_seq'::regclass),
	"agency_index_id" int4 DEFAULT NULL,
	"contact_index_id" int4 DEFAULT NULL,
	"resource_info_index_id" int4 DEFAULT NULL,
	"site_index_id" int4 DEFAULT NULL,
	"person_historical_index_id" int4 DEFAULT NULL,
	"address" varchar(50) DEFAULT NULL,
	"note" varchar(50) DEFAULT NULL,
	"person_email" varchar(50) DEFAULT NULL,
	"person_email_date_collected" timestamptz DEFAULT NULL,
	"person_email_date_effective" timestamptz DEFAULT NULL,
	"person_email_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "email_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "agency_child_2010"
-- ----------------------------
DROP TABLE IF EXISTS "agency_child_2010";
CREATE TABLE "agency_child_2010" (
	"id" int4 NOT NULL DEFAULT nextval('agency_child_2010_id_seq'::regclass),
	"export_index_id" varchar(50) DEFAULT NULL,
	"agency_index_id" int4 DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "agency_child_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "region_2010"
-- ----------------------------
DROP TABLE IF EXISTS "region_2010";
CREATE TABLE "region_2010" (
	"id" int4 NOT NULL DEFAULT nextval('region_2010_id_seq'::regclass),
	"export_index_id" varchar(50) DEFAULT NULL,
	"region_id_id_num" varchar(50) DEFAULT NULL,
	"region_id_id_str" varchar(50) DEFAULT NULL,
	"site_service_id" varchar(50) DEFAULT NULL,
	"region_type" varchar(50) DEFAULT NULL,
	"region_type_date_collected" timestamptz DEFAULT NULL,
	"region_type_date_effective" timestamptz DEFAULT NULL,
	"region_type_data_collection_stage" int4 DEFAULT NULL,
	"region_description" varchar(50) DEFAULT NULL,
	"region_description_date_collected" timestamptz DEFAULT NULL,
	"region_description_date_effective" timestamptz DEFAULT NULL,
	"region_description_data_collection_stage" int4 DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "region_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "service_2010"
-- ----------------------------
DROP TABLE IF EXISTS "service_2010";
CREATE TABLE "service_2010" (
	"id" int4 NOT NULL DEFAULT nextval('service_2010_id_seq'::regclass),
	"export_index_id" varchar(50) DEFAULT NULL,
	"attr_delete" int4 DEFAULT NULL,
	"attr_delete_occurred_date" timestamptz DEFAULT NULL,
	"attr_effective" timestamptz DEFAULT NULL,
	"airs_key" varchar(50) DEFAULT NULL,
	"airs_name" varchar(50) DEFAULT NULL,
	"coc_code" varchar(50) DEFAULT NULL,
	"configuration" varchar(50) DEFAULT NULL,
	"direct_service_code" varchar(50) DEFAULT NULL,
	"grantee_identifier" varchar(50) DEFAULT NULL,
	"individual_family_code" varchar(50) DEFAULT NULL,
	"residential_tracking_method" varchar(50) DEFAULT NULL,
	"service_type" varchar(50) DEFAULT NULL,
	"service_effective_period_start_date" timestamptz DEFAULT NULL,
	"service_effective_period_end_date" timestamptz DEFAULT NULL,
	"service_recorded_date" timestamptz DEFAULT NULL,
	"target_population_a" varchar(50) DEFAULT NULL,
	"target_population_b" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "service_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "source"
-- ----------------------------
DROP TABLE IF EXISTS "source";
CREATE TABLE "source" (
	"id" int4 NOT NULL DEFAULT nextval('source_id_seq'::regclass),
	"export_id" varchar(50) DEFAULT NULL,
	"source_id" varchar(50) DEFAULT NULL,
	"source_id_date_collected" timestamptz DEFAULT NULL,
	"source_email" varchar(50) DEFAULT NULL,
	"source_email_date_collected" timestamptz DEFAULT NULL,
	"source_contact_extension" varchar(10) DEFAULT NULL,
	"source_contact_extension_date_collected" timestamptz DEFAULT NULL,
	"source_contact_first" varchar(20) DEFAULT NULL,
	"source_contact_first_date_collected" timestamptz DEFAULT NULL,
	"source_contact_last" varchar(20) DEFAULT NULL,
	"source_contact_last_date_collected" timestamptz DEFAULT NULL,
	"source_contact_phone" varchar(20) DEFAULT NULL,
	"source_contact_phone_date_collected" timestamptz DEFAULT NULL,
	"source_name" varchar(50) DEFAULT NULL,
	"source_name_date_collected" timestamptz DEFAULT NULL,
	"attr_version" varchar(50) DEFAULT NULL,
	"source_id_id_id_num_2010" varchar(50) DEFAULT NULL,
	"source_id_id_id_str_2010" varchar(50) DEFAULT NULL,
	"source_id_id_delete_2010" int4 DEFAULT NULL,
	"source_id_id_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"source_id_id_delete_effective_2010" timestamptz DEFAULT NULL,
	"software_vendor_2010" varchar(50) DEFAULT NULL,
	"software_version_2010" varchar(50) DEFAULT NULL,
	"source_contact_email_2010" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "source" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "source_export_link_2010"
-- ----------------------------
DROP TABLE IF EXISTS "source_export_link_2010";
CREATE TABLE "source_export_link_2010" (
	"id" int4 NOT NULL DEFAULT nextval('source_export_link_2010_id_seq'::regclass),
	"source_index_id" int4 DEFAULT NULL,
	"export_index_id" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "source_export_link_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "license_accreditation_2010"
-- ----------------------------
DROP TABLE IF EXISTS "license_accreditation_2010";
CREATE TABLE "license_accreditation_2010" (
	"id" int4 NOT NULL DEFAULT nextval('license_accreditation_2010_id_seq'::regclass),
	"agency_index_id" int4 DEFAULT NULL,
	"license" varchar(50) DEFAULT NULL,
	"licensed_by" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "license_accreditation_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "person"
-- ----------------------------
DROP TABLE IF EXISTS "person";
CREATE TABLE "person" (
	"id" int4 NOT NULL DEFAULT nextval('person_id_seq'::regclass),
	"export_id" varchar(50) DEFAULT NULL,
	"person_id_hashed" varchar(32) DEFAULT NULL,
	"person_id_unhashed" varchar(50) DEFAULT NULL,
	"person_id_date_collected" timestamptz DEFAULT NULL,
	"person_date_of_birth_hashed" varchar(32) DEFAULT NULL,
	"person_date_of_birth_unhashed" date DEFAULT NULL,
	"person_date_of_birth_date_collected" timestamptz DEFAULT NULL,
	"person_ethnicity_hashed" varchar(32) DEFAULT NULL,
	"person_ethnicity_unhashed" int4 DEFAULT NULL,
	"person_ethnicity_date_collected" timestamptz DEFAULT NULL,
	"person_gender_hashed" varchar(32) DEFAULT NULL,
	"person_gender_unhashed" int4 DEFAULT NULL,
	"person_gender_date_collected" timestamptz DEFAULT NULL,
	"person_legal_first_name_hashed" varchar(32) DEFAULT NULL,
	"person_legal_first_name_unhashed" varchar(50) DEFAULT NULL,
	"person_legal_first_name_date_collected" timestamptz DEFAULT NULL,
	"person_legal_last_name_hashed" varchar(32) DEFAULT NULL,
	"person_legal_last_name_unhashed" varchar(50) DEFAULT NULL,
	"person_legal_last_name_date_collected" timestamptz DEFAULT NULL,
	"person_legal_middle_name_hashed" varchar(32) DEFAULT NULL,
	"person_legal_middle_name_unhashed" varchar(50) DEFAULT NULL,
	"person_legal_middle_name_date_collected" timestamptz DEFAULT NULL,
	"person_legal_suffix_hashed" varchar(32) DEFAULT NULL,
	"person_legal_suffix_unhashed" varchar(50) DEFAULT NULL,
	"person_legal_suffix_date_collected" timestamptz DEFAULT NULL,
	"person_social_security_number_hashed" varchar(32) DEFAULT NULL,
	"person_social_security_number_unhashed" varchar(9) DEFAULT NULL,
	"person_social_security_number_date_collected" timestamptz DEFAULT NULL,
	"person_social_sec_number_quality_code" varchar(2) DEFAULT NULL,
	"person_social_sec_number_quality_code_date_collected" timestamptz DEFAULT NULL,
	"reported" bool DEFAULT NULL,
	"person_id_id_num_2010" varchar(50) DEFAULT NULL,
	"person_id_id_str_2010" varchar(50) DEFAULT NULL,
	"person_id_delete_2010" int4 DEFAULT NULL,
	"person_id_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_id_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_date_of_birth_hashed_delete_2010" int4 DEFAULT NULL,
	"person_date_of_birth_hashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_date_of_birth_hashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_date_of_birth_unhashed_delete_2010" int4 DEFAULT NULL,
	"person_date_of_birth_unhashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_date_of_birth_unhashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_ethnicity_hashed_delete_2010" int4 DEFAULT NULL,
	"person_ethnicity_hashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_ethnicity_hashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_ethnicity_unhashed_delete_2010" int4 DEFAULT NULL,
	"person_ethnicity_unhashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_ethnicity_unhashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_gender_hashed_delete_2010" int4 DEFAULT NULL,
	"person_gender_hashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_gender_hashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_gender_unhashed_delete_2010" int4 DEFAULT NULL,
	"person_gender_unhashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_gender_unhashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_legal_first_name_hashed_delete_2010" int4 DEFAULT NULL,
	"person_legal_first_name_hashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_legal_first_name_hashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_legal_first_name_unhashed_delete_2010" int4 DEFAULT NULL,
	"person_legal_first_name_unhashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_legal_first_name_unhashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_legal_last_name_unhashed_delete_2010" int4 DEFAULT NULL,
	"person_legal_last_name_unhashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_legal_last_name_unhashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_legal_last_name_hashed_delete_2010" int4 DEFAULT NULL,
	"person_legal_last_name_hashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_legal_last_name_hashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_legal_middle_name_hashed_delete_2010" int4 DEFAULT NULL,
	"person_legal_middle_name_hashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_legal_middle_name_hashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_legal_middle_name_unhashed_delete_2010" int4 DEFAULT NULL,
	"person_legal_middle_name_unhashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_legal_middle_name_unhashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_legal_suffix_hashed_delete_2010" int4 DEFAULT NULL,
	"person_legal_suffix_hashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_legal_suffix_hashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_legal_suffix_unhashed_delete_2010" int4 DEFAULT NULL,
	"person_legal_suffix_unhashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_legal_suffix_unhashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_social_security_number_hashed_delete_2010" int4 DEFAULT NULL,
	"person_social_security_number_hashed_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_social_security_number_hashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_social_security_number_unhashed_delete_2010" int4 DEFAULT NULL,
	"person_social_security_number_unhashed_delete_occurred_date_201" timestamptz DEFAULT NULL,
	"person_social_security_number_unhashed_delete_effective_2010" timestamptz DEFAULT NULL,
	"person_social_security_number_quality_code_delete_2010" int4 DEFAULT NULL,
	"person_social_security_number_quality_code_delete_occurred_date" timestamptz DEFAULT NULL,
	"person_social_security_number_quality_code_delete_effective_201" timestamptz DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "person" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "agency_service_2010"
-- ----------------------------
DROP TABLE IF EXISTS "agency_service_2010";
CREATE TABLE "agency_service_2010" (
	"id" int4 NOT NULL DEFAULT nextval('agency_service_2010_id_seq'::regclass),
	"agency_index_id" int4 DEFAULT NULL,
	"key" varchar(50) DEFAULT NULL,
	"agency_key" varchar(50) DEFAULT NULL,
	"name" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "agency_service_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "service_group_2010"
-- ----------------------------
DROP TABLE IF EXISTS "service_group_2010";
CREATE TABLE "service_group_2010" (
	"id" int4 NOT NULL DEFAULT nextval('service_group_2010_id_seq'::regclass),
	"agency_index_id" int4 DEFAULT NULL,
	"key" varchar(50) DEFAULT NULL,
	"name" varchar(50) DEFAULT NULL,
	"program_name" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "service_group_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "seasonal_2010"
-- ----------------------------
DROP TABLE IF EXISTS "seasonal_2010";
CREATE TABLE "seasonal_2010" (
	"id" int4 NOT NULL DEFAULT nextval('seasonal_2010_id_seq'::regclass),
	"site_service_index_id" int4 DEFAULT NULL,
	"description" varchar(50) DEFAULT NULL,
	"start_date" timestamptz DEFAULT NULL,
	"end_date" timestamptz DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "seasonal_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "aka_2010"
-- ----------------------------
DROP TABLE IF EXISTS "aka_2010";
CREATE TABLE "aka_2010" (
	"id" int4 NOT NULL DEFAULT nextval('aka_2010_id_seq'::regclass),
	"agency_index_id" int4 DEFAULT NULL,
	"site_index_id" int4 DEFAULT NULL,
	"name" varchar(50) DEFAULT NULL,
	"confidential" varchar(50) DEFAULT NULL,
	"description" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "aka_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "url"
-- ----------------------------
DROP TABLE IF EXISTS "url";
CREATE TABLE "url" (
	"id" int4 NOT NULL DEFAULT nextval('url_id_seq'::regclass),
	"agency_index_id" int4 DEFAULT NULL,
	"site_index_id" int4 DEFAULT NULL,
	"address" varchar(50) DEFAULT NULL,
	"note" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "url" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "agency_2010"
-- ----------------------------
DROP TABLE IF EXISTS "agency_2010";
CREATE TABLE "agency_2010" (
	"id" int4 NOT NULL DEFAULT nextval('agency_2010_id_seq'::regclass),
	"export_index_id" varchar(50) DEFAULT NULL,
	"attr_delete" int4 DEFAULT NULL,
	"attr_delete_occurred_date" timestamptz DEFAULT NULL,
	"attr_effective" timestamptz DEFAULT NULL,
	"airs_key" varchar(50) DEFAULT NULL,
	"airs_name" varchar(50) DEFAULT NULL,
	"agency_description" varchar(50) DEFAULT NULL,
	"irs_status" varchar(50) DEFAULT NULL,
	"source_of_funds" varchar(50) DEFAULT NULL,
	"record_owner" varchar(50) DEFAULT NULL,
	"fein" varchar(50) DEFAULT NULL,
	"year_inc" varchar(50) DEFAULT NULL,
	"annual_budget_total" varchar(50) DEFAULT NULL,
	"legal_status" varchar(50) DEFAULT NULL,
	"exclude_from_website" varchar(50) DEFAULT NULL,
	"exclude_from_directory" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "agency_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "spatial_location_2010"
-- ----------------------------
DROP TABLE IF EXISTS "spatial_location_2010";
CREATE TABLE "spatial_location_2010" (
	"id" int4 NOT NULL DEFAULT nextval('spatial_location_2010_id_seq'::regclass),
	"site_index_id" int4 DEFAULT NULL,
	"description" varchar(50) DEFAULT NULL,
	"datum" varchar(50) DEFAULT NULL,
	"latitude" varchar(50) DEFAULT NULL,
	"longitude" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "spatial_location_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "other_address_2010"
-- ----------------------------
DROP TABLE IF EXISTS "other_address_2010";
CREATE TABLE "other_address_2010" (
	"id" int4 NOT NULL DEFAULT nextval('other_address_2010_id_seq'::regclass),
	"site_index_id" int4 DEFAULT NULL,
	"pre_address_line" varchar(50) DEFAULT NULL,
	"line_1" varchar(50) DEFAULT NULL,
	"line_2" varchar(50) DEFAULT NULL,
	"city" varchar(50) DEFAULT NULL,
	"county" varchar(50) DEFAULT NULL,
	"state" varchar(50) DEFAULT NULL,
	"zip_code" varchar(50) DEFAULT NULL,
	"country" varchar(50) DEFAULT NULL,
	"reason_withheld" varchar(50) DEFAULT NULL,
	"confidential" varchar(50) DEFAULT NULL,
	"description" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "other_address_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "residency_requirements_2010"
-- ----------------------------
DROP TABLE IF EXISTS "residency_requirements_2010";
CREATE TABLE "residency_requirements_2010" (
	"id" int4 NOT NULL DEFAULT nextval('residency_requirements_2010_id_seq'::regclass),
	"site_service_index_id" int4 DEFAULT NULL,
	"residency_requirements" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "residency_requirements_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "cross_street_2010"
-- ----------------------------
DROP TABLE IF EXISTS "cross_street_2010";
CREATE TABLE "cross_street_2010" (
	"id" int4 NOT NULL DEFAULT nextval('cross_street_2010_id_seq'::regclass),
	"site_index_id" int4 DEFAULT NULL,
	"cross_street" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "cross_street_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "pit_counts_2010"
-- ----------------------------
DROP TABLE IF EXISTS "pit_counts_2010";
CREATE TABLE "pit_counts_2010" (
	"id" int4 NOT NULL DEFAULT nextval('pit_counts_2010_id_seq'::regclass),
	"pit_count_set_index_id" int4 DEFAULT NULL,
	"pit_count_value" varchar(50) DEFAULT NULL,
	"pit_count_effective_period_start_date" timestamptz DEFAULT NULL,
	"pit_count_effective_period_end_date" timestamptz DEFAULT NULL,
	"pit_count_recorded_date" timestamptz DEFAULT NULL,
	"pit_count_household_type" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "pit_counts_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "other_requirements_2010"
-- ----------------------------
DROP TABLE IF EXISTS "other_requirements_2010";
CREATE TABLE "other_requirements_2010" (
	"id" int4 NOT NULL DEFAULT nextval('other_requirements_2010_id_seq'::regclass),
	"site_service_index_id" int4 DEFAULT NULL,
	"other_requirements" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "other_requirements_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "pit_count_set_2010"
-- ----------------------------
DROP TABLE IF EXISTS "pit_count_set_2010";
CREATE TABLE "pit_count_set_2010" (
	"id" int4 NOT NULL DEFAULT nextval('pit_count_set_2010_id_seq'::regclass),
	"site_service_index_id" int4 DEFAULT NULL,
	"pit_count_set_id_id_num" varchar(50) DEFAULT NULL,
	"pit_count_set_id_id_str" varchar(50) DEFAULT NULL,
	"pit_count_set_id_delete" int4 DEFAULT NULL,
	"pit_count_set_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"pit_count_set_id_delete_effective" timestamptz DEFAULT NULL,
	"hud_waiver_received" varchar(50) DEFAULT NULL,
	"hud_waiver_date" timestamptz DEFAULT NULL,
	"hud_waiver_effective_period_start_date" timestamptz DEFAULT NULL,
	"hud_waiver_effective_period_end_date" timestamptz DEFAULT NULL,
	"last_pit_sheltered_count_date" timestamptz DEFAULT NULL,
	"last_pit_unsheltered_count_date" timestamptz DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "pit_count_set_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "export"
-- ----------------------------
DROP TABLE IF EXISTS "export";
CREATE TABLE "export" (
	"export_id" varchar(50) NOT NULL DEFAULT NULL,
	"export_id_date_collected" timestamptz DEFAULT NULL,
	"export_date" timestamptz DEFAULT NULL,
	"export_date_date_collected" timestamptz DEFAULT NULL,
	"export_period_start_date" timestamptz DEFAULT NULL,
	"export_period_start_date_date_collected" timestamptz DEFAULT NULL,
	"export_period_end_date" timestamptz DEFAULT NULL,
	"export_period_end_date_date_collected" timestamptz DEFAULT NULL,
	"export_software_vendor" varchar(50) DEFAULT NULL,
	"export_software_vendor_date_collected" timestamptz DEFAULT NULL,
	"export_software_version" varchar(10) DEFAULT NULL,
	"export_software_version_date_collected" timestamptz DEFAULT NULL,
	"export_id_id_id_num_2010" varchar(50) DEFAULT NULL,
	"export_id_id_id_str_2010" varchar(50) DEFAULT NULL,
	"export_id_id_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"export_id_id_delete_effective_2010" timestamptz DEFAULT NULL,
	"export_id_id_delete_2010" int4 DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "export" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "languages_2010"
-- ----------------------------
DROP TABLE IF EXISTS "languages_2010";
CREATE TABLE "languages_2010" (
	"id" int4 NOT NULL DEFAULT nextval('languages_2010_id_seq'::regclass),
	"site_index_id" int4 DEFAULT NULL,
	"site_service_index_id" int4 DEFAULT NULL,
	"name" varchar(50) DEFAULT NULL,
	"notes" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "languages_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "site_2010"
-- ----------------------------
DROP TABLE IF EXISTS "site_2010";
CREATE TABLE "site_2010" (
	"id" int4 NOT NULL DEFAULT nextval('site_2010_id_seq'::regclass),
	"export_index_id" varchar(50) DEFAULT NULL,
	"agency_index_id" int4 DEFAULT NULL,
	"attr_delete" int4 DEFAULT NULL,
	"attr_delete_occurred_date" timestamptz DEFAULT NULL,
	"attr_effective" timestamptz DEFAULT NULL,
	"airs_key" varchar(50) DEFAULT NULL,
	"airs_name" varchar(50) DEFAULT NULL,
	"site_description" varchar(50) DEFAULT NULL,
	"physical_address_pre_address_line" varchar(50) DEFAULT NULL,
	"physical_address_line_1" varchar(50) DEFAULT NULL,
	"physical_address_line_2" varchar(50) DEFAULT NULL,
	"physical_address_city" varchar(50) DEFAULT NULL,
	"physical_address_country" varchar(50) DEFAULT NULL,
	"physical_address_state" varchar(50) DEFAULT NULL,
	"physical_address_zip_code" varchar(50) DEFAULT NULL,
	"physical_address_reason_withheld" varchar(50) DEFAULT NULL,
	"physical_address_confidential" varchar(50) DEFAULT NULL,
	"physical_address_description" varchar(50) DEFAULT NULL,
	"mailing_address_pre_address_line" varchar(50) DEFAULT NULL,
	"mailing_address_line_1" varchar(50) DEFAULT NULL,
	"mailing_address_line_2" varchar(50) DEFAULT NULL,
	"mailing_address_city" varchar(50) DEFAULT NULL,
	"mailing_address_country" varchar(50) DEFAULT NULL,
	"mailing_address_state" varchar(50) DEFAULT NULL,
	"mailing_address_zip_code" varchar(50) DEFAULT NULL,
	"mailing_address_reason_withheld" varchar(50) DEFAULT NULL,
	"mailing_address_confidential" varchar(50) DEFAULT NULL,
	"mailing_address_description" varchar(50) DEFAULT NULL,
	"no_physical_address_description" varchar(50) DEFAULT NULL,
	"no_physical_address_explanation" varchar(50) DEFAULT NULL,
	"disabilities_access" varchar(50) DEFAULT NULL,
	"physical_location_description" varchar(50) DEFAULT NULL,
	"bus_service_access" varchar(50) DEFAULT NULL,
	"public_access_to_transportation" varchar(50) DEFAULT NULL,
	"year_inc" varchar(50) DEFAULT NULL,
	"annual_budget_total" varchar(50) DEFAULT NULL,
	"legal_status" varchar(50) DEFAULT NULL,
	"exclude_from_website" varchar(50) DEFAULT NULL,
	"exclude_from_directory" varchar(50) DEFAULT NULL,
	"agency_key" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "site_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "time_open_2010"
-- ----------------------------
DROP TABLE IF EXISTS "time_open_2010";
CREATE TABLE "time_open_2010" (
	"id" int4 NOT NULL DEFAULT nextval('time_open_2010_id_seq'::regclass),
	"site_index_id" int4 DEFAULT NULL,
	"languages_index_id" int4 DEFAULT NULL,
	"site_service_index_id" int4 DEFAULT NULL,
	"notes" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "time_open_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "hmis_asset_2010"
-- ----------------------------
DROP TABLE IF EXISTS "hmis_asset_2010";
CREATE TABLE "hmis_asset_2010" (
	"id" int4 NOT NULL DEFAULT nextval('hmis_asset_2010_id_seq'::regclass),
	"site_index_id" int4 DEFAULT NULL,
	"asset_id_id_num" varchar(50) DEFAULT NULL,
	"asset_id_id_str" varchar(50) DEFAULT NULL,
	"asset_id_delete" int4 DEFAULT NULL,
	"asset_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"asset_id_delete_effective" timestamptz DEFAULT NULL,
	"asset_count" varchar(50) DEFAULT NULL,
	"asset_count_bed_availability" varchar(50) DEFAULT NULL,
	"asset_count_bed_type" varchar(50) DEFAULT NULL,
	"asset_count_bed_individual_family_type" varchar(50) DEFAULT NULL,
	"asset_count_chronic_homeless_bed" varchar(50) DEFAULT NULL,
	"asset_count_domestic_violence_shelter_bed" varchar(50) DEFAULT NULL,
	"asset_count_household_type" varchar(50) DEFAULT NULL,
	"asset_type" varchar(50) DEFAULT NULL,
	"asset_effective_period_start_date" timestamptz DEFAULT NULL,
	"asset_effective_period_end_date" timestamptz DEFAULT NULL,
	"asset_recorded_date" timestamptz DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "hmis_asset_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "time_open_days_2010"
-- ----------------------------
DROP TABLE IF EXISTS "time_open_days_2010";
CREATE TABLE "time_open_days_2010" (
	"id" int4 NOT NULL DEFAULT nextval('time_open_days_2010_id_seq'::regclass),
	"time_open_index_id" int4 DEFAULT NULL,
	"day_of_week" varchar(50) DEFAULT NULL,
	"from" varchar(50) DEFAULT NULL,
	"to" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "time_open_days_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "documents_required_2010"
-- ----------------------------
DROP TABLE IF EXISTS "documents_required_2010";
CREATE TABLE "documents_required_2010" (
	"id" int4 NOT NULL DEFAULT nextval('documents_required_2010_id_seq'::regclass),
	"site_service_index_id" int4 DEFAULT NULL,
	"documents_required" varchar(50) DEFAULT NULL,
	"description" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "documents_required_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "assignment_period_2010"
-- ----------------------------
DROP TABLE IF EXISTS "assignment_period_2010";
CREATE TABLE "assignment_period_2010" (
	"id" int4 NOT NULL DEFAULT nextval('assignment_period_2010_id_seq'::regclass),
	"assignment_index_id" int4 DEFAULT NULL,
	"assignment_period_start_date" timestamptz DEFAULT NULL,
	"assignment_period_end_date" timestamptz DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "assignment_period_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "inventory_2010"
-- ----------------------------
DROP TABLE IF EXISTS "inventory_2010";
CREATE TABLE "inventory_2010" (
	"id" int4 NOT NULL DEFAULT nextval('inventory_2010_id_seq'::regclass),
	"service_index_id" int4 DEFAULT NULL,
	"site_service_index_id" int4 DEFAULT NULL,
	"attr_delete" int4 DEFAULT NULL,
	"attr_delete_occurred_date" timestamptz DEFAULT NULL,
	"attr_effective" timestamptz DEFAULT NULL,
	"hmis_participation_period_start_date" timestamptz DEFAULT NULL,
	"hmis_participation_period_end_date" timestamptz DEFAULT NULL,
	"inventory_id_id_num" varchar(50) DEFAULT NULL,
	"inventory_id_id_str" varchar(50) DEFAULT NULL,
	"bed_inventory" varchar(50) DEFAULT NULL,
	"bed_availability" varchar(50) DEFAULT NULL,
	"bed_type" varchar(50) DEFAULT NULL,
	"bed_individual_family_type" varchar(50) DEFAULT NULL,
	"chronic_homeless_bed" varchar(50) DEFAULT NULL,
	"domestic_violence_shelter_bed" varchar(50) DEFAULT NULL,
	"household_type" varchar(50) DEFAULT NULL,
	"hmis_participating_beds" varchar(50) DEFAULT NULL,
	"inventory_effective_period_start_date" timestamptz DEFAULT NULL,
	"inventory_effective_period_end_date" timestamptz DEFAULT NULL,
	"inventory_recorded_date" timestamptz DEFAULT NULL,
	"unit_inventory" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "inventory_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "assignment_2010"
-- ----------------------------
DROP TABLE IF EXISTS "assignment_2010";
CREATE TABLE "assignment_2010" (
	"id" int4 NOT NULL DEFAULT nextval('assignment_2010_id_seq'::regclass),
	"hmis_asset_index_id" int4 DEFAULT NULL,
	"assignment_id_id_num" varchar(50) DEFAULT NULL,
	"assignment_id_id_str" varchar(50) DEFAULT NULL,
	"assignment_id_delete" int4 DEFAULT NULL,
	"assignment_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"assignment_id_delete_effective" timestamptz DEFAULT NULL,
	"person_id_id_num" varchar(50) DEFAULT NULL,
	"person_id_id_str" varchar(50) DEFAULT NULL,
	"household_id_id_num" varchar(50) DEFAULT NULL,
	"household_id_id_str" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "assignment_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "income_requirements_2010"
-- ----------------------------
DROP TABLE IF EXISTS "income_requirements_2010";
CREATE TABLE "income_requirements_2010" (
	"id" int4 NOT NULL DEFAULT nextval('income_requirements_2010_id_seq'::regclass),
	"site_service_index_id" int4 DEFAULT NULL,
	"income_requirements" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "income_requirements_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "age_requirements"
-- ----------------------------
DROP TABLE IF EXISTS "age_requirements";
CREATE TABLE "age_requirements" (
	"id" int4 NOT NULL DEFAULT nextval('age_requirements_id_seq'::regclass),
	"site_service_index_id" int4 DEFAULT NULL,
	"gender" varchar(50) DEFAULT NULL,
	"minimum_age" varchar(50) DEFAULT NULL,
	"maximum_age" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "age_requirements" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "geographic_area_served_2010"
-- ----------------------------
DROP TABLE IF EXISTS "geographic_area_served_2010";
CREATE TABLE "geographic_area_served_2010" (
	"id" int4 NOT NULL DEFAULT nextval('geographic_area_served_2010_id_seq'::regclass),
	"site_service_index_id" int4 DEFAULT NULL,
	"zipcode" varchar(50) DEFAULT NULL,
	"census_track" varchar(50) DEFAULT NULL,
	"city" varchar(50) DEFAULT NULL,
	"county" varchar(50) DEFAULT NULL,
	"state" varchar(50) DEFAULT NULL,
	"country" varchar(50) DEFAULT NULL,
	"description" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "geographic_area_served_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "aid_requirements"
-- ----------------------------
DROP TABLE IF EXISTS "aid_requirements";
CREATE TABLE "aid_requirements" (
	"id" int4 NOT NULL DEFAULT nextval('aid_requirements_id_seq'::regclass),
	"site_service_index_id" int4 DEFAULT NULL,
	"aid_requirements" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "aid_requirements" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "reasons_for_leaving_2010"
-- ----------------------------
DROP TABLE IF EXISTS "reasons_for_leaving_2010";
CREATE TABLE "reasons_for_leaving_2010" (
	"id" int4 NOT NULL DEFAULT nextval('reasons_for_leaving_2010_id_seq'::regclass),
	"site_service_participation_index_id" int4 DEFAULT NULL,
	"reason_for_leaving_id_id_num" varchar(50) DEFAULT NULL,
	"reason_for_leaving_id_id_str" varchar(50) DEFAULT NULL,
	"reason_for_leaving_id_delete" int4 DEFAULT NULL,
	"reason_for_leaving_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"reason_for_leaving_id_delete_effective" timestamptz DEFAULT NULL,
	"reason_for_leaving" varchar(50) DEFAULT NULL,
	"reason_for_leaving_date_collected" timestamptz DEFAULT NULL,
	"reason_for_leaving_date_effective" timestamptz DEFAULT NULL,
	"reason_for_leaving_data_collection_stage" varchar(50) DEFAULT NULL,
	"reason_for_leaving_other" varchar(50) DEFAULT NULL,
	"reason_for_leaving_other_date_collected" timestamptz DEFAULT NULL,
	"reason_for_leaving_other_date_effective" timestamptz DEFAULT NULL,
	"reason_for_leaving_other_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "reasons_for_leaving_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "site_service_participation"
-- ----------------------------
DROP TABLE IF EXISTS "site_service_participation";
CREATE TABLE "site_service_participation" (
	"id" int4 NOT NULL DEFAULT nextval('site_service_participation_id_seq'::regclass),
	"person_index_id" int4 DEFAULT NULL,
	"site_service_participation_idid_num" varchar(32) DEFAULT NULL,
	"site_service_participation_idid_num_date_collected" timestamptz DEFAULT NULL,
	"site_service_participation_idid_str" varchar(32) DEFAULT NULL,
	"site_service_participation_idid_str_date_collected" timestamptz DEFAULT NULL,
	"site_service_idid_num" varchar(32) DEFAULT NULL,
	"site_service_idid_num_date_collected" timestamptz DEFAULT NULL,
	"site_service_idid_str" varchar(32) DEFAULT NULL,
	"site_service_idid_str_date_collected" timestamptz DEFAULT NULL,
	"household_idid_num" varchar(32) DEFAULT NULL,
	"household_idid_num_date_collected" timestamptz DEFAULT NULL,
	"household_idid_str" varchar(32) DEFAULT NULL,
	"household_idid_str_date_collected" timestamptz DEFAULT NULL,
	"destination" varchar(32) DEFAULT NULL,
	"destination_date_collected" timestamptz DEFAULT NULL,
	"destination_other" varchar(32) DEFAULT NULL,
	"destination_other_date_collected" timestamptz DEFAULT NULL,
	"destination_tenure" varchar(32) DEFAULT NULL,
	"destination_tenure_date_collected" timestamptz DEFAULT NULL,
	"disabling_condition" varchar(32) DEFAULT NULL,
	"disabling_condition_date_collected" timestamptz DEFAULT NULL,
	"participation_dates_start_date" timestamptz DEFAULT NULL,
	"participation_dates_start_date_date_collected" timestamptz DEFAULT NULL,
	"participation_dates_end_date" timestamptz DEFAULT NULL,
	"participation_dates_end_date_date_collected" timestamptz DEFAULT NULL,
	"veteran_status" varchar(32) DEFAULT NULL,
	"veteran_status_date_collected" timestamptz DEFAULT NULL,
	"reported" bool DEFAULT NULL,
	"site_service_participation_id_delete_2010" int4 DEFAULT NULL,
	"site_service_participation_id_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"site_service_participation_id_delete_effective_2010" timestamptz DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "site_service_participation" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "application_process_2010"
-- ----------------------------
DROP TABLE IF EXISTS "application_process_2010";
CREATE TABLE "application_process_2010" (
	"id" int4 NOT NULL DEFAULT nextval('application_process_2010_id_seq'::regclass),
	"site_service_index_id" int4 DEFAULT NULL,
	"step" varchar(50) DEFAULT NULL,
	"description" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "application_process_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "family_requirements_2010"
-- ----------------------------
DROP TABLE IF EXISTS "family_requirements_2010";
CREATE TABLE "family_requirements_2010" (
	"id" int4 NOT NULL DEFAULT nextval('family_requirements_2010_id_seq'::regclass),
	"site_service_index_id" int4 DEFAULT NULL,
	"family_requirements" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "family_requirements_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "site_service_2010"
-- ----------------------------
DROP TABLE IF EXISTS "site_service_2010";
CREATE TABLE "site_service_2010" (
	"id" int4 NOT NULL DEFAULT nextval('site_service_2010_id_seq'::regclass),
	"export_index_id" varchar(50) DEFAULT NULL,
	"site_index_id" int4 DEFAULT NULL,
	"attr_delete" int4 DEFAULT NULL,
	"attr_delete_occurred_date" timestamptz DEFAULT NULL,
	"attr_effective" timestamptz DEFAULT NULL,
	"name" varchar(50) DEFAULT NULL,
	"key" varchar(50) DEFAULT NULL,
	"description" varchar(50) DEFAULT NULL,
	"fee_structure" varchar(50) DEFAULT NULL,
	"gender_requirements" varchar(50) DEFAULT NULL,
	"area_flexibility" varchar(50) DEFAULT NULL,
	"service_not_always_available" varchar(50) DEFAULT NULL,
	"service_group_key" varchar(50) DEFAULT NULL,
	"service_id" varchar(50) DEFAULT NULL,
	"site_id" varchar(50) DEFAULT NULL,
	"geographic_code" varchar(50) DEFAULT NULL,
	"geographic_code_date_collected" timestamptz DEFAULT NULL,
	"geographic_code_date_effective" timestamptz DEFAULT NULL,
	"geographic_code_data_collection_stage" varchar(50) DEFAULT NULL,
	"housing_type" varchar(50) DEFAULT NULL,
	"housing_type_date_collected" timestamptz DEFAULT NULL,
	"housing_type_date_effective" timestamptz DEFAULT NULL,
	"housing_type_data_collection_stage" varchar(50) DEFAULT NULL,
	"principal" varchar(50) DEFAULT NULL,
	"site_service_effective_period_start_date" timestamptz DEFAULT NULL,
	"site_service_effective_period_end_date" timestamptz DEFAULT NULL,
	"site_service_recorded_date" timestamptz DEFAULT NULL,
	"site_service_type" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "site_service_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "veteran_military_branches_2010"
-- ----------------------------
DROP TABLE IF EXISTS "veteran_military_branches_2010";
CREATE TABLE "veteran_military_branches_2010" (
	"id" int4 NOT NULL DEFAULT nextval('veteran_military_branches_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"military_branch_id_id_id_num" varchar(50) DEFAULT NULL,
	"military_branch_id_id_id_str" varchar(50) DEFAULT NULL,
	"military_branch_id_id_delete" int4 DEFAULT NULL,
	"military_branch_id_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"military_branch_id_id_delete_effective" timestamptz DEFAULT NULL,
	"discharge_status" varchar(50) DEFAULT NULL,
	"discharge_status_date_collected" timestamptz DEFAULT NULL,
	"discharge_status_date_effective" timestamptz DEFAULT NULL,
	"discharge_status_data_collection_stage" varchar(50) DEFAULT NULL,
	"discharge_status_other" varchar(50) DEFAULT NULL,
	"discharge_status_other_date_collected" timestamptz DEFAULT NULL,
	"discharge_status_other_date_effective" timestamptz DEFAULT NULL,
	"discharge_status_other_data_collection_stage" varchar(50) DEFAULT NULL,
	"military_branch" varchar(50) DEFAULT NULL,
	"military_branch_date_collected" timestamptz DEFAULT NULL,
	"military_branch_date_effective" timestamptz DEFAULT NULL,
	"military_branch_data_collection_stage" varchar(50) DEFAULT NULL,
	"military_branch_other" varchar(50) DEFAULT NULL,
	"military_branch_other_date_collected" timestamptz DEFAULT NULL,
	"military_branch_other_date_effective" timestamptz DEFAULT NULL,
	"military_branch_other_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "veteran_military_branches_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "veteran_service_era_2010"
-- ----------------------------
DROP TABLE IF EXISTS "veteran_service_era_2010";
CREATE TABLE "veteran_service_era_2010" (
	"id" int4 NOT NULL DEFAULT nextval('veteran_service_era_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"service_era" varchar(50) DEFAULT NULL,
	"service_era_date_collected" timestamptz DEFAULT NULL,
	"service_era_date_effective" timestamptz DEFAULT NULL,
	"service_era_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "veteran_service_era_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "taxonomy_2010"
-- ----------------------------
DROP TABLE IF EXISTS "taxonomy_2010";
CREATE TABLE "taxonomy_2010" (
	"id" int4 NOT NULL DEFAULT nextval('taxonomy_2010_id_seq'::regclass),
	"site_service_index_id" int4 DEFAULT NULL,
	"need_index_id" int4 DEFAULT NULL,
	"code" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "taxonomy_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "veteran_served_in_war_zone_2010"
-- ----------------------------
DROP TABLE IF EXISTS "veteran_served_in_war_zone_2010";
CREATE TABLE "veteran_served_in_war_zone_2010" (
	"id" int4 NOT NULL DEFAULT nextval('veteran_served_in_war_zone_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"served_in_war_zone" varchar(50) DEFAULT NULL,
	"served_in_war_zone_date_collected" timestamptz DEFAULT NULL,
	"served_in_war_zone_date_effective" timestamptz DEFAULT NULL,
	"served_in_war_zone_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "veteran_served_in_war_zone_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "housing_status_2010"
-- ----------------------------
DROP TABLE IF EXISTS "housing_status_2010";
CREATE TABLE "housing_status_2010" (
	"id" int4 NOT NULL DEFAULT nextval('housing_status_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"housing_status" varchar(50) DEFAULT NULL,
	"housing_status_date_collected" timestamptz DEFAULT NULL,
	"housing_status_date_effective" timestamptz DEFAULT NULL,
	"housing_status_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "housing_status_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "veteran_military_service_duration_2010"
-- ----------------------------
DROP TABLE IF EXISTS "veteran_military_service_duration_2010";
CREATE TABLE "veteran_military_service_duration_2010" (
	"id" int4 NOT NULL DEFAULT nextval('veteran_military_service_duration_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"military_service_duration" varchar(50) DEFAULT NULL,
	"military_service_duration_date_collected" timestamptz DEFAULT NULL,
	"military_service_duration_date_effective" timestamptz DEFAULT NULL,
	"military_service_duration_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "veteran_military_service_duration_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "need"
-- ----------------------------
DROP TABLE IF EXISTS "need";
CREATE TABLE "need" (
	"id" int4 NOT NULL DEFAULT nextval('need_id_seq'::regclass),
	"site_service_index_id" int4 DEFAULT NULL,
	"need_idid_num" varchar(32) DEFAULT NULL,
	"need_idid_num_date_collected" timestamptz DEFAULT NULL,
	"need_idid_str" varchar(32) DEFAULT NULL,
	"need_idid_str_date_collected" timestamptz DEFAULT NULL,
	"site_service_idid_num" varchar(32) DEFAULT NULL,
	"site_service_idid_num_date_collected" timestamptz DEFAULT NULL,
	"site_service_idid_str" varchar(32) DEFAULT NULL,
	"site_service_idid_str_date_collected" timestamptz DEFAULT NULL,
	"service_event_idid_num" varchar(32) DEFAULT NULL,
	"service_event_idid_num_date_collected" timestamptz DEFAULT NULL,
	"service_event_idid_str" varchar(32) DEFAULT NULL,
	"service_event_idid_str_date_collected" timestamptz DEFAULT NULL,
	"need_status" varchar(32) DEFAULT NULL,
	"need_status_date_collected" timestamptz DEFAULT NULL,
	"taxonomy" varchar(32) DEFAULT NULL,
	"reported" bool DEFAULT NULL,
	"person_index_id_2010" int4 DEFAULT NULL,
	"need_id_delete_2010" int4 DEFAULT NULL,
	"need_id_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"need_id_delete_delete_effective_2010" timestamptz DEFAULT NULL,
	"need_effective_period_start_date_2010" timestamptz DEFAULT NULL,
	"need_effective_period_end_date_2010" timestamptz DEFAULT NULL,
	"need_recorded_date_2010" timestamptz DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "need" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "service_event_notes_2010"
-- ----------------------------
DROP TABLE IF EXISTS "service_event_notes_2010";
CREATE TABLE "service_event_notes_2010" (
	"id" int4 NOT NULL DEFAULT nextval('service_event_notes_2010_id_seq'::regclass),
	"service_event_index_id" int4 DEFAULT NULL,
	"note_id_id_num" varchar(50) DEFAULT NULL,
	"note_id_id_str" varchar(50) DEFAULT NULL,
	"note_delete" int4 DEFAULT NULL,
	"note_delete_occurred_date" timestamptz DEFAULT NULL,
	"note_delete_effective" timestamptz DEFAULT NULL,
	"note_text" varchar(50) DEFAULT NULL,
	"note_text_date_collected" timestamptz DEFAULT NULL,
	"note_text_date_effective" timestamptz DEFAULT NULL,
	"note_text_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "service_event_notes_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "veteran_veteran_status_2010"
-- ----------------------------
DROP TABLE IF EXISTS "veteran_veteran_status_2010";
CREATE TABLE "veteran_veteran_status_2010" (
	"id" int4 NOT NULL DEFAULT nextval('veteran_veteran_status_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"veteran_status" varchar(50) DEFAULT NULL,
	"veteran_status_date_collected" timestamptz DEFAULT NULL,
	"veteran_status_date_effective" timestamptz DEFAULT NULL,
	"veteran_status_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "veteran_veteran_status_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "service_event"
-- ----------------------------
DROP TABLE IF EXISTS "service_event";
CREATE TABLE "service_event" (
	"id" int4 NOT NULL DEFAULT nextval('service_event_id_seq'::regclass),
	"site_service_index_id" int4 DEFAULT NULL,
	"service_event_idid_num" varchar(32) DEFAULT NULL,
	"service_event_idid_num_date_collected" timestamptz DEFAULT NULL,
	"service_event_idid_str" varchar(32) DEFAULT NULL,
	"service_event_idid_str_date_collected" timestamptz DEFAULT NULL,
	"household_idid_num" varchar(32) DEFAULT NULL,
	"household_idid_num_date_collected" timestamptz DEFAULT NULL,
	"household_idid_str" varchar(32) DEFAULT NULL,
	"household_idid_str_date_collected" timestamptz DEFAULT NULL,
	"is_referral" varchar(32) DEFAULT NULL,
	"is_referral_date_collected" timestamptz DEFAULT NULL,
	"quantity_of_service" varchar(32) DEFAULT NULL,
	"quantity_of_service_date_collected" timestamptz DEFAULT NULL,
	"quantity_of_service_measure" varchar(32) DEFAULT NULL,
	"quantity_of_service_measure_date_collected" timestamptz DEFAULT NULL,
	"service_airs_code" varchar(32) DEFAULT NULL,
	"service_airs_code_date_collected" timestamptz DEFAULT NULL,
	"service_period_start_date" timestamptz DEFAULT NULL,
	"service_period_start_date_date_collected" timestamptz DEFAULT NULL,
	"service_period_end_date" timestamptz DEFAULT NULL,
	"service_period_end_date_date_collected" timestamptz DEFAULT NULL,
	"service_unit" varchar(32) DEFAULT NULL,
	"service_unit_date_collected" timestamptz DEFAULT NULL,
	"type_of_service" varchar(32) DEFAULT NULL,
	"type_of_service_date_collected" timestamptz DEFAULT NULL,
	"type_of_service_other" varchar(32) DEFAULT NULL,
	"type_of_service_other_date_collected" timestamptz DEFAULT NULL,
	"type_of_service_par" int4 DEFAULT NULL,
	"reported" bool DEFAULT NULL,
	"person_index_id_2010" int4 DEFAULT NULL,
	"need_index_id_2010" int4 DEFAULT NULL,
	"service_event_id_delete_2010" int4 DEFAULT NULL,
	"service_event_ind_fam_2010" int4 DEFAULT NULL,
	"site_service_id_2010" varchar(50) DEFAULT NULL,
	"hmis_service_event_code_type_of_service_2010" varchar(50) DEFAULT NULL,
	"hmis_service_event_code_type_of_service_other_2010" varchar(50) DEFAULT NULL,
	"hprp_financial_assistance_service_event_code_2010" varchar(50) DEFAULT NULL,
	"hprp_relocation_stabilization_service_event_code_2010" varchar(50) DEFAULT NULL,
	"service_event_id_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"service_event_id_delete_effective_2010" timestamptz DEFAULT NULL,
	"service_event_provision_date_2010" timestamptz DEFAULT NULL,
	"service_event_recorded_date_2010" timestamptz DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "service_event" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "veteran_warzones_served_2010"
-- ----------------------------
DROP TABLE IF EXISTS "veteran_warzones_served_2010";
CREATE TABLE "veteran_warzones_served_2010" (
	"id" int4 NOT NULL DEFAULT nextval('veteran_warzones_served_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"war_zone_id_id_id_num" varchar(50) DEFAULT NULL,
	"war_zone_id_id_id_str" varchar(50) DEFAULT NULL,
	"war_zone_id_id_delete" int4 DEFAULT NULL,
	"war_zone_id_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"war_zone_id_id_delete_effective" timestamptz DEFAULT NULL,
	"months_in_war_zone" varchar(50) DEFAULT NULL,
	"months_in_war_zone_date_collected" timestamptz DEFAULT NULL,
	"months_in_war_zone_date_effective" timestamptz DEFAULT NULL,
	"months_in_war_zone_data_collection_stage" varchar(50) DEFAULT NULL,
	"received_fire" varchar(50) DEFAULT NULL,
	"received_fire_date_collected" timestamptz DEFAULT NULL,
	"received_fire_date_effective" timestamptz DEFAULT NULL,
	"received_fire_data_collection_stage" varchar(50) DEFAULT NULL,
	"war_zone" varchar(50) DEFAULT NULL,
	"war_zone_date_collected" timestamptz DEFAULT NULL,
	"war_zone_date_effective" timestamptz DEFAULT NULL,
	"war_zone_data_collection_stage" varchar(50) DEFAULT NULL,
	"war_zone_other" varchar(50) DEFAULT NULL,
	"war_zone_other_date_collected" timestamptz DEFAULT NULL,
	"war_zone_other_date_effective" timestamptz DEFAULT NULL,
	"war_zone_other_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "veteran_warzones_served_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "vocational_training_2010"
-- ----------------------------
DROP TABLE IF EXISTS "vocational_training_2010";
CREATE TABLE "vocational_training_2010" (
	"id" int4 NOT NULL DEFAULT nextval('vocational_training_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"vocational_training" varchar(50) DEFAULT NULL,
	"vocational_training_date_collected" timestamptz DEFAULT NULL,
	"vocational_training_date_effective" timestamptz DEFAULT NULL,
	"vocational_training_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "vocational_training_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "substance_abuse_problem_2010"
-- ----------------------------
DROP TABLE IF EXISTS "substance_abuse_problem_2010";
CREATE TABLE "substance_abuse_problem_2010" (
	"id" int4 NOT NULL DEFAULT nextval('substance_abuse_problem_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"has_substance_abuse_problem" varchar(50) DEFAULT NULL,
	"has_substance_abuse_problem_date_collected" timestamptz DEFAULT NULL,
	"has_substance_abuse_problem_date_effective" timestamptz DEFAULT NULL,
	"has_substance_abuse_problem_data_collection_stage" varchar(50) DEFAULT NULL,
	"substance_abuse_indefinite" varchar(50) DEFAULT NULL,
	"substance_abuse_indefinite_date_collected" timestamptz DEFAULT NULL,
	"substance_abuse_indefinite_date_effective" timestamptz DEFAULT NULL,
	"substance_abuse_indefinite_data_collection_stage" varchar(50) DEFAULT NULL,
	"receive_substance_abuse_services" varchar(50) DEFAULT NULL,
	"receive_substance_abuse_services_date_collected" timestamptz DEFAULT NULL,
	"receive_substance_abuse_services_date_effective" timestamptz DEFAULT NULL,
	"receive_substance_abuse_services_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "substance_abuse_problem_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "non_cash_benefits_last_30_days_2010"
-- ----------------------------
DROP TABLE IF EXISTS "non_cash_benefits_last_30_days_2010";
CREATE TABLE "non_cash_benefits_last_30_days_2010" (
	"id" int4 NOT NULL DEFAULT nextval('non_cash_benefits_last_30_days_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"income_last_30_days" varchar(50) DEFAULT NULL,
	"income_last_30_days_date_collected" timestamptz DEFAULT NULL,
	"income_last_30_days_date_effective" timestamptz DEFAULT NULL,
	"income_last_30_days_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "non_cash_benefits_last_30_days_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "pregnancy_2010"
-- ----------------------------
DROP TABLE IF EXISTS "pregnancy_2010";
CREATE TABLE "pregnancy_2010" (
	"id" int4 NOT NULL DEFAULT nextval('pregnancy_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"pregnancy_id_id_id_num" varchar(50) DEFAULT NULL,
	"pregnancy_id_id_id_str" varchar(50) DEFAULT NULL,
	"pregnancy_id_id_delete" int4 DEFAULT NULL,
	"pregnancy_id_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"pregnancy_id_id_delete_effective" timestamptz DEFAULT NULL,
	"pregnancy_status" varchar(50) DEFAULT NULL,
	"pregnancy_status_date_collected" timestamptz DEFAULT NULL,
	"pregnancy_status_date_effective" timestamptz DEFAULT NULL,
	"pregnancy_status_data_collection_stage" varchar(50) DEFAULT NULL,
	"due_date" timestamptz DEFAULT NULL,
	"due_date_date_collected" timestamptz DEFAULT NULL,
	"due_date_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "pregnancy_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "prior_residence_2010"
-- ----------------------------
DROP TABLE IF EXISTS "prior_residence_2010";
CREATE TABLE "prior_residence_2010" (
	"id" int4 NOT NULL DEFAULT nextval('prior_residence_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"prior_residence_id_id_id_num" varchar(50) DEFAULT NULL,
	"prior_residence_id_id_id_str" varchar(50) DEFAULT NULL,
	"prior_residence_id_id_delete" int4 DEFAULT NULL,
	"prior_residence_id_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"prior_residence_id_id_delete_effective" timestamptz DEFAULT NULL,
	"prior_residence_code" varchar(50) DEFAULT NULL,
	"prior_residence_code_date_collected" timestamptz DEFAULT NULL,
	"prior_residence_code_date_effective" timestamptz DEFAULT NULL,
	"prior_residence_code_data_collection_stage" varchar(50) DEFAULT NULL,
	"prior_residence_other" varchar(50) DEFAULT NULL,
	"prior_residence_other_date_collected" timestamptz DEFAULT NULL,
	"prior_residence_other_date_effective" timestamptz DEFAULT NULL,
	"prior_residence_other_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "prior_residence_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "income_total_monthly_2010"
-- ----------------------------
DROP TABLE IF EXISTS "income_total_monthly_2010";
CREATE TABLE "income_total_monthly_2010" (
	"id" int4 NOT NULL DEFAULT nextval('income_total_monthly_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"income_total_monthly" varchar(50) DEFAULT NULL,
	"income_total_monthly_date_collected" timestamptz DEFAULT NULL,
	"income_total_monthly_date_effective" timestamptz DEFAULT NULL,
	"income_total_monthly_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "income_total_monthly_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "mental_health_problem_2010"
-- ----------------------------
DROP TABLE IF EXISTS "mental_health_problem_2010";
CREATE TABLE "mental_health_problem_2010" (
	"id" int4 NOT NULL DEFAULT nextval('mental_health_problem_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"has_mental_health_problem" varchar(50) DEFAULT NULL,
	"has_mental_health_problem_date_collected" timestamptz DEFAULT NULL,
	"has_mental_health_problem_date_effective" timestamptz DEFAULT NULL,
	"has_mental_health_problem_data_collection_stage" varchar(50) DEFAULT NULL,
	"mental_health_indefinite" varchar(50) DEFAULT NULL,
	"mental_health_indefinite_date_collected" timestamptz DEFAULT NULL,
	"mental_health_indefinite_date_effective" timestamptz DEFAULT NULL,
	"mental_health_indefinite_data_collection_stage" varchar(50) DEFAULT NULL,
	"receive_mental_health_services" varchar(50) DEFAULT NULL,
	"receive_mental_health_services_date_collected" timestamptz DEFAULT NULL,
	"receive_mental_health_services_date_effective" timestamptz DEFAULT NULL,
	"receive_mental_health_services_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "mental_health_problem_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "physical_disability_2010"
-- ----------------------------
DROP TABLE IF EXISTS "physical_disability_2010";
CREATE TABLE "physical_disability_2010" (
	"id" int4 NOT NULL DEFAULT nextval('physical_disability_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"has_physical_disability" varchar(50) DEFAULT NULL,
	"has_physical_disability_date_collected" timestamptz DEFAULT NULL,
	"has_physical_disability_date_effective" timestamptz DEFAULT NULL,
	"has_physical_disability_data_collection_stage" varchar(50) DEFAULT NULL,
	"receive_physical_disability_services" varchar(50) DEFAULT NULL,
	"receive_physical_disability_services_date_collected" timestamptz DEFAULT NULL,
	"receive_physical_disability_services_date_effective" timestamptz DEFAULT NULL,
	"receive_physical_disability_services_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "physical_disability_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "income_last_30_days_2010"
-- ----------------------------
DROP TABLE IF EXISTS "income_last_30_days_2010";
CREATE TABLE "income_last_30_days_2010" (
	"id" int4 NOT NULL DEFAULT nextval('income_last_30_days_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"income_last_30_days" varchar(50) DEFAULT NULL,
	"income_last_30_days_date_collected" timestamptz DEFAULT NULL,
	"income_last_30_days_date_effective" timestamptz DEFAULT NULL,
	"income_last_30_days_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "income_last_30_days_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "non_cash_benefits_2010"
-- ----------------------------
DROP TABLE IF EXISTS "non_cash_benefits_2010";
CREATE TABLE "non_cash_benefits_2010" (
	"id" int4 NOT NULL DEFAULT nextval('non_cash_benefits_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"non_cash_benefit_id_id_id_num" varchar(50) DEFAULT NULL,
	"non_cash_benefit_id_id_id_str" varchar(50) DEFAULT NULL,
	"non_cash_benefit_id_id_delete" int4 DEFAULT NULL,
	"non_cash_benefit_id_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"non_cash_benefit_id_id_delete_effective" timestamptz DEFAULT NULL,
	"non_cash_source_code" varchar(50) DEFAULT NULL,
	"non_cash_source_code_date_collected" timestamptz DEFAULT NULL,
	"non_cash_source_code_date_effective" timestamptz DEFAULT NULL,
	"non_cash_source_code_data_collection_stage" varchar(50) DEFAULT NULL,
	"non_cash_source_other" varchar(50) DEFAULT NULL,
	"non_cash_source_other_date_collected" timestamptz DEFAULT NULL,
	"non_cash_source_other_date_effective" timestamptz DEFAULT NULL,
	"non_cash_source_other_data_collection_stage" varchar(50) DEFAULT NULL,
	"receiving_non_cash_source" varchar(50) DEFAULT NULL,
	"receiving_non_cash_source_date_collected" timestamptz DEFAULT NULL,
	"receiving_non_cash_source_date_effective" timestamptz DEFAULT NULL,
	"receiving_non_cash_source_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "non_cash_benefits_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "highest_school_level_2010"
-- ----------------------------
DROP TABLE IF EXISTS "highest_school_level_2010";
CREATE TABLE "highest_school_level_2010" (
	"id" int4 NOT NULL DEFAULT nextval('highest_school_level_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"highest_school_level" varchar(50) DEFAULT NULL,
	"highest_school_level_date_collected" timestamptz DEFAULT NULL,
	"highest_school_level_date_effective" timestamptz DEFAULT NULL,
	"highest_school_level_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "highest_school_level_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "length_of_stay_at_prior_residence_2010"
-- ----------------------------
DROP TABLE IF EXISTS "length_of_stay_at_prior_residence_2010";
CREATE TABLE "length_of_stay_at_prior_residence_2010" (
	"id" int4 NOT NULL DEFAULT nextval('length_of_stay_at_prior_residence_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"length_of_stay_at_prior_residence" varchar(50) DEFAULT NULL,
	"length_of_stay_at_prior_residence_date_collected" timestamptz DEFAULT NULL,
	"length_of_stay_at_prior_residence_date_effective" timestamptz DEFAULT NULL,
	"length_of_stay_at_prior_residence_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "length_of_stay_at_prior_residence_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "hud_chronic_homeless_2010"
-- ----------------------------
DROP TABLE IF EXISTS "hud_chronic_homeless_2010";
CREATE TABLE "hud_chronic_homeless_2010" (
	"id" int4 NOT NULL DEFAULT nextval('hud_chronic_homeless_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"hud_chronic_homeless" varchar(50) DEFAULT NULL,
	"hud_chronic_homeless_date_collected" timestamptz DEFAULT NULL,
	"hud_chronic_homeless_date_effective" timestamptz DEFAULT NULL,
	"hud_chronic_homeless_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "hud_chronic_homeless_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "hiv_aids_status_2010"
-- ----------------------------
DROP TABLE IF EXISTS "hiv_aids_status_2010";
CREATE TABLE "hiv_aids_status_2010" (
	"id" int4 NOT NULL DEFAULT nextval('hiv_aids_status_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"has_hiv_aids" varchar(50) DEFAULT NULL,
	"has_hiv_aids_date_collected" timestamptz DEFAULT NULL,
	"has_hiv_aids_date_effective" timestamptz DEFAULT NULL,
	"has_hiv_aids_data_collection_stage" varchar(50) DEFAULT NULL,
	"receive_hiv_aids_services" varchar(50) DEFAULT NULL,
	"receive_hiv_aids_services_date_collected" timestamptz DEFAULT NULL,
	"receive_hiv_aids_services_date_effective" timestamptz DEFAULT NULL,
	"receive_hiv_aids_services_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "hiv_aids_status_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "health_status_2010"
-- ----------------------------
DROP TABLE IF EXISTS "health_status_2010";
CREATE TABLE "health_status_2010" (
	"id" int4 NOT NULL DEFAULT nextval('health_status_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"health_status" varchar(50) DEFAULT NULL,
	"health_status_date_collected" timestamptz DEFAULT NULL,
	"health_status_date_effective" timestamptz DEFAULT NULL,
	"health_status_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "health_status_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "engaged_date_2010"
-- ----------------------------
DROP TABLE IF EXISTS "engaged_date_2010";
CREATE TABLE "engaged_date_2010" (
	"id" int4 NOT NULL DEFAULT nextval('engaged_date_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"engaged_date" timestamptz DEFAULT NULL,
	"engaged_date_date_collected" timestamptz DEFAULT NULL,
	"engaged_date_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "engaged_date_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "employment_2010"
-- ----------------------------
DROP TABLE IF EXISTS "employment_2010";
CREATE TABLE "employment_2010" (
	"id" int4 NOT NULL DEFAULT nextval('employment_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"employment_id_id_id_num" varchar(50) DEFAULT NULL,
	"employment_id_id_id_str" varchar(50) DEFAULT NULL,
	"employment_id_id_delete" int4 DEFAULT NULL,
	"employment_id_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"employment_id_id_delete_effective" timestamptz DEFAULT NULL,
	"currently_employed" varchar(50) DEFAULT NULL,
	"currently_employed_date_collected" timestamptz DEFAULT NULL,
	"currently_employed_date_effective" timestamptz DEFAULT NULL,
	"currently_employed_data_collection_stage" varchar(50) DEFAULT NULL,
	"hours_worked_last_week" varchar(50) DEFAULT NULL,
	"hours_worked_last_week_date_collected" timestamptz DEFAULT NULL,
	"hours_worked_last_week_date_effective" timestamptz DEFAULT NULL,
	"hours_worked_last_week_data_collection_stage" varchar(50) DEFAULT NULL,
	"employment_tenure" varchar(50) DEFAULT NULL,
	"employment_tenure_date_collected" timestamptz DEFAULT NULL,
	"employment_tenure_date_effective" timestamptz DEFAULT NULL,
	"employment_tenure_data_collection_stage" varchar(50) DEFAULT NULL,
	"looking_for_work" varchar(50) DEFAULT NULL,
	"looking_for_work_date_collected" timestamptz DEFAULT NULL,
	"looking_for_work_date_effective" timestamptz DEFAULT NULL,
	"looking_for_work_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "employment_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "domestic_violence_2010"
-- ----------------------------
DROP TABLE IF EXISTS "domestic_violence_2010";
CREATE TABLE "domestic_violence_2010" (
	"id" int4 NOT NULL DEFAULT nextval('domestic_violence_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"domestic_violence_survivor" varchar(50) DEFAULT NULL,
	"domestic_violence_survivor_date_collected" timestamptz DEFAULT NULL,
	"domestic_violence_survivor_date_effective" timestamptz DEFAULT NULL,
	"domestic_violence_survivor_data_collection_stage" varchar(50) DEFAULT NULL,
	"dvo_occurred" varchar(50) DEFAULT NULL,
	"dvo_occurred_date_collected" timestamptz DEFAULT NULL,
	"dvo_occurred_date_effective" timestamptz DEFAULT NULL,
	"dvo_occurred_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "domestic_violence_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "disabling_condition_2010"
-- ----------------------------
DROP TABLE IF EXISTS "disabling_condition_2010";
CREATE TABLE "disabling_condition_2010" (
	"id" int4 NOT NULL DEFAULT nextval('disabling_condition_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"disabling_condition" varchar(50) DEFAULT NULL,
	"disabling_condition_date_collected" timestamptz DEFAULT NULL,
	"disabling_condition_date_effective" timestamptz DEFAULT NULL,
	"disabling_condition_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "disabling_condition_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "contact_made_2010"
-- ----------------------------
DROP TABLE IF EXISTS "contact_made_2010";
CREATE TABLE "contact_made_2010" (
	"id" int4 NOT NULL DEFAULT nextval('contact_made_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"contact_id_id_num" varchar(50) DEFAULT NULL,
	"contact_id_id_str" varchar(50) DEFAULT NULL,
	"contact_id_delete" int4 DEFAULT NULL,
	"contact_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"contact_id_delete_effective" timestamptz DEFAULT NULL,
	"contact_date" timestamptz DEFAULT NULL,
	"contact_date_data_collection_stage" varchar(50) DEFAULT NULL,
	"contact_location" varchar(50) DEFAULT NULL,
	"contact_location_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "contact_made_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "degree_code_2010"
-- ----------------------------
DROP TABLE IF EXISTS "degree_code_2010";
CREATE TABLE "degree_code_2010" (
	"id" int4 NOT NULL DEFAULT nextval('degree_code_2010_id_seq'::regclass),
	"degree_index_id" int4 DEFAULT NULL,
	"degree_code" varchar(50) DEFAULT NULL,
	"degree_date_collected" timestamptz DEFAULT NULL,
	"degree_date_effective" timestamptz DEFAULT NULL,
	"degree_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "degree_code_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "developmental_disability_2010"
-- ----------------------------
DROP TABLE IF EXISTS "developmental_disability_2010";
CREATE TABLE "developmental_disability_2010" (
	"id" int4 NOT NULL DEFAULT nextval('developmental_disability_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"has_developmental_disability" varchar(50) DEFAULT NULL,
	"has_developmental_disability_date_collected" timestamptz DEFAULT NULL,
	"has_developmental_disability_date_effective" timestamptz DEFAULT NULL,
	"has_developmental_disability_data_collection_stage" varchar(50) DEFAULT NULL,
	"receive_developmental_disability" varchar(50) DEFAULT NULL,
	"receive_developmental_disability_date_collected" timestamptz DEFAULT NULL,
	"receive_developmental_disability_date_effective" timestamptz DEFAULT NULL,
	"receive_developmental_disability_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "developmental_disability_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "degree_2010"
-- ----------------------------
DROP TABLE IF EXISTS "degree_2010";
CREATE TABLE "degree_2010" (
	"id" int4 NOT NULL DEFAULT nextval('degree_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"degree_id_id_num" varchar(50) DEFAULT NULL,
	"degree_id_id_str" varchar(50) DEFAULT NULL,
	"degree_id_delete" int4 DEFAULT NULL,
	"degree_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"degree_id_delete_effective" timestamptz DEFAULT NULL,
	"degree_other" varchar(50) DEFAULT NULL,
	"degree_other_date_collected" timestamptz DEFAULT NULL,
	"degree_other_date_effective" timestamptz DEFAULT NULL,
	"degree_other_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "degree_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "child_enrollment_status_barrier_2010"
-- ----------------------------
DROP TABLE IF EXISTS "child_enrollment_status_barrier_2010";
CREATE TABLE "child_enrollment_status_barrier_2010" (
	"id" int4 NOT NULL DEFAULT nextval('child_enrollment_status_barrier_2010_id_seq'::regclass),
	"child_enrollment_status_index_id" int4 DEFAULT NULL,
	"barrier_id_id_num" varchar(50) DEFAULT NULL,
	"barrier_id_id_str" varchar(50) DEFAULT NULL,
	"barrier_id_delete" int4 DEFAULT NULL,
	"barrier_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"barrier_id_delete_effective" timestamptz DEFAULT NULL,
	"barried_code" varchar(50) DEFAULT NULL,
	"barried_code_date_collected" timestamptz DEFAULT NULL,
	"barried_code_date_effective" timestamptz DEFAULT NULL,
	"barried_code_data_collection_stage" varchar(50) DEFAULT NULL,
	"barrier_other" varchar(50) DEFAULT NULL,
	"barrier_other_date_collected" timestamptz DEFAULT NULL,
	"barrier_other_date_effective" timestamptz DEFAULT NULL,
	"barrier_other_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "child_enrollment_status_barrier_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "destinations_2010"
-- ----------------------------
DROP TABLE IF EXISTS "destinations_2010";
CREATE TABLE "destinations_2010" (
	"id" int4 NOT NULL DEFAULT nextval('destinations_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"destination_id_id_num" varchar(50) DEFAULT NULL,
	"destination_id_id_str" varchar(50) DEFAULT NULL,
	"destination_id_delete" int4 DEFAULT NULL,
	"destination_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"destination_id_delete_effective" timestamptz DEFAULT NULL,
	"destination_code" varchar(50) DEFAULT NULL,
	"destination_code_date_collected" timestamptz DEFAULT NULL,
	"destination_code_date_effective" timestamptz DEFAULT NULL,
	"destination_code_data_collection_stage" varchar(50) DEFAULT NULL,
	"destination_other" varchar(50) DEFAULT NULL,
	"destination_other_date_collected" timestamptz DEFAULT NULL,
	"destination_other_date_effective" timestamptz DEFAULT NULL,
	"destination_other_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "destinations_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "currently_in_school_2010"
-- ----------------------------
DROP TABLE IF EXISTS "currently_in_school_2010";
CREATE TABLE "currently_in_school_2010" (
	"id" int4 NOT NULL DEFAULT nextval('currently_in_school_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"currently_in_school" varchar(50) DEFAULT NULL,
	"currently_in_school_date_collected" timestamptz DEFAULT NULL,
	"currently_in_school_date_effective" timestamptz DEFAULT NULL,
	"currently_in_school_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "currently_in_school_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "child_enrollment_status_2010"
-- ----------------------------
DROP TABLE IF EXISTS "child_enrollment_status_2010";
CREATE TABLE "child_enrollment_status_2010" (
	"id" int4 NOT NULL DEFAULT nextval('child_enrollment_status_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"child_enrollment_status_id_id_num" varchar(50) DEFAULT NULL,
	"child_enrollment_status_id_id_str" varchar(50) DEFAULT NULL,
	"child_enrollment_status_id_delete" int4 DEFAULT NULL,
	"child_enrollment_status_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"child_enrollment_status_id_delete_effective" timestamptz DEFAULT NULL,
	"child_currently_enrolled_in_school" varchar(50) DEFAULT NULL,
	"child_currently_enrolled_in_school_date_effective" timestamptz DEFAULT NULL,
	"child_currently_enrolled_in_school_date_collected" timestamptz DEFAULT NULL,
	"child_currently_enrolled_in_school_data_collection_stage" varchar(50) DEFAULT NULL,
	"child_school_name" varchar(50) DEFAULT NULL,
	"child_school_name_date_effective" timestamptz DEFAULT NULL,
	"child_school_name_date_collected" timestamptz DEFAULT NULL,
	"child_school_name_data_collection_stage" varchar(50) DEFAULT NULL,
	"child_mckinney_vento_liaison" varchar(50) DEFAULT NULL,
	"child_mckinney_vento_liaison_date_effective" timestamptz DEFAULT NULL,
	"child_mckinney_vento_liaison_date_collected" timestamptz DEFAULT NULL,
	"child_mckinney_vento_liaison_data_collection_stage" varchar(50) DEFAULT NULL,
	"child_school_type" varchar(50) DEFAULT NULL,
	"child_school_type_date_effective" timestamptz DEFAULT NULL,
	"child_school_type_date_collected" timestamptz DEFAULT NULL,
	"child_school_type_data_collection_stage" varchar(50) DEFAULT NULL,
	"child_school_last_enrolled_date" timestamptz DEFAULT NULL,
	"child_school_last_enrolled_date_date_collected" timestamptz DEFAULT NULL,
	"child_school_last_enrolled_date_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "child_enrollment_status_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "chronic_health_condition_2010"
-- ----------------------------
DROP TABLE IF EXISTS "chronic_health_condition_2010";
CREATE TABLE "chronic_health_condition_2010" (
	"id" int4 NOT NULL DEFAULT nextval('chronic_health_condition_2010_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"has_chronic_health_condition" varchar(50) DEFAULT NULL,
	"has_chronic_health_condition_date_collected" timestamptz DEFAULT NULL,
	"has_chronic_health_condition_date_effective" timestamptz DEFAULT NULL,
	"has_chronic_health_condition_data_collection_stage" varchar(50) DEFAULT NULL,
	"receive_chronic_health_services" varchar(50) DEFAULT NULL,
	"receive_chronic_health_services_date_collected" timestamptz DEFAULT NULL,
	"receive_chronic_health_services_date_effective" timestamptz DEFAULT NULL,
	"receive_chronic_health_services_data_collection_stage" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "chronic_health_condition_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "release_of_information"
-- ----------------------------
DROP TABLE IF EXISTS "release_of_information";
CREATE TABLE "release_of_information" (
	"id" int4 NOT NULL DEFAULT nextval('release_of_information_id_seq'::regclass),
	"person_index_id" int4 DEFAULT NULL,
	"release_of_information_idid_num" varchar(32) DEFAULT NULL,
	"release_of_information_idid_num_date_collected" timestamptz DEFAULT NULL,
	"release_of_information_idid_str" varchar(32) DEFAULT NULL,
	"release_of_information_idid_str_date_collected" timestamptz DEFAULT NULL,
	"site_service_idid_num" varchar(32) DEFAULT NULL,
	"site_service_idid_num_date_collected" timestamptz DEFAULT NULL,
	"site_service_idid_str" varchar(32) DEFAULT NULL,
	"site_service_idid_str_date_collected" timestamptz DEFAULT NULL,
	"documentation" varchar(32) DEFAULT NULL,
	"documentation_date_collected" timestamptz DEFAULT NULL,
	"start_date" varchar(32) DEFAULT NULL,
	"start_date_date_collected" timestamptz DEFAULT NULL,
	"end_date" varchar(32) DEFAULT NULL,
	"end_date_date_collected" timestamptz DEFAULT NULL,
	"release_granted" varchar(32) DEFAULT NULL,
	"release_granted_date_collected" timestamptz DEFAULT NULL,
	"reported" bool DEFAULT NULL,
	"release_of_information_id_data_collection_stage_2010" int4 DEFAULT NULL,
	"release_of_information_id_date_effective_2010" timestamptz DEFAULT NULL,
	"documentation_data_collection_stage_2010" int4 DEFAULT NULL,
	"documentation_date_effective_2010" timestamptz DEFAULT NULL,
	"release_granted_data_collection_stage_2010" int4 DEFAULT NULL,
	"release_granted_date_effective_2010" timestamptz DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "release_of_information" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "income_and_sources"
-- ----------------------------
DROP TABLE IF EXISTS "income_and_sources";
CREATE TABLE "income_and_sources" (
	"id" int4 NOT NULL DEFAULT nextval('income_and_sources_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"amount" int4 DEFAULT NULL,
	"amount_date_collected" timestamptz DEFAULT NULL,
	"income_source_code" int4 DEFAULT NULL,
	"income_source_code_date_collected" timestamptz DEFAULT NULL,
	"income_source_other" varchar(32) DEFAULT NULL,
	"income_source_other_date_collected" timestamptz DEFAULT NULL,
	"income_and_source_id_id_id_num_2010" varchar(32) DEFAULT NULL,
	"income_and_source_id_id_id_str_2010" varchar(32) DEFAULT NULL,
	"income_and_source_id_id_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"income_and_source_id_id_delete_effective_2010" timestamptz DEFAULT NULL,
	"income_source_code_date_effective_2010" timestamptz DEFAULT NULL,
	"income_source_other_date_effective_2010" timestamptz DEFAULT NULL,
	"receiving_income_source_date_collected_2010" timestamptz DEFAULT NULL,
	"receiving_income_source_date_effective_2010" timestamptz DEFAULT NULL,
	"income_source_amount_date_effective_2010" timestamptz DEFAULT NULL,
	"income_and_source_id_id_delete_2010" int4 DEFAULT NULL,
	"income_source_code_data_collection_stage_2010" int4 DEFAULT NULL,
	"income_source_other_data_collection_stage_2010" int4 DEFAULT NULL,
	"receiving_income_source_2010" int4 DEFAULT NULL,
	"receiving_income_source_data_collection_stage_2010" int4 DEFAULT NULL,
	"income_source_amount_data_collection_stage_2010" int4 DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "income_and_sources" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "veteran"
-- ----------------------------
DROP TABLE IF EXISTS "veteran";
CREATE TABLE "veteran" (
	"id" int4 NOT NULL DEFAULT nextval('veteran_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"service_era" int4 DEFAULT NULL,
	"service_era_date_collected" timestamptz DEFAULT NULL,
	"military_service_duration" int4 DEFAULT NULL,
	"military_service_duration_date_collected" timestamptz DEFAULT NULL,
	"served_in_war_zone" int4 DEFAULT NULL,
	"served_in_war_zone_date_collected" timestamptz DEFAULT NULL,
	"war_zone" int4 DEFAULT NULL,
	"war_zone_date_collected" timestamptz DEFAULT NULL,
	"war_zone_other" varchar(50) DEFAULT NULL,
	"war_zone_other_date_collected" timestamptz DEFAULT NULL,
	"months_in_war_zone" int4 DEFAULT NULL,
	"months_in_war_zone_date_collected" timestamptz DEFAULT NULL,
	"received_fire" int4 DEFAULT NULL,
	"received_fire_date_collected" timestamptz DEFAULT NULL,
	"military_branch" int4 DEFAULT NULL,
	"military_branch_date_collected" timestamptz DEFAULT NULL,
	"military_branch_other" varchar(50) DEFAULT NULL,
	"military_branch_other_date_collected" timestamptz DEFAULT NULL,
	"discharge_status" int4 DEFAULT NULL,
	"discharge_status_date_collected" timestamptz DEFAULT NULL,
	"discharge_status_other" varchar(50) DEFAULT NULL,
	"discharge_status_other_date_collected" timestamptz DEFAULT NULL,
	"reported" bool DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "veteran" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "person_historical"
-- ----------------------------
DROP TABLE IF EXISTS "person_historical";
CREATE TABLE "person_historical" (
	"id" int4 NOT NULL DEFAULT nextval('person_historical_id_seq'::regclass),
	"person_index_id" int4 DEFAULT NULL,
	"site_service_index_id" int4 DEFAULT NULL,
	"person_historical_idid_num" varchar(32) DEFAULT NULL,
	"person_historical_idid_num_date_collected" timestamptz DEFAULT NULL,
	"person_historical_idid_str" varchar(32) DEFAULT NULL,
	"person_historical_idid_str_date_collected" timestamptz DEFAULT NULL,
	"barrier_code" varchar(32) DEFAULT NULL,
	"barrier_code_date_collected" timestamptz DEFAULT NULL,
	"barrier_other" varchar(32) DEFAULT NULL,
	"barrier_other_date_collected" timestamptz DEFAULT NULL,
	"child_currently_enrolled_in_school" varchar(32) DEFAULT NULL,
	"child_currently_enrolled_in_school_date_collected" timestamptz DEFAULT NULL,
	"currently_employed" varchar(32) DEFAULT NULL,
	"currently_employed_date_collected" timestamptz DEFAULT NULL,
	"currently_in_school" varchar(32) DEFAULT NULL,
	"currently_in_school_date_collected" timestamptz DEFAULT NULL,
	"degree_code" varchar(32) DEFAULT NULL,
	"degree_code_date_collected" timestamptz DEFAULT NULL,
	"degree_other" varchar(32) DEFAULT NULL,
	"degree_other_date_collected" timestamptz DEFAULT NULL,
	"developmental_disability" varchar(32) DEFAULT NULL,
	"developmental_disability_date_collected" timestamptz DEFAULT NULL,
	"domestic_violence" varchar(32) DEFAULT NULL,
	"domestic_violence_date_collected" timestamptz DEFAULT NULL,
	"domestic_violence_how_long" varchar(32) DEFAULT NULL,
	"domestic_violence_how_long_date_collected" timestamptz DEFAULT NULL,
	"due_date" varchar(32) DEFAULT NULL,
	"due_date_date_collected" timestamptz DEFAULT NULL,
	"employment_tenure" varchar(32) DEFAULT NULL,
	"employment_tenure_date_collected" timestamptz DEFAULT NULL,
	"health_status" varchar(32) DEFAULT NULL,
	"health_status_date_collected" timestamptz DEFAULT NULL,
	"highest_school_level" varchar(32) DEFAULT NULL,
	"highest_school_level_date_collected" timestamptz DEFAULT NULL,
	"hivaids_status" varchar(32) DEFAULT NULL,
	"hivaids_status_date_collected" timestamptz DEFAULT NULL,
	"hours_worked_last_week" varchar(32) DEFAULT NULL,
	"hours_worked_last_week_date_collected" timestamptz DEFAULT NULL,
	"hud_chronic_homeless" varchar(32) DEFAULT NULL,
	"hud_chronic_homeless_date_collected" timestamptz DEFAULT NULL,
	"hud_homeless" varchar(32) DEFAULT NULL,
	"hud_homeless_date_collected" timestamptz DEFAULT NULL,
	"length_of_stay_at_prior_residence" varchar(32) DEFAULT NULL,
	"length_of_stay_at_prior_residence_date_collected" timestamptz DEFAULT NULL,
	"looking_for_work" varchar(32) DEFAULT NULL,
	"looking_for_work_date_collected" timestamptz DEFAULT NULL,
	"mental_health_indefinite" varchar(32) DEFAULT NULL,
	"mental_health_indefinite_date_collected" timestamptz DEFAULT NULL,
	"mental_health_problem" varchar(32) DEFAULT NULL,
	"mental_health_problem_date_collected" timestamptz DEFAULT NULL,
	"non_cash_source_code" varchar(32) DEFAULT NULL,
	"non_cash_source_code_date_collected" timestamptz DEFAULT NULL,
	"non_cash_source_other" varchar(32) DEFAULT NULL,
	"non_cash_source_other_date_collected" timestamptz DEFAULT NULL,
	"person_email" varchar(32) DEFAULT NULL,
	"person_email_date_collected" timestamptz DEFAULT NULL,
	"person_phone_number" varchar(32) DEFAULT NULL,
	"person_phone_number_date_collected" timestamptz DEFAULT NULL,
	"physical_disability" varchar(32) DEFAULT NULL,
	"physical_disability_date_collected" timestamptz DEFAULT NULL,
	"pregnancy_status" varchar(32) DEFAULT NULL,
	"pregnancy_status_date_collected" timestamptz DEFAULT NULL,
	"prior_residence" varchar(32) DEFAULT NULL,
	"prior_residence_date_collected" timestamptz DEFAULT NULL,
	"prior_residence_other" varchar(32) DEFAULT NULL,
	"prior_residence_other_date_collected" timestamptz DEFAULT NULL,
	"reason_for_leaving" varchar(32) DEFAULT NULL,
	"reason_for_leaving_date_collected" timestamptz DEFAULT NULL,
	"reason_for_leaving_other" varchar(32) DEFAULT NULL,
	"reason_for_leaving_other_date_collected" timestamptz DEFAULT NULL,
	"school_last_enrolled_date" varchar(32) DEFAULT NULL,
	"school_last_enrolled_date_date_collected" timestamptz DEFAULT NULL,
	"school_name" varchar(32) DEFAULT NULL,
	"school_name_date_collected" timestamptz DEFAULT NULL,
	"school_type" varchar(32) DEFAULT NULL,
	"school_type_date_collected" timestamptz DEFAULT NULL,
	"subsidy_other" varchar(32) DEFAULT NULL,
	"subsidy_other_date_collected" timestamptz DEFAULT NULL,
	"subsidy_type" varchar(32) DEFAULT NULL,
	"subsidy_type_date_collected" timestamptz DEFAULT NULL,
	"substance_abuse_indefinite" varchar(32) DEFAULT NULL,
	"substance_abuse_indefinite_date_collected" timestamptz DEFAULT NULL,
	"substance_abuse_problem" varchar(32) DEFAULT NULL,
	"substance_abuse_problem_date_collected" timestamptz DEFAULT NULL,
	"total_income" varchar(32) DEFAULT NULL,
	"total_income_date_collected" timestamptz DEFAULT NULL,
	"vocational_training" varchar(32) DEFAULT NULL,
	"vocational_training_date_collected" timestamptz DEFAULT NULL,
	"reported" bool DEFAULT NULL,
	"person_historical_id_delete_2010" int4 DEFAULT NULL,
	"person_historical_id_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"person_historical_id_delete_effective_2010" timestamptz DEFAULT NULL,
	"site_service_id_2010" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "person_historical" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "races"
-- ----------------------------
DROP TABLE IF EXISTS "races";
CREATE TABLE "races" (
	"id" int4 NOT NULL DEFAULT nextval('races_id_seq'::regclass),
	"person_index_id" int4 DEFAULT NULL,
	"race_unhashed" int4 DEFAULT NULL,
	"race_hashed" varchar(32) DEFAULT NULL,
	"race_date_collected" timestamptz DEFAULT NULL,
	"reported" bool DEFAULT NULL,
	"race_data_collection_stage_2010" int4 DEFAULT NULL,
	"race_date_effective_2010" timestamptz DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "races" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "drug_history"
-- ----------------------------
DROP TABLE IF EXISTS "drug_history";
CREATE TABLE "drug_history" (
	"id" int4 NOT NULL DEFAULT nextval('drug_history_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"drug_history_id" varchar(32) DEFAULT NULL,
	"drug_history_id_date_collected" timestamptz DEFAULT NULL,
	"drug_code" int4 DEFAULT NULL,
	"drug_code_date_collected" timestamptz DEFAULT NULL,
	"drug_use_frequency" int4 DEFAULT NULL,
	"drug_use_frequency_date_collected" timestamptz DEFAULT NULL,
	"reported" bool DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "drug_history" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "emergency_contact"
-- ----------------------------
DROP TABLE IF EXISTS "emergency_contact";
CREATE TABLE "emergency_contact" (
	"id" int4 NOT NULL DEFAULT nextval('emergency_contact_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"emergency_contact_id" varchar(32) DEFAULT NULL,
	"emergency_contact_id_date_collected" timestamptz DEFAULT NULL,
	"emergency_contact_name" varchar(32) DEFAULT NULL,
	"emergency_contact_name_date_collected" timestamptz DEFAULT NULL,
	"emergency_contact_phone_number_0" varchar(32) DEFAULT NULL,
	"emergency_contact_phone_number_date_collected_0" timestamptz DEFAULT NULL,
	"emergency_contact_phone_number_type_0" varchar(32) DEFAULT NULL,
	"emergency_contact_phone_number_1" varchar(32) DEFAULT NULL,
	"emergency_contact_phone_number_date_collected_1" timestamptz DEFAULT NULL,
	"emergency_contact_phone_number_type_1" varchar(32) DEFAULT NULL,
	"emergency_contact_address_date_collected" timestamptz DEFAULT NULL,
	"emergency_contact_address_start_date" timestamptz DEFAULT NULL,
	"emergency_contact_address_start_date_date_collected" timestamptz DEFAULT NULL,
	"emergency_contact_address_end_date" timestamptz DEFAULT NULL,
	"emergency_contact_address_end_date_date_collected" timestamptz DEFAULT NULL,
	"emergency_contact_address_line1" varchar(32) DEFAULT NULL,
	"emergency_contact_address_line1_date_collected" timestamptz DEFAULT NULL,
	"emergency_contact_address_line2" varchar(32) DEFAULT NULL,
	"emergency_contact_address_line2_date_collected" timestamptz DEFAULT NULL,
	"emergency_contact_address_city" varchar(32) DEFAULT NULL,
	"emergency_contact_address_city_date_collected" timestamptz DEFAULT NULL,
	"emergency_contact_address_state" varchar(32) DEFAULT NULL,
	"emergency_contact_address_state_date_collected" timestamptz DEFAULT NULL,
	"emergency_contact_relation_to_client" varchar(32) DEFAULT NULL,
	"emergency_contact_relation_to_client_date_collected" timestamptz DEFAULT NULL,
	"reported" bool DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "emergency_contact" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "funding_source_2010"
-- ----------------------------
DROP TABLE IF EXISTS "funding_source_2010";
CREATE TABLE "funding_source_2010" (
	"id" int4 NOT NULL DEFAULT nextval('funding_source_2010_id_seq'::regclass),
	"service_index_id" int4 DEFAULT NULL,
	"service_event_index_id" int4 DEFAULT NULL,
	"funding_source_id_id_num" varchar(50) DEFAULT NULL,
	"funding_source_id_id_str" varchar(50) DEFAULT NULL,
	"funding_source_id_delete" varchar(50) DEFAULT NULL,
	"funding_source_id_delete_occurred_date" timestamptz DEFAULT NULL,
	"funding_source_id_delete_effective" timestamptz DEFAULT NULL,
	"federal_cfda_number" varchar(50) DEFAULT NULL,
	"receives_mckinney_funding" varchar(50) DEFAULT NULL,
	"advance_or_arrears" varchar(50) DEFAULT NULL,
	"financial_assistance_amount" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "funding_source_2010" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "hud_homeless_episodes"
-- ----------------------------
DROP TABLE IF EXISTS "hud_homeless_episodes";
CREATE TABLE "hud_homeless_episodes" (
	"id" int4 NOT NULL DEFAULT nextval('hud_homeless_episodes_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"start_date" varchar(32) DEFAULT NULL,
	"start_date_date_collected" timestamptz DEFAULT NULL,
	"end_date" varchar(32) DEFAULT NULL,
	"end_date_date_collected" timestamptz DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "hud_homeless_episodes" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "person_address"
-- ----------------------------
DROP TABLE IF EXISTS "person_address";
CREATE TABLE "person_address" (
	"id" int4 NOT NULL DEFAULT nextval('person_address_id_seq'::regclass),
	"person_historical_index_id" int4 DEFAULT NULL,
	"address_period_start_date" timestamptz DEFAULT NULL,
	"address_period_start_date_date_collected" timestamptz DEFAULT NULL,
	"address_period_end_date" timestamptz DEFAULT NULL,
	"address_period_end_date_date_collected" timestamptz DEFAULT NULL,
	"pre_address_line" varchar(32) DEFAULT NULL,
	"pre_address_line_date_collected" timestamptz DEFAULT NULL,
	"pre_address_line_date_effective_2010" timestamptz DEFAULT NULL,
	"pre_address_line_data_collection_stage_2010" int4 DEFAULT NULL,
	"line1" varchar(32) DEFAULT NULL,
	"line1_date_collected" timestamptz DEFAULT NULL,
	"line1_date_effective_2010" timestamptz DEFAULT NULL,
	"line1_data_collection_stage_2010" int4 DEFAULT NULL,
	"line2" varchar(32) DEFAULT NULL,
	"line2_date_collected" timestamptz DEFAULT NULL,
	"line2_date_effective_2010" timestamptz DEFAULT NULL,
	"line2_data_collection_stage_2010" int4 DEFAULT NULL,
	"city" varchar(32) DEFAULT NULL,
	"city_date_collected" timestamptz DEFAULT NULL,
	"city_date_effective_2010" timestamptz DEFAULT NULL,
	"city_data_collection_stage_2010" int4 DEFAULT NULL,
	"county" varchar(32) DEFAULT NULL,
	"county_date_collected" timestamptz DEFAULT NULL,
	"county_date_effective_2010" timestamptz DEFAULT NULL,
	"county_data_collection_stage_2010" int4 DEFAULT NULL,
	"state" varchar(32) DEFAULT NULL,
	"state_date_collected" timestamptz DEFAULT NULL,
	"state_date_effective_2010" timestamptz DEFAULT NULL,
	"state_data_collection_stage_2010" int4 DEFAULT NULL,
	"zipcode" varchar(10) DEFAULT NULL,
	"zipcode_date_collected" timestamptz DEFAULT NULL,
	"zipcode_date_effective_2010" timestamptz DEFAULT NULL,
	"zipcode_data_collection_stage_2010" int4 DEFAULT NULL,
	"country" varchar(32) DEFAULT NULL,
	"country_date_collected" timestamptz DEFAULT NULL,
	"country_date_effective_2010" timestamptz DEFAULT NULL,
	"country_data_collection_stage_2010" int4 DEFAULT NULL,
	"is_last_permanent_zip" int4 DEFAULT NULL,
	"is_last_permanent_zip_date_collected" timestamptz DEFAULT NULL,
	"is_last_permanent_zip_date_effective_2010" timestamptz DEFAULT NULL,
	"is_last_permanent_zip_data_collection_stage_2010" int4 DEFAULT NULL,
	"zip_quality_code" int4 DEFAULT NULL,
	"zip_quality_code_date_collected" timestamptz DEFAULT NULL,
	"zip_quality_code_date_effective_2010" timestamptz DEFAULT NULL,
	"zip_quality_code_data_collection_stage_2010" int4 DEFAULT NULL,
	"reported" bool DEFAULT NULL,
	"attr_delete_2010" int4 DEFAULT NULL,
	"attr_delete_occurred_date_2010" timestamptz DEFAULT NULL,
	"attr_effective_2010" timestamptz DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "person_address" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "members"
-- ----------------------------
DROP TABLE IF EXISTS "members";
CREATE TABLE "members" (
	"id" int4 NOT NULL DEFAULT nextval('members_id_seq'::regclass),
	"household_index_id" int4 DEFAULT NULL,
	"person_id_unhashed" varchar(32) DEFAULT NULL,
	"person_id_unhashed_date_collected" timestamptz DEFAULT NULL,
	"person_id_hashed" varchar(32) DEFAULT NULL,
	"person_id_hashed_date_collected" timestamptz DEFAULT NULL,
	"relationship_to_head_of_household" varchar(32) DEFAULT NULL,
	"relationship_to_head_of_household_date_collected" timestamptz DEFAULT NULL,
	"reported" bool DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "members" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "other_names"
-- ----------------------------
DROP TABLE IF EXISTS "other_names";
CREATE TABLE "other_names" (
	"id" int4 NOT NULL DEFAULT nextval('other_names_id_seq'::regclass),
	"person_index_id" int4 DEFAULT NULL,
	"other_first_name_unhashed" varchar(50) DEFAULT NULL,
	"other_first_name_hashed" varchar(32) DEFAULT NULL,
	"other_first_name_date_collected" timestamptz DEFAULT NULL,
	"other_first_name_date_effective_2010" timestamptz DEFAULT NULL,
	"other_first_name_data_collection_stage_2010" int4 DEFAULT NULL,
	"other_middle_name_unhashed" varchar(50) DEFAULT NULL,
	"other_middle_name_hashed" varchar(32) DEFAULT NULL,
	"other_middle_name_date_collected" timestamptz DEFAULT NULL,
	"other_middle_name_date_effective_2010" timestamptz DEFAULT NULL,
	"other_middle_name_data_collection_stage_2010" int4 DEFAULT NULL,
	"other_last_name_unhashed" varchar(50) DEFAULT NULL,
	"other_last_name_hashed" varchar(32) DEFAULT NULL,
	"other_last_name_date_collected" timestamptz DEFAULT NULL,
	"other_last_name_date_effective_2010" timestamptz DEFAULT NULL,
	"other_last_name_data_collection_stage_2010" int4 DEFAULT NULL,
	"other_suffix_unhashed" varchar(50) DEFAULT NULL,
	"other_suffix_hashed" varchar(32) DEFAULT NULL,
	"other_suffix_date_collected" timestamptz DEFAULT NULL,
	"other_suffix_date_effective_2010" timestamptz DEFAULT NULL,
	"other_suffix_data_collection_stage_2010" int4 DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "other_names" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "household"
-- ----------------------------
DROP TABLE IF EXISTS "household";
CREATE TABLE "household" (
	"id" int4 NOT NULL DEFAULT nextval('household_id_seq'::regclass),
	"export_id" varchar(50) DEFAULT NULL,
	"household_id_num" varchar(32) DEFAULT NULL,
	"household_id_num_date_collected" timestamptz DEFAULT NULL,
	"household_id_str" varchar(32) DEFAULT NULL,
	"household_id_str_date_collected" timestamptz DEFAULT NULL,
	"head_of_household_id_unhashed" varchar(32) DEFAULT NULL,
	"head_of_household_id_unhashed_date_collected" timestamptz DEFAULT NULL,
	"head_of_household_id_hashed" varchar(32) DEFAULT NULL,
	"head_of_household_id_hashed_date_collected" timestamptz DEFAULT NULL,
	"reported" bool DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "household" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "resource_info_2010"
-- ----------------------------
DROP TABLE IF EXISTS "resource_info_2010";
CREATE TABLE "resource_info_2010" (
	"id" int4 NOT NULL DEFAULT nextval('resource_info_2010_id_seq'::regclass),
	"agency_index_id" int4 DEFAULT NULL,
	"site_service_index_id" int4 DEFAULT NULL,
	"resource_specialist" varchar(50) DEFAULT NULL,
	"available_for_directory" varchar(50) DEFAULT NULL,
	"available_for_referral" varchar(50) DEFAULT NULL,
	"available_for_research" varchar(50) DEFAULT NULL,
	"date_added" timestamptz DEFAULT NULL,
	"date_last_verified" timestamptz DEFAULT NULL,
	"date_of_last_action" timestamptz DEFAULT NULL,
	"last_action_type" varchar(50) DEFAULT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "resource_info_2010" OWNER TO "postgres";


-- ----------------------------
--  Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "age_requirements_id_seq" OWNED BY "age_requirements"."id";
ALTER SEQUENCE "agency_2010_id_seq" OWNED BY "agency_2010"."id";
ALTER SEQUENCE "agency_child_2010_id_seq" OWNED BY "agency_child_2010"."id";
ALTER SEQUENCE "agency_service_2010_id_seq" OWNED BY "agency_service_2010"."id";
ALTER SEQUENCE "aid_requirements_id_seq" OWNED BY "aid_requirements"."id";
ALTER SEQUENCE "aka_2010_id_seq" OWNED BY "aka_2010"."id";
ALTER SEQUENCE "application_process_2010_id_seq" OWNED BY "application_process_2010"."id";
ALTER SEQUENCE "assignment_2010_id_seq" OWNED BY "assignment_2010"."id";
ALTER SEQUENCE "assignment_period_2010_id_seq" OWNED BY "assignment_period_2010"."id";
ALTER SEQUENCE "child_enrollment_status_2010_id_seq" OWNED BY "child_enrollment_status_2010"."id";
ALTER SEQUENCE "child_enrollment_status_barrier_2010_id_seq" OWNED BY "child_enrollment_status_barrier_2010"."id";
ALTER SEQUENCE "chronic_health_condition_2010_id_seq" OWNED BY "chronic_health_condition_2010"."id";
ALTER SEQUENCE "contact_2010_id_seq" OWNED BY "contact_2010"."id";
ALTER SEQUENCE "contact_made_2010_id_seq" OWNED BY "contact_made_2010"."id";
ALTER SEQUENCE "cross_street_2010_id_seq" OWNED BY "cross_street_2010"."id";
ALTER SEQUENCE "currently_in_school_2010_id_seq" OWNED BY "currently_in_school_2010"."id";
ALTER SEQUENCE "degree_2010_id_seq" OWNED BY "degree_2010"."id";
ALTER SEQUENCE "degree_code_2010_id_seq" OWNED BY "degree_code_2010"."id";
ALTER SEQUENCE "destinations_2010_id_seq" OWNED BY "destinations_2010"."id";
ALTER SEQUENCE "developmental_disability_2010_id_seq" OWNED BY "developmental_disability_2010"."id";
ALTER SEQUENCE "disabling_condition_2010_id_seq" OWNED BY "disabling_condition_2010"."id";
ALTER SEQUENCE "documents_required_2010_id_seq" OWNED BY "documents_required_2010"."id";
ALTER SEQUENCE "domestic_violence_2010_id_seq" OWNED BY "domestic_violence_2010"."id";
ALTER SEQUENCE "drug_history_id_seq" OWNED BY "drug_history"."id";
ALTER SEQUENCE "email_2010_id_seq" OWNED BY "email_2010"."id";
ALTER SEQUENCE "emergency_contact_id_seq" OWNED BY "emergency_contact"."id";
ALTER SEQUENCE "employment_2010_id_seq" OWNED BY "employment_2010"."id";
ALTER SEQUENCE "engaged_date_2010_id_seq" OWNED BY "engaged_date_2010"."id";
ALTER SEQUENCE "family_requirements_2010_id_seq" OWNED BY "family_requirements_2010"."id";
ALTER SEQUENCE "funding_source_2010_id_seq" OWNED BY "funding_source_2010"."id";
ALTER SEQUENCE "geographic_area_served_2010_id_seq" OWNED BY "geographic_area_served_2010"."id";
ALTER SEQUENCE "health_status_2010_id_seq" OWNED BY "health_status_2010"."id";
ALTER SEQUENCE "highest_school_level_2010_id_seq" OWNED BY "highest_school_level_2010"."id";
ALTER SEQUENCE "hiv_aids_status_2010_id_seq" OWNED BY "hiv_aids_status_2010"."id";
ALTER SEQUENCE "hmis_asset_2010_id_seq" OWNED BY "hmis_asset_2010"."id";
ALTER SEQUENCE "household_id_seq" OWNED BY "household"."id";
ALTER SEQUENCE "housing_status_2010_id_seq" OWNED BY "housing_status_2010"."id";
ALTER SEQUENCE "hud_chronic_homeless_2010_id_seq" OWNED BY "hud_chronic_homeless_2010"."id";
ALTER SEQUENCE "hud_homeless_episodes_id_seq" OWNED BY "hud_homeless_episodes"."id";
ALTER SEQUENCE "income_and_sources_id_seq" OWNED BY "income_and_sources"."id";
ALTER SEQUENCE "income_last_30_days_2010_id_seq" OWNED BY "income_last_30_days_2010"."id";
ALTER SEQUENCE "income_requirements_2010_id_seq" OWNED BY "income_requirements_2010"."id";
ALTER SEQUENCE "income_total_monthly_2010_id_seq" OWNED BY "income_total_monthly_2010"."id";
ALTER SEQUENCE "inventory_2010_id_seq" OWNED BY "inventory_2010"."id";
ALTER SEQUENCE "languages_2010_id_seq" OWNED BY "languages_2010"."id";
ALTER SEQUENCE "length_of_stay_at_prior_residence_2010_id_seq" OWNED BY "length_of_stay_at_prior_residence_2010"."id";
ALTER SEQUENCE "license_accreditation_2010_id_seq" OWNED BY "license_accreditation_2010"."id";
ALTER SEQUENCE "members_id_seq" OWNED BY "members"."id";
ALTER SEQUENCE "mental_health_problem_2010_id_seq" OWNED BY "mental_health_problem_2010"."id";
ALTER SEQUENCE "need_id_seq" OWNED BY "need"."id";
ALTER SEQUENCE "non_cash_benefits_2010_id_seq" OWNED BY "non_cash_benefits_2010"."id";
ALTER SEQUENCE "non_cash_benefits_last_30_days_2010_id_seq" OWNED BY "non_cash_benefits_last_30_days_2010"."id";
ALTER SEQUENCE "other_address_2010_id_seq" OWNED BY "other_address_2010"."id";
ALTER SEQUENCE "other_names_id_seq" OWNED BY "other_names"."id";
ALTER SEQUENCE "other_requirements_2010_id_seq" OWNED BY "other_requirements_2010"."id";
ALTER SEQUENCE "person_address_id_seq" OWNED BY "person_address"."id";
ALTER SEQUENCE "person_historical_id_seq" OWNED BY "person_historical"."id";
ALTER SEQUENCE "person_id_seq" OWNED BY "person"."id";
ALTER SEQUENCE "phone_2010_id_seq" OWNED BY "phone_2010"."id";
ALTER SEQUENCE "physical_disability_2010_id_seq" OWNED BY "physical_disability_2010"."id";
ALTER SEQUENCE "pit_count_set_2010_id_seq" OWNED BY "pit_count_set_2010"."id";
ALTER SEQUENCE "pit_counts_2010_id_seq" OWNED BY "pit_counts_2010"."id";
ALTER SEQUENCE "pregnancy_2010_id_seq" OWNED BY "pregnancy_2010"."id";
ALTER SEQUENCE "prior_residence_2010_id_seq" OWNED BY "prior_residence_2010"."id";
ALTER SEQUENCE "races_id_seq" OWNED BY "races"."id";
ALTER SEQUENCE "reasons_for_leaving_2010_id_seq" OWNED BY "reasons_for_leaving_2010"."id";
ALTER SEQUENCE "region_2010_id_seq" OWNED BY "region_2010"."id";
ALTER SEQUENCE "release_of_information_id_seq" OWNED BY "release_of_information"."id";
ALTER SEQUENCE "residency_requirements_2010_id_seq" OWNED BY "residency_requirements_2010"."id";
ALTER SEQUENCE "resource_info_2010_id_seq" OWNED BY "resource_info_2010"."id";
ALTER SEQUENCE "seasonal_2010_id_seq" OWNED BY "seasonal_2010"."id";
ALTER SEQUENCE "sender_system_configuration_id_seq" OWNED BY "sender_system_configuration"."id";
ALTER SEQUENCE "service_2010_id_seq" OWNED BY "service_2010"."id";
ALTER SEQUENCE "service_event_id_seq" OWNED BY "service_event"."id";
ALTER SEQUENCE "service_event_notes_2010_id_seq" OWNED BY "service_event_notes_2010"."id";
ALTER SEQUENCE "service_group_2010_id_seq" OWNED BY "service_group_2010"."id";
ALTER SEQUENCE "site_2010_id_seq" OWNED BY "site_2010"."id";
ALTER SEQUENCE "site_service_2010_id_seq" OWNED BY "site_service_2010"."id";
ALTER SEQUENCE "site_service_participation_id_seq" OWNED BY "site_service_participation"."id";
ALTER SEQUENCE "source_export_link_2010_id_seq" OWNED BY "source_export_link_2010"."id";
ALTER SEQUENCE "source_id_seq" OWNED BY "source"."id";
ALTER SEQUENCE "spatial_location_2010_id_seq" OWNED BY "spatial_location_2010"."id";
ALTER SEQUENCE "substance_abuse_problem_2010_id_seq" OWNED BY "substance_abuse_problem_2010"."id";
ALTER SEQUENCE "taxonomy_2010_id_seq" OWNED BY "taxonomy_2010"."id";
ALTER SEQUENCE "time_open_2010_id_seq" OWNED BY "time_open_2010"."id";
ALTER SEQUENCE "time_open_days_2010_id_seq" OWNED BY "time_open_days_2010"."id";
ALTER SEQUENCE "url_id_seq" OWNED BY "url"."id";
ALTER SEQUENCE "veteran_id_seq" OWNED BY "veteran"."id";
ALTER SEQUENCE "veteran_military_branches_2010_id_seq" OWNED BY "veteran_military_branches_2010"."id";
ALTER SEQUENCE "veteran_military_service_duration_2010_id_seq" OWNED BY "veteran_military_service_duration_2010"."id";
ALTER SEQUENCE "veteran_served_in_war_zone_2010_id_seq" OWNED BY "veteran_served_in_war_zone_2010"."id";
ALTER SEQUENCE "veteran_service_era_2010_id_seq" OWNED BY "veteran_service_era_2010"."id";
ALTER SEQUENCE "veteran_veteran_status_2010_id_seq" OWNED BY "veteran_veteran_status_2010"."id";
ALTER SEQUENCE "veteran_warzones_served_2010_id_seq" OWNED BY "veteran_warzones_served_2010"."id";
ALTER SEQUENCE "vocational_training_2010_id_seq" OWNED BY "vocational_training_2010"."id";
-- ----------------------------
--  Primary key structure for table "contact_2010"
-- ----------------------------
ALTER TABLE "contact_2010" ADD CONSTRAINT "contact_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "phone_2010"
-- ----------------------------
ALTER TABLE "phone_2010" ADD CONSTRAINT "phone_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "dedup_link"
-- ----------------------------
ALTER TABLE "dedup_link" ADD CONSTRAINT "dedup_link_pkey" PRIMARY KEY ("source_rec_id");

-- ----------------------------
--  Primary key structure for table "sender_system_configuration"
-- ----------------------------
ALTER TABLE "sender_system_configuration" ADD CONSTRAINT "sender_system_configuration_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "email_2010"
-- ----------------------------
ALTER TABLE "email_2010" ADD CONSTRAINT "email_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "agency_child_2010"
-- ----------------------------
ALTER TABLE "agency_child_2010" ADD CONSTRAINT "agency_child_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "region_2010"
-- ----------------------------
ALTER TABLE "region_2010" ADD CONSTRAINT "region_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "service_2010"
-- ----------------------------
ALTER TABLE "service_2010" ADD CONSTRAINT "service_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "source"
-- ----------------------------
ALTER TABLE "source" ADD CONSTRAINT "source_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "source_export_link_2010"
-- ----------------------------
ALTER TABLE "source_export_link_2010" ADD CONSTRAINT "source_export_link_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "license_accreditation_2010"
-- ----------------------------
ALTER TABLE "license_accreditation_2010" ADD CONSTRAINT "license_accreditation_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "person"
-- ----------------------------
ALTER TABLE "person" ADD CONSTRAINT "person_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "agency_service_2010"
-- ----------------------------
ALTER TABLE "agency_service_2010" ADD CONSTRAINT "agency_service_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "service_group_2010"
-- ----------------------------
ALTER TABLE "service_group_2010" ADD CONSTRAINT "service_group_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "seasonal_2010"
-- ----------------------------
ALTER TABLE "seasonal_2010" ADD CONSTRAINT "seasonal_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "aka_2010"
-- ----------------------------
ALTER TABLE "aka_2010" ADD CONSTRAINT "aka_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "url"
-- ----------------------------
ALTER TABLE "url" ADD CONSTRAINT "url_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "agency_2010"
-- ----------------------------
ALTER TABLE "agency_2010" ADD CONSTRAINT "agency_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "spatial_location_2010"
-- ----------------------------
ALTER TABLE "spatial_location_2010" ADD CONSTRAINT "spatial_location_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "other_address_2010"
-- ----------------------------
ALTER TABLE "other_address_2010" ADD CONSTRAINT "other_address_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "residency_requirements_2010"
-- ----------------------------
ALTER TABLE "residency_requirements_2010" ADD CONSTRAINT "residency_requirements_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "cross_street_2010"
-- ----------------------------
ALTER TABLE "cross_street_2010" ADD CONSTRAINT "cross_street_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "pit_counts_2010"
-- ----------------------------
ALTER TABLE "pit_counts_2010" ADD CONSTRAINT "pit_counts_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "other_requirements_2010"
-- ----------------------------
ALTER TABLE "other_requirements_2010" ADD CONSTRAINT "other_requirements_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "pit_count_set_2010"
-- ----------------------------
ALTER TABLE "pit_count_set_2010" ADD CONSTRAINT "pit_count_set_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "export"
-- ----------------------------
ALTER TABLE "export" ADD CONSTRAINT "export_pkey" PRIMARY KEY ("export_id");

-- ----------------------------
--  Primary key structure for table "languages_2010"
-- ----------------------------
ALTER TABLE "languages_2010" ADD CONSTRAINT "languages_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "site_2010"
-- ----------------------------
ALTER TABLE "site_2010" ADD CONSTRAINT "site_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "time_open_2010"
-- ----------------------------
ALTER TABLE "time_open_2010" ADD CONSTRAINT "time_open_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "hmis_asset_2010"
-- ----------------------------
ALTER TABLE "hmis_asset_2010" ADD CONSTRAINT "hmis_asset_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "time_open_days_2010"
-- ----------------------------
ALTER TABLE "time_open_days_2010" ADD CONSTRAINT "time_open_days_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "documents_required_2010"
-- ----------------------------
ALTER TABLE "documents_required_2010" ADD CONSTRAINT "documents_required_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "assignment_period_2010"
-- ----------------------------
ALTER TABLE "assignment_period_2010" ADD CONSTRAINT "assignment_period_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "inventory_2010"
-- ----------------------------
ALTER TABLE "inventory_2010" ADD CONSTRAINT "inventory_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "assignment_2010"
-- ----------------------------
ALTER TABLE "assignment_2010" ADD CONSTRAINT "assignment_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "income_requirements_2010"
-- ----------------------------
ALTER TABLE "income_requirements_2010" ADD CONSTRAINT "income_requirements_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "age_requirements"
-- ----------------------------
ALTER TABLE "age_requirements" ADD CONSTRAINT "age_requirements_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "geographic_area_served_2010"
-- ----------------------------
ALTER TABLE "geographic_area_served_2010" ADD CONSTRAINT "geographic_area_served_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "aid_requirements"
-- ----------------------------
ALTER TABLE "aid_requirements" ADD CONSTRAINT "aid_requirements_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "reasons_for_leaving_2010"
-- ----------------------------
ALTER TABLE "reasons_for_leaving_2010" ADD CONSTRAINT "reasons_for_leaving_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "site_service_participation"
-- ----------------------------
ALTER TABLE "site_service_participation" ADD CONSTRAINT "site_service_participation_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "application_process_2010"
-- ----------------------------
ALTER TABLE "application_process_2010" ADD CONSTRAINT "application_process_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "family_requirements_2010"
-- ----------------------------
ALTER TABLE "family_requirements_2010" ADD CONSTRAINT "family_requirements_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "site_service_2010"
-- ----------------------------
ALTER TABLE "site_service_2010" ADD CONSTRAINT "site_service_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "veteran_military_branches_2010"
-- ----------------------------
ALTER TABLE "veteran_military_branches_2010" ADD CONSTRAINT "veteran_military_branches_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "veteran_service_era_2010"
-- ----------------------------
ALTER TABLE "veteran_service_era_2010" ADD CONSTRAINT "veteran_service_era_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "taxonomy_2010"
-- ----------------------------
ALTER TABLE "taxonomy_2010" ADD CONSTRAINT "taxonomy_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "veteran_served_in_war_zone_2010"
-- ----------------------------
ALTER TABLE "veteran_served_in_war_zone_2010" ADD CONSTRAINT "veteran_served_in_war_zone_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "housing_status_2010"
-- ----------------------------
ALTER TABLE "housing_status_2010" ADD CONSTRAINT "housing_status_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "veteran_military_service_duration_2010"
-- ----------------------------
ALTER TABLE "veteran_military_service_duration_2010" ADD CONSTRAINT "veteran_military_service_duration_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "need"
-- ----------------------------
ALTER TABLE "need" ADD CONSTRAINT "need_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "service_event_notes_2010"
-- ----------------------------
ALTER TABLE "service_event_notes_2010" ADD CONSTRAINT "service_event_notes_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "veteran_veteran_status_2010"
-- ----------------------------
ALTER TABLE "veteran_veteran_status_2010" ADD CONSTRAINT "veteran_veteran_status_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "service_event"
-- ----------------------------
ALTER TABLE "service_event" ADD CONSTRAINT "service_event_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "veteran_warzones_served_2010"
-- ----------------------------
ALTER TABLE "veteran_warzones_served_2010" ADD CONSTRAINT "veteran_warzones_served_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "vocational_training_2010"
-- ----------------------------
ALTER TABLE "vocational_training_2010" ADD CONSTRAINT "vocational_training_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "substance_abuse_problem_2010"
-- ----------------------------
ALTER TABLE "substance_abuse_problem_2010" ADD CONSTRAINT "substance_abuse_problem_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "non_cash_benefits_last_30_days_2010"
-- ----------------------------
ALTER TABLE "non_cash_benefits_last_30_days_2010" ADD CONSTRAINT "non_cash_benefits_last_30_days_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "pregnancy_2010"
-- ----------------------------
ALTER TABLE "pregnancy_2010" ADD CONSTRAINT "pregnancy_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "prior_residence_2010"
-- ----------------------------
ALTER TABLE "prior_residence_2010" ADD CONSTRAINT "prior_residence_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "income_total_monthly_2010"
-- ----------------------------
ALTER TABLE "income_total_monthly_2010" ADD CONSTRAINT "income_total_monthly_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "mental_health_problem_2010"
-- ----------------------------
ALTER TABLE "mental_health_problem_2010" ADD CONSTRAINT "mental_health_problem_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "physical_disability_2010"
-- ----------------------------
ALTER TABLE "physical_disability_2010" ADD CONSTRAINT "physical_disability_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "income_last_30_days_2010"
-- ----------------------------
ALTER TABLE "income_last_30_days_2010" ADD CONSTRAINT "income_last_30_days_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "non_cash_benefits_2010"
-- ----------------------------
ALTER TABLE "non_cash_benefits_2010" ADD CONSTRAINT "non_cash_benefits_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "highest_school_level_2010"
-- ----------------------------
ALTER TABLE "highest_school_level_2010" ADD CONSTRAINT "highest_school_level_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "length_of_stay_at_prior_residence_2010"
-- ----------------------------
ALTER TABLE "length_of_stay_at_prior_residence_2010" ADD CONSTRAINT "length_of_stay_at_prior_residence_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "hud_chronic_homeless_2010"
-- ----------------------------
ALTER TABLE "hud_chronic_homeless_2010" ADD CONSTRAINT "hud_chronic_homeless_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "hiv_aids_status_2010"
-- ----------------------------
ALTER TABLE "hiv_aids_status_2010" ADD CONSTRAINT "hiv_aids_status_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "health_status_2010"
-- ----------------------------
ALTER TABLE "health_status_2010" ADD CONSTRAINT "health_status_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "engaged_date_2010"
-- ----------------------------
ALTER TABLE "engaged_date_2010" ADD CONSTRAINT "engaged_date_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "employment_2010"
-- ----------------------------
ALTER TABLE "employment_2010" ADD CONSTRAINT "employment_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "domestic_violence_2010"
-- ----------------------------
ALTER TABLE "domestic_violence_2010" ADD CONSTRAINT "domestic_violence_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "disabling_condition_2010"
-- ----------------------------
ALTER TABLE "disabling_condition_2010" ADD CONSTRAINT "disabling_condition_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "contact_made_2010"
-- ----------------------------
ALTER TABLE "contact_made_2010" ADD CONSTRAINT "contact_made_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "degree_code_2010"
-- ----------------------------
ALTER TABLE "degree_code_2010" ADD CONSTRAINT "degree_code_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "developmental_disability_2010"
-- ----------------------------
ALTER TABLE "developmental_disability_2010" ADD CONSTRAINT "developmental_disability_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "degree_2010"
-- ----------------------------
ALTER TABLE "degree_2010" ADD CONSTRAINT "degree_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "child_enrollment_status_barrier_2010"
-- ----------------------------
ALTER TABLE "child_enrollment_status_barrier_2010" ADD CONSTRAINT "child_enrollment_status_barrier_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "destinations_2010"
-- ----------------------------
ALTER TABLE "destinations_2010" ADD CONSTRAINT "destinations_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "currently_in_school_2010"
-- ----------------------------
ALTER TABLE "currently_in_school_2010" ADD CONSTRAINT "currently_in_school_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "child_enrollment_status_2010"
-- ----------------------------
ALTER TABLE "child_enrollment_status_2010" ADD CONSTRAINT "child_enrollment_status_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "chronic_health_condition_2010"
-- ----------------------------
ALTER TABLE "chronic_health_condition_2010" ADD CONSTRAINT "chronic_health_condition_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "release_of_information"
-- ----------------------------
ALTER TABLE "release_of_information" ADD CONSTRAINT "release_of_information_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "income_and_sources"
-- ----------------------------
ALTER TABLE "income_and_sources" ADD CONSTRAINT "income_and_sources_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "veteran"
-- ----------------------------
ALTER TABLE "veteran" ADD CONSTRAINT "veteran_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "person_historical"
-- ----------------------------
ALTER TABLE "person_historical" ADD CONSTRAINT "person_historical_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "races"
-- ----------------------------
ALTER TABLE "races" ADD CONSTRAINT "races_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "drug_history"
-- ----------------------------
ALTER TABLE "drug_history" ADD CONSTRAINT "drug_history_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "emergency_contact"
-- ----------------------------
ALTER TABLE "emergency_contact" ADD CONSTRAINT "emergency_contact_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "funding_source_2010"
-- ----------------------------
ALTER TABLE "funding_source_2010" ADD CONSTRAINT "funding_source_2010_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "hud_homeless_episodes"
-- ----------------------------
ALTER TABLE "hud_homeless_episodes" ADD CONSTRAINT "hud_homeless_episodes_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "person_address"
-- ----------------------------
ALTER TABLE "person_address" ADD CONSTRAINT "person_address_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "members"
-- ----------------------------
ALTER TABLE "members" ADD CONSTRAINT "members_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "other_names"
-- ----------------------------
ALTER TABLE "other_names" ADD CONSTRAINT "other_names_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "household"
-- ----------------------------
ALTER TABLE "household" ADD CONSTRAINT "household_pkey" PRIMARY KEY ("id");

-- ----------------------------
--  Primary key structure for table "resource_info_2010"
-- ----------------------------
ALTER TABLE "resource_info_2010" ADD CONSTRAINT "resource_info_2010_pkey" PRIMARY KEY ("id");

