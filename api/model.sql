CREATE TYPE "measurement_type" as ENUM ('pool', 'ambient');

DROP TABLE IF EXISTS "measurements";
CREATE TABLE "measurements" (
	"id" SERIAL PRIMARY KEY,
	"type" MEASUREMENT_TYPE,
	"measured_at" TIMESTAMP,
	"degrees_farenheit" NUMERIC(18, 2),
	"degrees_celsius" NUMERIC(18, 2)
);
