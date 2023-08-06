from decimal import Decimal
from typing import List


from raider_admin.raider import Account, MalformedConfigurationError, Payout, PayoutStatus, RaiderAdmin, ConnectionError
import unittest
import datetime
from unittest.mock import MagicMock, PropertyMock, patch

HOST = "localhost"
DATABASE = "raider"
USER = "remote"
PASSWORD = "SECRET_PASSWORD"

SAMPLE_CONFIG = dict(
    host=HOST,
    database=DATABASE,
    user=USER,
    password=PASSWORD
)


class MockCursor(object):
    def __init__(self, result=None) -> None:
        self.close_called = False
        self.query = None
        self.query_args = ()
        self.result = result
        self.i = None

    def execute(self, query, query_args=None):
        self.query = query
        self.query_args = query_args

    def fetchall(self):
        return self.result

    def fetchmany(self, i):
        self.i = i
        return self.result

    def close(self):
        self.close_called = True


class MockConnection(object):

    def __init__(self, cursor=MockCursor()) -> None:
        self.rollback_called = False
        self.commit_called = False
        self.close_called = False
        self._cursor = cursor

    def rollback(self):
        self.rollback_called = True

    def commit(self):
        self.commit_called = True

    def close(self):
        self.close_called = True

    def cursor(self, prepared=False):
        return self._cursor


class VigilTestSuite(unittest.TestCase):

    def test_init(self):
        raider_admin = RaiderAdmin(
            HOST,
            DATABASE,
            USER,
            PASSWORD
        )

        assert raider_admin.host == HOST
        assert raider_admin.database == DATABASE
        assert raider_admin.user == USER
        assert raider_admin.password == PASSWORD

    def test_init_missing_param(self):
        self.assertRaises(ValueError, lambda: RaiderAdmin(None, None, None, None))

    def test_repr(self):
        raider_admin = RaiderAdmin(
            HOST,
            DATABASE,
            USER,
            PASSWORD
        )
        assert repr(raider_admin) == f"RaiderAdmin connected to {USER}@{HOST}/{DATABASE}"
        assert str(raider_admin) == f"RaiderAdmin connected to {USER}@{HOST}/{DATABASE}"

    def test_init_from_config(self):
        raider_admin = RaiderAdmin.from_config(SAMPLE_CONFIG)
        assert raider_admin.host == HOST
        assert raider_admin.database == DATABASE
        assert raider_admin.user == USER
        assert raider_admin.password == PASSWORD

    def test_init_from_config_case_insensitive(self):
        config = dict(
            HOST=HOST,
            DATABASE=DATABASE,
            USER=USER,
            PASSWORD=PASSWORD
        )
        raider_admin = RaiderAdmin.from_config(config)
        assert raider_admin.host == HOST
        assert raider_admin.database == DATABASE
        assert raider_admin.user == USER
        assert raider_admin.password == PASSWORD

    def test_config_missing_param(self):
        self.assertRaises(MalformedConfigurationError, lambda: RaiderAdmin.from_config({}))

    def test_try_connect_raises_error(self):
        raider_admin = RaiderAdmin.from_config(SAMPLE_CONFIG)
        self.assertRaises(ConnectionError, lambda: raider_admin._try_connect())

    def test_dataclass_payout(self):
        sample_record = (4, 1, Decimal('150.00'), 'EUR', 'processed', "blu", "bli", 2,
                         datetime.datetime(2020, 7, 10, 12, 37, 49),
                         datetime.datetime(2020, 7, 10, 12, 37, 49))
        payout = Payout.from_tuple(sample_record)
        assert payout
        assert payout.id == 4
        assert payout.number == 1
        assert payout.amount == 150
        assert payout.currency == "EUR"
        assert payout.status.value == PayoutStatus.Processed.value
        assert payout.account_id == 2
        assert payout.created_at == datetime.datetime(2020, 7, 10, 12, 37, 49)

    def test_payout_status_values(self):
        assert PayoutStatus('accepted') == PayoutStatus.Accepted
        assert PayoutStatus('pending') == PayoutStatus.Pending
        assert PayoutStatus('rejected') == PayoutStatus.Rejected
        assert PayoutStatus('processed') == PayoutStatus.Processed

    def test_dataclass_account(self):
        sample_record = (2, 'leon.morten@gmail.com', Decimal('1.00'), 'Leon Richter', 'Sophienhof 17', 'DE', 'paypal',
                         'suppoer@smartphoniker.de', datetime.datetime(2020, 7, 10, 12, 5, 26), datetime.datetime(2020, 7, 10, 12, 5, 26))
        account = Account.from_tuple(sample_record)
        assert account.id == 2
        assert account.email == "leon.morten@gmail.com"
        assert account.comission == 1
        assert account.full_name == "Leon Richter"
        assert account.address == "Sophienhof 17"
        assert account.country == "DE"
        assert account.payout_method == "paypal"
        assert account.payout_instructions == "suppoer@smartphoniker.de"
        assert account.created_at == datetime.datetime(2020, 7, 10, 12, 5, 26)

    def test_connection_context(self):

        with patch('raider_admin.raider.RaiderAdmin._try_connect')as mock_func:
            mock_conn = MockConnection()
            mock_func.return_value = mock_conn
            raider_admin = RaiderAdmin.from_config(SAMPLE_CONFIG)

            with raider_admin.connection() as conn:
                assert conn

            # assert commit and close are called if function does not raise an error
            assert mock_conn.commit_called
            assert mock_conn.close_called

            # but rollback was not called
            assert not mock_conn.rollback_called

    def test_connection_with_error(self):
        with patch('raider_admin.raider.RaiderAdmin._try_connect') as mock_func:
            mock_conn = MockConnection()
            mock_func.return_value = mock_conn
            raider_admin = RaiderAdmin.from_config(SAMPLE_CONFIG)

            try:
                with raider_admin.connection() as conn:
                    raise ValueError("Blub")
            except ValueError:
                pass

            # assert rollback and close are called if function does not raise an error
            assert mock_conn.rollback_called
            assert mock_conn.close_called

            # but commit not
            assert not mock_conn.commit_called

    def test_cursor_context(self):
        with patch('raider_admin.raider.RaiderAdmin._try_connect') as mock_func:
            mock_conn = MockConnection()
            mock_func.return_value = mock_conn
            raider_admin = RaiderAdmin.from_config(SAMPLE_CONFIG)

            assert not mock_conn._cursor.close_called

            with raider_admin.cursor() as cur:
                assert cur

            assert mock_conn._cursor.close_called

    def test_payout(self):
        with patch('raider_admin.raider.RaiderAdmin._try_connect') as mock_func:
            mock_cursor = MockCursor(result=[
                (
                    4, 1, Decimal('150.00'), 'EUR', 'processed', "blu", "bli", 2,
                    datetime.datetime(2020, 7, 10, 12, 37, 49),
                    datetime.datetime(2020, 7, 10, 12, 37, 49)
                )
            ])
            mock_conn = MockConnection(mock_cursor)
            mock_func.return_value = mock_conn
            raider_admin = RaiderAdmin.from_config(SAMPLE_CONFIG)

            payout = raider_admin.get_payout(34)

            assert payout
            assert isinstance(payout, Payout)

    def test_get_open_payouts(self):
        with patch('raider_admin.raider.RaiderAdmin._try_connect') as mock_func:
            mock_cursor = MockCursor(result=[
                (
                    4, 1, Decimal('150.00'), 'EUR', 'processed', "blu", "bli", 2,
                    datetime.datetime(2020, 7, 10, 12, 37, 49),
                    datetime.datetime(2020, 7, 10, 12, 37, 49)
                )
            ])
            mock_conn = MockConnection(mock_cursor)
            mock_func.return_value = mock_conn
            raider_admin = RaiderAdmin.from_config(SAMPLE_CONFIG)
            payouts = raider_admin.get_open_payouts()

            assert isinstance(payouts, List)
            assert isinstance(payouts[0], Payout)
            assert len(payouts) == 1

    def test_get_account_data(self):
        with patch('raider_admin.raider.RaiderAdmin._try_connect') as mock_func:
            mock_cursor = MockCursor(result=[
                (2, 'leon.morten@gmail.com', Decimal('1.00'), 'Leon Richter', 'Sophienhof 17', 'DE', 'paypal',
                 'suppoer@smartphoniker.de', datetime.datetime(2020, 7, 10, 12, 5, 26), datetime.datetime(2020, 7, 10, 12, 5, 26))
            ])
            mock_conn = MockConnection(mock_cursor)
            mock_func.return_value = mock_conn
            raider_admin = RaiderAdmin.from_config(SAMPLE_CONFIG)
            acc = raider_admin.get_account_data(45)

            assert isinstance(acc, Account)
            
    def test_set_status(self):
        with patch('raider_admin.raider.RaiderAdmin._try_connect') as mock_func:
            mock_cursor = MockCursor(result=[
                (2, 'leon.morten@gmail.com', Decimal('1.00'), 'Leon Richter', 'Sophienhof 17', 'DE', 'paypal',
                 'suppoer@smartphoniker.de', datetime.datetime(2020, 7, 10, 12, 5, 26), datetime.datetime(2020, 7, 10, 12, 5, 26))
            ])
            mock_conn = MockConnection(mock_cursor)
            mock_func.return_value = mock_conn
            raider_admin = RaiderAdmin.from_config(SAMPLE_CONFIG)

            assert raider_admin.set_status(34, PayoutStatus.Pending)
            self.assertTupleEqual(mock_cursor.query_args, (PayoutStatus.Pending.value, 34))
           