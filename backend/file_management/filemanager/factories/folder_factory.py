from ..repositories.folder_repository import FolderRepository
from ..exceptions import ValidationException
from ..serializers import FolderSerializer
from ..utils import create_folder_data

class FolderFactory: 
    @staticmethod
    def create_root_folder():
        """
        Create a root folder.

        This factory method creates the root folder with a predefined ID and name. 
        It validates the folder data using the serializer and saves the instance to the database.

        Returns:
            Folder: The created root folder instance.

        Raises:
            ValidationException: If the folder data fails validation.
        """
        data = {"id": "root", "name": "Root"}
        
        serializer = FolderSerializer(data=data)
        if serializer.is_valid():
            return serializer.save()
    
        raise ValidationException(serializer.errors)
    
    @staticmethod
    def create_subfolder(parentFolder):
        """
        Create a subfolder for a given parent folder.

        This factory method generates a new folder ID by incrementing the highest numeric suffix 
        of the subfolder IDs for the given parent folder. It then validates and saves the subfolder 
        instance using the serializer.

        Args:
            parentFolder (Folder): The parent folder under which the new subfolder will be created.

        Returns:
            Folder: The created subfolder instance.

        Raises:
            ValidationException: If the subfolder data fails validation.
        """
        maxId = FolderRepository.get_max_folder_id(parentFolder)

        newFolderId = maxId + 1
        
        serializer = FolderSerializer(data=create_folder_data(parentFolder, newFolderId))
        if serializer.is_valid():
            return serializer.save()
        
        raise ValidationException(serializer.errors)
    