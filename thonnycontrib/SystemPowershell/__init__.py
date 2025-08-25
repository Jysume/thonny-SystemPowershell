import os
import platform
import sys
import subprocess

from thonny import get_runner, get_workbench
from thonny.common import get_augmented_system_path, get_exe_dirs
from thonny.misc_utils import inside_flatpak, show_command_not_available_in_flatpak_message
from thonny.running import get_environment_overrides_for_python_subprocess
from shutil import which

code = get_workbench().get_option("general.language")


def plugin_language() -> dict:
    add_command_args = dict(
    command_id = "OpenSystemPowershell",
    menu_name = "tools",
    handler = _open_system_pwsh,
    group = 80,
    image = "terminal",
    )
    if code == 'zh_CN':
        add_command_args['command_label'] = "打开系统 Powershell..."
    else:
        add_command_args['command_label'] = "Open system powershell..."
    return add_command_args


def run_in_terminal_keep_open(cmd, cwd, env_overrides={}):
    from thonny.running import get_environment_with_overrides

    env = get_environment_with_overrides(env_overrides)

    if not cwd or not os.path.exists(cwd):
        cwd = os.getcwd()

    if sys.platform == "win32":
        quoted_args = " ".join(
            map(lambda s: s if s == "|" else '"' + s + '"', cmd))
        term_cmd = "pwsh" if which("pwsh") else "powershell"
        cmd_line = """start {term_cmd} -NoExit -Command "{quoted_args}" """.format(
            term_cmd=term_cmd,
            quoted_args=quoted_args,
        )
        subprocess.Popen(cmd_line, cwd=cwd, env=env, shell=True)
    else:
        raise RuntimeError("Can't launch powershell in " + platform.system())


def _open_system_pwsh():
    if inside_flatpak():
        show_command_not_available_in_flatpak_message()
        return

    cwd = get_workbench().get_local_cwd()

    proxy = get_runner().get_backend_proxy()
    if proxy and proxy.has_custom_system_shell():
        proxy.open_custom_system_shell()
        return
    if proxy and proxy.has_local_interpreter():
        target_executable = proxy.get_target_executable()
    else:
        target_executable = sys.executable

    exe_dirs = get_exe_dirs()
    if hasattr(proxy, "get_exe_dirs") and proxy.get_exe_dirs():
        # use both backend and frontend exe dirs
        exe_dirs = proxy.get_exe_dirs() + exe_dirs

    env_overrides = get_environment_overrides_for_python_subprocess(
        target_executable)
    env_overrides["PATH"] = get_augmented_system_path(exe_dirs)

    explainer = os.path.join(os.path.dirname(__file__),
                             "explain_environment.py")
    cmd = [target_executable, explainer]

    activate = os.path.join(
        os.path.dirname(target_executable),
        "Activate.ps1",
    )

    if os.path.isfile(activate):
        del env_overrides["PATH"]
        if sys.platform == "win32":
            cmd = [activate, "|"] + cmd
        else:
            raise RuntimeError("Can't launch powershell in " + platform.system())

    return run_in_terminal_keep_open(cmd, cwd, env_overrides)


def load_plugin() -> None:
    get_workbench().add_command(**plugin_language())
