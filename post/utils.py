
from .constants import IMAGE_EXTENSIONS
from bs4 import BeautifulSoup
import logging
import sys

logger = logging.getLogger(__name__)

def get_user_directory_path(instance, filename):
    try:
        logger.info("Inside get_user_directory_path ", extra={'AppName': 'post'})
        id = instance.post.user.id
        ext = filename.split('.')[-1]

        if ext not in IMAGE_EXTENSIONS:
            raise ValueError(f"invalid File format. uploaded file does not belong to {IMAGE_EXTENSIONS}")
        
        filename = f"{id}_{filename}"
        return f"images/{id}/{filename}"
    
    except ValueError as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("get_user_directory_path %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
        return None
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("ERROR in get_user_directory_path %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
        return "image"
    

def remove_html_tags(text):
    try:
        logger.info("Inside remove_html_tags ", extra={'AppName': 'BaseApp'})
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("ERROR in remove_html_tags %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
        return None

def get_tag_list_from_caption(caption):
    try:
        return [word[1:] for word in caption.split(' ') if word.startswith('#') and len(word) > 1]
    except Exception as e:
        return []