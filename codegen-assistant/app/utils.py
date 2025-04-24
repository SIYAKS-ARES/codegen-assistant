import re

def format_code_for_html(code):
    """Python kodunu HTML içinde görüntülemek için formatlar.
    
    Args:
        code (str): Formatlanacak Python kodu
        
    Returns:
        str: HTML için güvenli formatlı kod
    """
    # HTML özel karakterlerini escape et
    code = code.replace('&', '&amp;')
    code = code.replace('<', '&lt;')
    code = code.replace('>', '&gt;')
    
    return code 