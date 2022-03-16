import asyncio
import aiohttp
import json
from config import TEST_FILE, DOMAINS, logger
from .sender import send_report, send_to_bot


async def url_param_to_list(param: str):
    start = param.find('{{')
    end = param.find('}}')
    if start != -1 and end != -1:
        params = param[start+2: end].split('||')
        urls = [
            f'{param[:start]}{_param}{param[end+2:]}'
            for _param in params
        ]
    else:
        urls = [param]
    return [u.format(**DOMAINS) for u in urls]


async def __str_to_coded_type(s: str):
    t, value = s.split('_')
    if t == 'str':
        return value
    elif t == 'int':
        return int(value)
    elif t == 'bool':
        return value.lower() == 'true'
    return value


async def __check_result(data, query_list):
    try:
        q_len = len(query_list)
        if q_len == 0:
            return True
        else:
            if q_len == 1:
                query, result = query_list[0].split('=')
                result = await __str_to_coded_type(result)
                return data[query] == result
            else:
                field: str = query_list[0]
                if field.isdigit():
                    return await __check_result(data[int(field)], query_list[1:])
                else:
                    return await __check_result(data[field], query_list[1:])
    except:
        return False


async def check_result(data, queries):
    if len(queries) == 0 or queries is None:
        return True
    return all([await __check_result(data, q.split('.')) for q in queries])


async def __request_status(
        title: str,
        tag: str,
        _url: str,
        session_params,
        request_params,
        json_query=None,
        method: str = 'get',
        result_status: int = None,
):
    try:
        async with aiohttp.ClientSession(
                **session_params
        ) as session:
            async with session.__getattribute__(method)(_url, **request_params) as response:
                response: aiohttp.ClientResponse
                if result_status is not None:
                    if result_status != response.status:
                        return False, lambda: send_report(
                            title=title, url=_url, tag=tag, is_error=True,
                            message=f'Неверный статус ответа: {response.status}\n'
                                    f'Ожидался: {result_status}'
                        )
                if not response.ok:
                    return False, lambda: send_report(
                        title=title, url=_url, tag=tag, is_error=True,
                        message=f'Ошибка запроса: {response.status}\n'
                    )
                else:
                    if json_query is not None:
                        data: dict = await response.json()
                        if isinstance(data, dict) and 'error' in data.keys():
                            return False, lambda: send_report(
                                title=title, url=_url, tag=tag,
                                message=f'ПАДЕНИЕ. Ответ содержит поле "error"', is_error=True
                            )
                        elif not await check_result(data, json_query):
                            return False, lambda: send_report(
                                title=title, url=_url, tag=tag,
                                message=f'ПАДЕНИЕ. Сравнение с образцом', is_error=True
                            )
                    return True, lambda: send_report(
                        title=title, url=_url, tag=tag,
                        message=f'Неполадки устранены. Продолжение работы в прежнем режиме', is_error=False
                    )
    except Exception as error:
        logger.error(f'ERROR {title}: {error}\n{_url}')
        return False, lambda: send_report(
            title=title, url=_url, message=f'Ошибка на стороне бота', tag=tag, is_error=True
        )


async def check_endpoint(
        title: str,
        tag: str,
        url: str,
        data_for_check=None,
        json_query=None,
        method: str = 'get',
        delay_success: int = 5,
        delay_error: int = 5,
        auth: str = None,
        headers: dict = None,
        result_status: int = None
):
    session_params = {
        'headers': {'Authorization': auth}
    } if auth is not None else {}
    if headers is not None:
        if 'headers' in session_params:
            session_params['headers'].update(headers)
        else:
            session_params = {'headers': headers}
    request_params = {'json': data_for_check} if data_for_check is not None else {}
    urls = await url_param_to_list(url)
    is_work = True
    while True:
        result = [
            await __request_status(
                title=title,
                tag=tag,
                _url=_url,
                session_params=session_params,
                request_params=request_params,
                json_query=json_query,
                method=method,
                result_status=result_status
            )
            for _url in urls
        ]
        current_work = all(list(map(lambda x: x[0], result)))
        if is_work != current_work:
            item = list(filter(lambda x: x[0] == current_work, result))[0]
            await item[-1]()
            is_work = current_work
        await asyncio.sleep(delay_success if is_work else delay_error)


async def check_all():
    with open(TEST_FILE, 'r') as file:
        tests = json.loads(file.read())
    await send_to_bot('Бот для проверки системы запущен')
    await asyncio.gather(*[
        check_endpoint(**test)
        for test in tests
    ])
