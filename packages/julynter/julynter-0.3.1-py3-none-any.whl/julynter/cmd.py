import argparse
import sys
import pkg_resources
import os
import re
from jupyterlab import labapp, labextensions
from jupyterlab.commands import install_extension, build


RESOURCE_NAME = 'julynter'
PACKAGE_NAME = 'julynter-labextension-{}.tgz'
PACKAGE_RE = re.compile('^' + PACKAGE_NAME.format('(.*)\\'))


def lab_cmd(args, rest):
    path = pkg_resources.resource_filename(RESOURCE_NAME, 'julynterlab')
    os.environ['JUPYTERLAB_DIR'] = path
    labapp.LabApp.app_dir = os.environ['JUPYTERLAB_DIR']
    labapp.LabApp.launch_instance(argv=rest)

def labextension_cmd(args, rest):
    path = pkg_resources.resource_filename(RESOURCE_NAME, 'julynterlab')
    os.environ['JUPYTERLAB_DIR'] = path
    labextensions.BaseExtensionApp.app_dir = os.environ['JUPYTERLAB_DIR']
    labextensions.LabExtensionApp.launch_instance(argv=rest)


def version_tuple(version):
    parts = version.split('.')
    return tuple(int(x) if x.isnumeric() else x for x in parts)


def install_cmd(args, rest):
    files = pkg_resources.resource_listdir(RESOURCE_NAME, 'labextension')
    versions = [version_tuple(PACKAGE_RE.sub(r'\1', x)) for x in files]
    latest = max(versions)
    latest_file = PACKAGE_NAME.format('.'.join(map(str, latest)))
    resource_file = pkg_resources.resource_filename(RESOURCE_NAME, 'labextension/' + latest_file)
    print('Installing labextension')
    install_extension(resource_file)
    build()


def base_experiment_cmd(args, rest):
    if not getattr(args, 'expfunc', None):
        args.command.print_help()
    else:
        args.expfunc(args)


def start_experiment_cmd(args, rest):
    print("ToDo Start")


def end_experiment_cmd(args, rest):
    print("ToDo End")


def zip_experiment_cmd(args, rest):
    print("ToDo zip")


def main():
    parser = argparse.ArgumentParser(description='Lint Jupyter Notebooks')
    subparsers = parser.add_subparsers()

    labparser = subparsers.add_parser('lab', help="Start Jupyter Lab with Julynter", add_help=False)
    labparser.set_defaults(func=lab_cmd, command=labparser)

    labextensionparser = subparsers.add_parser('labextension', help="Run Jupyter labextension from Julynter", add_help=False)
    labextensionparser.set_defaults(func=labextension_cmd, command=labextensionparser)

    installparser = subparsers.add_parser('install', help="Use nodejs to install the labextension")
    installparser.set_defaults(func=install_cmd, command=installparser)

    expparser = subparsers.add_parser('experiment', help="Configure Julynter experiment")
    expparser.set_defaults(func=base_experiment_cmd, command=expparser)
    expparser_sub = expparser.add_subparsers()
    expparser_start = expparser_sub.add_parser("start", help="Start Julynter experiment")
    expparser_stop = expparser_sub.add_parser("stop", help="Stop Julynter experiment")
    expparser_zip = expparser_sub.add_parser("zip", help="Zip current experiment results")



    expparser_start.set_defaults(expfunc=start_experiment_cmd)
    expparser_stop.set_defaults(expfunc=end_experiment_cmd)
    expparser_zip.set_defaults(expfunc=zip_experiment_cmd)

    args, rest = parser.parse_known_args()
    if not getattr(args, 'func', None):
        parser.print_help()
    else:
        args.func(args, rest)
