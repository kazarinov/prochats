#!/bin/bash

PYTHONPATH=.:$PYTHONPATH venv/bin/py.test tests/
