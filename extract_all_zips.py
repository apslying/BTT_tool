import os
import zipfile
import glob
import shutil
from pathlib import Path

def extract_all_zips(zip_folder=None):
    """
    Extract all zip files in the specified directory.
    Each zip file will be extracted to a folder with the same name (without .zip extension).
    
    Args:
        zip_folder (str): Name of the folder containing zip files. 
                         If None, uses current directory.
    """
    # Get current directory (where this script is located)
    current_dir = Path(__file__).parent
    
    # Determine the directory containing zip files
    if zip_folder:
        zip_dir = current_dir / zip_folder
        if not zip_dir.exists():
            print(f"Error: Folder '{zip_folder}' not found in {current_dir}")
            return
        if not zip_dir.is_dir():
            print(f"Error: '{zip_folder}' is not a directory")
            return
    else:
        zip_dir = current_dir
    
    print(f"Looking for zip files in: {zip_dir}")
    
    # Find all zip files in the specified directory
    zip_files = glob.glob(str(zip_dir / "*.zip"))
    
    if not zip_files:
        print(f"No zip files found in {zip_dir}")
        return
    
    print(f"Found {len(zip_files)} zip files to extract:")
    for zip_file in zip_files:
        print(f"  - {os.path.basename(zip_file)}")
    
    print("\nStarting extraction...")
    
    successful_extractions = 0
    failed_extractions = 0
    
    for zip_file_path in zip_files:
        zip_file_name = os.path.basename(zip_file_path)
        # Create extraction folder in the same directory as the zip file
        extract_folder = zip_dir / Path(zip_file_name).stem
        
        try:
            print(f"Extracting {zip_file_name}...")
            
            # Create extraction directory if it doesn't exist
            extract_folder.mkdir(exist_ok=True)
            
            # Extract the zip file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)
            
            print(f"  ✓ Successfully extracted to {extract_folder}")
            successful_extractions += 1
            
        except zipfile.BadZipFile:
            print(f"  ✗ Error: {zip_file_name} is not a valid zip file or is corrupted")
            failed_extractions += 1
        except PermissionError:
            print(f"  ✗ Error: Permission denied when extracting {zip_file_name}")
            failed_extractions += 1
        except Exception as e:
            print(f"  ✗ Error extracting {zip_file_name}: {str(e)}")
            failed_extractions += 1
    
    print(f"\nExtraction complete!")
    print(f"Successfully extracted: {successful_extractions} files")
    if failed_extractions > 0:
        print(f"Failed extractions: {failed_extractions} files")

def collect_notebooks(zip_folder=None, notebook_name="DataUnderstandingAndPreparation.ipynb"):
    """
    Find all specified notebook files from student folders,
    rename them with student names, and move them to an 'aaa_submissions' folder.
    
    Args:
        zip_folder (str): Name of the folder containing extracted student directories.
                         If None, uses current directory.
        notebook_name (str): Name of the notebook file to search for.
    """
    current_dir = Path(__file__).parent
    
    # Determine the directory containing student folders
    if zip_folder:
        search_dir = current_dir / zip_folder
        if not search_dir.exists():
            print(f"Error: Folder '{zip_folder}' not found in {current_dir}")
            return
    else:
        search_dir = current_dir
    
    submissions_dir = search_dir / "aaa_submissions"
    
    # Create submissions directory if it doesn't exist
    submissions_dir.mkdir(exist_ok=True)
    
    # Find all student directories (exclude submissions and other non-student folders)
    student_dirs = [d for d in search_dir.iterdir() 
                   if d.is_dir() and d.name not in ['aaa_submissions', '__pycache__', '.git']]
    
    if not student_dirs:
        print(f"No student directories found in {search_dir}")
        return
    
    print(f"\nSearching for notebooks in {len(student_dirs)} student directories...")
    
    notebooks_found = 0
    notebooks_moved = 0
    
    for student_dir in student_dirs:
        student_name = student_dir.name
        notebook_found = False
        
        # Search recursively for the notebook file
        for notebook_path in student_dir.rglob(notebook_name):
            if notebook_path.is_file():
                notebooks_found += 1
                notebook_found = True
                
                # Create new filename with student name (preserve original notebook name)
                notebook_base = Path(notebook_name).stem
                new_filename = f"{notebook_base}_{student_name}.ipynb"
                destination_path = submissions_dir / new_filename
                
                try:
                    # Copy the notebook to submissions folder with new name
                    shutil.copy2(notebook_path, destination_path)
                    # Show the relative path where the notebook was found
                    relative_path = notebook_path.relative_to(student_dir)
                    print(f"  ✓ Found and moved notebook from {student_name}/{relative_path} → aaa_submissions/{new_filename}")
                    notebooks_moved += 1
                    break  # Only take the first notebook found for each student
                    
                except Exception as e:
                    print(f"  ✗ Error moving notebook from {student_name}/: {str(e)}")
                    break
        
        if not notebook_found:
            print(f"  ! No notebook found in {student_name}/")
    
    print(f"\nNotebook collection complete!")
    print(f"Notebooks found: {notebooks_found}")
    print(f"Notebooks successfully moved: {notebooks_moved}")
    print(f"All notebooks saved to: {submissions_dir}")

def rename_notebooks_by_lastname(notebook_name="DataUnderstandingAndPreparation.ipynb", zip_folder=None):
    """
    Rename notebooks in the aaa_submissions folder to be sorted by last name instead of first name.
    Assumes the current format is: NotebookName_FirstName-LastName_id.ipynb
    Changes to: NotebookName_LastName-FirstName_id.ipynb
    
    Args:
        notebook_name (str): Base name of the notebook file (used to extract the prefix).
        zip_folder (str): Name of the folder containing the aaa_submissions folder.
                         If None, uses current directory.
    """
    current_dir = Path(__file__).parent
    
    # Determine the directory containing aaa_submissions folder
    if zip_folder:
        search_dir = current_dir / zip_folder
        if not search_dir.exists():
            print(f"Error: Folder '{zip_folder}' not found in {current_dir}")
            return
    else:
        search_dir = current_dir
    
    submissions_dir = search_dir / "aaa_submissions"
    
    if not submissions_dir.exists():
        print("Error: aaa_submissions folder not found.")
        return
    
    # Get the notebook base name (without .ipynb extension)
    notebook_base = Path(notebook_name).stem
    
    # Find all notebook files in aaa_submissions folder
    pattern = f"{notebook_base}_*.ipynb"
    notebook_files = list(submissions_dir.glob(pattern))
    
    if not notebook_files:
        print(f"No notebook files found matching pattern: {pattern}")
        return
    
    print(f"\nRenaming {len(notebook_files)} notebooks to sort by last name...")
    
    renamed_count = 0
    failed_count = 0
    
    for notebook_file in notebook_files:
        try:
            # Extract the student name part (everything after the notebook base name and underscore)
            filename = notebook_file.stem  # Remove .ipynb extension
            student_part = filename.replace(f"{notebook_base}_", "", 1)
            
            # Split the student name to get first name and last name with ID
            # Format is usually: FirstName-LastName_id or FirstName-LastName
            if '-' in student_part:
                parts = student_part.split('-', 1)  # Split only on first hyphen
                first_name = parts[0]
                lastname_and_id = parts[1]  # This could be "LastName_id" or just "LastName"
                
                # Create new filename with last name first
                new_student_part = f"{lastname_and_id}-{first_name}"
                new_filename = f"{notebook_base}_{new_student_part}.ipynb"
                new_path = submissions_dir / new_filename
                
                # Rename the file
                notebook_file.rename(new_path)
                print(f"  ✓ Renamed: {notebook_file.name} → {new_filename}")
                renamed_count += 1
                
            else:
                print(f"  ! Skipped: {notebook_file.name} (unexpected name format)")
                failed_count += 1
                
        except Exception as e:
            print(f"  ✗ Error renaming {notebook_file.name}: {str(e)}")
            failed_count += 1
    
    print(f"\nRenaming complete!")
    print(f"Successfully renamed: {renamed_count} files")
    if failed_count > 0:
        print(f"Failed to rename: {failed_count} files")

if __name__ == "__main__":
    ZIP_FOLDER = "assignment-3--train-decision-trees-after-data"  # CHANGE THIS!
    NOTEBOOK_NAME = "BuildADecisionTree.ipynb"  # CHANGE THIS!
    
    extract_all_zips(ZIP_FOLDER)
    collect_notebooks(ZIP_FOLDER, NOTEBOOK_NAME)
    rename_notebooks_by_lastname(NOTEBOOK_NAME, ZIP_FOLDER) 