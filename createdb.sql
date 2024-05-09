CREATE TABLE email (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id VARCHAR(255),
	created datetime,
	checked datetime
);
CREATE UNIQUE INDEX idx_email_email_id ON email (
    id
);
CREATE INDEX idx_email_id_pk ON email (
    id
);
