import subprocess
import sys

from big_boy_benchmarking.cli.main import main


def test_validate_contracts_command_works() -> None:
    assert main(["validate-contracts"]) == 0


def test_module_help_works() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "big_boy_benchmarking.cli", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "validate-contracts" in result.stdout


def test_unknown_command_exits_nonzero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "big_boy_benchmarking.cli", "nope"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
