"""Run custom addon tests on a NEW isolated database, never the working database."""
import argparse
import configparser
import datetime
import re
import subprocess
import sys
from pathlib import Path

import psycopg2


ROOT = Path(__file__).resolve().parents[2]


def validate_database(name):
    if not re.fullmatch(r"db_seanmusic_test_[a-z0-9_]{1,40}", name):
        raise ValueError("Test database must start with db_seanmusic_test_ and contain only a-z, 0-9, _.")
    return name


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--create-test-db", action="store_true")
    parser.add_argument("--database", default="db_seanmusic_test_" + datetime.datetime.now(datetime.UTC).strftime("%Y%m%d_%H%M%S"))
    args = parser.parse_args()
    if not args.create_test_db:
        parser.error("Explicit --create-test-db consent is required; the new database is kept after tests.")
    try:
        database = validate_database(args.database)
    except ValueError as error:
        parser.error(str(error))
    config_file = ROOT / "seanmusic.conf"
    config = configparser.ConfigParser(interpolation=None)
    if not config.read(config_file):
        parser.error("Create seanmusic.conf first with scripts/dev/init_local_config.py.")
    opts = config["options"]
    connect = {"dbname": "postgres", "connect_timeout": 10}
    for setting, key in (("db_host", "host"), ("db_port", "port"), ("db_user", "user"), ("db_password", "password")):
        value = opts.get(setting)
        if value and value.lower() not in ("false", "none"):
            connect[key] = value
    with psycopg2.connect(**connect) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database,))
            if cursor.fetchone():
                parser.error("Refusing an existing database. Choose a new test name; no database was modified.")
    log_dir = ROOT / "artifacts/tests" / database
    log_dir.mkdir(parents=True, exist_ok=False)
    command = [
        sys.executable, str(ROOT / "odoo/odoo-bin"), "-c", str(config_file),
        "-d", database, "--db-filter", "^" + database + "$",
        "--data-dir", str(log_dir / "odoo-data"),
        "-i", "sean_music_store,sean_music_collaborator",
        "--test-enable", "--test-tags", "/sean_music_store,/sean_music_collaborator",
        "--without-demo", "--no-http", "--stop-after-init", "--max-cron-threads=0",
    ]
    print("Creating isolated test database:", database, flush=True)
    print("Logs:", log_dir / "odoo.log", flush=True)
    with (log_dir / "odoo.log").open("w") as log:
        result = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    print("TEST_EXIT", result.returncode, "DB kept:", database, flush=True)
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
