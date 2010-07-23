-- Adding Column: reported
--person
ALTER TABLE person ADD COLUMN reported boolean;
ALTER TABLE person ALTER COLUMN reported SET STORAGE PLAIN;

--person_historical
ALTER TABLE person_historical ADD COLUMN reported boolean;
ALTER TABLE person_historical ALTER COLUMN reported SET STORAGE PLAIN;

--races
ALTER TABLE races ADD COLUMN reported boolean;
ALTER TABLE races ALTER COLUMN reported SET STORAGE PLAIN;

--site_svc_part
ALTER TABLE site_service_participation ADD COLUMN reported boolean;
ALTER TABLE site_service_participation ALTER COLUMN reported SET STORAGE PLAIN;

--release_of_information
ALTER TABLE release_of_information ADD COLUMN reported boolean;
ALTER TABLE release_of_information ALTER COLUMN reported SET STORAGE PLAIN;

--household
ALTER TABLE household ADD COLUMN reported boolean;
ALTER TABLE household ALTER COLUMN reported SET STORAGE PLAIN;

--members
ALTER TABLE members ADD COLUMN reported boolean;
ALTER TABLE members ALTER COLUMN reported SET STORAGE PLAIN;

--person_address
ALTER TABLE person_address ADD COLUMN reported boolean;
ALTER TABLE person_address ALTER COLUMN reported SET STORAGE PLAIN;

--veteran
ALTER TABLE veteran ADD COLUMN reported boolean;
ALTER TABLE veteran ALTER COLUMN reported SET STORAGE PLAIN;

--need
ALTER TABLE need ADD COLUMN reported boolean;
ALTER TABLE need ALTER COLUMN reported SET STORAGE PLAIN;
