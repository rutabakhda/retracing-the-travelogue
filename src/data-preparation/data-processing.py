"""
Data cleaning and preprocessing
"""

import re
import pandas as pd
import string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))


def strip_html_tags(text):
    """
    Removes HTML tags
    :param text: Input string
    :return: string without HTML tags
    """
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text()
    return stripped_text


def convert_to_lower(text):
    """
    Coverts text to lower case
    :param text: Input string
    :return:  lower case string
    """
    text = text.lower()
    return text


def remove_panctuations(text):
    """
    Removes panctuations from text
    :param text:  Input string
    :return: Cleaned text
    """
    text = text.translate(str.maketrans(' ', ' ', string.punctuation))
    return text


def remove_white_space(text):
    """
    Removes white space from around the text
    :param text: Input text
    :return: Text after stripping white text
    """
    text = text.strip()
    return text


def remove_special_characters(text):
    """
    Removes special characters from the text
    :param text: Input text
    :return: Cleaned text after removing panctuations
    """
    pattern = r'[^a-zA-z0-9\s]'
    text = re.sub(pattern, '', text)
    return text


def remove_stopwords(text):
    """
    Removes english stop words from text
    :param text: Input text
    :return: Output text without stop words
    """
    tokens = word_tokenize(text)
    cleaned_text_list = [i for i in tokens if not i in stop_words]
    cleaned_text = " " . join(cleaned_text_list)
    return cleaned_text


def lemmatize_text(text):

    text_tokens = word_tokenize(text)
    for word in text_tokens:
        text.replace(word,lemmatizer.lemmatize(word))
    return text


def data_processing(text):
    text = convert_to_lower(text)
    text = remove_panctuations(text)
    text = remove_white_space(text)
    # text = remove_special_characters(text)
    text = remove_stopwords(text)
    # text = lemmatize_text(text)w
    return text


basepath = os.path.dirname(os.path.abspath(__file__))
datapath = basepath +'/data/hugh-murray/chapter3/'
readfile = 'chapter3.csv'


data = pd.read_csv(datapath+readfile,sep='\t', encoding='ISO-8859-1',error_bad_lines=False)

data['sentence_cleaned'] = data['sentence'].apply(lambda s:data_processing(s))
print('data processed')
data.to_csv(datapath + 'chapter3-processed.csv', sep='\t', encoding='ISO-8859-1', index=False)

