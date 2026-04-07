BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "appointments" (
	"id"	INTEGER,
	"patient_id"	INTEGER,
	"doctor_id"	INTEGER NOT NULL,
	"reception_id"	INTEGER,
	"appointment_date"	TEXT NOT NULL,
	"appointment_time"	TEXT NOT NULL,
	"status"	TEXT DEFAULT 'booked' CHECK("status" IN ('booked', 'confirmed', 'completed', 'cancelled')),
	"diagnosis"	TEXT,
	"medicines"	TEXT,
	"notes"	TEXT,
	UNIQUE("doctor_id","appointment_date","appointment_time"),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("doctor_id") REFERENCES "doctors"("id") ON DELETE CASCADE,
	FOREIGN KEY("patient_id") REFERENCES "patients"("id") ON DELETE CASCADE,
	FOREIGN KEY("reception_id") REFERENCES "receptionists"("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "doctors" (
	"id"	INTEGER,
	"user_id"	INTEGER NOT NULL,
	"specialization"	TEXT NOT NULL,
	"available_time"	TEXT,
	"fee"	REAL DEFAULT 300.0,
	"mode"	TEXT DEFAULT 'offline' CHECK("mode" IN ('online', 'offline')),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "patients" (
	"id"	INTEGER,
	"user_id"	INTEGER NOT NULL,
	"name"	TEXT,
	"age"	INTEGER,
	"gender"	TEXT,
	"phone"	TEXT,
	"address"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "receptionists" (
	"id"	INTEGER,
	"user_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"role"	TEXT NOT NULL,
	"created_at"	TEXT DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "appointments" VALUES (2,2,2,2,'2026-04-08','10:00','booked',NULL,NULL,'First visit');
INSERT INTO "appointments" VALUES (3,3,3,3,'2026-04-08','11:30','confirmed',NULL,NULL,NULL);
INSERT INTO "appointments" VALUES (4,4,4,4,'2026-04-09','12:00','completed','Skin allergy','Ointment','Follow-up needed');
INSERT INTO "appointments" VALUES (5,5,5,5,'2026-04-09','01:30','booked',NULL,NULL,NULL);
INSERT INTO "appointments" VALUES (6,6,6,6,'2026-04-10','02:00','cancelled',NULL,NULL,'Patient unavailable');
INSERT INTO "appointments" VALUES (7,7,7,2,'2026-04-10','03:30','booked',NULL,NULL,NULL);
INSERT INTO "appointments" VALUES (8,8,8,3,'2026-04-11','09:30','confirmed',NULL,NULL,NULL);
INSERT INTO "appointments" VALUES (9,9,9,4,'2026-04-11','10:45','booked',NULL,NULL,NULL);
INSERT INTO "appointments" VALUES (10,10,10,5,'2026-04-12','12:00','booked',NULL,NULL,NULL);
INSERT INTO "appointments" VALUES (11,11,11,6,'2026-04-12','02:30','completed','Joint pain','Painkillers','Physiotherapy advised');
INSERT INTO "doctors" VALUES (2,4,'Cardiology','9AM-5PM',500.0,'offline');
INSERT INTO "doctors" VALUES (3,5,'Dentist','10AM-4PM',400.0,'offline');
INSERT INTO "doctors" VALUES (4,6,'Dermatology','11AM-6PM',450.0,'online');
INSERT INTO "doctors" VALUES (5,7,'Neurology','9AM-3PM',700.0,'offline');
INSERT INTO "doctors" VALUES (6,8,'Orthopedics','10AM-2PM',600.0,'offline');
INSERT INTO "doctors" VALUES (7,9,'Pediatrics','9AM-5PM',300.0,'online');
INSERT INTO "doctors" VALUES (8,10,'ENT','12PM-6PM',350.0,'offline');
INSERT INTO "doctors" VALUES (9,11,'Gynecology','10AM-4PM',550.0,'offline');
INSERT INTO "doctors" VALUES (10,12,'Psychiatry','2PM-7PM',650.0,'online');
INSERT INTO "doctors" VALUES (11,13,'Urology','11AM-5PM',500.0,'offline');
INSERT INTO "patients" VALUES (2,14,'Ravi Kumar',30,'Male','9000000001','Hyderabad');
INSERT INTO "patients" VALUES (3,15,'Sneha Reddy',22,'Female','9000000002','Guntur');
INSERT INTO "patients" VALUES (4,16,'Vikram Singh',35,'Male','9000000003','Vizag');
INSERT INTO "patients" VALUES (5,17,'Lakshmi Devi',28,'Female','9000000004','Vijayawada');
INSERT INTO "patients" VALUES (6,18,'Arun Kumar',26,'Male','9000000005','Hyderabad');
INSERT INTO "patients" VALUES (7,19,'Pooja Sharma',24,'Female','9000000006','Delhi');
INSERT INTO "patients" VALUES (8,20,'Rahul Verma',32,'Male','9000000007','Mumbai');
INSERT INTO "patients" VALUES (9,21,'Deepak Kumar',29,'Male','9000000008','Chennai');
INSERT INTO "patients" VALUES (10,22,'Keerthi Reddy',23,'Female','9000000009','Guntur');
INSERT INTO "patients" VALUES (11,23,'Suman Kumar',31,'Male','9000000010','Vizag');
INSERT INTO "patients" VALUES (12,24,'Ajay Kumar',27,'Male','9000000011','Hyderabad');
INSERT INTO "patients" VALUES (13,25,'Priya Singh',25,'Female','9000000012','Delhi');
INSERT INTO "patients" VALUES (14,26,'Manoj Kumar',33,'Male','9000000013','Bangalore');
INSERT INTO "patients" VALUES (15,27,'Nisha Sharma',21,'Female','9000000014','Pune');
INSERT INTO "patients" VALUES (16,28,'Karthik Reddy',34,'Male','9000000015','Hyderabad');
INSERT INTO "receptionists" VALUES (2,29);
INSERT INTO "receptionists" VALUES (3,30);
INSERT INTO "receptionists" VALUES (4,31);
INSERT INTO "receptionists" VALUES (5,32);
INSERT INTO "receptionists" VALUES (6,33);
INSERT INTO "users" VALUES (4,'Dr. Meena','meena@hms.com','pass1','doctor','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (5,'Dr. Kiran','kiran@hms.com','pass2','doctor','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (6,'Dr. Suresh','suresh@hms.com','pass3','doctor','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (7,'Dr. Anil','anil@hms.com','pass4','doctor','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (8,'Dr. Kavitha','kavitha@hms.com','pass5','doctor','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (9,'Dr. Ramesh','ramesh@hms.com','pass6','doctor','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (10,'Dr. Divya','divya@hms.com','pass7','doctor','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (11,'Dr. Teja','teja@hms.com','pass8','doctor','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (12,'Dr. Harsha','harsha@hms.com','pass9','doctor','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (13,'Dr. Nikhil','nikhil@hms.com','pass10','doctor','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (14,'Ravi Kumar','ravi@hms.com','pat1','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (15,'Sneha Reddy','sneha@hms.com','pat2','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (16,'Vikram Singh','vikram@hms.com','pat3','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (17,'Lakshmi Devi','lakshmi@hms.com','pat4','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (18,'Arun Kumar','arun@hms.com','pat5','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (19,'Pooja Sharma','pooja@hms.com','pat6','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (20,'Rahul Verma','rahul@hms.com','pat7','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (21,'Deepak Kumar','deepak@hms.com','pat8','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (22,'Keerthi Reddy','keerthi@hms.com','pat9','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (23,'Suman Kumar','suman@hms.com','pat10','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (24,'Ajay Kumar','ajay@hms.com','pat11','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (25,'Priya Singh','priya@hms.com','pat12','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (26,'Manoj Kumar','manoj@hms.com','pat13','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (27,'Nisha Sharma','nisha@hms.com','pat14','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (28,'Karthik Reddy','karthik@hms.com','pat15','patient','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (29,'Anjali','anjali@hms.com','rec1','receptionist','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (30,'Kavya','kavya@hms.com','rec2','receptionist','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (31,'Rohit','rohit@hms.com','rec3','receptionist','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (32,'Neha','neha@hms.com','rec4','receptionist','2026-04-07 09:20:21');
INSERT INTO "users" VALUES (33,'Arjun','arjun@hms.com','rec5','receptionist','2026-04-07 09:20:21');
COMMIT;
