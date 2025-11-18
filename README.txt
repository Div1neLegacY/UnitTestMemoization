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

# Fails on CHILD_SA AUTH, indicates mismatch in Phase 2


# Setup certificate
pki --gen --type ed25519 --outform pem > strongswanKey.pem

pki --self --ca --lifetime 3652 --in strongswanKey.pem \
--dn "C=CH, O=strongSwan, CN=strongSwan Root CA" --outform \
pem > /etc/swanctl/x509ca/strongswanCert.pem



pki --gen --type ed25519 --outform pem > moonKey.pem

pki --gen --type rsa --size 3072 > moonKey.der

pki --req --type priv --in moonKey.pem \
--dn "C=CH, O=strongswan, CN=moon.strongswan.org" \
--san moon.strongswan.org --outform pem > moonReq.pem

pki --issue --cacert strongswanCert.pem --cakey strongswanKey.pem \
--type pkcs10 --in moonReq.pem --serial 01 --lifetime 1826 \
--outform pem > /etc/swanctl/x509/moonCert.pem

pki --signcrl --cacert strongswanCert.pem --cakey strongswanKey.pem \
--lifetime 30 > /etc/swanctl/x509crl/strongswan.crl





# test

# create private key
openssl ecparam -name prime256v1 -genkey -noout -out /etc/swanctl/ecdsa/private.pem

# create public key from private
openssl ec -in private.pem -pubout -out /etc/swanctl/x509/public.pem

# create .pem CA certificate
openssl req -new -x509 -sha256 -days 3650 -key /etc/swanctl/ecdsa/private.pem -out /etc/swanctl/x509ca/ca-cert.pem

# Generate CSR from private key
openssl req -new -key private.pem -out public.csr
# Hit enter a bunch

# Test if a certificate is valid:
openssl x509 -in /etc/swanctl/x509/public.pem -text -noout
openssl x509 -in /etc/swanctl/x509ca/ca-cert.pem -text -noout