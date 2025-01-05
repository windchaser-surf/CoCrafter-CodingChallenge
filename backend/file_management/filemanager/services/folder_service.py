from ..repositories.folder_repository import FolderRepository
from ..exceptions import ValidationException
from ..factories.folder_factory import FolderFactory, NotFoundException
from ..serializers import FolderSerializer

class FolderService: 
    @staticmethod
    def create_folder(data):
        """
        Handle folder creation, including validating the parent folder and creating a new folder.
        
        If the `parentId` is not provided, it attempts to create a root folder, ensuring that
        a root folder does not already exist. If the `parentId` is provided, it validates the
        existence of the parent folder and creates a subfolder under it.
        
        Args:
            data: The request data to create the folder, which may contain:
                - 'parentId' (optional): ID of the parent folder.
        
        Returns:
            Folder: The created Folder instance.
        
        Raises:
            ValidationException: If the root folder already exists or the data is invalid.
            NotFoundException: If the parent folder specified by `parentId` does not exist.
        """
        if not data.get('parentId'):
            if FolderRepository.get_folder_by_id('root'):
                raise ValidationException(f"Root folder already exists.")
            return FolderFactory.create_root_folder()
        
        parentId = data.pop('parentId')
        parentFolder = FolderRepository.get_folder_by_id(parentId)
        if not parentFolder: 
            raise NotFoundException(f"Parent folder with ID {parentId} not found.")
        return FolderFactory.create_subfolder(parentFolder)
    
    def update_folder(folder, data):
        """
        Handle folder update by using the FolderSerializer for validation and saving.

        This method checks if the folder name is unique within the same parent folder and updates the folder 
        details using the FolderSerializer.

        Args:
            folder: The Folder instance to be updated.
            data: The updated data for the folder (e.g., new folder name).

        Returns:
            Folder: The updated Folder instance.

        Raises:
            ValidationException: If the folder name already exists in the same parent folder.
            ValidationException: If the serializer validation fails for the folder data.
        """
        newName = data.get('name')
        parentId = folder.parent.id if folder.parent else None

        if FolderRepository.is_folder_name_unique(parentId, newName, folder.id): 
            raise ValidationException("Folder name already exists")
        
        serializer = FolderSerializer(folder, data=data, partial=True)
        if serializer.is_valid():
            return serializer.save()
        else: 
            raise ValidationException(serializer.errors)