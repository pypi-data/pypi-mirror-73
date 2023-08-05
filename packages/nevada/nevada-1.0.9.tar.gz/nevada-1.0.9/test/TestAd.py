from nevada.API.Ad import *

base_url = 'https://api.naver.com' #그대로 두세요.

api_key = "01000000007705c93bf3d4717735ec919410620b09be66dba57008ea9ebd5c689cb34f9b03" #변경하세요.
secret_key = "AQAAAAB3Bck789RxdzXskZQQYgsJSgvA+JzNVuO1lfU2x5/4bA==" #변경하세요.
customer_id = 1839303 #변경하세요.

ad = Ad(base_url=base_url, api_key=api_key, secret_key=secret_key, customer_id=customer_id)


ad_json = ad.list(['nad-a001-01-000000086037429', 'nad-a001-03-000000086038948'])
ad_obj = CommonFunctions.json_to_object(ad_json, AdObject)
for i in ad_obj:
    CommonFunctions.print_all_attr(i)