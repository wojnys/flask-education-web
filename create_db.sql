BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"username"	VARCHAR(30) NOT NULL,
	"email"	VARCHAR(50) NOT NULL,
	"password_hash"	VARCHAR(80) NOT NULL,
	"budget"	INTEGER NOT NULL,
	"is_admin"	BOOLEAN,
	"had_first_login"	BOOLEAN,
	UNIQUE("email"),
	UNIQUE("username"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "answer" (
	"id"	INTEGER NOT NULL,
	"answer"	VARCHAR(1000) NOT NULL,
	"quiz_answer"	VARCHAR(300) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "topic" (
	"id"	INTEGER NOT NULL,
	"topic"	VARCHAR(60) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "question" (
	"id"	INTEGER NOT NULL,
	"question"	VARCHAR NOT NULL,
	"points"	INTEGER NOT NULL,
	"answer_id"	INTEGER,
	"topic_id"	INTEGER,
	FOREIGN KEY("topic_id") REFERENCES "topic"("id"),
	FOREIGN KEY("answer_id") REFERENCES "answer"("id"),
	PRIMARY KEY("id")
);
INSERT INTO "user" VALUES (1,'admin','admin@admin.cz','$2b$12$QnVX3vjP64qeTaxe6IdIB.N02Iz1De5kzYoq1ptfMiNbYJF4M1R5i',100,0,1);
INSERT INTO "user" VALUES (2,'tester','tester@tester.cz','$2b$12$QnVX3vjP64qeTaxe6IdIB.N02Iz1De5kzYoq1ptfMiNbYJF4M1R5i',100,0,1);

COMMIT;
