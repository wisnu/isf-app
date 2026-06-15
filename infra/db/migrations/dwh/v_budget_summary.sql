-- DWH View: dwh.v_budget_summary
-- Portal: zakat
-- Purpose: Aggregated budget summary by owner, period, and item grouping
-- Source: budget, budgetowner, budgetperiod, budgetitem
-- Used by: report-api endpoints for budget overview reports

CREATE OR REPLACE VIEW dwh.v_budget_summary AS
SELECT
  b.budgetid AS budget_id,
  b.budgetcode AS budget_code,
  bo.ownerid AS owner_id,
  bo.ownername AS owner_name,
  bo.ownercode AS owner_code,
  bp.periodid AS period_id,
  bp.periodvalue AS period_year,
  b.branchcode AS branch_code,
  -- Item hierarchy from budgetitem
  bi.itemid AS item_id,
  bi.budgetitemcode AS item_code,
  bi.budgetitemname AS item_name,
  bi.level,
  bi.parentitemid AS parent_item_id,
  -- Amount from budget table
  CAST(COALESCE(b.amount, 0) AS NUMERIC(20, 4)) AS amount,
  CAST(COALESCE(b.realization, 0) AS NUMERIC(20, 4)) AS realization,
  CAST(COALESCE(b.amount, 0) - COALESCE(b.realization, 0) AS NUMERIC(20, 4)) AS salvage_value,
  b.isdetail,
  b.budgettype,
  b.itemcode,
  b.itemname,
  b.currencycode,
  b.revisionid
FROM transaction.budget b
JOIN transaction.budgetowner bo ON b.ownerid = bo.ownerid
JOIN transaction.budgetperiod bp ON b.periodid = bp.periodid
  AND bp.parentperiodid IS NULL
LEFT JOIN transaction.budgetitem bi ON b.itemid = bi.itemid
WHERE b.budgettype = 'Y'
  AND b.isdetail = 'F'
;

COMMENT ON VIEW dwh.v_budget_summary IS
'Budget summary aggregation with realization amounts. Filters for year-based budgets (budgettype=Y, isdetail=F). Shows budget items grouped by owner, period, and item hierarchy.';
