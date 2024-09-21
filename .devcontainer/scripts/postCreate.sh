#!/bin/bash
set -e

#------------------------------
# PRE COMMIT
#------------------------------

NAME="Pre Commit"

echo -e "\e[34m»»» 📦 \e[32mInstalling \e[33m$NAME\e[0m ..."

make precommit-install
