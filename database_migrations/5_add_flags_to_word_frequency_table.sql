ALTER TABLE links_frequency_of_words
  ADD COLUMN in_vocabulary bool null,
  ADD COLUMN is_unique BOOL NULL,
  ADD COLUMN is_complete BOOL NULL;
