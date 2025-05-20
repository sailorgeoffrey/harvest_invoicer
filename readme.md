# Harvest Invoice Generator

This script connects to your Harvest account and generates invoices for the month.

## Setup
1. Generate a personal access token to [Harvest](https://id.getharvest.com/developers).
The script will prompt you for the account ID and token on the first run.
The token will be encrypted and saved in your keychain.
2. Use PIP to install the requirements.txt
3. Update template.md to use your details instead of mine.

## Usage
The command takes an optional month as a command line argument.  It is in the format YYYYMM.
If you don't provide one, it will generate an invoice for last month.
On the first run it will ask you for your hourly rate to calculate the totals.

    python3 invoicer.py [YYYYMM]

## Tips
Create a cronjob to run it on the first of every month without an arg, 
and you will always have last month's invoice done.
