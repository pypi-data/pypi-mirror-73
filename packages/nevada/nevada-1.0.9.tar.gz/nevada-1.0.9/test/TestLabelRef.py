from nevada.Common.Connector import *
from nevada.API.LabelRef import *

base_url = 'https://api.naver.com' #그대로 두세요.

api_key = "01000000007705c93bf3d4717735ec919410620b09be66dba57008ea9ebd5c689cb34f9b03" #변경하세요.
secret_key = "AQAAAAB3Bck789RxdzXskZQQYgsJSgvA+JzNVuO1lfU2x5/4bA==" #변경하세요.
customer_id = 1839303 #변경하세요.

lr = LabelRef(base_url=base_url, api_key=api_key, secret_key=secret_key, customer_id=customer_id)

result_json = lr.update(editTm='2020-02-10T03:14:52.000Z', customerId=1810030, enable=True, nccLabelId='lbl-a001-00-000000000106050',refId='nad-a001-01-000000086037429', refTp='AD', regTm='2020-02-10T02:48:38.000Z')
result_obj = CommonFunctions.json_to_object(result_json, LabelRefObject)
for i in result_obj:
    CommonFunctions.print_all_attr(i)