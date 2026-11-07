"""Create an ignored, machine-specific config; never overwrite existing secrets."""
import argparse
import configparser
import getpass
import os
import re
import secrets
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db-user", default=getpass.getuser())
    parser.add_argument("--db-name", default="db_seanmusic")
    parser.add_argument("--port", type=int, default=8079)
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("Use a port between 1024 and 65535.")
    target = ROOT / "seanmusic.conf"
    if target.exists():
        print("seanmusic.conf already exists; preserved without modification.")
        return
    config = configparser.ConfigParser(interpolation=None)
    config.read(ROOT / "config/seanmusic.conf.example")
    opts = config["options"]
    opts.update({
        "admin_passwd": secrets.token_urlsafe(48),
        "db_user": args.db_user,
        "db_name": args.db_name,
        "dbfilter": "^" + re.escape(args.db_name) + "$",
        "http_port": str(args.port),
        "addons_path": ",".join(str(ROOT / p) for p in (
            "custom_addons", "odoo/addons", "odoo/odoo/addons",
        )),
        "data_dir": str(ROOT / ".odoo-data"),
    })
    pg_dump = shutil.which("pg_dump")
    if pg_dump:
        opts["pg_path"] = str(Path(pg_dump).parent)
    # Exclusive creation prevents accidental replacement or a check/create race.
    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as output:
        config.write(output)
    print("Created seanmusic.conf with mode 0600. No database or user passwords changed.")


if __name__ == "__main__":
    main()
