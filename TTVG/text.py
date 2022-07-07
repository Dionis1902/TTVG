import re

emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"
                           u"\U0001F300-\U0001F5FF"
                           u"\U0001F680-\U0001F6FF"
                           u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE)

special_pattern = re.compile(r'["#$%&\'()*+\-/:;<=>@\[\\\]^_`{|}~]')
url_pattern = re.compile(r'https?:\/\/.*[\r\n]*')


def del_url(text):
    return url_pattern.sub(r'', text)


def get_printable_text(text):
    return emoji_pattern.sub(r'', del_url(text))


def get_voice_text(text):
    return special_pattern.sub(r'', get_printable_text(text)).replace('\n', '.')


