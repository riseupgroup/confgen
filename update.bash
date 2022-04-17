cd /root/confgen
python3 main.py

### Wireguard
for f in /etc/wireguard/peers/egp/*; do wg-quick down $f; done
rm -f /etc/wireguard/peers/egp/*
mkdir -p /etc/wireguard/peers/egp ## if not already there
cp ./configs/wg/* /etc/wireguard/peers/egp/
chmod 660 /etc/wireguard/peers/ -R
for f in /etc/wireguard/peers/egp/*; do wg-quick up $f; done

### Bird
rm -f /etc/bird/peers/egp/*
mkdir -p /etc/bird/peers/egp ## if not already there
cp ./configs/bird/* /etc/bird/peers/egp/
chown bird:bird /etc/bird/peers/*
chmod 550 /etc/bird/peers/* # yes, 550 is correect for some reason
birdc configure
