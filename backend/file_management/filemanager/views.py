from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Folder, Document
from .serializers import FolderSerializer, DocumentSerializer
from .services.folder_service import FolderService
from .services.document_service import DocumentService
from .exceptions import ValidationException, NotFoundException
from django.http import FileResponse


class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    
    def create(self, request):
        """
        Handle POST requests to create a new folder.
        
        The method calls a service layer (FolderService) to encapsulate the business logic
        for folder creation. This decouples the creation logic from the view and keeps the view cleaner.
        
        Args:
            request: The HTTP request containing the data for the new folder.
            
        Returns:
            Response: A Response object that contains the serialized data of the created folder or an error message.
        """
        try:
            folder = FolderService.create_folder(request.data)
            return Response(FolderSerializer(folder).data, status=status.HTTP_201_CREATED)
        except NotFoundException as e:
            return Response({"error": e.message}, status=status.HTTP_404_NOT_FOUND)
        except ValidationException as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """
        Handle GET requests to list the root folder.
        
        This method retrieves the root folder from the database. If it doesn't exist,
        it returns a 404 Not Found status with a descriptive error message.
        
        Args:
            request: The HTTP request for retrieving the list of folders.
            
        Returns:
            Response: A Response object containing the serialized data of the root folder or an error message.
        """
        try:
            root_folder = Folder.objects.get(id='root')
            serializer = self.get_serializer(root_folder)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Folder.DoesNotExist:
            return Response({"detail": "Root folder not found."}, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        """
        Handle DELETE requests to delete a folder.
        
        This method attempts to delete a folder by its primary key (pk). If the folder doesn't exist,
        a 404 Not Found error is returned. If successful, a 204 No Content status is returned.
        
        Args:
            request: The HTTP request to delete a folder.
            pk: The primary key of the folder to be deleted.
            
        Returns:
            Response: A Response object indicating success (204) or failure (404).
        """
        try:
            folder = Folder.objects.get(pk=pk)
            folder.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Folder.DoesNotExist:
            return Response({"detail": "Folder not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None, partial=False):
        """
        Handle folder update via a PATCH request.

        This method retrieves a folder by its ID (using pk) and updates its details using the
        FolderService. The updated folder is serialized for the response.

        Args:
            request: The HTTP request containing the updated folder data.
            pk: The primary key of the folder to be updated.

        Returns:
            Response: A Response object with the serialized updated folder data (HTTP 200 OK),
                    or an error message with the appropriate HTTP status.
        """
        try: 
            folder = Folder.objects.get(pk=pk)
        except:
            return Response({"detail": "Folder not found"}, status = status.HTTP_404_NOT_FOUND)
        
        try:
            updateFolder = FolderService.update_folder(folder, request.data, partial)
            return Response(FolderSerializer(updateFolder).data, status=status.HTTP_200_OK)
        except ValidationException as e:
            return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)
        

class DocumentAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)  

    def post(self, request, *args, **kwargs):
        """
        Handle document creation via a POST request.

        This method delegates the creation of a document to the DocumentService, which performs
        business logic and validation. It serializes the created document for the response.

        Args:
            request: The HTTP request containing the document data.

        Returns:
            Response: A Response object with the serialized document data (HTTP 201 Created),
                    or an error message with the appropriate HTTP status.
        """    
        try:
            document = DocumentService.create_document(request.data)
            return Response(DocumentSerializer(document).data, status=status.HTTP_201_CREATED)
        except NotFoundException as e: 
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)
        except ValidationException as e:
            return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)

    
    def get (self, request, *args, **kwargs):
        """
        Handle document retrieval via a GET request.

        This method retrieves a document by its ID and provides it as a downloadable file.
        The document's file handle is opened and returned in the response.

        Args:
            request: The HTTP request for retrieving the document.
            kwargs: Additional parameters, including the 'id' of the document.

        Returns:
            FileResponse: A response with the document file as an attachment (HTTP 200 OK).
            Response: A response with an error message (HTTP 404 Not Found) if the document is not found.

        Raises:
            NotFoundException: If the document with the provided ID does not exist.
        """
        documentId = kwargs.get('id')
        try: 
            document = DocumentService.get_document_by_id(documentId)
            file_handle = document.file.open()
            response = FileResponse(file_handle, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{document.name}"'           
            return response
        except NotFoundException as e: 
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)
  

    def patch(self, request, *args, **kwargs):
        """
        Handle document updates via a PATCH request.

        This method retrieves a document by its ID and updates its details using the
        DocumentService. The updated document is serialized for the response.

        Args:
            request: The HTTP request containing the updated document data.
            kwargs: Additional parameters, including the 'id' of the document.

        Returns:
            Response: A Response object with the serialized updated document data (HTTP 200 OK),
                    or an error message with the appropriate HTTP status.
        """
        documentId = kwargs.get('id')
        try: 
            document = DocumentService.get_document_by_id(documentId)
            updatetDocument = DocumentService.update_document(document, request.data)
            return Response(DocumentSerializer(updatetDocument).data, status=status.HTTP_200_OK)
        except NotFoundException as e:
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)
        except ValidationException as e:
            return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        """
        Handle document deletion via a DELETE request.

        This method retrieves a document by its ID and deletes it from the database.
        If the document does not exist, an appropriate error is returned.

        Args:
            request: The HTTP request to delete the document.
            kwargs: Additional parameters, including the 'id' of the document.

        Returns:
            Response: A Response object with no content (HTTP 204 No Content) on success,
                        or an error message (HTTP 404 Not Found) if the document is not found.
        """        
        document_id = kwargs.get('id')
        try: 
            document = Document.objects.get(id=document_id)
            document.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        except Document.DoesNotExist:
            return Response({'error': 'File does not exist.'}, status=status.HTTP_404_NOT_FOUND)
