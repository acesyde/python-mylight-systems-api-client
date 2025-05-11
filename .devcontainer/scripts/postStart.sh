#!/usr/bin/env bash
set -e

#------------------------------
# FUNCTIONS
#------------------------------
print_command() {
    local message=$1
    local icon=$2
    echo -e "\e[34m»»» $icon \e[32m$message\e[0m ..."
}

#------------------------------
# MISE
#------------------------------
MISE=$(which mise)

if [ -z "$MISE" ]; then
    echo "Mise is not installed. Please install Mise before running this script."
    exit 1
fi

print_command "Configuring Mise..." "🔧"

$MISE trust
echo "eval $($MISE activate bash)" >> ~/.bashrc
echo "eval $($MISE activate zsh)" >> ~/.zshrc

print_command "Mise is configured!" "✅"

print_command "Setting up Mise environment..." "🚀"

$MISE i

print_command "Mise environment is set up!" "✅"

# Get tools
GIT=$(which git)

#------------------------------
# PRE COMMIT
#------------------------------
print_command "Configuring pre-commit..." "🔧"

$MISE exec -- pre-commit install --install-hooks
$MISE exec -- pre-commit install --hook-type commit-msg

print_command "Pre-commit is configured!" "✅"

#------------------------------
# CONFIGURE ENV
#------------------------------
print_command "Configuring environment..." "🔧"

$GIT config --global pull.rebase false

print_command "Environment is configured!" "✅"
