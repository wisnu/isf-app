-- Migration: replace role_menu with role_menu_permission
-- Apply to both isf_auth_zakat and isf_auth_wakaf
--
-- Before running in production: ensure bff-api is updated to read from
-- role_menu_permission instead of role_menu (auth_db.py get_menus_by_roles).

BEGIN;

-- 1. Create new table
CREATE TABLE IF NOT EXISTS isf_auth.role_menu_permission (
    id          SERIAL PRIMARY KEY,
    role_id     VARCHAR(50)  NOT NULL,
    menu_key    VARCHAR(100) NOT NULL,
    action      VARCHAR(20)  NOT NULL
                CHECK (action IN ('view','tambah','edit','hapus','detail')),
    updated_by  VARCHAR(100),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_role_menu_action UNIQUE (role_id, menu_key, action)
);

-- 2. Migrate all existing role_menu rows → action='view'
--    Note: source column is id_peran (legacy naming), mapped to role_id
INSERT INTO isf_auth.role_menu_permission (role_id, menu_key, action)
SELECT id_peran, menu_key, 'view'
FROM isf_auth.role_menu
ON CONFLICT (role_id, menu_key, action) DO NOTHING;

-- 3. Drop old table
--    WARNING: bff-api auth_db.py still queries isf_auth.role_menu.
--    Update BFF to use role_menu_permission before applying DROP in production.
DROP TABLE IF EXISTS isf_auth.role_menu;

COMMIT;
