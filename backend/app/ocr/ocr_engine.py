import os
import re
from typing import Dict, Optional
from PIL import Image
import pytesseract
from app.core.config import settings


class OCREngine:
    """OCR Engine using Tesseract"""
    
    def __init__(self):
        if settings.TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
    
    def preprocess_image(self, image_path: str) -> Image.Image:
        """Preprocess image for better OCR accuracy"""
        image = Image.open(image_path)
        
        # Convert to grayscale
        image = image.convert('L')
        
        # You can add more preprocessing steps here:
        # - Noise reduction
        # - Contrast enhancement
        # - Binarization
        
        return image
    
    def extract_text(self, image_path: str) -> str:
        """Extract raw text from image"""
        image = self.preprocess_image(image_path)
        text = pytesseract.image_to_string(image, lang=settings.OCR_LANGUAGE)
        return text
    
    def parse_invoice_data(self, text: str) -> Dict:
        """Parse invoice data from extracted text"""
        data = {
            "invoice_number": None,
            "date": None,
            "supplier_name": None,
            "client_name": None,
            "subtotal": None,
            "tax": None,
            "total": None,
            "items": []
        }
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to extract invoice number
            invoice_patterns = [
                r'(?:invoice|factura|no\.?|#)\s*:?\s*([A-Z0-9\-]+)',
                r'(?:invoice number|número de factura)\s*:?\s*([A-Z0-9\-]+)'
            ]
            for pattern in invoice_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match and not data["invoice_number"]:
                    data["invoice_number"] = match.group(1)
            
            # Try to extract date
            date_patterns = [
                r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})'
            ]
            for pattern in date_patterns:
                match = re.search(pattern, line)
                if match and not data["date"]:
                    data["date"] = match.group(1)
            
            # Try to extract monetary amounts
            if re.search(r'(?:subtotal|sub-total)', line, re.IGNORECASE):
                amount = self._extract_amount(line)
                if amount and not data["subtotal"]:
                    data["subtotal"] = amount
            
            if re.search(r'(?:tax|iva|igv|impuesto)', line, re.IGNORECASE):
                amount = self._extract_amount(line)
                if amount and not data["tax"]:
                    data["tax"] = amount
            
            if re.search(r'(?:total|amount due)', line, re.IGNORECASE):
                amount = self._extract_amount(line)
                if amount and not data["total"]:
                    data["total"] = amount
        
        return data
    
    def _extract_amount(self, text: str) -> Optional[float]:
        """Extract monetary amount from text"""
        # Look for patterns like: $1,234.56 or 1234.56 or 1.234,56
        patterns = [
            r'\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'\$?\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    return float(amount_str)
                except ValueError:
                    continue
        
        return None
    
    def process_invoice(self, image_path: str) -> Dict:
        """Complete invoice processing pipeline"""
        try:
            # Extract text
            text = self.extract_text(image_path)
            
            # Parse invoice data
            data = self.parse_invoice_data(text)
            
            # Add raw text for reference
            data["raw_text"] = text
            data["status"] = "success"
            
            return data
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "raw_text": None
            }
