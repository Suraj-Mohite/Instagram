from .constants import IMAGE_EXTENSIONS
import logging
import sys

logger = logging.getLogger(__name__)

def get_user_directory_path(instance, filename):
    try:
        logger.info(f"Inside get_user_directory_path ====> {instance._meta.model_name}", extra={'AppName': 'base'})
        if instance._meta.model_name == "profile":
            id = instance.user.id
            folder_name = "profile_image"
        else:
            id = instance.post.user.id
            folder_name = "posts"

        ext = filename.split('.')[-1]

        if ext not in IMAGE_EXTENSIONS:
            raise ValueError(f"invalid File format. uploaded file does not belong to {IMAGE_EXTENSIONS}")
        
        filename = f"{id}_{filename}"
        return f"images/user_{id}/{folder_name}/{filename}"
    
    except ValueError as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("get_user_directory_path %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'base'})
        return None
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("ERROR in get_user_directory_path %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'base'})
        return "image"
    
