# Confgen - A Bird2 / Wireguard config file generator
This is for internal use for generating wireguard and bird config files from a google spreadsheet.

The tool needs to be re run on each change to the sheet.
It will delete all old config files on each regeneration.


## Setup 
***Make sure to BACKUP the files before!***

```bash
cd /root
git clone https://github.com/riseupgroup/confgen
cd confgen
```
- Create a google cloud plattform project
- Go to [GCP/SheetsAPI](https://console.cloud.google.com/apis/library/sheets.googleapis.com) and activate that api
- Got to [GCP/IAM/ServiceAccounts](https://console.cloud.google.com/iam-admin/serviceaccounts) and create a new service account with no rights or roles at all
- Copy email address of that account
- Click on the account and download it's api key/login file as json
- Go to the spreadsheet you want to use and share it with the email of the serive account
- Put the login file into confgen/credentials.json
- ```cp .env.example .env``` and fill in ```.env```
    - You can get the document/spreadsheet id from the url when it's opened
    - Sheet is the name of the sheet in the document
- You may need to change some of the permisisons of the /etc/bird folder. If bird cannot access a file try to set it/folder to chmod 550. Look into ```update.bash``` for help
## Run
```bash
cd /root/confgen
bash update.bash
```
