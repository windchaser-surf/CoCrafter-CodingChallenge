def create_folder_data(parentFolder, newFolderNumber):
    """
    Generate metadata for a new folder, including its ID and name.

    This method creates a unique ID and name for the folder based on its parent folder.
    If the parent folder is the root, the new folder is assigned a simpler name and ID.
    Otherwise, the name and ID are based on the parent's details.

    Args:
        parentFolder: The parent folder instance to which the new folder belongs.
        newFolderNumber: An integer representing the next folder number in the sequence.

    Returns:
        dict: A dictionary containing the ID, name, and parent ID of the new folder.
    """
    if parentFolder.name == "Root":
        newFolderName = f"Folder-{newFolderNumber}"
        newFolderId = f"folder-{newFolderNumber}"
    else: 
        newFolderName = f"{parentFolder.name}-{newFolderNumber}"
        newFolderId = f"{parentFolder.id}-{newFolderNumber}"
    return {
        "id": newFolderId,
        "name": newFolderName,
        "parent": parentFolder.id
    }