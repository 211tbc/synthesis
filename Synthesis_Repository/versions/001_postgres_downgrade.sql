-- Adding Column: reported
--person 
ALTER TABLE person DROP COLUMN reported;

--person_historical
ALTER TABLE person_historical DROP COLUMN reported;

--races
ALTER TABLE races DROP COLUMN reported;

--site_svc_part
ALTER TABLE site_service_participation DROP COLUMN reported;

--release_of_information
ALTER TABLE release_of_information DROP COLUMN reported;

--household
ALTER TABLE household DROP COLUMN reported;

--members
ALTER TABLE members DROP COLUMN reported;

--person_address
ALTER TABLE person_address DROP COLUMN reported;

--veteran
ALTER TABLE veteran DROP COLUMN reported;

--need
ALTER TABLE need DROP COLUMN reported;