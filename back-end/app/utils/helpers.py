import re
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

def generate_doc_id() -> str:
    """Generate a unique document ID"""
    return str(uuid.uuid4())

def generate_conversation_id() -> str:
    """Generate a unique conversation ID"""
    return f"conv_{str(uuid.uuid4())[:8]}"

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\-.,!?;:()\[\]{}"]', ' ', text)
    
    return text.strip()

def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to specified length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def format_timestamp(dt: datetime) -> str:
    """Format datetime to string"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def validate_url(url: str) -> bool:
    """Validate if string is a valid URL"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return ""

def calculate_similarity_score(query: str, text: str) -> float:
    """Simple text similarity calculation (can be improved with proper similarity metrics)"""
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())
    
    if not query_words or not text_words:
        return 0.0
    
    intersection = query_words.intersection(text_words)
    union = query_words.union(text_words)
    
    return len(intersection) / len(union) if union else 0.0

def safe_dict_get(dictionary: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get value from dictionary"""
    try:
        return dictionary.get(key, default)
    except (AttributeError, TypeError):
        return default

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names)-1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = filename.strip('. ')
    
    if not filename:
        filename = "untitled"
    
    return filename[:255]  # Limit length 

def filter_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Filter out None values from metadata dictionary for ChromaDB compatibility"""
    if not metadata:
        return {}
    
    filtered = {}
    for key, value in metadata.items():
        # ChromaDB only accepts str, int, float, bool
        if value is not None and isinstance(value, (str, int, float, bool)):
            filtered[key] = value
        elif value is not None:
            # Convert other types to string
            filtered[key] = str(value)
    
    return filtered

def create_document_metadata(
    doc_id: str,
    doc_type: str,
    title: Optional[str] = None,
    source: Optional[str] = None,
    custom_metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create document metadata dictionary with proper filtering"""
    metadata = {
        "doc_id": doc_id,
        "doc_type": doc_type,
    }
    
    # Add optional fields only if not None
    if title is not None:
        metadata["title"] = title
    if source is not None:
        metadata["source"] = source
    
    # Add and filter custom metadata
    if custom_metadata:
        filtered_custom = filter_metadata(custom_metadata)
        metadata.update(filtered_custom)
    
    return metadata 