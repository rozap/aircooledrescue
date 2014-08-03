#!/bin/bash

echo Starting Gunicron
gunicorn buspeople.wsgi:application -b unix:/tmp/buspeople.sock -p /tmp/buspeople.pid --access-logfile /home/chris/workspace/buspeople/buspeople/deploy/gunicorn_access.log
