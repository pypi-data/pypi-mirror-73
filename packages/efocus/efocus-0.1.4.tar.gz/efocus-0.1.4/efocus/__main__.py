import click
from efocus import preload
import sys
import pathlib


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.argument("script")
@click.option(
    "-f",
    "--function",
    default=".*",
    help="Show only output originated by function that matches regex.",
)
@click.option(
    "-e", "--log-enter", is_flag=True, default=False, help="Log function enter",
)
@click.command(name="python", context_settings=CONTEXT_SETTINGS)
def main(script, function, log_enter):
    """
    Used to filter prints and to log desired execution data.

    SCRIPT is the path to the python script to be executed.
    """
    preload.run(function, log_enter)
    sys.path.insert(0, str(pathlib.Path(script).parent))
    exec(open(script, "rt").read(), globals())


if __name__ == "__main__":
    main(prog_name="python3 -m efocus")  # Call with explicit `prog_name`
