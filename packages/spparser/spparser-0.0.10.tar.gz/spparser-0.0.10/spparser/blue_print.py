from nbparser import Extractor
from nbparser import dbReader
from nbparser import decoder
from nbparser import encoder


html = ""



res = Extractor.re_all(field_name="result",regex_str,target_str,)

res = Extractor.xpath_all(field_name="result",xpath_ex,target_str)

res = Extractor.read_csv()

res = Extractor.read_json()

res = Extractor.css_all()





