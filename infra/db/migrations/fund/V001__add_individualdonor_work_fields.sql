-- Migration: Add missing work-related columns to fund.individualdonor
-- These columns appear in legacy code (fEIndividualDonor2) but were absent in the DDL export.
-- Safe to re-run (IF NOT EXISTS).

ALTER TABLE fund.individualdonor ADD COLUMN IF NOT EXISTS donorgroup       VARCHAR(1);
ALTER TABLE fund.individualdonor ADD COLUMN IF NOT EXISTS workareaidinitial INTEGER;
ALTER TABLE fund.individualdonor ADD COLUMN IF NOT EXISTS workbusinessarea  VARCHAR(100);
ALTER TABLE fund.individualdonor ADD COLUMN IF NOT EXISTS workposition      VARCHAR(100);
ALTER TABLE fund.individualdonor ADD COLUMN IF NOT EXISTS workunit          VARCHAR(100);
