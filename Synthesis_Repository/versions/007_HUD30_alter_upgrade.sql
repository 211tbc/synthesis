--Adding columns and foreign keys to support HUD 3.0 data standard

--source
ALTER TABLE source ADD COLUMN attr_version VARCHAR(32) DEFAULT NULL;
ALTER TABLE source ADD COLUMN source_id_id_id_num_2010 VARCHAR(32) DEFAULT NULL;
ALTER TABLE source ADD COLUMN source_id_id_id_str_2010 VARCHAR(32) DEFAULT NULL;
ALTER TABLE source ADD COLUMN source_id_id_delete_2010 int2 DEFAULT NULL;
ALTER TABLE source ADD COLUMN source_id_id_delete_occurred_date_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE source ADD COLUMN source_id_id_delete_effective_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE source ADD COLUMN software_vendor_2010 VARCHAR(32) DEFAULT NULL;
ALTER TABLE source ADD COLUMN software_version_2010 VARCHAR(32) DEFAULT NULL;
ALTER TABLE source ADD COLUMN source_contact_email_2010 VARCHAR(32) DEFAULT NULL;

--export
ALTER TABLE export ADD COLUMN source_index_id_2010 int4 DEFAULT NULL;
ALTER TABLE export ADD CONSTRAINT "source_index_id_fkey" FOREIGN KEY ("source_index_id_2010") REFERENCES "public"."source" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE export ADD COLUMN export_id_id_id_num_2010 VARCHAR(32) DEFAULT NULL;
ALTER TABLE export ADD COLUMN export_id_id_id_str_2010 VARCHAR(32) DEFAULT NULL;
ALTER TABLE export ADD COLUMN export_id_id_delete_2010 int2 DEFAULT NULL;
ALTER TABLE export ADD COLUMN export_id_id_delete_occurred_date_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE export ADD COLUMN export_id_id_delete_effective_2010 TIMESTAMPTZ DEFAULT NULL;

--income_and_sources
ALTER TABLE income_and_sources ADD COLUMN income_and_source_id_id_id_num_2010 VARCHAR(32) DEFAULT NULL;
ALTER TABLE income_and_sources ADD COLUMN income_and_source_id_id_id_str_2010 VARCHAR(32) DEFAULT NULL;
ALTER TABLE income_and_sources ADD COLUMN income_and_source_id_id_delete_2010 int2 DEFAULT NULL;
ALTER TABLE income_and_sources ADD COLUMN income_and_source_id_id_delete_occurred_date_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE income_and_sources ADD COLUMN income_and_source_id_id_delete_effective_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE income_and_sources ADD COLUMN income_source_code_date_effective_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE income_and_sources ADD COLUMN income_source_code_data_collection_stage_2010 int4 DEFAULT NULL;
ALTER TABLE income_and_sources ADD COLUMN income_source_other_date_effective_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE income_and_sources ADD COLUMN income_source_other_data_collection_stage_2010 int4 DEFAULT NULL;
ALTER TABLE income_and_sources ADD COLUMN receiving_income_source_2010 int2 DEFAULT NULL;
ALTER TABLE income_and_sources ADD COLUMN receiving_income_source_date_collected_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE income_and_sources ADD COLUMN receiving_income_source_date_effective_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE income_and_sources ADD COLUMN receiving_income_source_data_collection_stage_2010 int4 DEFAULT NULL;
ALTER TABLE income_and_sources ADD COLUMN income_source_amount_date_effective_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE income_and_sources ADD COLUMN income_source_amount_data_collection_stage_2010 int4 DEFAULT NULL;

--need
ALTER TABLE export ADD COLUMN person_index_id_2010 int4 DEFAULT NULL;
ALTER TABLE export ADD CONSTRAINT "person_index_id_fkey" FOREIGN KEY ("person_index_id_2010") REFERENCES "public"."person" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE need ADD COLUMN need_id_delete_2010 int2 DEFAULT NULL;
ALTER TABLE need ADD COLUMN need_id_delete_occurred_date_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE need ADD COLUMN need_id_delete_delete_effective_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE need ADD COLUMN need_effective_period_start_date_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE need ADD COLUMN need_effective_period_end_date_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE need ADD COLUMN need_recorded_date_2010 TIMESTAMPTZ DEFAULT NULL;

--person
ALTER TABLE person ADD COLUMN person_id_id_num_2010 VARCHAR(32) DEFAULT NULL;
ALTER TABLE person ADD COLUMN person_id_id_str_2010 VARCHAR(32) DEFAULT NULL;
ALTER TABLE person ADD COLUMN person_id_delete_2010 int2 DEFAULT NULL;
ALTER TABLE person ADD COLUMN person_id_delete_occurred_date_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE person ADD COLUMN person_id_delete_effective_2010 TIMESTAMPTZ DEFAULT NULL;

--person_address
ALTER TABLE person_address ADD COLUMN attr_delete_2010 int2 DEFAULT NULL;
ALTER TABLE person_address ADD COLUMN attr_delete_occurred_date_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE person_address ADD COLUMN attr_effective_2010 TIMESTAMPTZ DEFAULT NULL;

--person_historical
ALTER TABLE person_historical ADD COLUMN person_historical_id_delete_2010 int2 DEFAULT NULL;
ALTER TABLE person_historical ADD COLUMN person_historical_id_delete_occurred_date_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE person_historical ADD COLUMN person_historical_id_delete_effective_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE person_historical ADD COLUMN site_service_id_2010 VARCHAR(32) DEFAULT NULL;

--races
ALTER TABLE races ADD COLUMN race_date_effective_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE races ADD COLUMN race_data_collection_stage_2010 int4 DEFAULT NULL;

--release_of_information
ALTER TABLE release_of_information ADD COLUMN release_of_information_id_date_effective_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE release_of_information ADD COLUMN release_of_information_id_data_collection_stage_2010 int4 DEFAULT NULL;
ALTER TABLE release_of_information ADD COLUMN documentation_date_effective_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE release_of_information ADD COLUMN documentation_data_collection_stage_2010 int4 DEFAULT NULL;
ALTER TABLE release_of_information ADD COLUMN release_granted_date_effective_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE release_of_information ADD COLUMN release_granted_data_collection_stage_2010 int4 DEFAULT NULL;

--service_event
ALTER TABLE service_event ADD COLUMN person_index_id_2010 int4 DEFAULT NULL;
ALTER TABLE service_event ADD CONSTRAINT "person_index_id_fkey" FOREIGN KEY ("person_index_id_2010") REFERENCES "public"."person" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE service_event ADD COLUMN need_index_id_2010 int4 DEFAULT NULL;
ALTER TABLE service_event ADD CONSTRAINT "need_index_id_fkey" FOREIGN KEY ("need_index_id_2010") REFERENCES "public"."need" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE service_event ADD COLUMN service_event_id_delete_2010 int2 DEFAULT NULL;
ALTER TABLE service_event ADD COLUMN service_event_id_delete_occurred_date_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE service_event ADD COLUMN service_event_id_delete_effective_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE service_event ADD COLUMN site_service_id_2010 VARCHAR(32) DEFAULT NULL;
ALTER TABLE service_event ADD COLUMN service_event_provision_date_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE service_event ADD COLUMN service_event_recorded_date_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE service_event ADD COLUMN service_event_ind_fam_2010 int2 DEFAULT NULL;
ALTER TABLE service_event ADD COLUMN hmis_service_event_code_type_of_service_2010 VARCHAR(32) DEFAULT NULL;
ALTER TABLE service_event ADD COLUMN hmis_service_event_code_type_of_service_other_2010 VARCHAR(32) DEFAULT NULL;
ALTER TABLE service_event ADD COLUMN hprp_financial_assistance_service_event_code_2010 VARCHAR(32) DEFAULT NULL;
ALTER TABLE service_event ADD COLUMN hprp_relocation_stabilization_service_event_code_2010 VARCHAR(32) DEFAULT NULL;

--site_service_participation
ALTER TABLE site_service_participation ADD COLUMN site_service_participation_id_delete_2010 int2 DEFAULT NULL;
ALTER TABLE site_service_participation ADD COLUMN site_service_participation_id_delete_occurred_date_2010 TIMESTAMPTZ DEFAULT NULL;
ALTER TABLE site_service_participation ADD COLUMN site_service_participation_id_delete_effective_2010 TIMESTAMPTZ DEFAULT NULL;