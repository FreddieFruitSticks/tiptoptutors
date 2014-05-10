
def convert_to_international_format(msisdn, country_code='27'):
    '''
    Tries to convert the MSISDN to international format.
    Examples:
    * convert_to_international_format('0731234567', '27') returns
    '27731234567'.
    * convert_to_international_format('+27731234567', '27') returns
    '27731234567'.
    '''
    if msisdn.startswith('+'):
        return msisdn.lstrip('+')
    elif msisdn.startswith('0'):
        return '%s%s' % (country_code, msisdn[1:])
    return msisdn
