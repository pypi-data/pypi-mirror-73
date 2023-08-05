import argparse
import os
import re
import jinja2

PROJECT_NAME_EXPRESSION = re.compile(r"^[a-zA-Z0-9_]+$")


def copy_sources(src_dir, dst_dir, appname):
    print(src_dir, dst_dir)
    context = {"appname": appname}
    for srcname in os.listdir(src_dir):
        srcname = os.path.join(src_dir, srcname)
        dstname = os.path.join(dst_dir, os.path.basename(srcname))
        dstname = dstname.replace("__appname__", appname)
        print(srcname, dstname)
        if os.path.isdir(srcname):
            os.makedirs(dstname)
            copy_sources(srcname, dstname, appname)
        elif os.path.isfile(srcname):
            with open(srcname) as tmplfile:
                tmpl = jinja2.Template(tmplfile.read())
                with open(dstname, "w") as outfile:
                    outfile.write(tmpl.render(context))


def run_create(args):
    appname = args.project_name[0]
    dirname = appname
    if not PROJECT_NAME_EXPRESSION.match(dirname):
        raise ValueError(f"Invalid project name {dirname}")
    dirname = os.path.abspath(f"./{dirname}")

    project_templates_dir = os.path.join(os.path.dirname(__file__), "project_templates")
    project_templates_dir = os.path.abspath(project_templates_dir)

    os.makedirs(dirname, exist_ok=False)
    copy_sources(project_templates_dir, dirname, appname)


def run_new_model(args):
    pass


def run_new_controller(args):
    pass


def run_new_task(args):
    pass


def main():
    parser = argparse.ArgumentParser(prog="glasskit")
    subparsers = parser.add_subparsers(dest="command", required=True, help="sub-command help")

    parser_create = subparsers.add_parser("create", help="bootstrap a new glasskit project")
    parser_create.add_argument("project_name", nargs=1, type=str, help="project name to create")

    parser_new = subparsers.add_parser("new", help="create a new unit, i.e. model, controller, task")
    parser_new.add_argument("unit", nargs=1, type=str, choices=["model", "controller", "task"])
    args = parser.parse_args()

    if args.command == "create":
        run_create(args)
    elif args.command == "new":
        unit_type = args.unit[0]
        if unit_type == "model":
            run_new_model(args)
        elif unit_type == "controller":
            run_new_controller(args)
        elif unit_type == "task":
            run_new_task(args)
        else:
            raise ValueError(f"unknown unit type f{unit_type}")


if __name__ == "__main__":
    main()
