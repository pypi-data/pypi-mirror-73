from nevada.API.Campaign import *

base_url = 'https://api.naver.com' #그대로 두세요.

api_key = "01000000007705c93bf3d4717735ec919410620b09be66dba57008ea9ebd5c689cb34f9b03" #변경하세요.
secret_key = "AQAAAAB3Bck789RxdzXskZQQYgsJSgvA+JzNVuO1lfU2x5/4bA==" #변경하세요.
customer_id = 1839303 #변경하세요.

campaign = Campaign(base_url=base_url, api_key=api_key, secret_key=secret_key, customer_id=customer_id)

result_json = campaign.get('cmp-a001-01-000000002696103')
result_obj = CommonFunctions.json_to_object(result_json, CampaignObject)
CommonFunctions.print_all_attr(result_obj)