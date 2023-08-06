# Worklog

Personal time-tracking system. 

## Installation

**Future** this project will be released on pypi, which will allow something
like:

`pip install worklog`

## Suggested use

TODO

## Commands

The base command is `work`.

`work --edit` opens the current worklog for editing.

`work --archive` archives the current worklog 

## Configuration



## Formats

Worklog relies on [hledger](https://hledger.org/), a Haskell implementation of
[ledger](https://github.com/ledger/ledger), for double-entry bookkeeping which
regards time as a resource just like money. One main design goal of this system
is a [human-readable ledger format](https://hledger.org/timeclock.html) which
can also be parsed by scripts. 



