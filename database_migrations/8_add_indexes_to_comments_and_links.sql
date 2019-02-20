CREATE FULLTEXT INDEX title_self_text_fulltext_index
  ON links (title, self_text);
CREATE INDEX created_utc_index
  ON links (created_utc);

CREATE INDEX auto_link_id_index
  ON comments (auto_link_id);
CREATE FULLTEXT INDEX body_fulltext_index
  ON comments (body);
CREATE INDEX created_utc_index
  ON comments (created_utc);
