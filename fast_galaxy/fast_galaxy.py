import yaml
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import atexit
import shutil

role_files_dir = "role_files"

def split_requirements(file_path):
    try:
        with open(file_path, 'r') as stream:
            data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        return []

    roles = data.get('roles', [])
    collections = data.get('collections', [])

    if not os.path.exists(role_files_dir):
        os.makedirs(role_files_dir)

    role_files = []
    for idx, role in enumerate(roles):
        role_filename = f'{role_files_dir}/role_{idx + 1}.yml'
        with open(role_filename, 'w') as role_file:
            yaml.dump({'roles': [role]}, role_file)
        role_files.append(role_filename)

    collection_files = []
    for idx, collection in enumerate(collections):
        collection_filename = f'{role_files_dir}/collection_{idx + 1}.yml'
        with open(collection_filename, 'w') as collection_file:
            yaml.dump({'collections': [collection]}, collection_file)
        collection_files.append(collection_filename)

    print(f"Split requirements file into individual role and collection files in the '{role_files_dir}' directory.")
    return role_files + collection_files

def install_requirements(file_path):
    try:
        result = subprocess.run(["ansible-galaxy", "install", "-r", file_path], check=True, capture_output=True, text=True)
        return f"Successfully installed from {file_path}\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Failed to install from {file_path}\n{e.stderr}"

def cleanup_temp_files():
    if os.path.exists(role_files_dir):
        shutil.rmtree(role_files_dir)
        print(f"Removed temporary directory '{role_files_dir}'.")

def main():
    atexit.register(cleanup_temp_files)

    parser = argparse.ArgumentParser(description="Split and install Ansible Galaxy requirements.")
    parser.add_argument('requirements_path', type=str, help="Path to the requirements.yml file")
    parser.add_argument('--parallel', type=int, default=10, help="Number of parallel installations (default: 10)")

    args = parser.parse_args()

    files_to_install = split_requirements(args.requirements_path)
    
    if files_to_install:
        with ThreadPoolExecutor(max_workers=args.parallel) as executor:
            future_to_file = {executor.submit(install_requirements, file): file for file in files_to_install}
            for future in as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    result = future.result()
                    print(result)
                except Exception as exc:
                    print(f'{file} generated an exception: {exc}')
