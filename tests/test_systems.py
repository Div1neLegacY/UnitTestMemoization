import pytest, subprocess, sys, os, socket

class TestSystems():

    # Called BEFORE every test
    def setup_method(self, method):
        print(f"\n\n##### STARTING {method.__name__} #####")

    # Called AFTER every test
    def teardown_method(self, method):
        print(f"\n##### FINISHED {method.__name__} #####\n\n")

    @pytest.fixture
    def systems_fixture(self):
        print("Called fixture")

    '''
    Runs an external app within the execution of this program.
    '''
    def start_external_app(self, command_list):
        try:
            process = subprocess.Popen(
                command_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,  # Decodes output as text
                bufsize=1,  # Line-buffered output
                universal_newlines=True # Ensures consistent newline handling
            )

            return process
        except FileNotFoundError:
            print(f"Error: Command '{command_list[0]}' not found.", file=sys.stderr)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)

    '''
    Configures a basic IPSec tunnel using strongswan's ipsec command.
    This is a simplified example and requires root privileges.
    '''
    def configure_ipsec_tunnel(self, local_ip, remote_ip, conn_name="ipsec_tunnel"):
        try:
            conn_config = """
# Example swanctl.conf for a basic site-to-site connection
    connections {
        ipsec_tunnel {
            local_addrs = %any
            remote_addrs = 127.0.0.1 # Remote gateway IP
            local {
                auth = psk
                id = @my_local_id
            }
            remote {
                auth = psk
                id = @my_remote_id
            }
            children {
                my_child {
                    local_ts = 127.0.0.1/24 # Local subnet
                    remote_ts = 127.0.0.1/24 # Remote subnet
                    mode = tunnel
                    dpd_action = restart
                    updown = /usr/local/sbin/updown.sh # Optional script for routing
                }
            }
        }
    }
    secrets {
        ike-my_tunnel {
            id = @my_local_id
            secret = "your_shared_secret"
        }
    }
"""

            # Add connection above to the ipsec configuration file
            ipsec_config_path = os.path.join("/etc", "swanctl", "swanctl.conf")
            with open(ipsec_config_path, "a") as f:
                f.truncate(0)
                f.write(conn_config)

        except subprocess.CalledProcessError as e:
            print(f"Error configuring IPSec tunnel: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    '''
    TEST 1
    '''
    def test_subprocesses(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            external_script_path = os.path.join(current_dir, "..", "src", "systems.py")

            process = self.start_external_app(['python', '-u', external_script_path])
            while True:
                line = process.stdout.readline()
                # Test END case
                if "ending" in line:
                    break
                # subprocess output
                print(line.rstrip())

        except subprocess.CalledProcessError as err:
            print(err.stderr)

    '''
    TEST 2
    '''
    def test_loopback_subprocesses(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            external_script_path = os.path.join(current_dir, "..", "src", "loopback.py")

            process = self.start_external_app(['python', '-u', external_script_path])
            while True:
                line = process.stdout.readline()
                # Test END case
                if "Server shutting down" in line:
                    break
                # subprocess output
                print(line.rstrip())

        except subprocess.CalledProcessError as err:
            print(err.stderr)

    '''
    TEST 3
    '''
    def test_fixture(self, systems_fixture):
        assert True

    '''
    TEST 4
    '''
    #@pytest.mark.skip(reason="This test is temporarily disabled until I can get these tests running in WSL.")
    def test_ipsec_tunnel(self):
        self.configure_ipsec_tunnel("192.168.1.10", "192.168.1.20", "ipsec_tunnel")

    '''
    TEST 5
    '''
    def test_scapy(self):
        assert True