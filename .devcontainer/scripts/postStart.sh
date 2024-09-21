#!/bin/bash
set -e

#------------------------------
# PRE COMMIT
#------------------------------

NAME="Configure Pre Commit Hooks"

echo -e "\e[34m»»» 🚀 \e[32mInit \e[33m$NAME\e[0m ..."

make precommit-configure

#------------------------------
# CONFIGURE ENV
#------------------------------

NAME="Configure Environment"
echo -e "\e[34m»»» 🚀 \e[32mInit \e[33m$NAME\e[0m ..."

workspace=$(pwd)
git config --global pull.rebase false
