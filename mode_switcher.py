from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Iterable

TURBO_MODE = "turbo"
BALANCED_MODE = "balanced"
SILENT_MODE = "silent"


class ModeSwitcher:
    def __init__(
        self,
        high_performance_apps: Iterable[str],
        ignored_processes: Iterable[str] | None = None,
    ) -> None:
        self.high_performance_apps = {
            self._normalize_process_name(name) for name in high_performance_apps if name
        }
        self.ignored_processes = {
            self._normalize_process_name(name)
            for name in (ignored_processes or ("systemd", "kthreadd", "init"))
            if name
        }

    @staticmethod
    def _normalize_process_name(name: str) -> str:
        return Path(name.strip()).stem.lower()

    def determine_mode(self, running_applications: Iterable[str]) -> str:
        normalized_apps = {
            self._normalize_process_name(app) for app in running_applications if app
        }
        if normalized_apps & self.high_performance_apps:
            return TURBO_MODE

        user_apps = normalized_apps - self.ignored_processes
        return BALANCED_MODE if user_apps else SILENT_MODE

    def get_running_applications(self) -> list[str]:
        result = subprocess.run(
            ["ps", "-eo", "comm="],
            capture_output=True,
            text=True,
            check=True,
        )
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]

    def select_mode(self) -> str:
        return self.determine_mode(self.get_running_applications())


def load_whitelist(path: Path) -> set[str]:
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }


def switch_mode(mode: str, dry_run: bool = False) -> str:
    mode_to_profile = {
        TURBO_MODE: "turbo",
        BALANCED_MODE: "balanced",
        SILENT_MODE: "quiet",
    }
    if mode not in mode_to_profile:
        raise ValueError(f"Unsupported mode: {mode}")

    command = ["asusctl", "profile", "-P", mode_to_profile[mode]]
    if not dry_run:
        subprocess.run(command, check=True)
    return " ".join(command)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Automatically select ASUS laptop performance mode from running apps.",
    )
    parser.add_argument(
        "--whitelist",
        type=Path,
        required=True,
        help="Path to a newline-delimited list of high-performance applications.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print mode command without applying it.",
    )
    args = parser.parse_args()

    whitelist = load_whitelist(args.whitelist)
    switcher = ModeSwitcher(high_performance_apps=whitelist)
    mode = switcher.select_mode()
    command = switch_mode(mode, dry_run=args.dry_run)
    print(f"Selected mode: {mode}")
    print(f"Command: {command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
