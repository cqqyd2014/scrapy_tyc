from scrapy_tyc import  ScrapyTyc


tyc=ScrapyTyc("yonghuming","mima")
try:
    tyc.get_company_main_info('company','2349015448')
finally:
    tyc.scrap_end()
