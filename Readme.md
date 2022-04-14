# Confgen - A Bird2 / Wireguard config file generator
This is for internal use for generating wireguard and bird config files from a google spreadsheet.
This can be used via symlinks to manage peering inside dn42.

The tool needs to be re run on each change to the sheet.
It will delete all old config files on each regeneration.


## Make sure to BACKUP the files before!
```bash
# Are you sure?
# rm -rf /etc/bird/peers/ebgp
ln -s ./configs/bird /etc/bird/peers/ebgp

# Are you sure?
# rm -rf /etc/wireguard/peers/ebgp
ln -s ./configs/wg /etc/wireguard/peers/ebgp
```