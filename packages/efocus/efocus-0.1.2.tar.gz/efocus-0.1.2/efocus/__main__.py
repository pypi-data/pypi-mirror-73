import click
from efocus import preload
import sys
import pathlib


@click.command()
@click.argument("script", default=None)
@click.option("--function", default=".*", help="The function name to filter.")
def main(script, function):
    if not script:
        return

    preload.implement(function)
    sys.path.insert(0, str(pathlib.Path(script).parent))
    exec(open(script, "rt").read(), globals())


if __name__ == "__main__":
    main()
