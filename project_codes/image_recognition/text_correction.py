import language_tool_python
import string
from autocorrect import Speller
import unicodedata

# language_tool_python API usage
tool = language_tool_python.LanguageTool('en-US')
spell = Speller(lang='en')

MAX_LEN_TEXT = 1000


def get_clean_text(text, replace=' '):
    """
        Args: 
            string, text that want to clean out garbled text

        Raises: -

        Returns: string, clean text
    """
    whitelist = "-_.() %s%s" % (string.ascii_letters, string.digits)
    char_limit = MAX_LEN_TEXT
    # replace spaces
    for r in replace:
        text = text.replace(r, ' ')

    # keep only valid ascii chars
    cleaned_text = unicodedata.normalize(
        'NFKD', text).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    cleaned_text = ''.join(c for c in cleaned_text if c in whitelist)
    if len(cleaned_text) > char_limit:
        print("Warning, texts truncated because it was over {}. Texts may no longer be unique".format(
            char_limit))
    else:
        return cleaned_text[:char_limit]


def get_corrected_text(text):
    """
        Args: 
            string, text that want to correct

        Raises: -

        Returns: string, corrected text
    """
    try:
        text = get_clean_text(text)
        text = tool.correct(text)
        text = text.strip()
        return text
    except:
        assert 0, "error with {get_corrected_text.__name__}"
        pass
