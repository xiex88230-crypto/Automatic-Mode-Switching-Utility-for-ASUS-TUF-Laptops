import tempfile
import unittest
from pathlib import Path

from mode_switcher import BALANCED_MODE, SILENT_MODE, TURBO_MODE, ModeSwitcher, load_whitelist


class ModeSwitcherTests(unittest.TestCase):
    def test_turbo_mode_when_whitelisted_app_is_running(self) -> None:
        switcher = ModeSwitcher(high_performance_apps={"game", "blender.exe"})
        mode = switcher.determine_mode(["python", "/games/Blender.exe"])
        self.assertEqual(mode, TURBO_MODE)

    def test_balanced_mode_when_non_whitelisted_user_apps_are_running(self) -> None:
        switcher = ModeSwitcher(high_performance_apps={"eldenring"})
        mode = switcher.determine_mode(["firefox", "code"])
        self.assertEqual(mode, BALANCED_MODE)

    def test_silent_mode_when_only_ignored_processes_are_running(self) -> None:
        switcher = ModeSwitcher(
            high_performance_apps={"eldenring"},
            ignored_processes={"systemd", "init"},
        )
        mode = switcher.determine_mode(["systemd", "init"])
        self.assertEqual(mode, SILENT_MODE)


class WhitelistTests(unittest.TestCase):
    def test_load_whitelist_ignores_comments_and_empty_lines(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            whitelist_file = Path(temp_dir) / "whitelist.txt"
            whitelist_file.write_text(
                "# comment\n\nblender\n game.exe \n",
                encoding="utf-8",
            )
            whitelist = load_whitelist(whitelist_file)
            self.assertEqual(whitelist, {"blender", "game.exe"})


if __name__ == "__main__":
    unittest.main()
