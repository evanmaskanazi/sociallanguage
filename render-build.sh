#!/usr/bin/env bash
# Install system dependencies for WeasyPrint
apt-get update
apt-get install -y python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b libpangocairo-1.0-0
