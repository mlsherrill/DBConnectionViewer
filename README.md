# DB Connection Viewer

Script written in Python to view the number of connections to a database.

## Setup

1. Setup a virtual environment:
```bash
python -m venv venv
```
2. Activate the virtual environment:
```bash
source venv/bin/activate
```
3. Install the required packages:
```bash
pip install -r requirements.txt
```
4. Create an `.env` file with the following content:
```bash
SERVER=<get from lastpass>
DATABASE=<you should know this>
USERNAME=<requires an account with access to master db>
PASSWORD=<password for above>
```
5. Assume the role of the account where the EC2 instances are running
6. Run the script:
```bash
python main.py
```