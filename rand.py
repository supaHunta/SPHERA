import random
import string


def generate_random_email(length):
    """
    Generates a random e-mail with a given lenght
    """
    return generate_random_string(length) +"@yandex.ru"


def generate_random_wrong_email(length):
    '''
    Generates random bunch of symbols with a "@" on the end
    '''
    
    return generate_random_string + "@"


def generate_random_string(length):
    all_symbols = string.ascii_uppercase + string.digits
    return ''.join(random.choice(all_symbols) for i in range(length))
