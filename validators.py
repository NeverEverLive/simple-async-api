import re


class Validator():
    __url_pattern = "^http(s)?://[a-zA-z]*.(com|ru)(/([a-zA-z]|\d*)*)*$"
    
    @staticmethod
    def validate_url(url: str):
        return re.search(Validator.__url_pattern, url)
