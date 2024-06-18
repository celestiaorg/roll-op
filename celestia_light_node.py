from config import Config
import libroll as lib
from processes import PROCESS_MGR


####################################################################################################

def start(config: Config):
    """
    Starts the celestia light node.
    """

    lib.ensure_port_unoccupied(
        "celestia light node", config.celestia_light_node_rpc_listen_addr, config.celestia_light_node_rpc_listen_port)

    log_file = config.celestia_light_node_log_file
    print(f"Starting celestia light node. Logging to {log_file}")

    command = [
        "celestia",
        "light",
        "start",
        "--p2p.network", "mocha",
        "--core.ip", "rpc-mocha.pops.one",
        "--gateway"
    ]

    config.log_l2_command("\n".join(command))

    def on_exit():
        print(f"celestia light node exited. Check {log_file} for details.\n"
              "You can re-run with `./rollop celestia-light-node` in another terminal\n"
              "(!! Make sure to specify the same config file and flags!)")

    PROCESS_MGR.start(
        "starting celestia-light-node",
        command,
        file=log_file,
        on_exit=on_exit)

####################################################################################################

def clean(config: Config):
    """
    Delete the celestia light node's data.
    """
    pass


####################################################################################################
