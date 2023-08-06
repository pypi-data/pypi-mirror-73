import os
import shutil
import subprocess
import sys
import termcolor

from .lib.skeleton import Skeleton
from .lib.argumentparser import InitArgumentParser
from .exceptions import B5ExecutionError


def _run_cmd(cmd, error='Command execution failed, see above'):
    try:
        subprocess.run(
            cmd,
            shell=False,
            check=True,
        )
    except subprocess.CalledProcessError:
        termcolor.cprint(error, color='red')
        sys.exit(1)


def main():
    try:
        parser = InitArgumentParser('b5-init', 'b5-init might be used to setup new projects')
        parser.add_arguments()
        args = parser.parse()

        skeleton = Skeleton(args.skeleton)
        branch = args.branch
        path = args.path

        full_path = os.path.realpath(os.path.join(os.getcwd(), path))
        os.makedirs(full_path, exist_ok=True)

        if os.listdir(full_path):
            raise B5ExecutionError('Cannot init an existing directory if not empty')

        _run_cmd(['git', 'clone', skeleton.get_url(), full_path], 'Could not clone skeleton repository, see above')
        os.chdir(full_path)
        if not branch is None:
            _run_cmd(['git', 'checkout', branch], 'Could not checkout required branch, see above')

        shutil.rmtree(os.path.join(full_path, '.git'))
        _run_cmd(['git', 'init', '.'])
        init_path = os.path.join(full_path, 'init')
        if os.path.exists(init_path) and os.path.exists(os.path.join(init_path, 'Taskfile')):
            _run_cmd(['b5',
                      '--quiet',
                      '--run-path', 'init',
                      '--config', 'config.yml',
                      '--config', 'config.init.yml',
                      '--config', 'config.local.yml',
                      'project:init'])
            shutil.rmtree(init_path)
        # _run_cmd(['git', 'add', '-A'])
        termcolor.cprint('Successful initialized {path}'.format(path=path), 'green')
        termcolor.cprint('  skeleton used: {skeleton_url}'.format(skeleton_url=skeleton.get_url()), 'green')
        termcolor.cprint('  project path: {full_path}'.format(full_path=full_path), 'green')
    except B5ExecutionError as error:
        termcolor.cprint(str(error), 'red')
        sys.exit(1)
