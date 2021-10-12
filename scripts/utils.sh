#!/usr/bin/env bash
DIRECTORY="$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

ROOT_DIRECTORY="$(dirname $DIRECTORY)"

# colors
red=$(tput setaf 1)
green=$(tput setaf 76)
tan=$(tput setaf 3)

success() {
  printf "${green}===> %s${reset}\n" "$@"
}

error() {
  printf "${red}===> %s${reset}\n" "$@"
}

warning() {
  printf "${tan}===> %s${reset}\n" "$@"
}

function addEnvFile() {
    ENV_FILE=$ROOT_DIRECTORY/.env
    warning "Adding .env file to the Songs API directory"
    echo " "

    if [ ! -f "$ENV_FILE" ]; then
          cat <<EOF >> "${ROOT_DIRECTORY}"/.env
API_KEY=${API_KEY}
EOF
        success "lsEnvironment file has been created successfully"
        return
    fi

    warning "Skipping, Environment file already exist"
}

"$@"