ALTER TABLE assessments ADD COLUMN new_column_name TEXT[];
UPDATE assessments SET new_column_name = ARRAY[assessment2];
ALTER TABLE assessments DROP COLUMN assessment2;
ALTER TABLE assessments RENAME COLUMN new_column_name TO assessment2;
ALTER TABLE assessments ADD CONSTRAINT assessment_unique_post UNIQUE (post_id);
