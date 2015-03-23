def _safe_extract(selector):
    ''' _safe_extract
        Takes a selector and performs an extract if it is callable and returns
        the result else returns the selector
    '''
    if 'extract' in selector and callable(selector.extract):
        data = selector.extract()
    else:
        data = selector
    return data
def _safe_pop(selector):
    ''' _safe_pop
        Takes a selector and returns the first value if it is a list and
        length > 0 else it returns the selector
    '''
    if type(selector) is list and len(selector) > 0:
        value = selector.pop()
    else:
        value = selector

def clean_scrape_generator(field):
    ''' clean_scrape_generator -
        params: field - the name of the field contained in selector
                selector - the selector containing the text of the content
                        should not require any more processing
        returns a function that is used to scrape an element where the
            data can be uniquely identified with an xpath
    '''
    def clean_scrape(selector):
        data = _safe_extract(selector)
        value = _safe_pop(selector)
        clean_value = value.strip()
        return (field, clean_value)

def split_scrape_generator(split_character, content_index, key_index=-1, field=""):
    ''' split_scrape_generator
        params:
            selector - the selector containing the text that will be split to yield
                the key and the content value
            split_character - the character that will be used to seperate the key
            content_index - the index in the list where the content will be after
                spliting the string contained in the selector
            key_index - index of the key in the split array
            field - the field the content will be stored in
                must specify either key index or field
        returns:
            parsing function that takes a selector and returns a ParseResult object
    '''
    def split_scrape(selector):
        data = _safe_extract(selector)
        value = _safe_pop(selector)
        clean_value = value.strip()
        key = field
        split_list = clean_value.split(split_character)
        if key_index != -1:
            key = split_list[key_index]
        return (key, split_list[content_index])

def nested_xpath_scrape_generator(content_xpath, key_xpath):
    ''' nested_xpath_scrape_generator
        params:
            selector - the selector containing the content and the key
            content_xpath - the xpath relative to the selector that will be used
                to extract the content. it should end with text()
            key_xpath - the xpath relative to the selector that will be used
                to extract the key. it should end with text()
        returns:
            parsing functiont that takes a selector and returns a ParseResult object
    '''
    def nested_xpath_scrape(selector):
        content_selector = selector.xpath(content_xpath)
        key_selector = selector.xpath(key_xpath)
        content = _safe_pop(_safe_extract(content_selector))
        key = _safe_pop(_safe_extract(content_selector))
        return (key, content)
