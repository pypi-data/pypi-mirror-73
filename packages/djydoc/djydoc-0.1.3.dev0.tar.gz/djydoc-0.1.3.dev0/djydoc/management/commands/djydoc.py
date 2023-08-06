import logging
import argparse
from django.core.management.base import BaseCommand, CommandError
import django
import pydoc
import sys

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Runs the pydoc command with Django loaded"

    def add_arguments(self, parser):
        parser.add_argument("--port", "-p", type=int)
        parser.add_argument("--keyword", "-k", type=str)
        parser.add_argument("--hostname", "-n", type=str)
        parser.add_argument("--any-port", "-b", action="store_true")
        parser.add_argument("--write-out", "-w", type=argparse.FileType("w"))
        parser.add_argument("name", nargs="*", type=str)

    def bootstrap_django(self):
        django.setup()

    def handle(self, *args, **options):
        port = options.get("port", None)
        hostname = options.get("hostname", None)
        any_port = options.get("hostname", None)

        self.bootstrap_django()

        if port or hostname:
            pydoc.browse(port=port, hostname=hostname or "0.0.0.0")
            sys.exit(0)

        name = options.get("name", None)
        if name:
            help(*name)
