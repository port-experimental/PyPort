import os

from pyport.constants import LOG_LEVEL
## Debugging Package from PyPi
from pyport import PortClient

## Debugging Package from Local
# from src.pyport.api_client import PortClient
from pyport.services.logging_svc import init_logging
from dotenv import load_dotenv


def init():
    init_logging(LOG_LEVEL)
    load_dotenv(dotenv_path=".env", override=True, encoding="utf-8")


def main():
    init()
    PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
    PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")
    pc = PortClient(client_id=PORT_CLIENT_ID, client_secret=PORT_CLIENT_SECRET, us_region=True)
    bps = pc.blueprints.get_blueprints()
    entities = pc.entities.get_entities(bps[0]["identifier"])
    #  update_port_blueprint(pc, "githubWorkflowRun", ENTITIES)
    print()


if __name__ == "__main__":
    main()
