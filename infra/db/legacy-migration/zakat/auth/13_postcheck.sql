-- 13_postcheck.sql — Verifikasi auth DB setelah init + provisioning user.
-- Dijalankan terpisah (setelah provision_auth_users.py), read-only kecuali gagal → error.
SET client_min_messages = notice;
DO $$
DECLARE n int; v text;
BEGIN
  SELECT count(*) INTO n FROM isf_auth.tenants;
  IF n = 0 THEN RAISE EXCEPTION 'POSTCHECK(auth): tenants kosong'; END IF;

  SELECT count(*) INTO n FROM isf_auth.menu;
  IF n < 100 THEN RAISE EXCEPTION 'POSTCHECK(auth): menu = % (expected >= 100)', n; END IF;

  SELECT count(*) INTO n FROM isf_auth.role_menu_permission r
   WHERE NOT EXISTS (SELECT 1 FROM isf_auth.menu m WHERE m.menu_key = r.menu_key);
  IF n > 0 THEN RAISE EXCEPTION 'POSTCHECK(auth): % role_menu_permission merujuk menu yang tidak ada', n; END IF;

  -- Mencegah BFF menjalankan seed_defaults() (ADMIN/admin123) saat start: users tidak boleh kosong
  SELECT count(*) INTO n FROM isf_auth.users WHERE status = 'active';
  IF n = 0 THEN RAISE EXCEPTION 'POSTCHECK(auth): tidak ada user aktif — BFF akan men-seed akun demo ADMIN/admin123!'; END IF;

  SELECT string_agg(u.id, ', ') INTO v FROM isf_auth.users u
   WHERE u.status = 'active'
     AND NOT EXISTS (SELECT 1 FROM isf_auth.user_credentials c WHERE c.user_id = u.id);
  IF v IS NOT NULL THEN RAISE EXCEPTION 'POSTCHECK(auth): user aktif tanpa password: %', v; END IF;

  SELECT string_agg(u.id, ', ') INTO v FROM isf_auth.users u
   WHERE NOT EXISTS (SELECT 1 FROM isf_auth.tenant_memberships t WHERE t.user_id = u.id AND t.is_default);
  IF v IS NOT NULL THEN RAISE EXCEPTION 'POSTCHECK(auth): user tanpa tenant default: %', v; END IF;

  -- Akun demo/dev tidak boleh aktif di produksi
  SELECT string_agg(id, ', ') INTO v FROM isf_auth.users
   WHERE status = 'active' AND id IN ('ADMIN', 'FINANCE.A', 'FINANCE.B', 'TESTUSR01');
  IF v IS NOT NULL THEN RAISE EXCEPTION 'POSTCHECK(auth): akun demo/dev masih aktif: %', v; END IF;

  RAISE NOTICE 'POSTCHECK(auth) OK';
END $$;

SELECT 'users' AS item, status AS key, count(*) AS n FROM isf_auth.users GROUP BY 2
UNION ALL SELECT 'user_credentials', NULL, count(*) FROM isf_auth.user_credentials
UNION ALL SELECT 'tenant_memberships', tenant_id, count(*) FROM isf_auth.tenant_memberships GROUP BY 2
UNION ALL SELECT 'menu', NULL, count(*) FROM isf_auth.menu
UNION ALL SELECT 'role_menu_permission', NULL, count(*) FROM isf_auth.role_menu_permission
ORDER BY 1, 2;
