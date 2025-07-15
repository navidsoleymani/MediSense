#!/bin/bash
# This script installs Python packages from a requirements file
# using a specified PyPI mirror to improve download speed and reliability.
# It then freezes the installed packages back into requirements.txt,
# ensuring your environment and requirements file are in sync.
# Freeze only happens if installation succeeds; otherwise, a warning is shown.

# Define the requirements file path
REQUIREMENTS_FILE="requirements.txt"

# Define the PyPI mirror URL
PYPI_MIRROR_URL="https://pypi.tuna.tsinghua.edu.cn/simple"

# Upgrade and install packages from requirements.txt using the specified mirror
echo "Installing/upgrading packages from ${REQUIREMENTS_FILE} using mirror ${PYPI_MIRROR_URL}..."

if pip install --upgrade --upgrade-strategy eager -r "${REQUIREMENTS_FILE}" -i "${PYPI_MIRROR_URL}"; then
    echo "Installation succeeded."
    echo "Freezing installed packages to ${REQUIREMENTS_FILE}..."
    pip freeze > "${REQUIREMENTS_FILE}"
    echo "Freeze completed successfully."
else
    echo "WARNING: Installation failed. Skipping freezing operation." >&2
fi

echo "Script execution finished."
