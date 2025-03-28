from ..exceptions import ValidationError
from ..models.email import EmailRequest

def validate_email_requirements(email: EmailRequest) -> None:
    """
    Validate email request based on conditional requirements.
    
    Args:
        email: EmailRequest object to validate
        
    Raises:
        ValidationError: If validation fails
    """
    # Template validation
    has_template = email.template_id is not None
    has_content = email.text is not None or email.html is not None
    
    # Check if we have content or template
    if not has_template and not has_content:
        raise ValidationError("Either template_id or text/html content is required")
        
    # Check subject is provided if no template with default subject
    if not email.subject and not has_template:
        raise ValidationError("Subject is required when not using a template")
        
    # Check from email is provided if no template with default sender
    if not email.from_email and not has_template:
        raise ValidationError("From email is required when not using a template")