from datetime import date
from app.modules.finance.transaction.fund_distribution.repo import build_list_where
from app.modules.finance.transaction.fund_distribution.schema import FUND_ENTITY_MAP


def test_fund_entity_map_z():
    assert FUND_ENTITY_MAP['Z'] == 1


def test_fund_entity_map_t_is_infaq():
    assert FUND_ENTITY_MAP['T'] == 2


def test_build_list_where_basic():
    where, args = build_list_where(
        begin='2026-01-01', end='2026-12-31',
        search=None, branch=None,
    )
    assert 't.transactioncode = $1' in where
    assert args[0] == 'DD001'
    assert len(args) == 3


def test_build_list_where_with_search():
    where, args = build_list_where(
        begin='2026-01-01', end='2026-12-31',
        search='KK-2026', branch=None,
    )
    assert 'LIKE' in where
    assert any('%KK-2026%' in str(a) for a in args)


def test_build_list_where_with_branch():
    where, args = build_list_where(
        begin='2026-01-01', end='2026-12-31',
        search=None, branch='001',
    )
    assert 'branchcode' in where
    assert '001' in args
