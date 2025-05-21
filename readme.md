# Harvest Invoice Generator

This script connects to your Harvest account and generates invoices for the month.

## Setup

1. Update template.md to use your details instead of mine.
2. Generate a personal access token to [Harvest](https://id.getharvest.com/developers).
   The script will prompt you for the account ID and token on the first run.
   The token will be encrypted and saved in your keychain.
3. Install the module: `pip install -e .`

## Usage

The command takes an optional month as a command line argument. It is in the format YYYYMM.
If you don't provide one, it will generate an invoice for last month.
On the first run it will ask you for your hourly rate to calculate the totals.

    invoicer [month] [--config CONFIG_FILE] [--preview]

### Examples

    invoicer 202504  # Generate invoice for April 2025
    invoicer --preview  # Preview invoice for last month

## Uninstall

If you want to uninstall the development version:

    pip uninstall invoicer 

## Tip

Create a cronjob to run it on the first of every month without an arg,
and you will always have last month's invoice done.
