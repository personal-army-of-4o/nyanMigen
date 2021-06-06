## What is nyanMigen?

nyanMigen is a python layer between nmigen and a human being. it converts state-of-the-art python subset with card games and senioritas into valid nmigen code.

key features:
- simplified, less redundant syntax
- consumes chain description wrapped in a class or a function
- generates __init__(), ports(), inputs(), outputs() based on chain description
- extracts ports from chain description
- extracts generics from chain descripton and exposes them as __init__ args
- outputs nmigen code
- runs nmigen for generated code

## Repo actions:

to test: `run_test.bash`
to test with docker images: `run_test.bash -g`

to install: `pip3 install .`

to build docker images: `cd docker && bash build.bash`

shortest hello world ever: [blink.py](examples/blink.py)

## Repo structure:

- [nyanMigen.py](nyanMigen.py)
- examples/*.py - nyanMigen examples and feature show cases
- examples/*.nmigen - nmigen code generated from nyanMigen examples
- examples/*.stat - some hard numbers extracted by nyanMigen
- [run_test.bash](run_test.bash) - test looper. runs onetest.bash for each .py from examples
- [onetest.bash](onetest.bash) - runs nyanMigen for one example

## Dependencies

based on nmigen project. tested with [this commit](https://github.com/nmigen/nmigen/commit/c84d4aff6ef62ebf7f06728bd04754bc298fddca)

## Links

[nyanMigen discord server](https://discord.gg/ytRqFgn2rj)
