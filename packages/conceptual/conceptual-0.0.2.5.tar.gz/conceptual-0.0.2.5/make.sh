#!/bin/sh
python setup.py bdist_wheel
python -m pip install dist/*
