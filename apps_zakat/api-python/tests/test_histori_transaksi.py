from __future__ import annotations
from app.modules.finance.inquiry.transaction_history.repo import build_search_where


def test_basic_date_filter():
    where, args = build_search_where(
        '2026-06-01', '2026-06-30', 'actual', 'none',
        None, None, None, True, '',
    )
    from datetime import date
    assert '$1' in where and '$2' in where
    assert args[0] == date(2026, 6, 1)
    assert args[1] == date(2026, 6, 30)


def test_transaction_date_type():
    where, _ = build_search_where(
        '2026-06-01', '2026-06-30', 'transaction', 'none',
        None, None, None, True, '',
    )
    assert 'transactiondate' in where


def test_non_spv_adds_inputer_filter():
    where, args = build_search_where(
        '2026-06-01', '2026-06-30', 'actual', 'none',
        None, None, None, False, 'HADI',
    )
    assert 'inputer' in where.lower()
    assert 'HADI' in args


def test_spv_no_inputer_filter():
    where, args = build_search_where(
        '2026-06-01', '2026-06-30', 'actual', 'none',
        None, None, None, True, 'HADI',
    )
    assert 'inputer' not in where.lower()


def test_branch_filter():
    where, args = build_search_where(
        '2026-06-01', '2026-06-30', 'actual', 'none',
        None, None, '001', True, '',
    )
    assert 'branchcode' in where
    assert '001' in args


def test_search_text_filter():
    where, args = build_search_where(
        '2026-06-01', '2026-06-30', 'actual', 'donorname',
        'budi', None, None, True, '',
    )
    assert 'donorname' in where.lower()
    assert '%BUDI%' in args


def test_cash_account_filter():
    where, args = build_search_where(
        '2026-06-01', '2026-06-30', 'actual', 'none',
        None, 'ACC001', None, True, '',
    )
    assert 'channelaccountno' in where
    assert 'ACC001' in args


from app.modules.finance.inquiry.transaction_history.export import build_histori_xlsx, _dmy
from app.modules.finance.inquiry.transaction_history.schema import TransactionRow


def _sample_row(**kw) -> TransactionRow:
    base = dict(
        transactionid=1, transactionno='TX-001',
        transactiondate='2026-06-01', actualdate='2026-06-01',
        amount=100000.0, donorno='D001', donorname='Budi',
        referenceno='REF01', description='Test', inputer='HADI',
        authstatus='T', isposted='T', authoperationmode=None,
        branchcode='001', channelaccountno='ACC001', channelname='Bank A',
        exttransactionid=None, titlesubsystem=None,
    )
    base.update(kw)
    return TransactionRow(**base)


def test_dmy_converts_iso():
    assert _dmy('2026-06-01') == '01-06-2026'


def test_dmy_handles_none():
    assert _dmy(None) == ''


def test_export_returns_bytes():
    rows = [_sample_row(), _sample_row(transactionid=2, transactionno='TX-002')]
    result = build_histori_xlsx(rows, '2026-06-01', '2026-06-30')
    assert isinstance(result, bytes)
    assert len(result) > 100
