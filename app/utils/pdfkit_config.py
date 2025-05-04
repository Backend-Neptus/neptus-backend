import os
import platform
import pdfkit

def get_pdfkit_config():
    if platform.system() == 'Windows':
        return pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    else:
        return pdfkit.configuration()