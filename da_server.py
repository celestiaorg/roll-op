import os
from config import Config
import libroll as lib
from processes import PROCESS_MGR

####################################################################################################

def start(config: Config):
    """
    Starts the da server.
    """

    lib.ensure_port_unoccupied(
        "da server", config.da_server_rpc_listen_addr, config.da_server_rpc_listen_port)

    log_file = config.da_server_log_file
    print(f"Starting da server. Logging to {log_file}")

    auth_token = os.getenv("CELESTIA_NODE_AUTH_TOKEN")
    if not auth_token:
        auth_token = lib.run("Generating celestia auth token", [
            "celestia",
            "light",
            "auth",
            "write",
            "--p2p.network", "mocha",
        ]).strip()

    command = [
        "da-server",
        "--addr=0.0.0.0",
        "--port=3100",
        "--log.level=debug",
        "--generic-commitment=1",
        "--celestia.server=http://127.0.0.1:26658",
        f"--celestia.auth-token='{auth_token}'",
        "--celestia.namespace=00000000000000000000000000000000000000000008e5f679bf7116cb",
    ]

    config.log_l2_command("\n".join(command))

    def on_exit():
        print(f"da server exited. Check {log_file} for details.\n"
              "You can re-run with `./rollop da-server` in another terminal\n"
              "(!! Make sure to specify the same config file and flags!)")

    PROCESS_MGR.start(
        "starting da-server",
        command,
        file=log_file,
        on_exit=on_exit)

####################################################################################################

def clean(config: Config):
    """
    Delete the da server's data.
    """
    pass


####################################################################################################
