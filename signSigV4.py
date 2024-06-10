from botocore.auth import SigV4Auth
import requests
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials
import botocore.session
import sys

def make_request(endpoint_url, method):
    session = botocore.session.Session()
    sigv4 = SigV4Auth(session.get_credentials(), 'vpc-lattice-svcs', 'ap-northeast-2')
    endpoint = endpoint_url
    data = "some-data-here"
    headers = {'Content-Type': 'application/json'}
    if method.lower() == "post":
        request = AWSRequest(method='POST', url=endpoint, data=data, headers=headers)
        request.context["payload_signing_enabled"] = False # This is mandatory since VpcLattice does not support payload signing. Not providing this will result in error.
        sigv4.add_auth(request)

        prepped = request.prepare()
        response = requests.post(prepped.url, headers=prepped.headers, data=data)
    elif method.lower() == "get":
        request = AWSRequest(method='GET', url=endpoint, headers=headers)
        request.context["payload_signing_enabled"] = False # This is mandatory since VpcLattice does not support payload signing. Not providing this will result in error.
        sigv4.add_auth(request)

        prepped = request.prepare()
        response = requests.get(prepped.url, headers=prepped.headers)
    else:
        print ("Pls enter GET or POST for method and make sure the URL is accessible")
        return

    print (response.text)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Please provide endpoint URL and method (GET or POST) as arguments")
        sys.exit(1)

    endpoint_url = sys.argv[1]
    method = sys.argv[2]

    make_request(endpoint_url, method)
