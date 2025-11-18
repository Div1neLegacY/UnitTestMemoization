# Open up a terminal that has a built-in 'source' command and allows smartSwan IpSec
# Ubuntu WSL recommended

cd UnitTestMemoization


sudo apt update; sudo apt install \
python3 \
python3-pytest \
python-is-python3 \
strongswan \
strongswan-pki \
strongswan-swanctl \
libcharon-extra-plugins \
python3-pip \
python3-venv

# Create .venv (if not existing)
python3 -m venv .venv

# Source virtual env
source .venv/bin/activate

# Install dependencies
.venv/bin/pip install -r requirements.txt

# Run python test application with standard output
pytest -s

# strongswan

# Specify log details for strong swanctl
vi /etc/strongswan.conf

# strongswan.conf - strongSwan configuration file
#
# Refer to the strongswan.conf(5) manpage for details
#
# Configuration changes should be made in the included files

charon {

        syslog {
                # Defines the identifier for use with openlog(3).
                # For example, you can specify a syslog facility like LOG_DAEMON or LOG_AUTHPRIV.
                daemon {
                        # Default log level for all subsystems not explicitly defined below.    
                        default = 4
                }
        }
        load_modular = yes
        plugins {
                include strongswan.d/charon/*.conf
        }
}

include strongswan.d/*.conf

# Reload log settings
swanctl --reload-settings


#
sudo systemctl start strongswan-starter
sudo swanctl --load-all
sudo swanctl --initiate --child my_child