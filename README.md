# Tax scripts

I have created this repository for my own purposes. Banks usually provide reports in very different formats with the worst being PDF files.
Manually copying the data from PDFs to a spreadsheet while preparing tax report can be to labourious, so I decided to write some python scripts to automate this for me.

## Why leaving it public then

1. It can be easily shared with friends who may use same reports as my (from Brazilian banks)
2. Friends reading this repo can suggest better ways for me to achieve the same (I have tried ChatGPT Pro but it wasn't able to read correctly from PDFs).
3. Why not?

## Current available script(s)

1. `foreign_income_br_cdb.py`: this script reads reports provided by Bradesco informing statement monthly allowing me to find the interests earned for a given financial year.

## Running

The current available script relies on exchangerate.host API to fetch, well, the exchange rate from BRL to AUD on a given point in time.
So, in order for `foreign_income_br_cdb.py` to work, one needs to provide the access key for your account with the `EXCHANGE_RATE_HOST_API_ACCESS_KEY` environment variable.

 

