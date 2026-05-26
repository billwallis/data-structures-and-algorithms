import argparse
import logging
import pathlib
import shutil
from collections.abc import Sequence

SUCCESS = 0
FAILURE = 1
ROOT = pathlib.Path(__file__).parent.parent
FILES_TO_COPY = [
    ".github/workflows/tests.yaml",
    ".gitignore",
    ".pre-commit-config.yaml",
    "LICENSE",
    "pyproject.toml",
]


def _copy_file_to_target(
    source: pathlib.Path,
    destination: pathlib.Path,
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(source, destination)


def copy_files_to_target(target: pathlib.Path) -> int:
    if not target.exists():
        logging.error(f"target {target} does not exist")
        return FAILURE
    if not target.is_dir():
        logging.error(f"target {target} is not a directory")
        return FAILURE

    ret = SUCCESS
    for file in FILES_TO_COPY:
        try:
            _copy_file_to_target(source=ROOT / file, destination=target / file)
        except Exception as e:
            logging.error(str(e))
            ret = FAILURE

    return ret


def main(argv: Sequence[str] | None = None) -> int:
    """
    Parse the arguments and run the command.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("targets", nargs="*")

    args = parser.parse_args(argv)
    ret = SUCCESS
    if not args.targets:
        parser.print_help()
    for target in args.targets:
        ret |= copy_files_to_target(target=pathlib.Path(target).resolve())

    return ret


if __name__ == "__main__":
    # python -m tools.apply <target>
    raise SystemExit(main())
