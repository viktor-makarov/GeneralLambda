import json
import requests
import base64



def str_to_bool(s):
    if not s:
        return False
    # Пример для включения: если строка 'включено', 'true', 'yes' и т.п. — True, иначе False
    return s.lower() in ('true', 'yes', '1', 'включено')

def proxyIncomingRequests(event, context):
    # Extract the original request details
    method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']
    isBase64Encoded = event.get('isBase64Encoded', False)
    headers = event['headers']
    
    multiValueHeaders = event.get('multiValueHeaders', {})
    body = event.get('body', None)
    stageVariables = event.get('stageVariables', {})
    queryStringParameters = event.get('queryStringParameters', {})

    domain, loginput, logoutput, logrequest_args = stageVariables.get("domain"), str_to_bool(stageVariables.get("loginput")), str_to_bool(stageVariables.get("logoutput")), str_to_bool(stageVariables.get("logrequest_args"))

    if loginput:
        print("input event",event)

    # We do not need to decode body as we pass it AS IS to the backend, without any changes

    # Remove the 'Forwarded' header if it exists
    headers.pop('x-forwarded-for', None)
    #headers.pop('via', None)

    # Define your backend URL
    # Define your backend URL
    if queryStringParameters:
        query_params = '&'.join([f"{k}={v}" for k, v in queryStringParameters.items()])
        backend_url = f"{domain}{path}?{query_params}"
    else:
        backend_url = f"{domain}{path}"
    
    # Forward the request to the backend
    # Handle multiValueHeaders if they exist
    if multiValueHeaders:
        # Convert multiValueHeaders to requests library format
        # In requests, multiple values for the same header are passed as a list
        for header, values in multiValueHeaders.items():
            if values:  # Only set if there are values
                headers[header] = values if len(values) > 1 else values[0]
    
    # Forward the request to the backend
    # Create a dictionary of request arguments
    request_args = {
        'method': method,
        'url': backend_url,
        'headers': headers,
        'params': queryStringParameters
    }
    # Only include the body if it's not None
    if body is not None:
        request_args['data'] = body
    
    if logrequest_args:
        print("request args",request_args)
    # Send the request with unpacked arguments
    response = requests.request(**request_args)

    # Return the backend's response

    output = {
        'isBase64Encoded': isBase64Encoded,
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.content
    }

    if logoutput:
        print("output result",output)

    return output

def main(event, context=None):
    result = proxyIncomingRequests(event,context)

    return result

event = {
  "httpMethod": "GET",
  "path": "/headers",
  "headers": {
    "host": "postman-echo.com",
    "x-request-start": "t1745310826.092",
    "connection": "close",
    "x-forwarded-proto": "https",
    "x-forwarded-port": "443",
    "x-amzn-trace-id": "Root=1-6807546a-007d833c4fb168445aa66cab",
    "cache-control": "max-age=0",
    "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "priority": "u=0, i",
    "cookie": "sails.sid=s%3Ar7MNW37HbXNPbudXxkMXE258WABpO6lz.yyPqyh2GFNmipMfo3AyBlzfpAkZNRJLexRK%2FxIbrQMw"
  },
  "multiValueHeaders": {
    "accept": ["text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"],
    "accept-language": ["ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"]
  },
  "queryStringParameters": {},
  "pathParameters": {},
  "stageVariables": {},
  "requestContext": {},
  "isBase64Encoded": False
}

if __name__ == "__main__":
    result = main(event)
    print("result",result)