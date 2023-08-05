import os.path

from erdpy import utils


DOWNLOAD_MIRROR = "https://ide.elrond.com"
MODULES_CONFIG_URL = "https://raw.githubusercontent.com/ElrondNetwork/elrond-sdk/master/deps.json"
WITH_CHAIN_ID_AND_TX_VERSION = False
CHAIN_ID = ""
TX_VERSION = 0

ROOT_FOLDER_NAME = "elrondsdk"
CONFIG_PATH = os.path.expanduser("~/elrondsdk/erdpy.json")

DEFAULT_GAS_PRICE = 200000000000
GAS_PER_DATA_BYTE = 1500
MIN_GAS_LIMIT = 50000


class MetaChainSystemSCsCost:
    STAKE = 5000000
    UNSTAKE = 5000000
    UNBOND = 5000000
    CLAIM = 5000000
    GET = 5000000
    CHANGE_REWARD_ADDRESS = 5000000
    CHANGE_VALIDATOR_KEYS = 5000000
    UNJAIL = 5000000


def update_value(name, value):
    pass


def get_value(name):
    pass


def get_names() -> [str]:
    return ["proxy", "chainID", "txVersion"]


def _read_file():
    utils.read_json_file(CONFIG_PATH)
