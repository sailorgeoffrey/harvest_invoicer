# Harvest Invoice Generator

This script connects to your Harvest account and generates invoices for the month.

## Setup
1. Generate a personal access token to [Harvest](https://id.getharvest.com/developers).
The script will prompt you for the account ID and token on the first run.
The token will be encrypted and saved in your keychain.
2. Use PIP to install the requirements.txt

## Usage
The command takes an optional date as a command line argument.  It is in the format YYYYMM.
It will prompt you for this if you don't provide it.  On the first run it will ask you for
your hourly rate to calculate the totals.

    python invoicer.py [date]
