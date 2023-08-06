# docci

Various document management utils

## Usage

The `docci.file.FileAttchment` class is root of whole package. 
It abstracts work with files and provides useful properties like base64 convertion, content-disposition header generation, mimetype detection:

```python
from docci.file import FileAttachment

# Create file attachment from file
file = FileAttachment.load("path/to/file")

# Now you can use the FileAttachment features:
# Get base64 file representation
file.content_base64

# Generate Content-Disposition header with file name
file.content_disposition

# Get file extension
file.extension

# Get file mimetype
file.mimetype

# Save file to disk
file.save("path/to/file")
```  

To see other features proceed to the [documentation](https://docci.readthedocs.io/en/latest/) 