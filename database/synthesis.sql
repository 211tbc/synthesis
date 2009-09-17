CREATE SCHEMA public;
CREATE TABLE public.database (
    id serial NOT NULL DEFAULT nextval('database_id_seq'::regclass),
    export_id varchar(50),
    database_id varchar(50),
    database_id_date_collected timestamptz,
    database_email varchar(50),
    database_email_date_collected timestamptz,
    database_contact_extension varchar(10),
    database_contact_extension_date_collected timestamptz,
    database_contact_last varchar(20),
    database_contact_last_date_collected timestamptz,
    database_contact_phone varchar(20),
    database_contact_phone_date_collected timestamptz,
    database_name varchar(50),
    database_name_date_collected timestamptz
);
ALTER TABLE public.database ADD CONSTRAINT database_pkey PRIMARY KEY(id);
CREATE TABLE public.export (
    export_id varchar(50) NOT NULL,
    export_id_date_collected timestamptz,
    export_date timestamptz,
    export_date_date_collected timestamptz,
    export_period_start_date timestamptz,
    export_period_start_date_date_collected timestamptz,
    export_period_end_date timestamptz,
    export_period_end_date_date_collected timestamptz,
    export_software_vendor varchar(50),
    export_software_vendor_date_collected timestamptz,
    export_software_version varchar(10),
    export_software_version_date_collected timestamptz
);
ALTER TABLE public.export ADD CONSTRAINT export_pkey PRIMARY KEY(export_id);
CREATE TABLE public.household (
    id serial NOT NULL DEFAULT nextval('household_id_seq'::regclass),
    household_id_num varchar(32),
    household_id_num_date_collected timestamptz,
    household_id_str varchar(32),
    household_id_str_date_collected timestamptz,
    head_of_household_id_unhashed varchar(32),
    head_of_household_id_unhashed_date_collected timestamptz,
    head_of_household_id_hashed varchar(32),
    head_of_household_id_hashed_date_collected timestamptz
);
ALTER TABLE public.household ADD CONSTRAINT household_pkey PRIMARY KEY(id);
CREATE TABLE public.hud_homeless_episodes (
    id serial NOT NULL DEFAULT nextval('hud_homeless_episodes_id_seq'::regclass),
    person_historical_index_id int4,
    start_date varchar(32),
    start_date_date_collected timestamptz,
    end_date varchar(32),
    end_date_date_collected timestamptz
);
ALTER TABLE public.hud_homeless_episodes ADD CONSTRAINT hud_homeless_episodes_pkey PRIMARY KEY(id);
CREATE TABLE public.income_and_sources (
    id serial NOT NULL DEFAULT nextval('income_and_sources_id_seq'::regclass),
    person_historical_index_id int4,
    amount int4,
    amount_date_collected timestamptz,
    income_source_code int4,
    income_source_code_date_collected timestamptz,
    income_source_other varchar(32),
    income_source_other_date_collected timestamptz
);
ALTER TABLE public.income_and_sources ADD CONSTRAINT income_and_sources_pkey PRIMARY KEY(id);
CREATE TABLE public.members (
    id serial NOT NULL DEFAULT nextval('members_id_seq'::regclass),
    household_index_id int4,
    person_id_unhashed varchar(32),
    person_id_unhashed_date_collected timestamptz,
    person_id_hashed varchar(32),
    person_id_hashed_date_collected timestamptz,
    relationship_to_head_of_household varchar(32),
    relationship_to_head_of_household_date_collected timestamptz
);
ALTER TABLE public.members ADD CONSTRAINT members_pkey PRIMARY KEY(id);
CREATE TABLE public.other_names (
    id serial NOT NULL DEFAULT nextval('other_names_id_seq'::regclass),
    person_index_id int4,
    other_first_name_unhashed varchar(50),
    other_first_name_hashed varchar(32),
    other_first_name_date_collected timestamptz,
    other_middle_name_unhashed varchar(50),
    other_middle_name_hashed varchar(32),
    other_middle_name_date_collected timestamptz,
    other_last_name_unhashed varchar(50),
    other_last_name_hashed varchar(32),
    other_last_name_date_collected timestamptz,
    other_suffix_unhashed varchar(50),
    other_suffix_hashed varchar(32),
    other_suffix_date_collected timestamptz
);
ALTER TABLE public.other_names ADD CONSTRAINT other_names_pkey PRIMARY KEY(id);
CREATE TABLE public.person (
    id serial NOT NULL DEFAULT nextval('person_id_seq'::regclass),
    export_id varchar(50),
    person_id_hashed varchar(32),
    person_id_unhashed varchar(50),
    person_id_date_collected timestamptz,
    person_date_of_birth_hashed varchar(32),
    person_date_of_birth_unhashed date,
    person_date_of_birth_date_collected timestamptz,
    person_ethnicity_hashed varchar(32),
    person_ethnicity_unhashed int4,
    person_ethnicity_date_collected timestamptz,
    person_gender_hashed varchar(32),
    person_gender_unhashed int4,
    person_gender_date_collected timestamptz,
    person_legal_first_name_hashed varchar(32),
    person_legal_first_name_unhashed varchar(50),
    person_legal_first_name_date_collected timestamptz,
    person_legal_last_name_hashed varchar(32),
    person_legal_last_name_unhashed varchar(50),
    person_legal_last_name_date_collected timestamptz,
    person_legal_middle_name_hashed varchar(32),
    person_legal_middle_name_unhashed varchar(50),
    person_legal_middle_name_date_collected timestamptz,
    person_legal_suffix_hashed varchar(32),
    person_legal_suffix_unhashed varchar(50),
    person_legal_suffix_date_collected timestamptz,
    person_social_security_number_hashed varchar(32),
    person_social_security_number_unhashed varchar(9),
    person_social_security_number_date_collected timestamptz,
    person_social_sec_number_quality_code varchar(2),
    person_social_sec_number_quality_code_date_collected timestamptz
);
ALTER TABLE public.person ADD CONSTRAINT person_pkey PRIMARY KEY(id);
CREATE TABLE public.person_address (
    id serial NOT NULL DEFAULT nextval('person_address_id_seq'::regclass),
    person_historical_index_id int4,
    address_period_start_date timestamptz,
    address_period_start_date_date_collected timestamptz,
    address_period_end_date timestamptz,
    address_period_end_date_date_collected timestamptz,
    pre_address_line varchar(32),
    pre_address_line_date_collected timestamptz,
    line1 varchar(32),
    line1_date_collected timestamptz,
    line2 varchar(32),
    line2_date_collected timestamptz,
    city varchar(32),
    city_date_collected timestamptz,
    county varchar(32),
    county_date_collected timestamptz,
    state varchar(32),
    state_date_collected timestamptz,
    zipcode varchar(10),
    zipcode_date_collected timestamptz,
    country varchar(32),
    country_date_collected timestamptz,
    is_last_permanent_zip int4,
    is_last_permanent_zip_date_collected timestamptz,
    zip_quality_code int4,
    zip_quality_code_date_collected timestamptz
);
ALTER TABLE public.person_address ADD CONSTRAINT person_address_pkey PRIMARY KEY(id);
CREATE TABLE public.person_historical (
    id serial NOT NULL DEFAULT nextval('person_historical_id_seq'::regclass),
    person_index_id int4,
    person_historical_id_num int4,
    person_historical_id_num_date_collected timestamptz,
    person_historical_id_str varchar(32),
    person_historical_id_str_date_collected timestamptz,
    barrier_code int4,
    barrier_code_date_collected timestamptz,
    barrier_other varchar(50),
    barrier_other_date_collected timestamptz,
    child_currently_enrolled_in_school int4,
    child_currently_enrolled_in_school_date_collected timestamptz,
    currently_employed int4,
    currently_employed_date_collected timestamptz,
    currently_in_school int4,
    currently_in_school_date_collected timestamptz,
    degree_code int4,
    degree_code_date_collected timestamptz,
    degree_other varchar(50),
    degree_other_date_collected timestamptz,
    developmental_disability int4,
    developmental_disability_date_collected timestamptz,
    domestic_violence int4,
    domestic_violence_date_collected timestamptz,
    domestic_violence_how_long int4,
    domestic_violence_how_long_date_collected timestamptz,
    due_date date,
    due_date_date_collected timestamptz,
    employment_tenure int4,
    employment_tenure_date_collected timestamptz,
    health_status int4,
    health_status_date_collected timestamptz,
    highest_school_level int4,
    highest_school_level_date_collected timestamptz,
    hivaids_status int4,
    hivaids_status_date_collected timestamptz,
    hours_worked_last_week int4,
    hours_worked_last_week_date_collected timestamptz,
    hud_chronic_homeless int4,
    hud_chronic_homeless_date_collected timestamptz,
    hud_homeless int4,
    hud_homeless_date_collected timestamptz,
    length_of_stay_at_prior_residence int4,
    length_of_stay_at_prior_residence_date_collected timestamptz,
    looking_for_work int4,
    looking_for_work_date_collected timestamptz,
    mental_health_indefinite int4,
    mental_health_indefinite_date_collected timestamptz,
    mental_health_problem int4,
    mental_health_problem_date_collected timestamptz,
    non_cash_source_code int4,
    non_cash_source_code_date_collected timestamptz,
    non_cash_source_other varchar(50),
    non_cash_source_other_date_collected timestamptz,
    person_email text,
    person_email_date_collected timestamptz,
    person_phone_number text,
    person_phone_number_date_collected timestamptz,
    physical_disability int4,
    physical_disability_data_col_stage int4,
    physical_disability_date_collected timestamptz,
    physical_disability_date_effective timestamptz,
    pregnancy_status int4,
    pregnancy_status_date_collected timestamptz,
    prior_residence int4,
    prior_residence_date_collected timestamptz,
    prior_residence_other varchar(50),
    prior_residence_other_date_collected timestamptz,
    reason_for_leaving int4,
    reason_for_leaving_date_collected timestamptz,
    reason_for_leaving_other varchar(50),
    reason_for_leaving_other_date_collected timestamptz,
    school_last_enrolled_date date,
    school_last_enrolled_date_date_collected timestamptz,
    school_name varchar(50),
    school_name_date_collected timestamptz,
    school_type int4,
    school_type_date_collected timestamptz,
    subsidy_other varchar(50),
    subsidy_other_date_collected timestamptz,
    subsidy_type int4,
    subsidy_type_date_collected timestamptz,
    substance_abuse_indefinite int4,
    substance_abuse_indefinite_date_collected timestamptz,
    substance_abuse_problem int4,
    substance_abuse_problem_date_collected timestamptz,
    total_income numeric(5,2),
    total_income_date_collected timestamptz,
    vocational_training int4,
    vocational_training_date_collected timestamptz
);
ALTER TABLE public.person_historical ADD CONSTRAINT person_historical_pkey PRIMARY KEY(id);
CREATE TABLE public.races (
    id serial NOT NULL DEFAULT nextval('races_id_seq'::regclass),
    person_index_id int4,
    race_unhashed int4,
    race_hashed varchar(32),
    race_date_collected timestamptz
);
ALTER TABLE public.races ADD CONSTRAINT races_pkey PRIMARY KEY(id);
CREATE TABLE public.release_of_information (
    id serial NOT NULL DEFAULT nextval('release_of_information_id_seq'::regclass),
    person_index_id int4,
    release_of_information_idid_num varchar(32),
    release_of_information_idid_num_date_collected timestamptz,
    release_of_information_idid_str varchar(32),
    release_of_information_idid_str_date_collected timestamptz,
    site_service_idid_num varchar(32),
    site_service_idid_num_date_collected timestamptz,
    site_service_idid_str varchar(32),
    site_service_idid_str_date_collected timestamptz,
    documentation varchar(32),
    documentation_date_collected timestamptz,
    start_date varchar(32),
    start_date_date_collected timestamptz,
    end_date varchar(32),
    end_date_date_collected timestamptz,
    release_granted varchar(32),
    release_granted_date_collected timestamptz
);
ALTER TABLE public.release_of_information ADD CONSTRAINT release_of_information_pkey PRIMARY KEY(id);
CREATE TABLE public.veteran (
    id serial NOT NULL DEFAULT nextval('veteran_id_seq'::regclass),
    person_historical_index_id int4,
    service_era int4,
    service_era_date_collected timestamptz,
    military_service_duration int4,
    military_service_duration_date_collected timestamptz,
    served_in_war_zone int4,
    served_in_war_zone_date_collected timestamptz,
    war_zone int4,
    war_zone_date_collected timestamptz,
    war_zone_other varchar(50),
    war_zone_other_date_collected timestamptz,
    months_in_war_zone int4,
    months_in_war_zone_date_collected timestamptz,
    received_fire int4,
    received_fire_date_collected timestamptz,
    military_branch int4,
    military_branch_date_collected timestamptz,
    military_branch_other varchar(50),
    military_branch_other_date_collected timestamptz,
    discharge_status int4,
    discharge_status_date_collected timestamptz,
    discharge_status_other varchar(50),
    discharge_status_other_date_collected timestamptz
);
ALTER TABLE public.veteran ADD CONSTRAINT veteran_pkey PRIMARY KEY(id);
ALTER TABLE public.database ADD CONSTRAINT database_export_id_fkey FOREIGN KEY (export_id) REFERENCES public.export(export_id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE public.hud_homeless_episodes ADD CONSTRAINT hud_homeless_episodes_person_historical_index_id_fkey FOREIGN KEY (person_historical_index_id) REFERENCES public.person_historical(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE public.income_and_sources ADD CONSTRAINT income_and_sources_person_historical_index_id_fkey FOREIGN KEY (person_historical_index_id) REFERENCES public.person_historical(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE public.members ADD CONSTRAINT members_household_index_id_fkey FOREIGN KEY (household_index_id) REFERENCES public.household(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE public.other_names ADD CONSTRAINT other_names_person_index_id_fkey FOREIGN KEY (person_index_id) REFERENCES public.person(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE public.person ADD CONSTRAINT person_export_id_fkey FOREIGN KEY (export_id) REFERENCES public.export(export_id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE public.person_address ADD CONSTRAINT person_address_person_historical_index_id_fkey FOREIGN KEY (person_historical_index_id) REFERENCES public.person_historical(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE public.person_historical ADD CONSTRAINT person_historical_person_index_id_fkey FOREIGN KEY (person_index_id) REFERENCES public.person(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE public.races ADD CONSTRAINT races_person_index_id_fkey FOREIGN KEY (person_index_id) REFERENCES public.person(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE public.release_of_information ADD CONSTRAINT release_of_information_person_index_id_fkey FOREIGN KEY (person_index_id) REFERENCES public.person(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE public.veteran ADD CONSTRAINT veteran_person_historical_index_id_fkey FOREIGN KEY (person_historical_index_id) REFERENCES public.person_historical(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
