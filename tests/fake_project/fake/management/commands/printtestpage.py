import json
import re
from functools import partial

from django.core.management.base import BaseCommand, CommandParser
from django.test import Client

from gesha.conf import get_setting

JSON_INDENT_LEVEL: int = 2


class Command(BaseCommand):
    help = (
        "GET the home page using Django's test client and write the HTML response to "
        "stdout."
    )

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-o",
            "--outfile",
            action="store",
            help="Write to file instead of stdout.",
        )
        parser.add_argument(
            "-p",
            "--pretty",
            action="store_true",
            default=False,
            help="Prettify JSON in gesha's <script> tag.",
        )

    def handle(self, *args, **options) -> None:
        if options["pretty"]:
            # override json.dumps so django.utils.html.json_script indents the JSON
            json.dumps = partial(json.dumps, indent=JSON_INDENT_LEVEL)
        # get html as string
        html = Client().get("/").content.decode("utf-8")
        if options["pretty"]:
            # reset json.dumps
            json.dumps = json.dumps
            # generate string for matching for gesha's <script> tag
            script_id = get_setting("GESHA_JSCONTEXT_KEY")
            script_tag = rf"<script id=\"{script_id}\" type=\"application/json\">"
            # find initial indent for script and target base indentation level for JSON
            initial_indent = re.search(
                rf"(?<=\n)([^\S\n\t]*)(?={script_tag})",
                html,
            ).group(1)
            base_indent = initial_indent + (" " * JSON_INDENT_LEVEL)
            # add base indentation to all lines and newlines for outermost curly braces
            html = re.sub(
                r"(?<=" + script_tag + r")({)(.*)(})(?=</script>)",
                lambda match: (
                    "\n"
                    + base_indent
                    + match.group(1)
                    + match.group(2).replace("\n", "\n" + base_indent)
                    + match.group(3)
                    + "\n"
                    + initial_indent
                ),
                html,
                flags=re.DOTALL,
            )
        if options["outfile"]:
            with open(options["outfile"], "w") as f:
                f.write(html)
        else:
            self.stdout.write(html)
