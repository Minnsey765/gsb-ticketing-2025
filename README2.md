0. Change to app dir: `cd app`
1. Create a virtual environment: `python3 -m venv .venv`
2. Activate the environment: `. .venv/bin/activate` ( For Powershell `.venv/scripts/activate.ps1`)
3. Change to cdk dir: `cd ../cdk`
4. Install dependencies: `pip install -r requirements.txt`
5. Deploy postgres locally: `docker compose up --force-recreate --build`
6. Deploy onto awds using cdk: `cdk deploy`

note - make sure line endings in vscode are set to LF rather than CRLF otherwise docker won't work
