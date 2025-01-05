from rest_framework import serializers
from .models import Folder, Document

class FolderSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ['id', 'parent', 'name', 'created_at', 'updated_at', 'children', 'documents']

    def get_children(self, obj):
        """
        Retrieve and serialize the child folders of the current folder object.
        
        This method handles the recursion for serializing child folders (subfolders) of the given folder.
        It fetches all the child folders using the `children` related manager and serializes them recursively.
        
        Args:
            obj: The current folder instance being serialized.
            
        Returns:
            List: A list of serialized child folders.
        """
        children = obj.children.all()
        # Recursively serialize the children and return the data
        return FolderSerializer(children, many=True).data

    def get_documents(self, obj):
        """
        Retrieve and serialize the documents associated with the current folder object.
        
        This method fetches all the documents linked to the folder and serializes them using the DocumentSerializer.
        
        Args:
            obj: The current folder instance being serialized.
            
        Returns:
            List: A list of serialized documents associated with the folder.
        """
        documents = obj.documents.all()
        return DocumentSerializer(documents, many=True).data


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'parent', 'name', 'file']