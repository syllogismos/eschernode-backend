#!/bin/bash

export ESCHERNODE_ENV=prod
gunicorn -w 3 backend.wsgi