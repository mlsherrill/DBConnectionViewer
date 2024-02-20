# DB Connection Viewer

Script written in Python to view the number of connections to a database.

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```
2. Create an `.env` file with the following content:
```bash
SERVER=<get from lastpass>
DATABASE=<you should know this>
USERNAME=<requires an account with access to master db>
PASSWORD=<password for above>
```
3. Assume the role of the account where the EC2 instances are running

4. Run the script:
```bash
python main.py
```