/* SQLEditor (Postgres)*/

CREATE TABLE "public"."dedup_link"
(
"source_rec_id" VARCHAR(50) NOT NULL,
"destination_rec_id" VARCHAR(50),
"weight_factor" INT4,
PRIMARY KEY ("source_rec_id")
);

CREATE TABLE "public"."sender_system_configuration"
(
"id" SERIAL NOT NULL DEFAULT nextval('sender_system_configuration_id_seq'::regclass),
"vendor_name" VARCHAR(50),
"processing_mode" VARCHAR(4),
"source_id" VARCHAR(50),
"odbid" INT4,
"providerid" INT4,
"userid" INT4,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."export"
(
"export_id" VARCHAR(50) NOT NULL,
"export_id_date_collected" TIMESTAMPTZ,
"export_date" TIMESTAMPTZ,
"export_date_date_collected" TIMESTAMPTZ,
"export_period_start_date" TIMESTAMPTZ,
"export_period_start_date_date_collected" TIMESTAMPTZ,
"export_period_end_date" TIMESTAMPTZ,
"export_period_end_date_date_collected" TIMESTAMPTZ,
"export_software_vendor" VARCHAR(50),
"export_software_vendor_date_collected" TIMESTAMPTZ,
"export_software_version" VARCHAR(10),
"export_software_version_date_collected" TIMESTAMPTZ,
"export_id_id_id_num_2010" VARCHAR(50),
"export_id_id_id_str_2010" VARCHAR(50),
"export_id_id_delete_occurred_date_2010" TIMESTAMPTZ,
"export_id_id_delete_effective_2010" TIMESTAMPTZ,
"export_id_id_delete_2010" INT4,
PRIMARY KEY ("export_id")
);

CREATE TABLE "public"."agency_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('agency_2010_id_seq'::regclass),
"export_index_id" VARCHAR(50),
"region_id_id_num" VARCHAR(50),
"region_id_id_str" VARCHAR(50),
"site_service_id" VARCHAR(50),
"region_type" VARCHAR(50),
"region_type_date_collected" TIMESTAMPTZ,
"region_type_date_effective" TIMESTAMPTZ,
"region_type_data_collection_stage" INT4,
"region_description" VARCHAR(50),
"region_description_date_collected" TIMESTAMPTZ,
"region_description_date_effective" TIMESTAMPTZ,
"region_description_data_collection_stage" INT4,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."agency_service_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('agency_service_2010_id_seq'::regclass),
"agency_index_id" INT4,
"key" VARCHAR(50),
"agency_key" VARCHAR(50),
"name" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."service_group_2010"
(
"agency_index_id" INT4,
"key" VARCHAR(50),
"name" VARCHAR(50),
"program_name" VARCHAR(50)
);

CREATE TABLE "public"."agency_child_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('agency_child_2010_id_seq'::regclass),
"export_index_id" VARCHAR(50),
"agency_index_id" INT4,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."source"
(
"id" SERIAL NOT NULL DEFAULT nextval('source_id_seq'::regclass),
"export_id" VARCHAR(50),
"source_id" VARCHAR(50),
"source_id_date_collected" TIMESTAMPTZ,
"source_email" VARCHAR(50),
"source_email_date_collected" TIMESTAMPTZ,
"source_contact_extension" VARCHAR(10),
"source_contact_extension_date_collected" TIMESTAMPTZ,
"source_contact_first" VARCHAR(20),
"source_contact_first_date_collected" TIMESTAMPTZ,
"source_contact_last" VARCHAR(20),
"source_contact_last_date_collected" TIMESTAMPTZ,
"source_contact_phone" VARCHAR(20),
"source_contact_phone_date_collected" TIMESTAMPTZ,
"source_name" VARCHAR(50),
"source_name_date_collected" TIMESTAMPTZ,
"attr_version" VARCHAR(50),
"source_id_id_id_num_2010" VARCHAR(50),
"source_id_id_id_str_2010" VARCHAR(50),
"source_id_id_delete_2010" INT4,
"source_id_id_delete_occurred_date_2010" TIMESTAMPTZ,
"source_id_id_delete_effective_2010" TIMESTAMPTZ,
"software_vendor_2010" VARCHAR(50),
"software_version_2010" VARCHAR(50),
"source_contact_email_2010" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."source_export_link_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('source_export_link_2010_id_seq'::regclass),
"source_index_id" INT4,
"export_index_id" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."site_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('site_2010_id_seq'::regclass),
"export_index_id" VARCHAR(50),
"agency_index_id" INT4,
"attr_delete" INT4,
"attr_delete_occurred_date" TIMESTAMPTZ,
"attr_effective" TIMESTAMPTZ,
"airs_key" VARCHAR(50),
"airs_name" VARCHAR(50),
"site_description" VARCHAR(50),
"physical_address_pre_address_line" VARCHAR(50),
"physical_address_line_1" VARCHAR(50),
"physical_address_line_2" VARCHAR(50),
"physical_address_city" VARCHAR(50),
"physical_address_country" VARCHAR(50),
"physical_address_state" VARCHAR(50),
"physical_address_zip_code" VARCHAR(50),
"physical_address_reason_withheld" VARCHAR(50),
"physical_address_confidential" VARCHAR(50),
"physical_address_description" VARCHAR(50),
"mailing_address_pre_address_line" VARCHAR(50),
"mailing_address_line_1" VARCHAR(50),
"mailing_address_line_2" VARCHAR(50),
"mailing_address_city" VARCHAR(50),
"mailing_address_country" VARCHAR(50),
"mailing_address_state" VARCHAR(50),
"mailing_address_zip_code" VARCHAR(50),
"mailing_address_reason_withheld" VARCHAR(50),
"mailing_address_confidential" VARCHAR(50),
"mailing_address_description" VARCHAR(50),
"no_physical_address_description" VARCHAR(50),
"no_physical_address_explanation" VARCHAR(50),
"disabilities_access" VARCHAR(50),
"physical_location_description" VARCHAR(50),
"bus_service_access" VARCHAR(50),
"public_access_to_transportation" VARCHAR(50),
"year_inc" VARCHAR(50),
"annual_budget_total" VARCHAR(50),
"legal_status" VARCHAR(50),
"exclude_from_website" VARCHAR(50),
"exclude_from_directory" VARCHAR(50),
"agency_key" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."aka_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('aka_2010_id_seq'::regclass),
"agency_index_id" INT4,
"site_index_id" INT4,
"name" VARCHAR(50),
"confidential" VARCHAR(50),
"description" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."url"
(
"id" SERIAL NOT NULL DEFAULT nextval('url_id_seq'::regclass),
"agency_index_id" INT4,
"site_index_id" INT4,
"address" VARCHAR(50),
"note" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."spatial_location_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('spatial_location_2010_id_seq'::regclass),
"site_index_id" INT4,
"description" VARCHAR(50),
"datum" VARCHAR(50),
"latitude" VARCHAR(50),
"longitude" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."cross_street_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('cross_street_2010_id_seq'::regclass),
"site_index_id" INT4,
"cross_street" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."site_service_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('site_service_2010_id_seq'::regclass),
"export_index_id" VARCHAR(50),
"site_index_id" INT4,
"attr_delete" INT4,
"attr_delete_occurred_date" TIMESTAMPTZ,
"attr_effective" TIMESTAMPTZ,
"name" VARCHAR(50),
"key" VARCHAR(50),
"description" VARCHAR(50),
"fee_structure" VARCHAR(50),
"gender_requirements" VARCHAR(50),
"area_flexibility" VARCHAR(50),
"service_not_always_available" VARCHAR(50),
"service_group_key" VARCHAR(50),
"service_id" VARCHAR(50),
"site_id" VARCHAR(50),
"geographic_code" VARCHAR(50),
"geographic_code_date_collected" TIMESTAMPTZ,
"geographic_code_date_effective" TIMESTAMPTZ,
"geographic_code_data_collection_stage" VARCHAR(50),
"housing_type" VARCHAR(50),
"housing_type_date_collected" TIMESTAMPTZ,
"housing_type_date_effective" TIMESTAMPTZ,
"housing_type_data_collection_stage" VARCHAR(50),
"principal" VARCHAR(50),
"site_service_effective_period_start_date" TIMESTAMPTZ,
"site_service_effective_period_end_date" TIMESTAMPTZ,
"site_service_recorded_date" TIMESTAMPTZ,
"site_service_type" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."age_requirements"
(
"id" SERIAL NOT NULL DEFAULT nextval('age_requirements_id_seq'::regclass),
"site_service_index_id" INT4,
"gender" VARCHAR(50),
"minimum_age" VARCHAR(50),
"maximum_age" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."aid_requirements"
(
"id" SERIAL NOT NULL DEFAULT nextval('aid_requirements_id_seq'::regclass),
"site_service_index_id" INT4,
"aid_requirements" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."application_process_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('application_process_2010_id_seq'::regclass),
"site_service_index_id" INT4,
"step" VARCHAR(50),
"description" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."documents_required_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('documents_required_2010_id_seq'::regclass),
"site_service_index_id" INT4,
"documents_required" VARCHAR(50),
"description" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."seasonal_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('seasonal_2010_id_seq'::regclass),
"site_service_index_id" INT4,
"description" VARCHAR(50),
"start_date" TIMESTAMPTZ,
"end_date" TIMESTAMPTZ,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."resource_info_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('resource_info_2010_id_seq'::regclass),
"agency_index_id" INT4,
"site_service_index_id" INT4,
"resource_specialist" VARCHAR(50),
"available_for_directory" VARCHAR(50),
"available_for_referral" VARCHAR(50),
"available_for_research" VARCHAR(50),
"date_added" TIMESTAMPTZ,
"date_last_verified" TIMESTAMPTZ,
"date_of_last_action" TIMESTAMPTZ,
"last_action_type" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."contact_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('contact_2010_id_seq'::regclass),
"agency_index_id" INT4,
"resource_info_index_id" INT4,
"site_index_id" INT4,
"title" VARCHAR(50),
"name" VARCHAR(50),
"type" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."residency_requirements_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('residency_requirements_2010_id_seq'::regclass),
"site_service_index_id" INT4,
"residency_requirements" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."service_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('service_2010_id_seq'::regclass),
"export_index_id" VARCHAR(50),
"attr_delete" INT4,
"attr_delete_occurred_date" TIMESTAMPTZ,
"attr_effective" TIMESTAMPTZ,
"airs_key" VARCHAR(50),
"airs_name" VARCHAR(50),
"coc_code" VARCHAR(50),
"configuration" VARCHAR(50),
"direct_service_code" VARCHAR(50),
"grantee_identifier" VARCHAR(50),
"individual_family_code" VARCHAR(50),
"residential_tracking_method" VARCHAR(50),
"service_type" VARCHAR(50),
"service_effective_period_start_date" TIMESTAMPTZ,
"service_effective_period_end_date" TIMESTAMPTZ,
"service_recorded_date" TIMESTAMPTZ,
"target_population_a" VARCHAR(50),
"target_population_b" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."region_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('region_2010_id_seq'::regclass),
"export_index_id" VARCHAR(50),
"region_id_id_num" VARCHAR(50),
"region_id_id_str" VARCHAR(50),
"site_service_id" VARCHAR(50),
"region_type" VARCHAR(50),
"region_type_date_collected" TIMESTAMPTZ,
"region_type_date_effective" TIMESTAMPTZ,
"region_type_data_collection_stage" INT4,
"region_description" VARCHAR(50),
"region_description_date_collected" TIMESTAMPTZ,
"region_description_date_effective" TIMESTAMPTZ,
"region_description_data_collection_stage" INT4,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."family_requirements_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('family_requirements_2010_id_seq'::regclass),
"site_service_index_id" INT4,
"family_requirements" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."geographic_area_served_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('geographic_area_served_2010_id_seq'::regclass),
"site_service_index_id" INT4,
"zipcode" VARCHAR(50),
"census_track" VARCHAR(50),
"city" VARCHAR(50),
"county" VARCHAR(50),
"state" VARCHAR(50),
"country" VARCHAR(50),
"description" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."pit_count_set_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('pit_count_set_2010_id_seq'::regclass),
"site_service_index_id" INT4,
"pit_count_set_id_id_num" VARCHAR(50),
"pit_count_set_id_id_str" VARCHAR(50),
"pit_count_set_id_delete" INT4,
"pit_count_set_id_delete_occurred_date" TIMESTAMPTZ,
"pit_count_set_id_delete_effective" TIMESTAMPTZ,
"hud_waiver_received" VARCHAR(50),
"hud_waiver_date" TIMESTAMPTZ,
"hud_waiver_effective_period_start_date" TIMESTAMPTZ,
"hud_waiver_effective_period_end_date" TIMESTAMPTZ,
"last_pit_sheltered_count_date" TIMESTAMPTZ,
"last_pit_unsheltered_count_date" TIMESTAMPTZ,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."pit_counts_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('pit_counts_2010_id_seq'::regclass),
"pit_count_set_index_id" INT4,
"pit_count_value" VARCHAR(50),
"pit_count_effective_period_start_date" TIMESTAMPTZ,
"pit_count_effective_period_end_date" TIMESTAMPTZ,
"pit_count_recorded_date" TIMESTAMPTZ,
"federal_cfda_number" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."hmis_asset_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('hmis_asset_2010_id_seq'::regclass),
"site_index_id" INT4,
"asset_id_id_num" VARCHAR(50),
"asset_id_id_str" VARCHAR(50),
"asset_id_delete" INT4,
"asset_id_delete_occurred_date" TIMESTAMPTZ,
"asset_id_delete_effective" TIMESTAMPTZ,
"asset_count" VARCHAR(50),
"asset_count_bed_availability" VARCHAR(50),
"asset_count_bed_type" VARCHAR(50),
"asset_count_bed_individual_family_type" VARCHAR(50),
"asset_count_chronic_homeless_bed" VARCHAR(50),
"asset_count_domestic_violence_shelter_bed" VARCHAR(50),
"asset_count_household_type" VARCHAR(50),
"asset_type" VARCHAR(50),
"asset_effective_period_start_date" TIMESTAMPTZ,
"asset_effective_period_end_date" TIMESTAMPTZ,
"asset_recorded_date" TIMESTAMPTZ,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."assignment_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('assignment_2010_id_seq'::regclass),
"hmis_asset_index_id" INT4,
"assignment_id_id_num" VARCHAR(50),
"assignment_id_id_str" VARCHAR(50),
"assignment_id_delete" INT4,
"assignment_id_delete_occurred_date" TIMESTAMPTZ,
"assignment_id_delete_effective" TIMESTAMPTZ,
"person_id_id_num" VARCHAR(50),
"person_id_id_str" VARCHAR(50),
"household_id_id_num" VARCHAR(50),
"household_id_id_str" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."assignment_period_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('assignment_period_2010_id_seq'::regclass),
"assignment_index_id" INT4,
"assignment_period_start_date" TIMESTAMPTZ,
"assignment_period_end_date" TIMESTAMPTZ,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."household"
(
"id" SERIAL NOT NULL DEFAULT nextval('household_id_seq'::regclass),
"export_id" VARCHAR(50),
"household_id_num" VARCHAR(32),
"household_id_num_date_collected" TIMESTAMPTZ,
"household_id_str" VARCHAR(32),
"household_id_str_date_collected" TIMESTAMPTZ,
"head_of_household_id_unhashed" VARCHAR(32),
"head_of_household_id_unhashed_date_collected" TIMESTAMPTZ,
"head_of_household_id_hashed" VARCHAR(32),
"head_of_household_id_hashed_date_collected" TIMESTAMPTZ,
"reported" BOOL,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."person"
(
"id" SERIAL NOT NULL DEFAULT nextval('person_id_seq'::regclass),
"export_id" VARCHAR(50),
"person_id_hashed" VARCHAR(32),
"person_id_unhashed" VARCHAR(50),
"person_id_date_collected" TIMESTAMPTZ,
"person_date_of_birth_hashed" VARCHAR(32),
"person_date_of_birth_unhashed" DATE,
"person_date_of_birth_date_collected" TIMESTAMPTZ,
"person_ethnicity_hashed" VARCHAR(32),
"person_ethnicity_unhashed" INT4,
"person_ethnicity_date_collected" TIMESTAMPTZ,
"person_gender_hashed" VARCHAR(32),
"person_gender_unhashed" INT4,
"person_gender_date_collected" TIMESTAMPTZ,
"person_legal_first_name_hashed" VARCHAR(32),
"person_legal_first_name_unhashed" VARCHAR(50),
"person_legal_first_name_date_collected" TIMESTAMPTZ,
"person_legal_last_name_hashed" VARCHAR(32),
"person_legal_last_name_unhashed" VARCHAR(50),
"person_legal_last_name_date_collected" TIMESTAMPTZ,
"person_legal_middle_name_hashed" VARCHAR(32),
"person_legal_middle_name_unhashed" VARCHAR(50),
"person_legal_middle_name_date_collected" TIMESTAMPTZ,
"person_legal_suffix_hashed" VARCHAR(32),
"person_legal_suffix_unhashed" VARCHAR(50),
"person_legal_suffix_date_collected" TIMESTAMPTZ,
"person_social_security_number_hashed" VARCHAR(32),
"person_social_security_number_unhashed" VARCHAR(9),
"person_social_security_number_date_collected" TIMESTAMPTZ,
"person_social_sec_number_quality_code" VARCHAR(2),
"person_social_sec_number_quality_code_date_collected" TIMESTAMPTZ,
"reported" BOOL,
"person_id_id_num_2010" VARCHAR(50),
"person_id_id_str_2010" VARCHAR(50),
"person_id_delete_2010" INT4,
"person_id_delete_occurred_date_2010" TIMESTAMPTZ,
"person_id_delete_effective_2010" TIMESTAMPTZ,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."site_service_participation"
(
"id" SERIAL NOT NULL DEFAULT nextval('site_service_participation_id_seq'::regclass),
"person_index_id" INT4,
"site_service_participation_idid_num" VARCHAR(32),
"site_service_participation_idid_num_date_collected" TIMESTAMPTZ,
"site_service_participation_idid_str" VARCHAR(32),
"site_service_participation_idid_str_date_collected" TIMESTAMPTZ,
"site_service_idid_num" VARCHAR(32),
"site_service_idid_num_date_collected" TIMESTAMPTZ,
"site_service_idid_str" VARCHAR(32),
"site_service_idid_str_date_collected" TIMESTAMPTZ,
"household_idid_num" VARCHAR(32),
"household_idid_num_date_collected" TIMESTAMPTZ,
"household_idid_str" VARCHAR(32),
"household_idid_str_date_collected" TIMESTAMPTZ,
"destination" VARCHAR(32),
"destination_date_collected" TIMESTAMPTZ,
"destination_other" VARCHAR(32),
"destination_other_date_collected" TIMESTAMPTZ,
"destination_tenure" VARCHAR(32),
"destination_tenure_date_collected" TIMESTAMPTZ,
"disabling_condition" VARCHAR(32),
"disabling_condition_date_collected" TIMESTAMPTZ,
"participation_dates_start_date" TIMESTAMPTZ,
"participation_dates_start_date_date_collected" TIMESTAMPTZ,
"participation_dates_end_date" TIMESTAMPTZ,
"participation_dates_end_date_date_collected" TIMESTAMPTZ,
"veteran_status" VARCHAR(32),
"veteran_status_date_collected" TIMESTAMPTZ,
"reported" BOOL,
"site_service_participation_id_delete_2010" INT4,
"site_service_participation_id_delete_occurred_date_2010" TIMESTAMPTZ,
"site_service_participation_id_delete_effective_2010" TIMESTAMPTZ,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."reasons_for_leaving_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('reasons_for_leaving_2010_id_seq'::regclass),
"site_service_participation_index_id" INT4,
"reason_for_leaving_id_id_num" VARCHAR(50),
"reason_for_leaving_id_id_str" VARCHAR(50),
"reason_for_leaving_id_delete" INT4,
"reason_for_leaving_id_delete_occurred_date" TIMESTAMPTZ,
"reason_for_leaving_id_delete_effective" TIMESTAMPTZ,
"reason_for_leaving" VARCHAR(50),
"reason_for_leaving_date_collected" TIMESTAMPTZ,
"reason_for_leaving_date_effective" TIMESTAMPTZ,
"reason_for_leaving_data_collection_stage" VARCHAR(50),
"reason_for_leaving_other" VARCHAR(50),
"reason_for_leaving_other_date_collected" TIMESTAMPTZ,
"reason_for_leaving_other_date_effective" TIMESTAMPTZ,
"reason_for_leaving_other_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."release_of_information"
(
"id" SERIAL NOT NULL DEFAULT nextval('release_of_information_id_seq'::regclass),
"person_index_id" INT4,
"release_of_information_idid_num" VARCHAR(32),
"release_of_information_idid_num_date_collected" TIMESTAMPTZ,
"release_of_information_idid_str" VARCHAR(32),
"release_of_information_idid_str_date_collected" TIMESTAMPTZ,
"site_service_idid_num" VARCHAR(32),
"site_service_idid_num_date_collected" TIMESTAMPTZ,
"site_service_idid_str" VARCHAR(32),
"site_service_idid_str_date_collected" TIMESTAMPTZ,
"documentation" VARCHAR(32),
"documentation_date_collected" TIMESTAMPTZ,
"start_date" VARCHAR(32),
"start_date_date_collected" TIMESTAMPTZ,
"end_date" VARCHAR(32),
"end_date_date_collected" TIMESTAMPTZ,
"release_granted" VARCHAR(32),
"release_granted_date_collected" TIMESTAMPTZ,
"reported" BOOL,
"release_of_information_id_data_collection_stage_2010" INT4,
"release_of_information_id_date_effective_2010" TIMESTAMPTZ,
"documentation_data_collection_stage_2010" INT4,
"documentation_date_effective_2010" TIMESTAMPTZ,
"release_granted_data_collection_stage_2010" INT4,
"release_granted_date_effective_2010" TIMESTAMPTZ,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."races"
(
"id" SERIAL NOT NULL DEFAULT nextval('races_id_seq'::regclass),
"person_index_id" INT4,
"race_unhashed" INT4,
"race_hashed" VARCHAR(32),
"race_date_collected" TIMESTAMPTZ,
"reported" BOOL,
"race_data_collection_stage_2010" INT4,
"race_date_effective_2010" TIMESTAMPTZ,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."person_historical"
(
"id" SERIAL NOT NULL DEFAULT nextval('person_historical_id_seq'::regclass),
"person_index_id" INT4,
"site_service_index_id" INT4,
"person_historical_idid_num" VARCHAR(32),
"person_historical_idid_num_date_collected" TIMESTAMPTZ,
"person_historical_idid_str" VARCHAR(32),
"person_historical_idid_str_date_collected" TIMESTAMPTZ,
"barrier_code" VARCHAR(32),
"barrier_code_date_collected" TIMESTAMPTZ,
"barrier_other" VARCHAR(32),
"barrier_other_date_collected" TIMESTAMPTZ,
"child_currently_enrolled_in_school" VARCHAR(32),
"child_currently_enrolled_in_school_date_collected" TIMESTAMPTZ,
"currently_employed" VARCHAR(32),
"currently_employed_date_collected" TIMESTAMPTZ,
"currently_in_school" VARCHAR(32),
"currently_in_school_date_collected" TIMESTAMPTZ,
"degree_code" VARCHAR(32),
"degree_code_date_collected" TIMESTAMPTZ,
"degree_other" VARCHAR(32),
"degree_other_date_collected" TIMESTAMPTZ,
"developmental_disability" VARCHAR(32),
"developmental_disability_date_collected" TIMESTAMPTZ,
"domestic_violence" VARCHAR(32),
"domestic_violence_date_collected" TIMESTAMPTZ,
"domestic_violence_how_long" VARCHAR(32),
"domestic_violence_how_long_date_collected" TIMESTAMPTZ,
"due_date" VARCHAR(32),
"due_date_date_collected" TIMESTAMPTZ,
"employment_tenure" VARCHAR(32),
"employment_tenure_date_collected" TIMESTAMPTZ,
"health_status" VARCHAR(32),
"health_status_date_collected" TIMESTAMPTZ,
"highest_school_level" VARCHAR(32),
"highest_school_level_date_collected" TIMESTAMPTZ,
"hivaids_status" VARCHAR(32),
"hivaids_status_date_collected" TIMESTAMPTZ,
"hours_worked_last_week" VARCHAR(32),
"hours_worked_last_week_date_collected" TIMESTAMPTZ,
"hud_chronic_homeless" VARCHAR(32),
"hud_chronic_homeless_date_collected" TIMESTAMPTZ,
"hud_homeless" VARCHAR(32),
"hud_homeless_date_collected" TIMESTAMPTZ,
"length_of_stay_at_prior_residence" VARCHAR(32),
"length_of_stay_at_prior_residence_date_collected" TIMESTAMPTZ,
"looking_for_work" VARCHAR(32),
"looking_for_work_date_collected" TIMESTAMPTZ,
"mental_health_indefinite" VARCHAR(32),
"mental_health_indefinite_date_collected" TIMESTAMPTZ,
"mental_health_problem" VARCHAR(32),
"mental_health_problem_date_collected" TIMESTAMPTZ,
"non_cash_source_code" VARCHAR(32),
"non_cash_source_code_date_collected" TIMESTAMPTZ,
"non_cash_source_other" VARCHAR(32),
"non_cash_source_other_date_collected" TIMESTAMPTZ,
"person_email" VARCHAR(32),
"person_email_date_collected" TIMESTAMPTZ,
"person_phone_number" VARCHAR(32),
"person_phone_number_date_collected" TIMESTAMPTZ,
"physical_disability" VARCHAR(32),
"physical_disability_date_collected" TIMESTAMPTZ,
"pregnancy_status" VARCHAR(32),
"pregnancy_status_date_collected" TIMESTAMPTZ,
"prior_residence" VARCHAR(32),
"prior_residence_date_collected" TIMESTAMPTZ,
"prior_residence_other" VARCHAR(32),
"prior_residence_other_date_collected" TIMESTAMPTZ,
"reason_for_leaving" VARCHAR(32),
"reason_for_leaving_date_collected" TIMESTAMPTZ,
"reason_for_leaving_other" VARCHAR(32),
"reason_for_leaving_other_date_collected" TIMESTAMPTZ,
"school_last_enrolled_date" VARCHAR(32),
"school_last_enrolled_date_date_collected" TIMESTAMPTZ,
"school_name" VARCHAR(32),
"school_name_date_collected" TIMESTAMPTZ,
"school_type" VARCHAR(32),
"school_type_date_collected" TIMESTAMPTZ,
"subsidy_other" VARCHAR(32),
"subsidy_other_date_collected" TIMESTAMPTZ,
"subsidy_type" VARCHAR(32),
"subsidy_type_date_collected" TIMESTAMPTZ,
"substance_abuse_indefinite" VARCHAR(32),
"substance_abuse_indefinite_date_collected" TIMESTAMPTZ,
"substance_abuse_problem" VARCHAR(32),
"substance_abuse_problem_date_collected" TIMESTAMPTZ,
"total_income" VARCHAR(32),
"total_income_date_collected" TIMESTAMPTZ,
"vocational_training" VARCHAR(32),
"vocational_training_date_collected" TIMESTAMPTZ,
"reported" BOOL,
"person_historical_id_delete_2010" INT4,
"person_historical_id_delete_occurred_date_2010" TIMESTAMPTZ,
"person_historical_id_delete_effective_2010" TIMESTAMPTZ,
"site_service_id_2010" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."vocational_training_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('vocational_training_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"vocational_training" VARCHAR(50),
"vocational_training_date_collected" TIMESTAMPTZ,
"vocational_training_date_effective" TIMESTAMPTZ,
"vocational_training_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."veteran_warzones_served_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('veteran_warzones_served_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"war_zone_id_id_id_num" VARCHAR(50),
"war_zone_id_id_id_str" VARCHAR(50),
"war_zone_id_id_delete" INT4,
"war_zone_id_id_delete_occurred_date" TIMESTAMPTZ,
"war_zone_id_id_delete_effective" TIMESTAMPTZ,
"months_in_war_zone" VARCHAR(50),
"months_in_war_zone_date_collected" TIMESTAMPTZ,
"months_in_war_zone_date_effective" TIMESTAMPTZ,
"months_in_war_zone_data_collection_stage" VARCHAR(50),
"received_fire" VARCHAR(50),
"received_fire_date_collected" TIMESTAMPTZ,
"received_fire_date_effective" TIMESTAMPTZ,
"received_fire_data_collection_stage" VARCHAR(50),
"war_zone" VARCHAR(50),
"war_zone_date_collected" TIMESTAMPTZ,
"war_zone_date_effective" TIMESTAMPTZ,
"war_zone_data_collection_stage" VARCHAR(50),
"war_zone_other" VARCHAR(50),
"war_zone_other_date_collected" TIMESTAMPTZ,
"war_zone_other_date_effective" TIMESTAMPTZ,
"war_zone_other_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."veteran_veteran_status_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('veteran_veteran_status_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"veteran_status" VARCHAR(50),
"veteran_status_date_collected" TIMESTAMPTZ,
"veteran_status_date_effective" TIMESTAMPTZ,
"veteran_status_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."veteran_service_era_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('veteran_service_era_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"service_era" VARCHAR(50),
"service_era_date_collected" TIMESTAMPTZ,
"service_era_date_effective" TIMESTAMPTZ,
"service_era_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."veteran_served_in_war_zone_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('veteran_served_in_war_zone_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"served_in_war_zone" VARCHAR(50),
"served_in_war_zone_date_collected" TIMESTAMPTZ,
"served_in_war_zone_date_effective" TIMESTAMPTZ,
"served_in_war_zone_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."veteran_military_service_duration_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('veteran_military_service_duration_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"military_service_duration" VARCHAR(50),
"military_service_duration_date_collected" TIMESTAMPTZ,
"military_service_duration_date_effective" TIMESTAMPTZ,
"military_service_duration_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."veteran_military_branches_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('veteran_military_branches_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"military_branch_id_id_id_num" VARCHAR(50),
"military_branch_id_id_id_str" VARCHAR(50),
"military_branch_id_id_delete" INT4,
"military_branch_id_id_delete_occurred_date" TIMESTAMPTZ,
"military_branch_id_id_delete_effective" TIMESTAMPTZ,
"discharge_status" VARCHAR(50),
"discharge_status_date_collected" TIMESTAMPTZ,
"discharge_status_date_effective" TIMESTAMPTZ,
"discharge_status_data_collection_stage" VARCHAR(50),
"discharge_status_other" VARCHAR(50),
"discharge_status_other_date_collected" TIMESTAMPTZ,
"discharge_status_other_date_effective" TIMESTAMPTZ,
"discharge_status_other_data_collection_stage" VARCHAR(50),
"military_branch" VARCHAR(50),
"military_branch_date_collected" TIMESTAMPTZ,
"military_branch_date_effective" TIMESTAMPTZ,
"military_branch_data_collection_stage" VARCHAR(50),
"military_branch_other" VARCHAR(50),
"military_branch_other_date_collected" TIMESTAMPTZ,
"military_branch_other_date_effective" TIMESTAMPTZ,
"military_branch_other_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."veteran"
(
"id" SERIAL NOT NULL DEFAULT nextval('veteran_id_seq'::regclass),
"person_historical_index_id" INT4,
"service_era" INT4,
"service_era_date_collected" TIMESTAMPTZ,
"military_service_duration" INT4,
"military_service_duration_date_collected" TIMESTAMPTZ,
"served_in_war_zone" INT4,
"served_in_war_zone_date_collected" TIMESTAMPTZ,
"war_zone" INT4,
"war_zone_date_collected" TIMESTAMPTZ,
"war_zone_other" VARCHAR(50),
"war_zone_other_date_collected" TIMESTAMPTZ,
"months_in_war_zone" INT4,
"months_in_war_zone_date_collected" TIMESTAMPTZ,
"received_fire" INT4,
"received_fire_date_collected" TIMESTAMPTZ,
"military_branch" INT4,
"military_branch_date_collected" TIMESTAMPTZ,
"military_branch_other" VARCHAR(50),
"military_branch_other_date_collected" TIMESTAMPTZ,
"discharge_status" INT4,
"discharge_status_date_collected" TIMESTAMPTZ,
"discharge_status_other" VARCHAR(50),
"discharge_status_other_date_collected" TIMESTAMPTZ,
"reported" BOOL,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."child_enrollment_status_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('child_enrollment_status_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"child_enrollment_status_id_id_num" VARCHAR(50),
"child_enrollment_status_id_id_str" VARCHAR(50),
"child_enrollment_status_id_delete" INT4,
"child_enrollment_status_id_delete_occurred_date" TIMESTAMPTZ,
"child_enrollment_status_id_delete_effective" TIMESTAMPTZ,
"child_currently_enrolled_in_school" VARCHAR(50),
"child_currently_enrolled_in_school_date_effective" TIMESTAMPTZ,
"child_currently_enrolled_in_school_date_collected" TIMESTAMPTZ,
"child_currently_enrolled_in_school_data_collection_stage" VARCHAR(50),
"child_school_name" VARCHAR(50),
"child_school_name_date_effective" TIMESTAMPTZ,
"child_school_name_date_collected" TIMESTAMPTZ,
"child_school_name_data_collection_stage" VARCHAR(50),
"child_mckinney_vento_liaison" VARCHAR(50),
"child_mckinney_vento_liaison_date_effective" TIMESTAMPTZ,
"child_mckinney_vento_liaison_date_collected" TIMESTAMPTZ,
"child_mckinney_vento_liaison_data_collection_stage" VARCHAR(50),
"child_school_type" VARCHAR(50),
"child_school_type_date_effective" TIMESTAMPTZ,
"child_school_type_date_collected" TIMESTAMPTZ,
"child_school_type_data_collection_stage" VARCHAR(50),
"child_school_last_enrolled_date" TIMESTAMPTZ,
"child_school_last_enrolled_date_date_collected" TIMESTAMPTZ,
"child_school_last_enrolled_date_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."child_enrollment_status_barrier_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('child_enrollment_status_barrier_2010_id_seq'::regclass),
"child_enrollment_status_index_id" INT4,
"barrier_id_id_num" VARCHAR(50),
"barrier_id_id_str" VARCHAR(50),
"barrier_id_delete" INT4,
"barrier_id_delete_occurred_date" TIMESTAMPTZ,
"barrier_id_delete_effective" TIMESTAMPTZ,
"barried_code" VARCHAR(50),
"barried_code_date_collected" TIMESTAMPTZ,
"barried_code_date_effective" TIMESTAMPTZ,
"barried_code_data_collection_stage" VARCHAR(50),
"barrier_other" VARCHAR(50),
"barrier_other_date_collected" TIMESTAMPTZ,
"barrier_other_date_effective" TIMESTAMPTZ,
"barrier_other_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."chronic_health_condition_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('chronic_health_condition_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"has_chronic_health_condition" VARCHAR(50),
"has_chronic_health_condition_date_collected" TIMESTAMPTZ,
"has_chronic_health_condition_date_effective" TIMESTAMPTZ,
"has_chronic_health_condition_data_collection_stage" VARCHAR(50),
"receive_chronic_health_services" VARCHAR(50),
"receive_chronic_health_services_date_collected" TIMESTAMPTZ,
"receive_chronic_health_services_date_effective" TIMESTAMPTZ,
"receive_chronic_health_services_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."substance_abuse_problem_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('substance_abuse_problem_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"has_substance_abuse_problem" VARCHAR(50),
"has_substance_abuse_problem_date_collected" TIMESTAMPTZ,
"has_substance_abuse_problem_date_effective" TIMESTAMPTZ,
"has_substance_abuse_problem_data_collection_stage" VARCHAR(50),
"substance_abuse_indefinite" VARCHAR(50),
"substance_abuse_indefinite_date_collected" TIMESTAMPTZ,
"substance_abuse_indefinite_date_effective" TIMESTAMPTZ,
"substance_abuse_indefinite_data_collection_stage" VARCHAR(50),
"receive_substance_abuse_services" VARCHAR(50),
"receive_substance_abuse_services_date_collected" TIMESTAMPTZ,
"receive_substance_abuse_services_date_effective" TIMESTAMPTZ,
"receive_substance_abuse_services_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."contact_made_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('contact_made_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"contact_id_id_num" VARCHAR(50),
"contact_id_id_str" VARCHAR(50),
"contact_id_delete" INT4,
"contact_id_delete_occurred_date" TIMESTAMPTZ,
"contact_id_delete_effective" TIMESTAMPTZ,
"contact_date" TIMESTAMPTZ,
"contact_date_data_collection_stage" VARCHAR(50),
"contact_location" VARCHAR(50),
"contact_location_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."currently_in_school_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('currently_in_school_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"currently_in_school" VARCHAR(50),
"currently_in_school_date_collected" TIMESTAMPTZ,
"currently_in_school_date_effective" TIMESTAMPTZ,
"currently_in_school_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."degree_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('degree_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"degree_id_id_num" VARCHAR(50),
"degree_id_id_str" VARCHAR(50),
"degree_id_delete" INT4,
"degree_id_delete_occurred_date" TIMESTAMPTZ,
"degree_id_delete_effective" TIMESTAMPTZ,
"degree_other" VARCHAR(50),
"degree_other_date_collected" TIMESTAMPTZ,
"degree_other_date_effective" TIMESTAMPTZ,
"degree_other_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."degree_code_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('degree_code_2010_id_seq'::regclass),
"degree_index_id" INT4,
"degree_code" VARCHAR(50),
"degree_date_collected" TIMESTAMPTZ,
"degree_date_effective" TIMESTAMPTZ,
"degree_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."destinations_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('destinations_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"destination_id_id_num" VARCHAR(50),
"destination_id_id_str" VARCHAR(50),
"destination_id_delete" INT4,
"destination_id_delete_occurred_date" TIMESTAMPTZ,
"destination_id_delete_effective" TIMESTAMPTZ,
"destination_code" VARCHAR(50),
"destination_code_date_collected" TIMESTAMPTZ,
"destination_code_date_effective" TIMESTAMPTZ,
"destination_code_data_collection_stage" VARCHAR(50),
"destination_other" VARCHAR(50),
"destination_other_date_collected" TIMESTAMPTZ,
"destination_other_date_effective" TIMESTAMPTZ,
"destination_other_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."developmental_disability_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('developmental_disability_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"has_developmental_disability" VARCHAR(50),
"has_developmental_disability_date_collected" TIMESTAMPTZ,
"has_developmental_disability_date_effective" TIMESTAMPTZ,
"has_developmental_disability_data_collection_stage" VARCHAR(50),
"receive_developmental_disability" VARCHAR(50),
"receive_developmental_disability_date_collected" TIMESTAMPTZ,
"receive_developmental_disability_date_effective" TIMESTAMPTZ,
"receive_developmental_disability_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."disabling_condition_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('disabling_condition_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"disabling_condition" VARCHAR(50),
"disabling_condition_date_collected" TIMESTAMPTZ,
"disabling_condition_date_effective" TIMESTAMPTZ,
"disabling_condition_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."domestic_violence_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('domestic_violence_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"domestic_violence_survivor" VARCHAR(50),
"domestic_violence_survivor_date_collected" TIMESTAMPTZ,
"domestic_violence_survivor_date_effective" TIMESTAMPTZ,
"domestic_violence_survivor_data_collection_stage" VARCHAR(50),
"dvo_occurred" VARCHAR(50),
"dvo_occurred_date_collected" TIMESTAMPTZ,
"dvo_occurred_date_effective" TIMESTAMPTZ,
"dvo_occurred_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."drug_history"
(
"id" SERIAL NOT NULL DEFAULT nextval('drug_history_id_seq'::regclass),
"person_historical_index_id" INT4,
"drug_history_id" VARCHAR(32),
"drug_history_id_date_collected" TIMESTAMPTZ,
"drug_code" INT4,
"drug_code_date_collected" TIMESTAMPTZ,
"drug_use_frequency" INT4,
"drug_use_frequency_date_collected" TIMESTAMPTZ,
"reported" BOOL,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."email_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('email_2010_id_seq'::regclass),
"agency_index_id" INT4,
"contact_index_id" INT4,
"resource_info_index_id" INT4,
"site_index_id" INT4,
"person_historical_index_id" INT4,
"address" VARCHAR(50),
"note" VARCHAR(50),
"person_email" VARCHAR(50),
"person_email_date_collected" TIMESTAMPTZ,
"person_email_date_effective" TIMESTAMPTZ,
"person_email_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."emergency_contact"
(
"id" SERIAL NOT NULL DEFAULT nextval('emergency_contact_id_seq'::regclass),
"person_historical_index_id" INT4,
"emergency_contact_id" VARCHAR(32),
"emergency_contact_id_date_collected" TIMESTAMPTZ,
"emergency_contact_name" VARCHAR(32),
"emergency_contact_name_date_collected" TIMESTAMPTZ,
"emergency_contact_phone_number_0" VARCHAR(32),
"emergency_contact_phone_number_date_collected_0" TIMESTAMPTZ,
"emergency_contact_phone_number_type_0" VARCHAR(32),
"emergency_contact_phone_number_1" VARCHAR(32),
"emergency_contact_phone_number_date_collected_1" TIMESTAMPTZ,
"emergency_contact_phone_number_type_1" VARCHAR(32),
"emergency_contact_address_date_collected" TIMESTAMPTZ,
"emergency_contact_address_start_date" TIMESTAMPTZ,
"emergency_contact_address_start_date_date_collected" TIMESTAMPTZ,
"emergency_contact_address_end_date" TIMESTAMPTZ,
"emergency_contact_address_end_date_date_collected" TIMESTAMPTZ,
"emergency_contact_address_line1" VARCHAR(32),
"emergency_contact_address_line1_date_collected" TIMESTAMPTZ,
"emergency_contact_address_line2" VARCHAR(32),
"emergency_contact_address_line2_date_collected" TIMESTAMPTZ,
"emergency_contact_address_city" VARCHAR(32),
"emergency_contact_address_city_date_collected" TIMESTAMPTZ,
"emergency_contact_address_state" VARCHAR(32),
"emergency_contact_address_state_date_collected" TIMESTAMPTZ,
"emergency_contact_relation_to_client" VARCHAR(32),
"emergency_contact_relation_to_client_date_collected" TIMESTAMPTZ,
"reported" BOOL,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."employment_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('employment_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"employment_id_id_id_num" VARCHAR(50),
"employment_id_id_id_str" VARCHAR(50),
"employment_id_id_delete" INT4,
"employment_id_id_delete_occurred_date" TIMESTAMPTZ,
"employment_id_id_delete_effective" TIMESTAMPTZ,
"currently_employed" VARCHAR(50),
"currently_employed_date_collected" TIMESTAMPTZ,
"currently_employed_date_effective" TIMESTAMPTZ,
"currently_employed_data_collection_stage" VARCHAR(50),
"hours_worked_last_week" VARCHAR(50),
"hours_worked_last_week_date_collected" TIMESTAMPTZ,
"hours_worked_last_week_date_effective" TIMESTAMPTZ,
"hours_worked_last_week_data_collection_stage" VARCHAR(50),
"employment_tenure" VARCHAR(50),
"employment_tenure_date_collected" TIMESTAMPTZ,
"employment_tenure_date_effective" TIMESTAMPTZ,
"employment_tenure_data_collection_stage" VARCHAR(50),
"looking_for_work" VARCHAR(50),
"looking_for_work_date_collected" TIMESTAMPTZ,
"looking_for_work_date_effective" TIMESTAMPTZ,
"looking_for_work_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."engaged_date_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('engaged_date_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"engaged_date" TIMESTAMPTZ,
"engaged_date_date_collected" TIMESTAMPTZ,
"engaged_date_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."prior_residence_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('prior_residence_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"prior_residence_id_id_id_num" VARCHAR(50),
"prior_residence_id_id_id_str" VARCHAR(50),
"prior_residence_id_id_delete" INT4,
"prior_residence_id_id_delete_occurred_date" TIMESTAMPTZ,
"prior_residence_id_id_delete_effective" TIMESTAMPTZ,
"prior_residence_code" VARCHAR(50),
"prior_residence_code_date_collected" TIMESTAMPTZ,
"prior_residence_code_date_effective" TIMESTAMPTZ,
"prior_residence_code_data_collection_stage" VARCHAR(50),
"prior_residence_other" VARCHAR(50),
"prior_residence_other_date_collected" TIMESTAMPTZ,
"prior_residence_other_date_effective" TIMESTAMPTZ,
"prior_residence_other_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."pregnancy_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('pregnancy_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"pregnancy_id_id_id_num" VARCHAR(50),
"pregnancy_id_id_id_str" VARCHAR(50),
"pregnancy_id_id_delete" INT4,
"pregnancy_id_id_delete_occurred_date" TIMESTAMPTZ,
"pregnancy_id_id_delete_effective" TIMESTAMPTZ,
"pregnancy_status" VARCHAR(50),
"pregnancy_status_date_collected" TIMESTAMPTZ,
"pregnancy_status_date_effective" TIMESTAMPTZ,
"pregnancy_status_data_collection_stage" VARCHAR(50),
"due_date" TIMESTAMPTZ,
"due_date_date_collected" TIMESTAMPTZ,
"due_date_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."health_status_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('health_status_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"health_status" VARCHAR(50),
"health_status_date_collected" TIMESTAMPTZ,
"health_status_date_effective" TIMESTAMPTZ,
"health_status_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."highest_school_level_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('highest_school_level_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"highest_school_level" VARCHAR(50),
"highest_school_level_date_collected" TIMESTAMPTZ,
"highest_school_level_date_effective" TIMESTAMPTZ,
"highest_school_level_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."physical_disability_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('physical_disability_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"has_physical_disability" VARCHAR(50),
"has_physical_disability_date_collected" TIMESTAMPTZ,
"has_physical_disability_date_effective" TIMESTAMPTZ,
"has_physical_disability_data_collection_stage" VARCHAR(50),
"receive_physical_disability_services" VARCHAR(50),
"receive_physical_disability_services_date_collected" TIMESTAMPTZ,
"receive_physical_disability_services_date_effective" TIMESTAMPTZ,
"receive_physical_disability_services_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."hiv_aids_status_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('hiv_aids_status_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"has_hiv_aids" VARCHAR(50),
"has_hiv_aids_date_collected" TIMESTAMPTZ,
"has_hiv_aids_date_effective" TIMESTAMPTZ,
"has_hiv_aids_data_collection_stage" VARCHAR(50),
"receive_hiv_aids_services" VARCHAR(50),
"receive_hiv_aids_services_date_collected" TIMESTAMPTZ,
"receive_hiv_aids_services_date_effective" TIMESTAMPTZ,
"receive_hiv_aids_services_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."phone_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('phone_2010_id_seq'::regclass),
"agency_index_id" INT4,
"contact_index_id" INT4,
"resource_info_index_id" INT4,
"site_index_id" INT4,
"site_service_index_id" INT4,
"person_historical_index_id" INT4,
"phone_number" VARCHAR(50),
"reason_withheld" VARCHAR(50),
"extension" VARCHAR(50),
"description" VARCHAR(50),
"type" VARCHAR(50),
"function" VARCHAR(50),
"toll_free" VARCHAR(50),
"confidential" VARCHAR(50),
"person_phone_number" VARCHAR(50),
"person_phone_number_date_collected" TIMESTAMPTZ,
"person_phone_number_date_effective" TIMESTAMPTZ,
"person_phone_number_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."person_address"
(
"id" SERIAL NOT NULL DEFAULT nextval('person_address_id_seq'::regclass),
"person_historical_index_id" INT4,
"address_period_start_date" TIMESTAMPTZ,
"address_period_start_date_date_collected" TIMESTAMPTZ,
"address_period_end_date" TIMESTAMPTZ,
"address_period_end_date_date_collected" TIMESTAMPTZ,
"pre_address_line" VARCHAR(32),
"pre_address_line_date_collected" TIMESTAMPTZ,
"line1" VARCHAR(32),
"line1_date_collected" TIMESTAMPTZ,
"line2" VARCHAR(32),
"line2_date_collected" TIMESTAMPTZ,
"city" VARCHAR(32),
"city_date_collected" TIMESTAMPTZ,
"county" VARCHAR(32),
"county_date_collected" TIMESTAMPTZ,
"state" VARCHAR(32),
"state_date_collected" TIMESTAMPTZ,
"zipcode" VARCHAR(10),
"zipcode_date_collected" TIMESTAMPTZ,
"country" VARCHAR(32),
"country_date_collected" TIMESTAMPTZ,
"is_last_permanent_zip" INT4,
"is_last_permanent_zip_date_collected" TIMESTAMPTZ,
"zip_quality_code" INT4,
"zip_quality_code_date_collected" TIMESTAMPTZ,
"reported" BOOL,
"attr_delete_2010" INT4,
"attr_delete_occurred_date_2010" TIMESTAMPTZ,
"attr_effective_2010" TIMESTAMPTZ,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."housing_status_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('housing_status_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"housing_status" VARCHAR(50),
"housing_status_date_collected" TIMESTAMPTZ,
"housing_status_date_effective" TIMESTAMPTZ,
"housing_status_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."hud_chronic_homeless_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('hud_chronic_homeless_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"hud_chronic_homeless" VARCHAR(50),
"hud_chronic_homeless_date_collected" TIMESTAMPTZ,
"hud_chronic_homeless_date_effective" TIMESTAMPTZ,
"hud_chronic_homeless_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."other_requirements_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('other_requirements_2010_id_seq'::regclass),
"site_service_index_id" INT4,
"other_requirements" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."hud_homeless_episodes"
(
"id" SERIAL NOT NULL DEFAULT nextval('hud_homeless_episodes_id_seq'::regclass),
"person_historical_index_id" INT4,
"start_date" VARCHAR(32),
"start_date_date_collected" TIMESTAMPTZ,
"end_date" VARCHAR(32),
"end_date_date_collected" TIMESTAMPTZ,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."other_names"
(
"id" SERIAL NOT NULL DEFAULT nextval('other_names_id_seq'::regclass),
"person_index_id" INT4,
"other_first_name_unhashed" VARCHAR(50),
"other_first_name_hashed" VARCHAR(32),
"other_first_name_date_collected" TIMESTAMPTZ,
"other_middle_name_unhashed" VARCHAR(50),
"other_middle_name_hashed" VARCHAR(32),
"other_middle_name_date_collected" TIMESTAMPTZ,
"other_last_name_unhashed" VARCHAR(50),
"other_last_name_hashed" VARCHAR(32),
"other_last_name_date_collected" TIMESTAMPTZ,
"other_suffix_unhashed" VARCHAR(50),
"other_suffix_hashed" VARCHAR(32),
"other_suffix_date_collected" TIMESTAMPTZ,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."income_and_sources"
(
"id" SERIAL NOT NULL DEFAULT nextval('income_and_sources_id_seq'::regclass),
"person_historical_index_id" INT4,
"amount" INT4,
"amount_date_collected" TIMESTAMPTZ,
"income_source_code" INT4,
"income_source_code_date_collected" TIMESTAMPTZ,
"income_source_other" VARCHAR(32),
"income_source_other_date_collected" TIMESTAMPTZ,
"income_and_source_id_id_id_num_2010" VARCHAR(32),
"income_and_source_id_id_id_str_2010" VARCHAR(32),
"income_and_source_id_id_delete_occurred_date_2010" TIMESTAMPTZ,
"income_and_source_id_id_delete_effective_2010" TIMESTAMPTZ,
"income_source_code_date_effective_2010" TIMESTAMPTZ,
"income_source_other_date_effective_2010" TIMESTAMPTZ,
"receiving_income_source_date_collected_2010" TIMESTAMPTZ,
"receiving_income_source_date_effective_2010" TIMESTAMPTZ,
"income_source_amount_date_effective_2010" TIMESTAMPTZ,
"income_and_source_id_id_delete_2010" INT4,
"income_source_code_data_collection_stage_2010" INT4,
"income_source_other_data_collection_stage_2010" INT4,
"receiving_income_source_2010" INT4,
"receiving_income_source_data_collection_stage_2010" INT4,
"income_source_amount_data_collection_stage_2010" INT4,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."other_address_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('other_address_2010_id_seq'::regclass),
"site_index_id" INT4,
"pre_address_line" VARCHAR(50),
"line_1" VARCHAR(50),
"line_2" VARCHAR(50),
"city" VARCHAR(50),
"county" VARCHAR(50),
"state" VARCHAR(50),
"zip_code" VARCHAR(50),
"country" VARCHAR(50),
"reason_withheld" VARCHAR(50),
"confidential" VARCHAR(50),
"description" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."income_last_30_days_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('income_last_30_days_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"income_last_30_days" VARCHAR(50),
"income_last_30_days_date_collected" TIMESTAMPTZ,
"income_last_30_days_date_effective" TIMESTAMPTZ,
"income_last_30_days_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."income_requirements_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('income_requirements_2010_id_seq'::regclass),
"site_service_index_id" INT4,
"income_requirements" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."non_cash_benefits_last_30_days_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('non_cash_benefits_last_30_days_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"income_last_30_days" VARCHAR(50),
"income_last_30_days_date_collected" TIMESTAMPTZ,
"income_last_30_days_date_effective" TIMESTAMPTZ,
"income_last_30_days_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."income_total_monthly_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('income_total_monthly_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"income_total_monthly" VARCHAR(50),
"income_total_monthly_date_collected" TIMESTAMPTZ,
"income_total_monthly_date_effective" TIMESTAMPTZ,
"income_total_monthly_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."non_cash_benefits_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('non_cash_benefits_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"non_cash_benefit_id_id_id_num" VARCHAR(50),
"non_cash_benefit_id_id_id_str" VARCHAR(50),
"non_cash_benefit_id_id_delete" INT4,
"non_cash_benefit_id_id_delete_occurred_date" TIMESTAMPTZ,
"non_cash_benefit_id_id_delete_effective" TIMESTAMPTZ,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."non_cash_benefits_sub_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('non_cash_benefits_sub_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"non_cash_benefits_index_id" INT4,
"non_cash_source_code" VARCHAR(50),
"non_cash_source_code_date_collected" TIMESTAMPTZ,
"non_cash_source_code_date_effective" TIMESTAMPTZ,
"non_cash_source_code_data_collection_stage" VARCHAR(50),
"non_cash_source_other" VARCHAR(50),
"non_cash_source_other_date_collected" TIMESTAMPTZ,
"non_cash_source_other_date_effective" TIMESTAMPTZ,
"non_cash_source_other_data_collection_stage" VARCHAR(50),
"receiving_non_cash_source" VARCHAR(50),
"receiving_non_cash_source_date_collected" TIMESTAMPTZ,
"receiving_non_cash_source_date_effective" TIMESTAMPTZ,
"receiving_non_cash_source_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."inventory_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('inventory_2010_id_seq'::regclass),
"service_index_id" INT4,
"site_service_index_id" INT4,
"attr_delete" INT4,
"attr_delete_occurred_date" TIMESTAMPTZ,
"attr_effective" TIMESTAMPTZ,
"hmis_participation_period_start_date" TIMESTAMPTZ,
"hmis_participation_period_end_date" TIMESTAMPTZ,
"inventory_id_id_num" VARCHAR(50),
"inventory_id_id_str" VARCHAR(50),
"bed_availability" VARCHAR(50),
"bed_type" VARCHAR(50),
"bed_individual_family_type" VARCHAR(50),
"chronic_homeless_bed" VARCHAR(50),
"domestic_violence_shelter_bed" VARCHAR(50),
"household_type" VARCHAR(50),
"hmis_participating_beds" VARCHAR(50),
"inventory_effective_period_start_date" TIMESTAMPTZ,
"inventory_effective_period_end_date" TIMESTAMPTZ,
"inventory_recorded_date" TIMESTAMPTZ,
"unit_inventory" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."need"
(
"id" SERIAL NOT NULL DEFAULT nextval('need_id_seq'::regclass),
"site_service_index_id" INT4,
"need_idid_num" VARCHAR(32),
"need_idid_num_date_collected" TIMESTAMPTZ,
"need_idid_str" VARCHAR(32),
"need_idid_str_date_collected" TIMESTAMPTZ,
"site_service_idid_num" VARCHAR(32),
"site_service_idid_num_date_collected" TIMESTAMPTZ,
"site_service_idid_str" VARCHAR(32),
"site_service_idid_str_date_collected" TIMESTAMPTZ,
"service_event_idid_num" VARCHAR(32),
"service_event_idid_num_date_collected" TIMESTAMPTZ,
"service_event_idid_str" VARCHAR(32),
"service_event_idid_str_date_collected" TIMESTAMPTZ,
"need_status" VARCHAR(32),
"need_status_date_collected" TIMESTAMPTZ,
"taxonomy" VARCHAR(32),
"reported" BOOL,
"person_index_id_2010" INT4,
"need_id_delete_2010" INT4,
"need_id_delete_occurred_date_2010" TIMESTAMPTZ,
"need_id_delete_delete_effective_2010" TIMESTAMPTZ,
"need_effective_period_start_date_2010" TIMESTAMPTZ,
"need_effective_period_end_date_2010" TIMESTAMPTZ,
"need_recorded_date_2010" TIMESTAMPTZ,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."taxonomy_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('taxonomy_2010_id_seq'::regclass),
"site_service_index_id" INT4,
"need_index_id" INT4,
"code" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."service_event"
(
"id" SERIAL NOT NULL DEFAULT nextval('service_event_id_seq'::regclass),
"site_service_index_id" INT4,
"service_event_idid_num" VARCHAR(32),
"service_event_idid_num_date_collected" TIMESTAMPTZ,
"service_event_idid_str" VARCHAR(32),
"service_event_idid_str_date_collected" TIMESTAMPTZ,
"household_idid_num" VARCHAR(32),
"household_idid_num_date_collected" TIMESTAMPTZ,
"household_idid_str" VARCHAR(32),
"household_idid_str_date_collected" TIMESTAMPTZ,
"is_referral" VARCHAR(32),
"is_referral_date_collected" TIMESTAMPTZ,
"quantity_of_service" VARCHAR(32),
"quantity_of_service_date_collected" TIMESTAMPTZ,
"quantity_of_service_measure" VARCHAR(32),
"quantity_of_service_measure_date_collected" TIMESTAMPTZ,
"service_airs_code" VARCHAR(32),
"service_airs_code_date_collected" TIMESTAMPTZ,
"service_period_start_date" TIMESTAMPTZ,
"service_period_start_date_date_collected" TIMESTAMPTZ,
"service_period_end_date" TIMESTAMPTZ,
"service_period_end_date_date_collected" TIMESTAMPTZ,
"service_unit" VARCHAR(32),
"service_unit_date_collected" TIMESTAMPTZ,
"type_of_service" VARCHAR(32),
"type_of_service_date_collected" TIMESTAMPTZ,
"type_of_service_other" VARCHAR(32),
"type_of_service_other_date_collected" TIMESTAMPTZ,
"type_of_service_par" INT4,
"reported" BOOL,
"person_index_id_2010" INT4,
"need_index_id_2010" INT4,
"service_event_id_delete_2010" INT4,
"service_event_ind_fam_2010" INT4,
"site_service_id_2010" VARCHAR(50),
"hmis_service_event_code_type_of_service_2010" VARCHAR(50),
"hmis_service_event_code_type_of_service_other_2010" VARCHAR(50),
"hprp_financial_assistance_service_event_code_2010" VARCHAR(50),
"hprp_relocation_stabilization_service_event_code_2010" VARCHAR(50),
"service_event_id_delete_occurred_date_2010" TIMESTAMPTZ,
"service_event_id_delete_effective_2010" TIMESTAMPTZ,
"service_event_provision_date_2010" TIMESTAMPTZ,
"service_event_recorded_date_2010" TIMESTAMPTZ,
PRIMARY KEY ("id")
);

CREATE TABLE "public"."service_event_notes_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('service_event_notes_2010_id_seq'::regclass),
"service_event_index_id" INT4,
"note_id_id_num" VARCHAR(50),
"note_id_id_str" VARCHAR(50),
"note_delete" INT4,
"note_delete_occurred_date" TIMESTAMPTZ,
"note_delete_effective" TIMESTAMPTZ,
"note_text" VARCHAR(50),
"note_text_date_collected" TIMESTAMPTZ,
"note_text_date_effective" TIMESTAMPTZ,
"note_text_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."funding_source_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('funding_source_2010_id_seq'::regclass),
"service_index_id" INT4,
"service_event_index_id" INT4,
"funding_source_id_id_num" VARCHAR(50),
"funding_source_id_id_str" VARCHAR(50),
"funding_source_id_delete" VARCHAR(50),
"funding_source_id_delete_occurred_date" TIMESTAMPTZ,
"funding_source_id_delete_effective" TIMESTAMPTZ,
"federal_cfda_number" VARCHAR(50),
"receives_mckinney_funding" VARCHAR(50),
"advance_or_arrears" VARCHAR(50),
"financial_assistance_amount" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."languages_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('languages_2010_id_seq'::regclass),
"site_index_id" INT4,
"site_service_index_id" INT4,
"name" VARCHAR(50),
"notes" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."time_open_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('time_open_2010_id_seq'::regclass),
"site_index_id" INT4,
"languages_index_id" INT4,
"site_service_index_id" INT4,
"day_of_week" VARCHAR(50),
"from" VARCHAR(50),
"to" VARCHAR(50),
"notes" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."migrate_version"
(
"repository_id" VARCHAR(255) NOT NULL,
"repository_path" TEXT,
"version" INT4,
PRIMARY KEY ("repository_id")
);

CREATE TABLE "public"."length_of_stay_at_prior_residence_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('length_of_stay_at_prior_residence_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"length_of_stay_at_prior_residence" VARCHAR(50),
"length_of_stay_at_prior_residence_date_collected" TIMESTAMPTZ,
"length_of_stay_at_prior_residence_date_effective" TIMESTAMPTZ,
"length_of_stay_at_prior_residence_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."mental_health_problem_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('mental_health_problem_2010_id_seq'::regclass),
"person_historical_index_id" INT4,
"has_mental_health_problem" VARCHAR(50),
"has_mental_health_problem_date_collected" TIMESTAMPTZ,
"has_mental_health_problem_date_effective" TIMESTAMPTZ,
"has_mental_health_problem_data_collection_stage" VARCHAR(50),
"mental_health_indefinite" VARCHAR(50),
"mental_health_indefinite_date_collected" TIMESTAMPTZ,
"mental_health_indefinite_date_effective" TIMESTAMPTZ,
"mental_health_indefinite_data_collection_stage" VARCHAR(50),
"receive_mental_health_services" VARCHAR(50),
"receive_mental_health_services_date_collected" TIMESTAMPTZ,
"receive_mental_health_services_date_effective" TIMESTAMPTZ,
"receive_mental_health_services_data_collection_stage" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."license_accreditation_2010"
(
"id" SERIAL NOT NULL DEFAULT nextval('license_accreditation_2010_id_seq'::regclass),
"agency_index_id" INT4,
"license" VARCHAR(50),
"licensed_by" VARCHAR(50),
PRIMARY KEY ("id")
);

CREATE TABLE "public"."members"
(
"id" SERIAL NOT NULL DEFAULT nextval('members_id_seq'::regclass),
"household_index_id" INT4,
"person_id_unhashed" VARCHAR(32),
"person_id_unhashed_date_collected" TIMESTAMPTZ,
"person_id_hashed" VARCHAR(32),
"person_id_hashed_date_collected" TIMESTAMPTZ,
"relationship_to_head_of_household" VARCHAR(32),
"relationship_to_head_of_household_date_collected" TIMESTAMPTZ,
"reported" BOOL,
PRIMARY KEY ("id")
);

CREATE INDEX "dedup_link_pkey" ON "public"."dedup_link" ("source_rec_id");

CREATE INDEX "sender_system_configuration_pkey" ON "public"."sender_system_configuration" ("id");

CREATE INDEX "export_pkey" ON "public"."export" ("export_id");

ALTER TABLE "public"."agency_2010" ADD FOREIGN KEY ("export_index_id") REFERENCES "public"."export" ("export_id");

CREATE INDEX "agency_2010_pkey" ON "public"."agency_2010" ("id");

ALTER TABLE "public"."agency_service_2010" ADD FOREIGN KEY ("agency_index_id") REFERENCES "public"."agency_2010" ("id");

CREATE INDEX "agency_service_2010_pkey" ON "public"."agency_service_2010" ("id");

ALTER TABLE "public"."service_group_2010" ADD FOREIGN KEY ("agency_index_id") REFERENCES "public"."agency_2010" ("id");

ALTER TABLE "public"."agency_child_2010" ADD FOREIGN KEY ("export_index_id") REFERENCES "public"."export" ("export_id");

ALTER TABLE "public"."agency_child_2010" ADD FOREIGN KEY ("agency_index_id") REFERENCES "public"."agency_2010" ("id");

CREATE INDEX "agency_child_2010_pkey" ON "public"."agency_child_2010" ("id");

ALTER TABLE "public"."source" ADD FOREIGN KEY ("export_id") REFERENCES "public"."export" ("export_id");

CREATE INDEX "source_pkey" ON "public"."source" ("id");

ALTER TABLE "public"."source_export_link_2010" ADD FOREIGN KEY ("source_index_id") REFERENCES "public"."source" ("id");

ALTER TABLE "public"."source_export_link_2010" ADD FOREIGN KEY ("export_index_id") REFERENCES "public"."export" ("export_id");

CREATE INDEX "source_export_link_2010_pkey" ON "public"."source_export_link_2010" ("id");

ALTER TABLE "public"."site_2010" ADD FOREIGN KEY ("export_index_id") REFERENCES "public"."export" ("export_id");

ALTER TABLE "public"."site_2010" ADD FOREIGN KEY ("agency_index_id") REFERENCES "public"."agency_2010" ("id");

CREATE INDEX "site_2010_pkey" ON "public"."site_2010" ("id");

ALTER TABLE "public"."aka_2010" ADD FOREIGN KEY ("agency_index_id") REFERENCES "public"."agency_2010" ("id");

ALTER TABLE "public"."aka_2010" ADD FOREIGN KEY ("site_index_id") REFERENCES "public"."site_2010" ("id");

CREATE INDEX "aka_2010_pkey" ON "public"."aka_2010" ("id");

ALTER TABLE "public"."url" ADD FOREIGN KEY ("agency_index_id") REFERENCES "public"."agency_2010" ("id");

ALTER TABLE "public"."url" ADD FOREIGN KEY ("site_index_id") REFERENCES "public"."site_2010" ("id");

CREATE INDEX "url_pkey" ON "public"."url" ("id");

ALTER TABLE "public"."spatial_location_2010" ADD FOREIGN KEY ("site_index_id") REFERENCES "public"."site_2010" ("id");

CREATE INDEX "spatial_location_2010_pkey" ON "public"."spatial_location_2010" ("id");

ALTER TABLE "public"."cross_street_2010" ADD FOREIGN KEY ("site_index_id") REFERENCES "public"."site_2010" ("id");

CREATE INDEX "cross_street_2010_pkey" ON "public"."cross_street_2010" ("id");

ALTER TABLE "public"."site_service_2010" ADD FOREIGN KEY ("export_index_id") REFERENCES "public"."export" ("export_id");

ALTER TABLE "public"."site_service_2010" ADD FOREIGN KEY ("site_index_id") REFERENCES "public"."site_2010" ("id");

CREATE INDEX "site_service_2010_pkey" ON "public"."site_service_2010" ("id");

ALTER TABLE "public"."age_requirements" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "age_requirements_pkey" ON "public"."age_requirements" ("id");

ALTER TABLE "public"."aid_requirements" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "aid_requirements_pkey" ON "public"."aid_requirements" ("id");

ALTER TABLE "public"."application_process_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "application_process_2010_pkey" ON "public"."application_process_2010" ("id");

ALTER TABLE "public"."documents_required_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "documents_required_2010_pkey" ON "public"."documents_required_2010" ("id");

ALTER TABLE "public"."seasonal_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "seasonal_2010_pkey" ON "public"."seasonal_2010" ("id");

ALTER TABLE "public"."resource_info_2010" ADD FOREIGN KEY ("agency_index_id") REFERENCES "public"."agency_2010" ("id");

ALTER TABLE "public"."resource_info_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "resource_info_2010_pkey" ON "public"."resource_info_2010" ("id");

ALTER TABLE "public"."contact_2010" ADD FOREIGN KEY ("agency_index_id") REFERENCES "public"."agency_2010" ("id");

ALTER TABLE "public"."contact_2010" ADD FOREIGN KEY ("resource_info_index_id") REFERENCES "public"."resource_info_2010" ("id");

ALTER TABLE "public"."contact_2010" ADD FOREIGN KEY ("site_index_id") REFERENCES "public"."site_2010" ("id");

CREATE INDEX "contact_2010_pkey" ON "public"."contact_2010" ("id");

ALTER TABLE "public"."residency_requirements_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "residency_requirements_2010_pkey" ON "public"."residency_requirements_2010" ("id");

ALTER TABLE "public"."service_2010" ADD FOREIGN KEY ("export_index_id") REFERENCES "public"."export" ("export_id");

CREATE INDEX "service_2010_pkey" ON "public"."service_2010" ("id");

ALTER TABLE "public"."region_2010" ADD FOREIGN KEY ("export_index_id") REFERENCES "public"."export" ("export_id");

CREATE INDEX "region_2010_pkey" ON "public"."region_2010" ("id");

ALTER TABLE "public"."family_requirements_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "family_requirements_2010_pkey" ON "public"."family_requirements_2010" ("id");

ALTER TABLE "public"."geographic_area_served_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "geographic_area_served_2010_pkey" ON "public"."geographic_area_served_2010" ("id");

ALTER TABLE "public"."pit_count_set_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "pit_count_set_2010_pkey" ON "public"."pit_count_set_2010" ("id");

ALTER TABLE "public"."pit_counts_2010" ADD FOREIGN KEY ("pit_count_set_index_id") REFERENCES "public"."pit_count_set_2010" ("id");

CREATE INDEX "pit_counts_2010_pkey" ON "public"."pit_counts_2010" ("id");

ALTER TABLE "public"."hmis_asset_2010" ADD FOREIGN KEY ("site_index_id") REFERENCES "public"."site_2010" ("id");

CREATE INDEX "hmis_asset_2010_pkey" ON "public"."hmis_asset_2010" ("id");

ALTER TABLE "public"."assignment_2010" ADD FOREIGN KEY ("hmis_asset_index_id") REFERENCES "public"."hmis_asset_2010" ("id");

CREATE INDEX "assignment_2010_pkey" ON "public"."assignment_2010" ("id");

ALTER TABLE "public"."assignment_period_2010" ADD FOREIGN KEY ("assignment_index_id") REFERENCES "public"."assignment_2010" ("id");

CREATE INDEX "assignment_period_2010_pkey" ON "public"."assignment_period_2010" ("id");

ALTER TABLE "public"."household" ADD FOREIGN KEY ("export_id") REFERENCES "public"."export" ("export_id");

CREATE INDEX "household_pkey" ON "public"."household" ("id");

ALTER TABLE "public"."person" ADD FOREIGN KEY ("export_id") REFERENCES "public"."export" ("export_id");

CREATE INDEX "person_pkey" ON "public"."person" ("id");

ALTER TABLE "public"."site_service_participation" ADD FOREIGN KEY ("person_index_id") REFERENCES "public"."person" ("id");

CREATE INDEX "site_service_participation_pkey" ON "public"."site_service_participation" ("id");

ALTER TABLE "public"."reasons_for_leaving_2010" ADD FOREIGN KEY ("site_service_participation_index_id") REFERENCES "public"."site_service_participation" ("id");

CREATE INDEX "reasons_for_leaving_2010_pkey" ON "public"."reasons_for_leaving_2010" ("id");

ALTER TABLE "public"."release_of_information" ADD FOREIGN KEY ("person_index_id") REFERENCES "public"."person" ("id");

CREATE INDEX "release_of_information_pkey" ON "public"."release_of_information" ("id");

ALTER TABLE "public"."races" ADD FOREIGN KEY ("person_index_id") REFERENCES "public"."person" ("id");

CREATE INDEX "races_pkey" ON "public"."races" ("id");

ALTER TABLE "public"."person_historical" ADD FOREIGN KEY ("person_index_id") REFERENCES "public"."person" ("id");

ALTER TABLE "public"."person_historical" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_participation" ("id");

CREATE INDEX "person_historical_pkey" ON "public"."person_historical" ("id");

ALTER TABLE "public"."vocational_training_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "vocational_training_2010_pkey" ON "public"."vocational_training_2010" ("id");

ALTER TABLE "public"."veteran_warzones_served_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "veteran_warzones_served_2010_pkey" ON "public"."veteran_warzones_served_2010" ("id");

ALTER TABLE "public"."veteran_veteran_status_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "veteran_veteran_status_2010_pkey" ON "public"."veteran_veteran_status_2010" ("id");

ALTER TABLE "public"."veteran_service_era_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "veteran_service_era_2010_pkey" ON "public"."veteran_service_era_2010" ("id");

ALTER TABLE "public"."veteran_served_in_war_zone_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "veteran_served_in_war_zone_2010_pkey" ON "public"."veteran_served_in_war_zone_2010" ("id");

ALTER TABLE "public"."veteran_military_service_duration_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "veteran_military_service_duration_2010_pkey" ON "public"."veteran_military_service_duration_2010" ("id");

ALTER TABLE "public"."veteran_military_branches_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "veteran_military_branches_2010_pkey" ON "public"."veteran_military_branches_2010" ("id");

ALTER TABLE "public"."veteran" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "veteran_pkey" ON "public"."veteran" ("id");

ALTER TABLE "public"."child_enrollment_status_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "child_enrollment_status_2010_pkey" ON "public"."child_enrollment_status_2010" ("id");

ALTER TABLE "public"."child_enrollment_status_barrier_2010" ADD FOREIGN KEY ("child_enrollment_status_index_id") REFERENCES "public"."child_enrollment_status_2010" ("id");

CREATE INDEX "child_enrollment_status_barrier_2010_pkey" ON "public"."child_enrollment_status_barrier_2010" ("id");

ALTER TABLE "public"."chronic_health_condition_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "chronic_health_condition_2010_pkey" ON "public"."chronic_health_condition_2010" ("id");

ALTER TABLE "public"."substance_abuse_problem_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "substance_abuse_problem_2010_pkey" ON "public"."substance_abuse_problem_2010" ("id");

ALTER TABLE "public"."contact_made_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "contact_made_2010_pkey" ON "public"."contact_made_2010" ("id");

ALTER TABLE "public"."currently_in_school_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "currently_in_school_2010_pkey" ON "public"."currently_in_school_2010" ("id");

ALTER TABLE "public"."degree_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "degree_2010_pkey" ON "public"."degree_2010" ("id");

ALTER TABLE "public"."degree_code_2010" ADD FOREIGN KEY ("degree_index_id") REFERENCES "public"."degree_2010" ("id");

CREATE INDEX "degree_code_2010_pkey" ON "public"."degree_code_2010" ("id");

ALTER TABLE "public"."destinations_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "destinations_2010_pkey" ON "public"."destinations_2010" ("id");

ALTER TABLE "public"."developmental_disability_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "developmental_disability_2010_pkey" ON "public"."developmental_disability_2010" ("id");

ALTER TABLE "public"."disabling_condition_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "disabling_condition_2010_pkey" ON "public"."disabling_condition_2010" ("id");

ALTER TABLE "public"."domestic_violence_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "domestic_violence_2010_pkey" ON "public"."domestic_violence_2010" ("id");

ALTER TABLE "public"."drug_history" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "drug_history_pkey" ON "public"."drug_history" ("id");

ALTER TABLE "public"."email_2010" ADD FOREIGN KEY ("agency_index_id") REFERENCES "public"."agency_2010" ("id");

ALTER TABLE "public"."email_2010" ADD FOREIGN KEY ("contact_index_id") REFERENCES "public"."contact_2010" ("id");

ALTER TABLE "public"."email_2010" ADD FOREIGN KEY ("resource_info_index_id") REFERENCES "public"."resource_info_2010" ("id");

ALTER TABLE "public"."email_2010" ADD FOREIGN KEY ("site_index_id") REFERENCES "public"."site_2010" ("id");

ALTER TABLE "public"."email_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "email_2010_pkey" ON "public"."email_2010" ("id");

ALTER TABLE "public"."emergency_contact" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "emergency_contact_pkey" ON "public"."emergency_contact" ("id");

ALTER TABLE "public"."employment_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "employment_2010_pkey" ON "public"."employment_2010" ("id");

ALTER TABLE "public"."engaged_date_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "engaged_date_2010_pkey" ON "public"."engaged_date_2010" ("id");

ALTER TABLE "public"."prior_residence_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "prior_residence_2010_pkey" ON "public"."prior_residence_2010" ("id");

ALTER TABLE "public"."pregnancy_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "pregnancy_2010_pkey" ON "public"."pregnancy_2010" ("id");

ALTER TABLE "public"."health_status_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "health_status_2010_pkey" ON "public"."health_status_2010" ("id");

ALTER TABLE "public"."highest_school_level_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "highest_school_level_2010_pkey" ON "public"."highest_school_level_2010" ("id");

ALTER TABLE "public"."physical_disability_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "physical_disability_2010_pkey" ON "public"."physical_disability_2010" ("id");

ALTER TABLE "public"."hiv_aids_status_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "hiv_aids_status_2010_pkey" ON "public"."hiv_aids_status_2010" ("id");

ALTER TABLE "public"."phone_2010" ADD FOREIGN KEY ("agency_index_id") REFERENCES "public"."agency_2010" ("id");

ALTER TABLE "public"."phone_2010" ADD FOREIGN KEY ("contact_index_id") REFERENCES "public"."contact_2010" ("id");

ALTER TABLE "public"."phone_2010" ADD FOREIGN KEY ("resource_info_index_id") REFERENCES "public"."resource_info_2010" ("id");

ALTER TABLE "public"."phone_2010" ADD FOREIGN KEY ("site_index_id") REFERENCES "public"."site_2010" ("id");

ALTER TABLE "public"."phone_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

ALTER TABLE "public"."phone_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "phone_2010_pkey" ON "public"."phone_2010" ("id");

ALTER TABLE "public"."person_address" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "person_address_pkey" ON "public"."person_address" ("id");

ALTER TABLE "public"."housing_status_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "housing_status_2010_pkey" ON "public"."housing_status_2010" ("id");

ALTER TABLE "public"."hud_chronic_homeless_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "hud_chronic_homeless_2010_pkey" ON "public"."hud_chronic_homeless_2010" ("id");

ALTER TABLE "public"."other_requirements_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "other_requirements_2010_pkey" ON "public"."other_requirements_2010" ("id");

ALTER TABLE "public"."hud_homeless_episodes" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "hud_homeless_episodes_pkey" ON "public"."hud_homeless_episodes" ("id");

ALTER TABLE "public"."other_names" ADD FOREIGN KEY ("person_index_id") REFERENCES "public"."person" ("id");

CREATE INDEX "other_names_pkey" ON "public"."other_names" ("id");

ALTER TABLE "public"."income_and_sources" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "income_and_sources_pkey" ON "public"."income_and_sources" ("id");

ALTER TABLE "public"."other_address_2010" ADD FOREIGN KEY ("site_index_id") REFERENCES "public"."site_2010" ("id");

CREATE INDEX "other_address_2010_pkey" ON "public"."other_address_2010" ("id");

ALTER TABLE "public"."income_last_30_days_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "income_last_30_days_2010_pkey" ON "public"."income_last_30_days_2010" ("id");

ALTER TABLE "public"."income_requirements_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "income_requirements_2010_pkey" ON "public"."income_requirements_2010" ("id");

ALTER TABLE "public"."non_cash_benefits_last_30_days_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "non_cash_benefits_last_30_days_2010_pkey" ON "public"."non_cash_benefits_last_30_days_2010" ("id");

ALTER TABLE "public"."income_total_monthly_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "income_total_monthly_2010_pkey" ON "public"."income_total_monthly_2010" ("id");

ALTER TABLE "public"."non_cash_benefits_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "non_cash_benefits_2010_pkey" ON "public"."non_cash_benefits_2010" ("id");

ALTER TABLE "public"."non_cash_benefits_sub_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

ALTER TABLE "public"."non_cash_benefits_sub_2010" ADD FOREIGN KEY ("non_cash_benefits_index_id") REFERENCES "public"."non_cash_benefits_2010" ("id");

CREATE INDEX "non_cash_benefits_sub_2010_pkey" ON "public"."non_cash_benefits_sub_2010" ("id");

ALTER TABLE "public"."inventory_2010" ADD FOREIGN KEY ("service_index_id") REFERENCES "public"."service_2010" ("id");

ALTER TABLE "public"."inventory_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "inventory_2010_pkey" ON "public"."inventory_2010" ("id");

ALTER TABLE "public"."need" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_participation" ("id");

ALTER TABLE "public"."need" ADD FOREIGN KEY ("person_index_id_2010") REFERENCES "public"."person" ("id");

CREATE INDEX "need_pkey" ON "public"."need" ("id");

ALTER TABLE "public"."taxonomy_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

ALTER TABLE "public"."taxonomy_2010" ADD FOREIGN KEY ("need_index_id") REFERENCES "public"."need" ("id");

CREATE INDEX "taxonomy_2010_pkey" ON "public"."taxonomy_2010" ("id");

ALTER TABLE "public"."service_event" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_participation" ("id");

ALTER TABLE "public"."service_event" ADD FOREIGN KEY ("person_index_id_2010") REFERENCES "public"."person" ("id");

ALTER TABLE "public"."service_event" ADD FOREIGN KEY ("need_index_id_2010") REFERENCES "public"."need" ("id");

CREATE INDEX "service_event_pkey" ON "public"."service_event" ("id");

ALTER TABLE "public"."service_event_notes_2010" ADD FOREIGN KEY ("service_event_index_id") REFERENCES "public"."service_event" ("id");

CREATE INDEX "service_event_notes_2010_pkey" ON "public"."service_event_notes_2010" ("id");

ALTER TABLE "public"."funding_source_2010" ADD FOREIGN KEY ("service_index_id") REFERENCES "public"."service_2010" ("id");

ALTER TABLE "public"."funding_source_2010" ADD FOREIGN KEY ("service_event_index_id") REFERENCES "public"."service_event" ("id");

CREATE INDEX "funding_source_2010_pkey" ON "public"."funding_source_2010" ("id");

ALTER TABLE "public"."languages_2010" ADD FOREIGN KEY ("site_index_id") REFERENCES "public"."site_2010" ("id");

ALTER TABLE "public"."languages_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "languages_2010_pkey" ON "public"."languages_2010" ("id");

ALTER TABLE "public"."time_open_2010" ADD FOREIGN KEY ("site_index_id") REFERENCES "public"."site_2010" ("id");

ALTER TABLE "public"."time_open_2010" ADD FOREIGN KEY ("languages_index_id") REFERENCES "public"."languages_2010" ("id");

ALTER TABLE "public"."time_open_2010" ADD FOREIGN KEY ("site_service_index_id") REFERENCES "public"."site_service_2010" ("id");

CREATE INDEX "time_open_2010_pkey" ON "public"."time_open_2010" ("id");

CREATE INDEX "migrate_version_pkey" ON "public"."migrate_version" ("repository_id");

ALTER TABLE "public"."length_of_stay_at_prior_residence_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "length_of_stay_at_prior_residence_2010_pkey" ON "public"."length_of_stay_at_prior_residence_2010" ("id");

ALTER TABLE "public"."mental_health_problem_2010" ADD FOREIGN KEY ("person_historical_index_id") REFERENCES "public"."person_historical" ("id");

CREATE INDEX "mental_health_problem_2010_pkey" ON "public"."mental_health_problem_2010" ("id");

ALTER TABLE "public"."license_accreditation_2010" ADD FOREIGN KEY ("agency_index_id") REFERENCES "public"."agency_2010" ("id");

CREATE INDEX "license_accreditation_2010_pkey" ON "public"."license_accreditation_2010" ("id");

ALTER TABLE "public"."members" ADD FOREIGN KEY ("household_index_id") REFERENCES "public"."household" ("id");

CREATE INDEX "members_pkey" ON "public"."members" ("id");
