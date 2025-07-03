from PyPDF2 import PdfMerger
import tempfile
import os
import pdfkit
import shutil
from concurrent.futures import ThreadPoolExecutor
import functools
import base64
import io

# Create temporary directory for individual PDFs
def create_pdf_file(data:dict):
    temp_dir = tempfile.mkdtemp()
    pdf_files = []

    try:
        options = {
        'page-size': 'A5',  # Smaller page size (A5 is half the size of A4)
        'page-width': '150mm',  # Custom width (optional, overrides page-size width)
        'page-height': '220mm',  # Custom height (optional, overrides page-size height)
        'margin-top': '0',
        'margin-right': '0',
        'margin-bottom': '0',
        'margin-left': '0',
        'encoding': "UTF-8",
        # 'print-media-type': '', 
        'no-outline': None
    }
        # Convert each HTML to a separate PDF
        def get_pdf(html_content, temp_pdf_path, options):
            pdfkit.from_string(html_content, temp_pdf_path, options=options)
            return temp_pdf_path

        with ThreadPoolExecutor(max_workers=10) as executor:
            # Create partial function with fixed options
            create_pdf_with_options = functools.partial(get_pdf, options=options)
            
            # Submit all tasks
            futures = []
            for i, html_content in enumerate(data['pdf_html']):
                temp_pdf_path = os.path.join(temp_dir, f'temp_{i}.pdf')
                future = executor.submit(create_pdf_with_options, html_content, temp_pdf_path)
                futures.append((future, temp_pdf_path))
            
            # Collect results
            for future, temp_pdf_path in futures:
                future.result()  # Wait for completion
                pdf_files.append(temp_pdf_path)
        

        # Merge all PDFs into one in memory
        merger = PdfMerger()
        for pdf_file in pdf_files:
            merger.append(pdf_file)
        
        # Write to BytesIO buffer instead of file
        pdf_buffer = io.BytesIO()
        merger.write(pdf_buffer)
        merger.close()
        
        # Convert to base64
        pdf_buffer.seek(0)
        pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')
        
    finally:
        # Clean up temporary files
        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):
                os.remove(pdf_file)
        shutil.rmtree(temp_dir)

    return pdf_base64