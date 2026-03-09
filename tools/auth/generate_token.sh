#!/usr/bin/env bash

source .venv/bin/activate

set -a
source .env
set +a

python -um tools.auth.generate_keycloak_token "$@" 
