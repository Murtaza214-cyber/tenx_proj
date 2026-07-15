# app/utils/regex_utils.py
import re
from typing import Optional

# Pre-compiled regex patterns for performance
# Matches patterns like ORD-12345, ord-12345, #12345, or just standalone digits with 4+ characters
ORDER_ID_PATTERN = re.compile(r'(?:ord-|#)?\b(\d{4,8})\b', re.IGNORECASE)

# Matches standard Pakistani mobile numbers (e.g., 03001234567, +923001234567, 92-300-1234567)
PK_PHONE_PATTERN = re.compile(r'^(?:\+?92|0)?-?3[0-9]{2}-?[0-9]{7}$')

# Basic email validation pattern
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


class RegexUtils:
    @staticmethod
    def extract_order_id(text: str) -> Optional[int]:
        """
        Parses raw conversational text to extract a clean, numeric order ID.
        Examples:
            "Where is my order ORD-1025?" -> 1025
            "status of #2048"             -> 2048
            "Is 9531 shipped yet?"        -> 9531
        """
        match = ORDER_ID_PATTERN.search(text)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return None
        return None

    @staticmethod
    def is_valid_pk_phone(phone: str) -> bool:
        """
        Validates if a string is a properly formatted Pakistani mobile phone number.
        """
        # Remove any whitespace or hyphens before testing
        cleaned_phone = re.sub(r'[\s-]', '', phone)
        return bool(PK_PHONE_PATTERN.match(cleaned_phone))

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validates if a string matches standard email formatting.
        """
        if not email:
            return False
        return bool(EMAIL_PATTERN.match(email.strip()))
