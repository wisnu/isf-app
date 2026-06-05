from __future__ import annotations
from app.modules.transaksi_histori.repository import build_search_where


def test_basic_date_filter():
    where, args = build_search_where(
        '2026-06-01', '2026-06-30', 'actual', 'none',
        None, None, None, True, '',
    )
    assert '$1' in where and '$2' in where
    assert args[0] == '2026-06-01'
    assert args[1] == '2026-06-30'


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
