import shutil
import getpass
import subprocess
import typer

from pathlib import Path

from watchdog.observers import Observer

from anxiety.should_be_deleted.hanlder import DownloadFolderHandler
from anxiety.nice_desk.handler import NiceDeskHandler


app = typer.Typer(help="Personal project to keep my download folder organized.")

command_name = "anxiety"
plist_file_name = "me.steban.www.anxiety.plist"


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Hacking my Digital Hoarding, one file at a time.
    """
    if ctx.invoked_subcommand is None:
        banner = """
    ___                _      __       
   /   |  ____  _  __(_)__  / /___  __
  / /| | / __ \| |/_/ / _ \/ __/ / / /
 / ___ |/ / / />  </ /  __/ /_/ /_/ / 
/_/  |_/_/ /_/_/|_/_/\___/\__/\__, /  
                             /____/   
        """
        typer.secho(banner, fg="cyan", bold=True)
        typer.secho("🚀 Hacking the Digital Hoarding, one file at a time.\n", fg="yellow", bold=True)
        
        motivation = (
            "This project was born from the need to manage the cognitive load of a cluttered "
            "Downloads and Desktop folder. It moves files to a 'transition zone' to reduce the "
            "anxiety of immediate deletion, helping you maintain a zen-like workspace automatically."
        )
        typer.echo(motivation)
        typer.echo("\nUse --help to see available commands.")


@app.command()
def watch(
    should_be_deleted: bool = typer.Option(
        False, "-s", "--nice_download", help="Keep your download folder nice."
    ),
    nice_desktop: bool = typer.Option(
        False, "-d", "--nice_desktop", help="Keep your desktop folder nice."
    ),
):
    """
    Watch your Downloads folder for new files.
    """

    if not should_be_deleted and not nice_desktop:
        should_be_deleted = True
        nice_desktop = True

    observer = Observer()

    if should_be_deleted:
        observer.schedule(
            DownloadFolderHandler(), DownloadFolderHandler.get_folder(), recursive=True
        )

    if nice_desktop:
        observer.schedule(
            NiceDeskHandler(), NiceDeskHandler.get_folder(), recursive=True
        )

    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()


def _get_target_plist_file_path() -> Path:
    return Path(f"~/Library/LaunchAgents/{plist_file_name}").expanduser()


@app.command()
def init(
    nice_download: bool = typer.Option(
        False, "-s", "--nice_download", help="Watch Downloads folder only."
    ),
    nice_desktop: bool = typer.Option(
        False, "-d", "--nice_desktop", help="Watch Desktop folder only."
    ),
):
    """
    Run anxiety in the background.
    """

    # Apply to strategies/mode if any strategy is passed by argument
    if not nice_download and not nice_desktop:
        nice_download = True
        nice_desktop = True

    # arguments for anxiety command for the plist file
    program_args = ["<string>watch</string>"]
    if nice_download:
        program_args.append("<string>--nice_download</string>")
    if nice_desktop:
        program_args.append("<string>--nice_desktop</string>")

    program_arguments_xml = "\n".join(program_args)

    root_path = Path(__file__).parent

    with open(root_path / "plist.xml", "r") as f:
        plist_content = f.read().format(
            username=getpass.getuser(),
            command_path=shutil.which(command_name),
            program_arguments=program_arguments_xml,
        )

    plist_file = _get_target_plist_file_path()
    plist_file.parent.mkdir(parents=True, exist_ok=True)
    plist_file.write_text(plist_content)

    result = subprocess.run(
        ["launchctl", "load", str(plist_file)],
        check=True,
        capture_output=True,
        text=True,
    )

    result.check_returncode()

    typer.secho("Initialized successfully!", fg="green")


@app.command()
def stop():
    """
    Stop the background process.
    """
    result = subprocess.run(
        ["launchctl", "unload", str(_get_target_plist_file_path())],
        capture_output=True,
        text=True,
    )

    result.check_returncode()

    typer.secho("Stopped successfully!", fg="green")


@app.command()
def status():
    """
    Check if anxiety is running.
    """
    process_name = plist_file_name.replace(".plist", "")

    result = subprocess.run(
        ["launchctl", "list", process_name], capture_output=True, text=True
    )

    try:
        result.check_returncode()

        plist_file = _get_target_plist_file_path()
        strategies = []

        if plist_file.exists():
            with open(plist_file, "r") as f:
                content = f.read()
                if "--nice_download" in content or "nice_download" in content:
                    strategies.append("nice_download")
                if "--nice_desktop" in content or "nice_desktop" in content:
                    strategies.append("nice_desktop")

        if strategies:
            typer.secho(
                f"Service is running with strategies: {', '.join(strategies)}",
                fg="green",
            )
        else:
            typer.secho("Service is running", fg="green")

    except subprocess.CalledProcessError as e:
        if e.returncode == 113:
            typer.secho("Service is not running!", fg="red")
        else:
            raise e


if __name__ == "__main__":
    app()
