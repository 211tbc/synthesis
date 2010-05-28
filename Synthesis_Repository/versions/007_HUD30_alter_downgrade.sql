--DROPing columns and foreign keys to support HUD 3.0 data standard

--source
ALTER TABLE source DROP COLUMN attr_version;
ALTER TABLE source DROP COLUMN source_id_id_id_num_2010;
ALTER TABLE source DROP COLUMN source_id_id_id_str_2010;
ALTER TABLE source DROP COLUMN source_id_id_delete_2010;
ALTER TABLE source DROP COLUMN source_id_id_delete_occurred_date_2010;
ALTER TABLE source DROP COLUMN source_id_id_delete_effective_2010;
ALTER TABLE source DROP COLUMN software_vendor_2010;
ALTER TABLE source DROP COLUMN software_version_2010;
ALTER TABLE source DROP COLUMN source_contact_email_2010;

--export
ALTER TABLE export DROP COLUMN source_index_id_2010;
ALTER TABLE export DROP CONSTRAINT "source_index_id_fkey";
ALTER TABLE export DROP COLUMN export_id_id_id_num_2010;
ALTER TABLE export DROP COLUMN export_id_id_id_str_2010;
ALTER TABLE export DROP COLUMN export_id_id_delete_2010;
ALTER TABLE export DROP COLUMN export_id_id_delete_occurred_date_2010;
ALTER TABLE export DROP COLUMN export_id_id_delete_effective_2010;

--income_and_sources
ALTER TABLE income_and_sources DROP COLUMN income_and_source_id_id_id_num_2010;
ALTER TABLE income_and_sources DROP COLUMN income_and_source_id_id_id_str_2010;
ALTER TABLE income_and_sources DROP COLUMN income_and_source_id_id_delete_2010;
ALTER TABLE income_and_sources DROP COLUMN income_and_source_id_id_delete_occurred_date_2010;
ALTER TABLE income_and_sources DROP COLUMN income_and_source_id_id_delete_effective_2010;
ALTER TABLE income_and_sources DROP COLUMN income_source_code_date_effective_2010;
ALTER TABLE income_and_sources DROP COLUMN income_source_code_data_collection_stage_2010;
ALTER TABLE income_and_sources DROP COLUMN income_source_other_date_effective_2010;
ALTER TABLE income_and_sources DROP COLUMN income_source_other_data_collection_stage_2010;
ALTER TABLE income_and_sources DROP COLUMN receiving_income_source_2010;
ALTER TABLE income_and_sources DROP COLUMN receiving_income_source_date_collected_2010;
ALTER TABLE income_and_sources DROP COLUMN receiving_income_source_date_effective_2010;
ALTER TABLE income_and_sources DROP COLUMN receiving_income_source_data_collection_stage_2010;
ALTER TABLE income_and_sources DROP COLUMN income_source_amount_date_effective_2010;
ALTER TABLE income_and_sources DROP COLUMN income_source_amount_data_collection_stage_2010;

--need
ALTER TABLE export DROP COLUMN person_index_id_2010;
ALTER TABLE export DROP CONSTRAINT "person_index_id_fkey";
ALTER TABLE need DROP COLUMN need_id_delete_2010;
ALTER TABLE need DROP COLUMN need_id_delete_occurred_date_2010;
ALTER TABLE need DROP COLUMN need_id_delete_delete_effective_2010;
ALTER TABLE need DROP COLUMN need_effective_period_start_date_2010;
ALTER TABLE need DROP COLUMN need_effective_period_end_date_2010;
ALTER TABLE need DROP COLUMN need_recorded_date_2010;

--person
ALTER TABLE person DROP COLUMN person_id_id_num_2010;
ALTER TABLE person DROP COLUMN person_id_id_str_2010;
ALTER TABLE person DROP COLUMN person_id_delete_2010;
ALTER TABLE person DROP COLUMN person_id_delete_occurred_date_2010;
ALTER TABLE person DROP COLUMN person_id_delete_effective_2010;

--person_DROPress
ALTER TABLE person_DROPress DROP COLUMN attr_delete_2010;
ALTER TABLE person_DROPress DROP COLUMN attr_delete_occurred_date_2010;
ALTER TABLE person_DROPress DROP COLUMN attr_effective_2010;

--person_historical
ALTER TABLE person_historical DROP COLUMN person_historical_id_delete_2010;
ALTER TABLE person_historical DROP COLUMN person_historical_id_delete_occurred_date_2010;
ALTER TABLE person_historical DROP COLUMN person_historical_id_delete_effective_2010;
ALTER TABLE person_historical DROP COLUMN site_service_id_2010;

--races
ALTER TABLE races DROP COLUMN race_date_effective_2010;
ALTER TABLE races DROP COLUMN race_data_collection_stage_2010;

--release_of_information
ALTER TABLE release_of_information DROP COLUMN release_of_information_id_date_effective_2010;
ALTER TABLE release_of_information DROP COLUMN release_of_information_id_data_collection_stage_2010;
ALTER TABLE release_of_information DROP COLUMN documentation_date_effective_2010;
ALTER TABLE release_of_information DROP COLUMN documentation_data_collection_stage_2010;
ALTER TABLE release_of_information DROP COLUMN release_granted_date_effective_2010;
ALTER TABLE release_of_information DROP COLUMN release_granted_data_collection_stage_2010;

--service_event
ALTER TABLE export DROP COLUMN person_index_id_2010;
ALTER TABLE export DROP CONSTRAINT "person_index_id_fkey";
ALTER TABLE export DROP COLUMN need_index_id_2010;
ALTER TABLE export DROP CONSTRAINT "need_index_id_fkey";
ALTER TABLE service_event DROP COLUMN service_event_id_delete_2010;
ALTER TABLE service_event DROP COLUMN service_event_id_delete_occurred_date_2010;
ALTER TABLE service_event DROP COLUMN service_event_id_delete_effective_2010;
ALTER TABLE service_event DROP COLUMN site_service_id_2010;
ALTER TABLE service_event DROP COLUMN service_event_provision_date_2010;
ALTER TABLE service_event DROP COLUMN service_event_recorded_date_2010;
ALTER TABLE service_event DROP COLUMN service_event_ind_fam_2010;
ALTER TABLE service_event DROP COLUMN hmis_service_event_code_type_of_service_2010;
ALTER TABLE service_event DROP COLUMN hmis_service_event_code_type_of_service_other_2010;
ALTER TABLE service_event DROP COLUMN hprp_financial_assistance_service_event_code_2010;
ALTER TABLE service_event DROP COLUMN hprp_relocation_stabilization_service_event_code_2010;

--site_service_participation
ALTER TABLE site_service_participation DROP COLUMN site_service_participation_id_delete_2010;
ALTER TABLE site_service_participation DROP COLUMN site_service_participation_id_delete_occurred_date_2010;
ALTER TABLE site_service_participation DROP COLUMN site_service_participation_id_delete_effective_2010;