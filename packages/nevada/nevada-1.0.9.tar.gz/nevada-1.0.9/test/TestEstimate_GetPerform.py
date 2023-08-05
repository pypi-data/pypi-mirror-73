from nevada.API.Estimate import *
from nevada.Common.Connector import *

base_url = 'https://api.naver.com' #그대로 두세요.

api_key = "01000000007705c93bf3d4717735ec919410620b09be66dba57008ea9ebd5c689cb34f9b03" #변경하세요.
secret_key = "AQAAAAB3Bck789RxdzXskZQQYgsJSgvA+JzNVuO1lfU2x5/4bA==" #변경하세요.
customer_id = 1839303 #변경하세요.

estimate = Estimate(base_url=base_url, api_key=api_key, secret_key=secret_key, customer_id=customer_id)

result = estimate.get_performance_json(type='keyword', device='BOTH', keywordplus=False, key='종이빨대', bids=[100, 200, 300])
print(result, "\n")

result_list = estimate.get_performance_list(type='keyword', device='BOTH', keywordplus=False, key='종이빨대', bids=[100, 200, 300])

for i in result_list:
    print("종이빨대")
    CommonFunctions.print_all_attr(i)  # from nevada.Common.Connector import * 를 해줘야 함.

