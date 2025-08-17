# Tax scripts

I have created this repository for my own purposes. Banks usually provide reports in very different formats with the worst being PDF files.
Manually copying the data from PDFs to a spreadsheet while preparing tax report can be too labourious, so I decided to write some python scripts to automate this for me.

## Why leaving it public then

1. It can be easily shared with friends who may use same reports as mine (from Brazilian banks)
2. Friends reading this repo can suggest better ways for me to achieve the same (I have tried ChatGPT Pro but it wasn't able to read correctly from PDFs).
3. Why not sharing?

## Current available script(s)

1. `foreign_income_br_cdb.py`: this script reads reports provided by Bradesco informing statement monthly allowing me to find the interests earned for a given financial year.

## Running

### Requirements

- To run the script, you need to have Python 3 installed on your machine.
- Set `EXCHANGE_RATE_HOST_API_ACCESS_KEY` environment variable because the main script relies on exchangerate.host API to fetch the exchange rate.

### Usage

For more information on how to use the script, you can run:

```bash
$ python ./foreign_income_br_cdb.py --help
```

Output:
```
usage: foreign_income_br_cdb.py [-h] [--dry-run] [directory]

Process financial data from PDFs

positional arguments:
  directory   Directory containing PDF files

options:
  -h, --help  show this help message and exit
  --dry-run   Run without making external API calls
```
