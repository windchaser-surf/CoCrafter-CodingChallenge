from ..models import Folder, Document
from ..exceptions import NotFoundException, ValidationException
from ..serializers import DocumentSerializer
from django.utils.text import slugify
import os


class DocumentService: 
    @staticmethod
    def handle_duplicate_filename(parent_folder, file):
        """
        Check if a file with the same name already exists in the given folder.
        If it does, append a number (e.g., 'file1', 'file2', etc.) to create a unique filename.
        
        Args:
            parent_folder: The folder in which to check for the file.
            file: The file object being uploaded.
        
        Returns:
            str: The unique file name to be used for saving the file.
        """
        original_name, extension = os.path.splitext(file.name)
        file_name = slugify(original_name) #removes spaces and special character and replace it with '-'
        
        counter = 1
        new_file_name = f"{file_name}{extension}"
        
        while Document.objects.filter(parent=parent_folder, name=new_file_name).exists():
            new_file_name = f"{file_name}{counter}{extension}"
            counter += 1
        
        return new_file_name
    
    @staticmethod
    def create_document(data):
        """
        Handle document creation, including saving the document and performing validation.
        
        Args:
            data: The request data to create the document (including parent folder and file).
        
        Returns:
            Document: The created Document instance.
        
        Raises:
            ValidationException: If the data is invalid.
            NotFoundException: If the parent folder does not exist.
        """        
        parentId = data.get('parentId')
        file = data.get('data')
        if not parentId or not file: 
            raise ValidationException("Missing parentId or file")
        
        try:
            parentFolder = Folder.objects.get(id=parentId)
        except Folder.DoesNotExist:
            raise NotFoundException("Parent folder does not exist")
        
        uniqueFileName = DocumentService.handle_duplicate_filename(parentFolder, file)

        data = {
            'parent': parentFolder.id,
            'name': uniqueFileName,
            'file': file
        }

        serializer = DocumentSerializer(data=data)
        if serializer.is_valid():
            return serializer.save()
        raise ValidationException("Invalid document data")
    
    @staticmethod
    def get_document_by_id(documentId):
        """
        Retrieve a document by its ID.

        Args:
            documentId: The ID of the document.

        Returns:
            Document: The document object.

        Raises:
            NotFoundException: If the document does not exist.
        """
        try:
            return Document.objects.get(id=documentId)
        except Document.DoesNotExist: 
            raise NotFoundException("Document not found")
    
    @staticmethod
    def update_document(document, data):
        """
        Handle the partial update of a document.
        
        Args:
            document: The document instance to update.
            data: The data to update the document with.
        
        Returns:
            Document: The updated document instance.
        
        Raises:
            ValidationException: If the update data is invalid or file name already exists.
        """
        if Document.objects.filter(parent=document.parent.id, name=data.get('name')).exists():
            raise ValidationException("File name already in use.")
        serializer = DocumentSerializer(document, data=data, partial=True)
        if serializer.is_valid():
            return serializer.save()
        else: 
            raise ValidationException("Invalid data for update.")


