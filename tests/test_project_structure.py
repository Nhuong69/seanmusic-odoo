"""No database/network writes: reproducibility and repository safety checks."""
import ast
import configparser
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]


def load_script(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProjectStructureTests(unittest.TestCase):
    def test_reference_images_resolve(self):
        manifest = json.loads((ROOT / "assets/products/references/sources.json").read_text())
        self.assertTrue(manifest)
        for code, source in manifest.items():
            with self.subTest(code=code):
                photo = (ROOT / source["file"]).resolve()
                self.assertTrue(photo.is_relative_to(ROOT / "assets/products/references"))
                self.assertTrue(photo.is_file())
                self.assertTrue(source["page"].startswith("https://"))
                image_url = urlparse(urljoin(source["page"], source["url"]))
                self.assertIn(image_url.scheme, ("http", "https"))
                self.assertTrue(image_url.hostname)

    def test_private_paths_are_ignored(self):
        paths = ["seanmusic.conf", "odoo.conf", ".venv/", ".odoo-data/", ".idea/", "artifacts/", "backups/sample.dump"]
        result = subprocess.run(["git", "check-ignore", "--", *paths], cwd=ROOT, capture_output=True, text=True, check=True)
        self.assertEqual(set(result.stdout.splitlines()), set(paths))
        tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
        self.assertFalse(set(paths[:2]) & set(tracked))
        self.assertFalse(any(p.startswith((".odoo-data/", ".venv/", ".idea/")) for p in tracked))

    def test_upstream_is_pinned_submodule(self):
        modules = configparser.ConfigParser()
        modules.read(ROOT / ".gitmodules")
        self.assertEqual(modules['submodule "odoo"']["path"], "odoo")
        head = subprocess.check_output(["git", "-C", str(ROOT / "odoo"), "rev-parse", "HEAD"], text=True).strip()
        entry = subprocess.check_output(["git", "ls-files", "--stage", "odoo"], cwd=ROOT, text=True).split()
        self.assertEqual(entry[:2], ["160000", head])

    def test_manifest_dependencies_and_test_discovery(self):
        home = ast.literal_eval((ROOT / "custom_addons/sean_music_home/__manifest__.py").read_text())
        self.assertEqual(set(home["depends"]), {"web", "website"})
        for addon in ("sean_music_store", "sean_music_collaborator"):
            tests = ROOT / "custom_addons" / addon / "tests"
            imports = (tests / "__init__.py").read_text()
            files = list(tests.glob("test_*.py"))
            self.assertTrue(files)
            for file in files:
                self.assertIn(file.stem, imports)
                ast.parse(file.read_text())

    def test_shared_ide_configuration(self):
        launch = json.loads((ROOT / ".vscode/launch.json").read_text())
        for item in launch["configurations"]:
            self.assertIn("${workspaceFolder}/seanmusic.conf", item["args"])
            self.assertEqual(item["python"], "${workspaceFolder}/.venv/bin/python")
        run = ElementTree.parse(ROOT / ".run/Sean Music local.run.xml")
        options = {el.get("name"): el.get("value") for el in run.findall(".//option")}
        self.assertEqual(options["SDK_HOME"], "$PROJECT_DIR$/.venv/bin/python")
        self.assertIn("seanmusic.conf", options["PARAMETERS"])

    def test_config_generator_is_portable_and_does_not_overwrite(self):
        script = load_script("init_config", "scripts/dev/init_local_config.py")
        with tempfile.TemporaryDirectory(prefix="seanmusic-config-test-") as directory:
            root = Path(directory)
            (root / "config").mkdir()
            (root / "config/seanmusic.conf.example").write_bytes((ROOT / "config/seanmusic.conf.example").read_bytes())
            with patch.object(script, "ROOT", root), patch("sys.argv", ["init_local_config.py", "--db-user", "test_role"]):
                script.main()
                target = root / "seanmusic.conf"
                first = target.read_bytes()
                script.main()
                self.assertEqual(first, target.read_bytes())
            config = configparser.ConfigParser(interpolation=None)
            config.read(target)
            self.assertEqual(config["options"]["http_port"], "8079")
            self.assertEqual(config["options"]["http_interface"], "127.0.0.1")
            self.assertEqual(config["options"]["db_user"], "test_role")
            self.assertNotEqual(config["options"]["admin_passwd"], "CHANGE_ME")
            self.assertEqual(target.stat().st_mode & 0o777, 0o600)
            self.assertIn(str(root / "custom_addons"), config["options"]["addons_path"])

    def test_test_runner_rejects_working_database(self):
        runner = load_script("test_runner", "scripts/checks/run_odoo_tests.py")
        for name in ("db_seanmusic", "postgres", "db_seanmusic_test_", "db_seanmusic_test_bad-name"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                runner.validate_database(name)
        self.assertEqual(runner.validate_database("db_seanmusic_test_isolated"), "db_seanmusic_test_isolated")


if __name__ == "__main__":
    unittest.main()
