import os
import base64
from typing import Dict, Any, List
import logging

from ..exceptions import ValidationError
from ..models.email import EmailAttachment

logger = logging.getLogger(__name__)

def process_file_attachments(attachments: List[Dict[str, Any]]) -> List[EmailAttachment]:
    """
    Process file attachments by reading file content and encoding as base64.
    
    Args:
        attachments: List of attachment dictionaries with possible 'file_path' keys
        
    Returns:
        List of processed Attachment objects
        
    Raises:
        ValidationError: If file cannot be read or attachment data is invalid
    """
    processed_attachments = []
    
    for attachment_data in attachments:
        # Handle file_path if present
        if isinstance(attachment_data, dict) and 'file_path' in attachment_data:
            file_path = attachment_data.pop('file_path')
            
            try:
                # Read and encode file content
                with open(file_path, 'rb') as file:
                    file_content = base64.b64encode(file.read()).decode('utf-8')
                
                # Use filename from path if not provided
                if 'filename' not in attachment_data:
                    attachment_data['filename'] = os.path.basename(file_path)
                    
                # Set default disposition if not provided
                if 'disposition' not in attachment_data:
                    attachment_data['disposition'] = 'attachment'
                
                # Add file content
                attachment_data['content'] = file_content
                
            except IOError as e:
                logger.error(f"Failed to read attachment file {file_path}: {str(e)}")
                raise ValidationError(f"Cannot read attachment file {file_path}: {str(e)}")
        
        # Create Attachment object from the dict
        try:
            attachment = EmailAttachment(**attachment_data)
            processed_attachments.append(attachment)
            logger.debug(f"Processed attachment: {attachment.filename}")
        except Exception as e:
            logger.error(f"Failed to create Attachment object: {str(e)}")
            raise ValidationError(f"Invalid attachment data: {str(e)}")
    
    return processed_attachments