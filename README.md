# README

Sleep or shutdown instances that have not been touched in some time, in order to save on resources on a test or dev cloud.


## Usage

```
usage: instancesleeper [-h] [-e EXCEPTIONS] [-m MAX_AGE] [--shutdown] [--project-exceptions PROJECT_EXCEPTIONS] [--dry-run] [--report-container REPORT_CONTAINER] [--all]

Sleep or shutdown OpenStack instances not modified in some time.

options:
  -h, --help            show this help message and exit
  -e EXCEPTIONS, --exceptions EXCEPTIONS
                        Path to the instance-exceptions.txt file.
  -m MAX_AGE, --max-age MAX_AGE
                        Maximum modified age in days. Default: 20
  --shutdown            Shutdown instances instead of suspending.
  --project-exceptions PROJECT_EXCEPTIONS
                        Comma-separated list of project names to exclude from processing.
  --dry-run             Print messages about shutdown or suspend without actually performing the action.
  --report-container REPORT_CONTAINER
                        Bucket to upload a report of the program's operation.
  --all                 Operate on all instances in the cloud, not just the ones in the default project.

```
