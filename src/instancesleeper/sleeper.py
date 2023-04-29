from dateutil import tz
import datetime
import os
import re
import tempfile

import openstack
from dateutil import parser as date_parser


def get_instances(conn, all_projects=False):
    return list(conn.compute.servers(all_projects=all_projects))


def filter_instances(instances, days=20, project_exceptions=None):
    if project_exceptions is None:
        project_exceptions = set()

    now = datetime.datetime.utcnow().replace(tzinfo=tz.UTC)
    delta = datetime.timedelta(days=days)
    return [
        instance
        for instance in instances
        if (
            now - date_parser.parse(instance.updated_at).replace(tzinfo=tz.UTC)
            > delta
            and instance.project_id not in project_exceptions
        )
    ]


def read_exceptions_patterns(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    return [
        re.compile(line.strip())
        for line in lines
        if not line.startswith("#") and line.strip()
    ]


def remove_exceptions(instances, except_patterns):
    return [
        instance
        for instance in instances
        if not any(
            re.match(pattern, instance.name) for pattern in except_patterns
        )
    ]


def shutdown_or_suspend_instances(
    conn, instances, shutdown=False, dry_run=False, report_container=None
):
    output_file = None

    if report_container:
        output_file = tempfile.NamedTemporaryFile(mode="w", delete=False)

    for instance in instances:
        action = "Shutting down" if shutdown else "Suspending"
        if dry_run:
            action = f"[DRY-RUN] {action}"

        print(f"{action} instance: {instance.name}", file=output_file or None)

        if not dry_run:
            if shutdown:
                conn.compute.stop_server(instance)
            else:
                conn.compute.suspend_server(instance)

    import pdb;pdb.set_trace()
    if report_container:
        output_file.close()
        current_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        conn.object_store.upload_object(
            report_container,
            "instance_sleeper_{}.txt".format(current_date),
            output_file.name,
        )
        os.unlink(output_file.name)


def main(
    instance_exceptions_path,
    max_age,
    shutdown=False,
    project_exceptions=None,
    dry_run=False,
    report_container=None,
    all_projects=False,
):
    conn = openstack.connect()

    #openstack.enable_logging(debug=True)

    instances = get_instances(conn, all_projects=all_projects)

    project_exceptions = (
        set(project_exceptions.split(",")) if project_exceptions else set()
    )
    filtered_instances = filter_instances(
        instances, max_age, project_exceptions
    )

    if os.path.exists(instance_exceptions_path):
        except_patterns = read_exceptions_patterns(instance_exceptions_path)
        final_instances = remove_exceptions(
            filtered_instances, except_patterns
        )
    else:
        final_instances = filtered_instances

    shutdown_or_suspend_instances(
        conn, final_instances, shutdown, dry_run, report_container
    )
