"""Django command to wait for DB to become available"""

import time

from django.core.management.base import BaseCommand

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError


class Command(BaseCommand):

    def handle(self, *args, **optional):
        """Entrypoint for command"""
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("DB unavailable... waiting for 1 second")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("DB available"))
