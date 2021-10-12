#!/usr/bin/env bash
echo "Starting api..."
gunicorn manage:application -b 0.0.0.0:5000 -t 3600