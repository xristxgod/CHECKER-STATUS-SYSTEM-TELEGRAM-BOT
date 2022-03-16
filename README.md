#How it works?


There is a file `stage_endpoints.json`.

Here you can write params for our services' health checking.

### Example:

``` json
[
... ,
{
    "url": "{domain_bank}/api/health/check/{{btc||bnb||tron}}/timeUpdate",
    "title": "Обновление курсов валют",
    "tag": "crypto",
    "method": "get",
    "json_query": [
      "checkResponse.LastTimeEntryExchangeCheck=bool_true"
    ],
    "delay": 5,
    "data_for_check": null,
    "auth": "Bearer adminGYzYjE1ZDhmZmU0YzIwMWZjOTRkN2NkYjMzZmI0MDQ4NDY0NjgwZWQwZDdkODQ1MzljMGNlYWY4ZWE0ZA"
  },

...

]
```

### Available parameters:

> `title` - This title will be displayed in telegram's message in bot.
> 
> `tag` - hashtag # for quick search in chat's history.
> 
> `method` - http method for getting information.
> 
> `data_for_check` - if method == `POST`, then here we can write JSON object for POST request.
> 
> `json_query` - instructions for checking api endpoint status.
>> "json_query": `["0.checkResponse.LastTimeEntryExchangeCheck=bool_true"]`.
>>
>> Here check next information from JSON:
>> 
>> ``` json [{"checkResponse": {"LastTimeEntryExchangeCheck": true}, ...}, ...] ```
>> 
>> If JSON has this structure - then our check function will return `True`.
> 
> `delay` - How often we run this checking in seconds.
> 
> `auth` - JWT Bearer authentication token.
> 
> `url` - api endpoint for checking. There is a lot of special parameters
>> Example: `{domain_bank}/api/health/check/{{btc||bnb||tron}}/timeUpdate`
>>
>> `{domain_bank}` - it's variable from virtual environment. It must be startswith `domain_` 
>> and used in `{...}`.
>>
>> `{{btc||bnb||tron}}` - when we use this construction, in checking this endpoint will be checking 
>> like 3 endpoint:
>> `{domain_bank}/api/health/check/btc/timeUpdate`
>>
>> `{domain_bank}/api/health/check/bnb/timeUpdate`
>>
>> `{domain_bank}/api/health/check/tron/timeUpdate`