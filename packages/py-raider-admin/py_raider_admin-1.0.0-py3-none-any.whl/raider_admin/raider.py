"""
Raider admin code.
"""
import contextlib
from dataclasses import dataclass
import datetime
import decimal
from enum import Enum
import functools
import re
import typing
from unittest.main import main
import mysql.connector as mysql
from mysql.connector import Error

# Custom exceptions


class ConnectionError(Exception):
    pass


class MalformedConfigurationError(Exception):
    pass


class PayoutStatus(Enum):
    """
    These are all possible status values a payout can have.
    """
    Undefined = ''
    Accepted = 'accepted'
    Pending = 'pending'
    Rejected = 'rejected'
    Processed = 'processed'

# Dataclasses


@dataclass
class Payout:
    id: int
    number: int
    amount: decimal.Decimal
    currency: str
    status: PayoutStatus
    account: str
    invoice_url: str
    account_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    def from_tuple(cls, payout_values: typing.Tuple[int, int, decimal.Decimal, str, str, str, str, int, datetime.datetime, datetime.datetime]):
        return cls(
            id=payout_values[0],
            number=payout_values[1],
            amount=payout_values[2],
            currency=payout_values[3],
            status=(PayoutStatus(payout_values[4]) if payout_values[4] else PayoutStatus.Undefined),
            account=payout_values[5],
            invoice_url=payout_values[6],
            account_id=payout_values[7],
            created_at=payout_values[8],
            updated_at=payout_values[9],
        )


@dataclass
class Account:
    id: int
    email: str
    comission: decimal.Decimal
    full_name: str
    address: str
    country: str
    payout_method: str
    payout_instructions: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    def from_tuple(cls, values: typing.Tuple[int, str, decimal.Decimal, str, str, str, str, str, datetime.datetime, datetime.datetime]):
        return cls(
            id=values[0],
            email=values[1],
            comission=values[2],
            full_name=values[3],
            address=values[4],
            country=values[5],
            payout_method=values[6],
            payout_instructions=values[7],
            created_at=values[8],
            updated_at=values[9],
        )


class RaiderAdmin(object):

    __slots__ = (
        'host',
        'database',
        'user',
        'password',
    )

    def __init__(
        self,
        host: str,
        database: str,
        user: str,
        password: str
    ) -> None:
        """
        You either have to run this script on the same machine as your DB is running on or expose the db to the outide world.
        If you decide to do the latter, you should create a special user with limited privileges for that.
        """
        self.host: str = host
        self.database: str = database
        self.user: str = user
        self.password: str = password

        # all these values are needed
        for attr in ('host', 'database', 'user', 'password'):
            if not getattr(self, attr):
                raise ValueError(f"{attr} must not be None!")

    def __repr__(self) -> str:
        return f"RaiderAdmin connected to {self.connection_string}"

    @property
    def connection_string(self):
        return f"{self.user}@{self.host}/{self.database}"

    @classmethod
    def from_config(cls, config: typing.Dict):
        """
        Convenience method. 
        Make sure your dict has the following keys: [host, database, user, password]
        """
        config = {k.lower(): v for k, v in config.items()}
        try:
            return cls(
                host=config['host'],
                database=config['database'],
                user=config['user'],
                password=config['password'],
            )
        except KeyError as e:
            raise MalformedConfigurationError("Your Config is malformed!") from e

    def _try_connect(self):
        """
        Try to connec to to MySQL and raise an ConnectionError on error
        """
        try:
            return mysql.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                passwd=self.password
            )
        except Error as e:
            raise ConnectionError(f"Could not connect to {self.connection_string}") from e

    @contextlib.contextmanager
    def connection(self):
        """
        Custom context manager that handles commits, rollbacks and closes.
        Usage:

        >>> with self.connection() as conn:
                # do something
        """
        connection = self._try_connect()

        try:
            yield connection
        except Exception:
            connection.rollback()
            raise
        else:
            connection.commit()
        finally:
            connection.close()

    @contextlib.contextmanager
    def cursor(self):
        """
        Custom context manager that handles closing the cursor.
        Usage:
        >>> with self.cursor() as cur:
                # do something
        """
        with self.connection() as conn:
            cursor = conn.cursor(prepared=True)
            try:
                yield cursor
            finally:
                cursor.close()

    # Actual queries below

    def get_payout(self, payout_id: int) -> typing.Optional[Payout]:
        with self.cursor() as cur:
            query = "SELECT * FROM `payout` WHERE `payout`.`id`=%s;"
            cur.execute(query, (payout_id,))
            record = cur.fetchmany(1)
            if record and len(record):
                return Payout.from_tuple(record[0])
            return None

    def get_open_payouts(self, limit: int = 100, offset: int = 0) -> typing.List[Payout]:
        with self.cursor() as cur:
            query = "SELECT * FROM `payout` WHERE `payout`.`status`=\"pending\" ORDER BY `payout`.`updated_at` LIMIT %s OFFSET %s;"
            cur.execute(query, (limit, offset))
            records = cur.fetchall()
            return [Payout.from_tuple(payout) for payout in records]

    def get_all_payouts(self, limit: int = 100, offset: int = 0) -> typing.List[Payout]:
        with self.cursor() as cur:
            query = "SELECT * FROM `payout` ORDER BY `payout`.`updated_at` LIMIT %s OFFSET %s;"
            cur.execute(query, (limit, offset))
            records = cur.fetchall()
            return [Payout.from_tuple(payout) for payout in records]

    def get_account_data(self, acc_id: int) -> typing.Optional[Account]:
        with self.cursor() as cur:
            query = "SELECT `account`.id, `account`.`email`, `account`.`commission`, `account`.`full_name`, `account`.`address`,`account`.`country`, `account`.`payout_method`, `account`.`payout_instructions`, `account`.`created_at`, `account`.`updated_at` FROM `account` WHERE `account`.`id`=%s;"
            cur.execute(query, (acc_id,))
            record = cur.fetchmany(1)
            if record and len(record):
                return Account.from_tuple(record[0])
            return None

    def set_status(self, payout_id: int, status: PayoutStatus) -> bool:
        with self.cursor() as cur:
            query = "UPDATE `payout` SET `status` = %s WHERE `payout`.`id` = %s;"
            cur.execute(query, (status.value, payout_id))
            return True
