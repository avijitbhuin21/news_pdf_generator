import os
import glob
from pathlib import Path
from typing import List, Union
import pdfkit
from PyPDF2 import PdfMerger
import tempfile
from datetime import datetime

class HTMLToPDFConverter:
    """
    A class to convert HTML files or content to PDF pages and combine them into a single PDF document.
    """
    
    def __init__(self, output_dir: str = "generated_pdf"):
        """
        Initialize the converter.
        
        Args:
            output_dir (str): Directory to save the generated PDF files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # PDF generation options for better quality
        self.pdf_options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'print-media-type': None,
            'disable-smart-shrinking': None,
        }
    
    def html_to_pdf_page(self, html_content: str, output_path: str) -> bool:
        """
        Convert HTML content to a single PDF page.
        
        Args:
            html_content (str): HTML content as string
            output_path (str): Path where the PDF should be saved
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            pdfkit.from_string(html_content, output_path, options=self.pdf_options)
            return True
        except Exception as e:
            print(f"Error converting HTML to PDF: {e}")
            return False
    
    def html_file_to_pdf_page(self, html_file_path: str, output_path: str) -> bool:
        """
        Convert HTML file to a single PDF page.
        
        Args:
            html_file_path (str): Path to the HTML file
            output_path (str): Path where the PDF should be saved
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            pdfkit.from_file(html_file_path, output_path, options=self.pdf_options)
            return True
        except Exception as e:
            print(f"Error converting HTML file {html_file_path} to PDF: {e}")
            return False
    
    def convert_html_files_to_pdf(self, html_files: List[str], output_filename: str = None) -> str:
        """
        Convert multiple HTML files to individual PDF pages and combine them into one PDF.
        
        Args:
            html_files (List[str]): List of HTML file paths
            output_filename (str): Name of the final combined PDF file
            
        Returns:
            str: Path to the combined PDF file
        """
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"combined_news_{timestamp}.pdf"
        
        output_path = self.output_dir / output_filename
        temp_pdfs = []
        
        try:
            # Convert each HTML file to a temporary PDF
            for i, html_file in enumerate(html_files):
                if not os.path.exists(html_file):
                    print(f"Warning: HTML file {html_file} not found, skipping...")
                    continue
                
                temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
                temp_pdf.close()
                
                print(f"Converting {html_file} to PDF page {i+1}...")
                if self.html_file_to_pdf_page(html_file, temp_pdf.name):
                    temp_pdfs.append(temp_pdf.name)
                else:
                    os.unlink(temp_pdf.name)  # Clean up failed conversion
            
            if not temp_pdfs:
                raise Exception("No HTML files were successfully converted to PDF")
            
            # Combine all PDF pages into one document
            print(f"Combining {len(temp_pdfs)} PDF pages into {output_filename}...")
            self._combine_pdfs(temp_pdfs, str(output_path))
            
            # Clean up temporary files
            for temp_pdf in temp_pdfs:
                try:
                    os.unlink(temp_pdf)
                except:
                    pass
            
            print(f"Successfully created combined PDF: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"Error during PDF conversion: {e}")
            # Clean up any temporary files
            for temp_pdf in temp_pdfs:
                try:
                    os.unlink(temp_pdf)
                except:
                    pass
            raise
    
    def convert_html_content_list_to_pdf(self, html_contents: List[str], output_filename: str = None) -> str:
        """
        Convert a list of HTML content strings to individual PDF pages and combine them into one PDF.
        
        Args:
            html_contents (List[str]): List of HTML content strings
            output_filename (str): Name of the final combined PDF file
            
        Returns:
            str: Path to the combined PDF file
        """
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"combined_news_{timestamp}.pdf"
        
        output_path = self.output_dir / output_filename
        temp_pdfs = []
        
        try:
            # Convert each HTML content to a temporary PDF
            for i, html_content in enumerate(html_contents):
                temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
                temp_pdf.close()
                
                print(f"Converting HTML content {i+1} to PDF page...")
                if self.html_to_pdf_page(html_content, temp_pdf.name):
                    temp_pdfs.append(temp_pdf.name)
                else:
                    os.unlink(temp_pdf.name)  # Clean up failed conversion
            
            if not temp_pdfs:
                raise Exception("No HTML content was successfully converted to PDF")
            
            # Combine all PDF pages into one document
            print(f"Combining {len(temp_pdfs)} PDF pages into {output_filename}...")
            self._combine_pdfs(temp_pdfs, str(output_path))
            
            # Clean up temporary files
            for temp_pdf in temp_pdfs:
                try:
                    os.unlink(temp_pdf)
                except:
                    pass
            
            print(f"Successfully created combined PDF: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"Error during PDF conversion: {e}")
            # Clean up any temporary files
            for temp_pdf in temp_pdfs:
                try:
                    os.unlink(temp_pdf)
                except:
                    pass
            raise
    
    def _combine_pdfs(self, pdf_files: List[str], output_path: str):
        """
        Combine multiple PDF files into one.
        
        Args:
            pdf_files (List[str]): List of PDF file paths to combine
            output_path (str): Path for the combined PDF file
        """
        merger = PdfMerger()
        
        try:
            for pdf_file in pdf_files:
                merger.append(pdf_file)
            
            with open(output_path, 'wb') as output_file:
                merger.write(output_file)
        finally:
            merger.close()
    
    def find_html_files(self, directory: str = ".", pattern: str = "*.html") -> List[str]:
        """
        Find all HTML files in a directory.
        
        Args:
            directory (str): Directory to search for HTML files
            pattern (str): File pattern to match (default: "*.html")
            
        Returns:
            List[str]: List of HTML file paths
        """
        search_path = os.path.join(directory, pattern)
        html_files = glob.glob(search_path)
        html_files.sort()  # Sort for consistent ordering
        return html_files


def convert_html_files_to_combined_pdf(html_files: List[str], output_filename: str = None, output_dir: str = "generated_pdf") -> str:
    """
    Convenience function to convert HTML files to a combined PDF.
    
    Args:
        html_files (List[str]): List of HTML file paths
        output_filename (str): Name of the output PDF file
        output_dir (str): Directory to save the PDF
        
    Returns:
        str: Path to the generated PDF file
    """
    converter = HTMLToPDFConverter(output_dir)
    return converter.convert_html_files_to_pdf(html_files, output_filename)


def convert_html_content_to_combined_pdf(html_contents: List[str], output_filename: str = None, output_dir: str = "generated_pdf") -> str:
    """
    Convenience function to convert HTML content strings to a combined PDF.
    
    Args:
        html_contents (List[str]): List of HTML content strings
        output_filename (str): Name of the output PDF file
        output_dir (str): Directory to save the PDF
        
    Returns:
        str: Path to the generated PDF file
    """
    converter = HTMLToPDFConverter(output_dir)
    return converter.convert_html_content_list_to_pdf(html_contents, output_filename)


# Example usage
if __name__ == "__main__":
    # Example 1: Convert HTML files from a directory
    converter = HTMLToPDFConverter()
    
    # Find all HTML files in current directory
    html_files = converter.find_html_files(".", "*.html")
    
    if html_files:
        print(f"Found {len(html_files)} HTML files: {html_files}")
        output_pdf = converter.convert_html_files_to_pdf(html_files, "news_articles.pdf")
        print(f"Combined PDF saved as: {output_pdf}")
    else:
        print("No HTML files found in current directory")
        
        # Example 2: Create sample HTML content and convert to PDF
        from handler_functions.html import get_html_content
        
        sample_data = [
            {
                'title': 'Spain and England Record Hottest June as Heatwave Grips Europe',
                'description': 'Several European regions had their highest temperatures on the last day of June, as a heatwave continues into July.',
                'media_url': 'https://ichef.bbci.co.uk/ace/standard/240/cpsprodpb/4bad/live/164eb1a0-566f-11f0-9f6a-932e10cc460f.jpg',
                'link': 'https://www.bbc.com/news/articles/c70rrlexnwzo'
            },
            {
                'title': 'AI Technology Breakthrough in Medical Research',
                'description': 'Researchers have developed a new AI system that can diagnose diseases with 95% accuracy.',
                'media_url': 'https://picsum.photos/600/400',
                'link': 'https://example.com/ai-medical-research'
            }
        ]
        
        html_contents = [get_html_content(data) for data in sample_data]
        output_pdf = converter.convert_html_content_list_to_pdf(html_contents, "sample_news.pdf")
        print(f"Sample PDF created: {output_pdf}")