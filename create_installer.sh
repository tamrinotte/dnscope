#!/usr/bin/bash

set -euo pipefail

main() {
    declare_variables
    purge_the_app
    delete_the_old_files
    create_a_new_executable_file
    package_the_tool
    create_installer
    start_the_installer
    print_info_message "Installation complete."
}

print_info_message() {
    echo -e "\e[1;34m[INFO]\e[0m ${1}"
}

declare_variables() {
    app_name="dnscope"
    version="0.1.3"
    username="${SUDO_USER:-${USER}}"
    build_dirs=("dist" "build" "package")
    installer="${app_name}.deb"
    package_base_dir="package"
    package_usr_bin_dir="${package_base_dir}/usr/bin"
}

purge_the_app() {
    # Purge existing installation if present
    print_info_message "Purging existing installation of ${app_name} (if installed)..."
    if dpkg -l | grep -q "^ii  ${app_name} "; then
        sudo apt purge --autoremove -y "${app_name}"
    else
        print_info_message "No existing installation found."
    fi
}

delete_the_old_files() {
    # Clean old build artifacts
    for dir in "${build_dirs[@]}"; do
        if [[ -d "${dir}" ]]; then
            print_info_message "Removing existing directory: ${dir}"
            rm -rf "${dir}"
        fi
    done

    if [[ -f "${installer}" ]]; then
        print_info_message "Removing existing installer: ${installer}"
        rm -f "${installer}"
    fi
}

create_a_new_executable_file() {
    # Create executable
    print_info_message "Creating standalone executable using PyInstaller..."
    pyinstaller --onefile --name=dnscope "${app_name}.py" --collect-all=dns --collect-all=whois
}

package_the_tool() {
    # Setup package structure
    print_info_message "Creating package directory hierarchy..."
    mkdir -p "${package_usr_bin_dir}"

    # Move executable
    print_info_message "Copying executable to package directory..."
    cp "dist/${app_name}" "${package_usr_bin_dir}"

    # Set permissions and ownership
    print_info_message "Setting permissions and ownership for package directory..."
    chmod 755 -R "${package_base_dir}"
    chown "${username}:${username}" -R "${package_base_dir}"
}

create_installer() {
    # Build Debian installer with FPM
    print_info_message "Creating Debian installer with FPM..."
    fpm -C "${package_base_dir}" -s dir -t deb -n "${app_name}" -v "${version}" -p "${installer}" --after-install "post_install_script.sh"
}

start_the_installer() {
    # Install generated package
    print_info_message "Installing the new ${app_name} package..."
    sudo dpkg -i "${installer}"
}

main