from ..models import Folder
import re

class FolderRepository:
    @staticmethod
    def get_folder_by_id(folderId):
        """
        Retrieve a folder by its ID.

        Args:
            folderId (str): The unique identifier of the folder.

        Returns:
            Folder: The folder instance if found, otherwise None.
        """        
        return Folder.objects.filter(id=folderId).first()
    
    @staticmethod
    def is_folder_name_unique(parentId, name, folderId=None):
        """
        Check if a folder name is unique within the same parent folder, excluding a specific folder.
        
        Args:
            parent_folder: The parent folder to check against.
            name: The name of the folder to check.
            folder_id: The folder ID to exclude from the check (in case of updating).
        
        Returns:
            bool: True if the folder name is unique, False otherwise.
        """
        return Folder.objects.filter(parent=parentId, name=name).exclude(id=folderId).exists()
    
    @staticmethod
    def get_max_folder_id(parent_folder):
        """
        Determine the highest numeric suffix among the IDs of subfolders.

        This method retrieves all IDs of subfolders for a given parent folder and extracts the numeric suffix 
        (if present) using a regular expression. It then calculates the maximum numeric value from these suffixes.

        Args:
            parent_folder (Folder): The parent folder whose subfolders are being inspected.

        Returns:
            int: The highest numeric suffix found among the subfolder IDs. Returns 0 if no numeric suffixes are found.
        """        
        folderIds = Folder.objects.filter(parent=parent_folder).values_list('id', flat=True)

        max_number = 0
        for folderId in folderIds:
            #explain design pattern
            match = re.search(r'(\d+)$', folderId)
            if match:
                number = int(match.group(1))
                max_number = max(max_number, number)

        return max_number
