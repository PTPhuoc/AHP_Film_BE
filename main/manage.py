#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from alembic.config import Config
from alembic import command


def run_migrations():
    try:
        alembic_path = os.path.join(os.path.dirname(__file__), "alembic.ini")
        alembic_cfg = Config(alembic_path)
        command.upgrade(alembic_cfg, "head")
        print("Đồng bộ Database thành công!")
    except Exception as ex:
        print("Lỗi trong quá trình đồng bộ: ", ex)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    run_migrations()
    main()
