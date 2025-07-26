import subprocess
import shutil
import os

INITIAL_COMMIT_MSG = "Initial commit"
TEMPLATE_REPO = "https://github.com/Varollo/godot-cs-template.git"

PROJ_FILE = "project.godot"
SOLU_FILE = "PROJ_NAME.sln"
CSPR_FILE = "PROJ_NAME.csproj"

def main():
    project_name = input(f"[?] Project Name: ")
    project_path = os.path.join(os.getcwd(), project_name)

    clone_repo(TEMPLATE_REPO, project_path)
    remove_git(project_path)
    init_git(project_path)
    edit_proj_files(project_path, project_name)
    
    input("-----Done!-----\nPress Enter to open the directory...")
    subprocess.Popen(fr'explorer /open,"{project_path}"')

def remove_git(repo_path):
    git_folder = os.path.join(repo_path, '.git')
    print(f"Removing git folder at \"{git_folder}\"")
    
    try:
        shutil.rmtree(git_folder, ignore_errors=True)        
        print(f"Git removed from \"{repo_path}\" successfully.")
        
    except PermissionError:
        print(f"Permission error: Could not delete \"{git_folder}\". Make sure to run script as administrator.")

def init_git(repo_path):
    print(f"Initializing new repository...")
    
    try:        
        os.chdir(repo_path)
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', INITIAL_COMMIT_MSG], check=True)
        print(f"New repository started on \"{repo_path}\" successfully.")
        
    except subprocess.CalledProcessError as e:
        input(f"Error initializing new repository: {e}")

def edit_proj_files(project_path, project_name):    
    proj_file_path = os.path.join(project_path, PROJ_FILE)
    
    old_solu_file_path = os.path.join(project_path, SOLU_FILE)
    old_cspr_file_path = os.path.join(project_path, CSPR_FILE)
    
    new_solu_file_path = os.path.join(project_path, f"{project_name}.sln")
    new_cspr_file_path = os.path.join(project_path, f"{project_name}.csproj")
        
    print(f"Editing content in project file at \"{proj_file_path}\"")
    replace_in_file(proj_file_path, { "PROJ_NAME": project_name })
    
    print(f"Editing content in solution file at \"{old_solu_file_path}\"")
    replace_in_file(old_solu_file_path, { "PROJ_NAME": project_name })
    
    print(f"Renaming solution file from \"{SOLU_FILE}\" to \"{project_name}.sln\"")
    os.rename(old_solu_file_path, new_solu_file_path)
    
    print(f"Renaming csproj file from \"{CSPR_FILE}\" to \"{project_name}.csproj\"")
    os.rename(old_cspr_file_path, new_cspr_file_path)

def clone_repo(repo_url, destination_folder):
    print(f"Cloning template repository \n << from \"{repo_url}\"\n >> to \"{destination_folder}\"")
    
    try:
        subprocess.run(['git', 'clone', repo_url, destination_folder], check=True)
        print(f"Repository cloned successfully to \"{destination_folder}\".")
        
    except subprocess.CalledProcessError as e:
        input(f"Error cloning repository: {e}")

def replace_in_file(file_path, replace_dict):    
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            
        for old_string1, new_string1 in replace_dict.items():
            text = text.replace(old_string1, new_string1)

        with open(file_path, 'w') as file:
            file.write(text)

        print(f"Project file \"{file_path}\" edited successfully.")

    except FileNotFoundError:
        print(f"The file \"{file_path}\" does not exist.")

    except IOError as e:
        print(f"Error while modifying project file ({file_path}): {e}")



if __name__ == "__main__":
    main()