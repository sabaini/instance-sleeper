import argparse
from instancesleeper.sleeper import main


def create_parser():
    parser = argparse.ArgumentParser(
        description="Sleep or shutdown OpenStack instances not modified in some time."
    )
    parser.add_argument(
        "-e",
        "--exceptions",
        default="instance-exceptions.txt",
        help="Path to the instance-exceptions.txt file.",
    )
    parser.add_argument(
        "-m",
        "--max-age",
        type=int,
        default=20,
        help="Maximum modified age in days. Default: 20",
    )
    parser.add_argument(
        "--shutdown",
        action="store_true",
        help="Shutdown instances instead of suspending.",
    )
    parser.add_argument(
        "--project-exceptions",
        default="admin,services",
        help="Comma-separated list of project names to exclude from processing.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print messages about shutdown or suspend without actually performing the action.",
    )
    parser.add_argument(
        "--report-container",
        help="Bucket to upload a report of the program's operation.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Operate on all instances in the cloud, not just the ones in the default project.",
    )

    return parser


def run():
    parser = create_parser()
    args = parser.parse_args()
    main(
        args.exceptions,
        args.max_age,
        args.shutdown,
        args.project_exceptions,
        args.dry_run,
        args.report_container,
        args.all,
    )


if __name__ == "__main__":
    run()
