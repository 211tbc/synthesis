
ALTER TABLE site_service_participation ADD COLUMN person_id integer;
ALTER TABLE site_service_participation ALTER COLUMN person_id SET STORAGE PLAIN;

ALTER TABLE site_service_participation
  ADD CONSTRAINT person_id_fkey FOREIGN KEY (person_id)
      REFERENCES person (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;