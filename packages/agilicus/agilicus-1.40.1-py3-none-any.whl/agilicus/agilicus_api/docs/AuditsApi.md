# agilicus_api.AuditsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_audits**](AuditsApi.md#list_audits) | **GET** /v1/audits | View audit records


# **list_audits**
> ListAuditsResponse list_audits(limit=limit, user_id=user_id, dt_from=dt_from, dt_to=dt_to, action=action, target_id=target_id, token_id=token_id, api_name=api_name, target_resource_type=target_resource_type, org_id=org_id)

View audit records

View audit records for any API

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.AuditsApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
user_id = '1234' # str | Query based on user id (optional)
dt_from = '' # str | Search criteria from when the query happened. * Inclusive. * In UTC. * Supports human-friendly values such as \"now\", \"today\", \"now-1day\".  (optional) (default to '')
dt_to = '' # str | Search criteria until when the query happened. * Exclusive. * In UTC. * Supports human-friendly values such as \"now\", \"today\", \"now-1day\".  (optional) (default to '')
action = '' # str | the type of action which caused the log (optional) (default to '')
target_id = '' # str | The identifier for the target of the log (e.g. the jti of a created token).  (optional) (default to '')
token_id = 'token_id_example' # str | The id of the bearer token for which to find records. (optional)
api_name = '' # str | The name of the API which generated the audit logs (optional) (default to '')
target_resource_type = '' # str | Filters the type of resource associated with the audit records. (optional) (default to '')
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # View audit records
        api_response = api_instance.list_audits(limit=limit, user_id=user_id, dt_from=dt_from, dt_to=dt_to, action=action, target_id=target_id, token_id=token_id, api_name=api_name, target_resource_type=target_resource_type, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AuditsApi->list_audits: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **user_id** | **str**| Query based on user id | [optional] 
 **dt_from** | **str**| Search criteria from when the query happened. * Inclusive. * In UTC. * Supports human-friendly values such as \&quot;now\&quot;, \&quot;today\&quot;, \&quot;now-1day\&quot;.  | [optional] [default to &#39;&#39;]
 **dt_to** | **str**| Search criteria until when the query happened. * Exclusive. * In UTC. * Supports human-friendly values such as \&quot;now\&quot;, \&quot;today\&quot;, \&quot;now-1day\&quot;.  | [optional] [default to &#39;&#39;]
 **action** | **str**| the type of action which caused the log | [optional] [default to &#39;&#39;]
 **target_id** | **str**| The identifier for the target of the log (e.g. the jti of a created token).  | [optional] [default to &#39;&#39;]
 **token_id** | **str**| The id of the bearer token for which to find records. | [optional] 
 **api_name** | **str**| The name of the API which generated the audit logs | [optional] [default to &#39;&#39;]
 **target_resource_type** | **str**| Filters the type of resource associated with the audit records. | [optional] [default to &#39;&#39;]
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**ListAuditsResponse**](ListAuditsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The query ran without error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

