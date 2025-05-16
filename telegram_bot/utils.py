import re

def escape_markdown_v2(text: str) -> str:
    """
    Экранирует специальные символы MarkdownV2, включая те, которые Telegram не использует, но могут вызывать ошибки.
    """
    if not isinstance(text, str):
        return text

    # Все спецсимволы из документации Telegram
    special_chars = r'_*[]()~`>#+-=|{}.!'

    return re.sub(f'([{re.escape(special_chars)}])', r'\\\1', text)
