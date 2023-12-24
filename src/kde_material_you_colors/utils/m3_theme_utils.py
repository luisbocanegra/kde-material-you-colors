import subprocess
import json
import logging
from .. import settings


def themeFromSourceColorCli(source_info):
    with open(settings.SOURCE_INFO_FOR_NODE, "w", encoding="utf-8") as f:
        f.write(json.dumps(source_info))
    # logging.warning(source_info)
    cmd = [
        "node",
        settings.MATERIAL_CLI_PATH,
        settings.SOURCE_INFO_FOR_NODE,
    ]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=True,
    )
    o = result.stdout
    r = json.loads(o)
    # print(r)
    # exit(0)
    return r
