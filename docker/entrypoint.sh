#!/bin/bash
set -e

# Start virtual display for headless rendering
Xvfb :99 -screen 0 1280x1024x24 &
sleep 1

exec "$@"
