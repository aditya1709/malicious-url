import logging
from aiohttp import web
import json
import urlcheck

def parseMonitorFilterPayload(payloadstr):
    """
    The payload from the envoyfilter isn't quite json.  Fix it and marshall
    :param payloadstr: raw payload string of the message from the monitor envoyfilter
    :return:
       dictionary of json marshalled data
    :raises:
       json.JSONDecodeError
    """
    #print(payloadstr)
    payloadstr = payloadstr.replace('\\"', '"')
    #print(payloadstr)
    payloadstr = payloadstr.replace('\"', '"')
    #print(payloadstr)
    payloadstr = payloadstr.replace('"{', '{')
    payloadstr = payloadstr.replace('}"', '}')
    payloadstr = payloadstr.replace('\\n', ' ')
    #print(payloadstr)
    try:
        payloadData = json.loads(payloadstr)
    except json.JSONDecodeError as e:
        print(f"Failed decoding json: {e}")
        raise e
    return payloadData


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def handlePostRequest(request):
    print(f"received request, headers: {request.raw_headers}")
    if request.body_exists:
        post_data = (await request.read()).decode()
        print(f"body: {post_data}\n")
        try:
            data = parseMonitorFilterPayload(post_data)
        except json.JSONDecodeError as e:
            print(f"failed decoding request")
            return web.Response(status=404)

        prompt = urlcheck.getPromptFromPayload(request.headers.get("x-monitor-authority"), data)
        print(f'prompt: {request.headers.get("x-monitor-authority")}')
        if prompt != "":
            print(f"Found prompt: {prompt}")
            if urlcheck.isMaliciousUrlPresent(prompt):
                print(f"Malicious URL detected\n")
                return web.Response(status=400, text="Prompt is malicious")
        else:
            print(f"Unable to determine prompt")
            return web.Response(status=403, text="Unable to determine prompt")
    return web.Response(text="processed prompt, ok")

async def handlePostResponse(request):
    print(f"received response, headers: {request.raw_headers}")
    if request.body_exists:
        post_data = (await request.read()).decode()
        print(f"body: {post_data}\n")
    return web.Response(text="processed response, ok")

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle),
                web.post('/request', handlePostRequest),
                web.post('/response', handlePostResponse)])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, port=8000)