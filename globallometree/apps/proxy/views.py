import requests
import json

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required

from globallometree.apps.data_sharing.data_tools import restrict_access

def parse_request_path(path):
    """

        Returns a list of properties that define the request

        call / string /
            a string representing the type of call being made to elasticsearch
        cluster / boolean /
            does this request apply to the cluster resources?
        indices / list /
            a simple list of indices that are included in the request
    
    """

    parsed = {}

    # Figure out what the call is to elasticsearch
    # Cut the first slash "/" off the path and split the rest on forward slash
    path_parts = path[1:].split('/')

    # we are looking for calls which are not meta_calls.
    # if we find an underscored word, not in the meta_calls list,
    # it becomes the returned call.
    meta_calls = ['_all', '_primary', '_local']
    for part in path_parts:
        if part.startswith('_') and part not in meta_calls:
            parsed['call'] = part
            break

    # If a call (such as _search or _update) was not found,
    # we add the two calls _home, and _document
    # that don't exist in the real elasticsearch path.
    # assuming home if the path is empty or one char
    # and _document if the path is longer
    if 'call' not in parsed.keys():
        if request.path == '/':
            parsed['call'] = '_home'
        else:
            parsed['call'] = '_document'

    #Is this a cluster call, or a call to indices?
    if (
        path == '/' or
        path_parts[0].startswith('_') and
        path_parts[0] != '_all'
    ):
        #This is a call to the root or "cluster" so we set cluster to be true
        parsed['cluster'] = True
        parsed['indices'] = []
    else:
        #This is a call to an index or multiple indices - so we get those
        parsed['cluster'] = False
        parsed['indices'] = path_parts[0].split(',')
   
    return parsed


@csrf_exempt
@login_required(login_url='/accounts/login/')
def es_proxy(request):
    user = request.user
    es_path = request.path.replace('/elastic', '')
    resource_requested = parse_request_path(es_path)

    # Allow access to the cluster _mapping and _nodes for kibana
    if resource_requested['cluster'] == True:
        if resource_requested['call'] not in ['_mapping', '_nodes']:
            raise PermissionDenied()
        request_method = requests.get
    # Allow access to _search by POST only
    else:
        if request.method not in ['POST', 'GET'] or resource_requested['call'] != '_search':
            raise PermissionDenied()
        request_method = requests.post
    
    r = request_method('http://localhost:9200%s' % es_path, data=request.body)

    if resource_requested['cluster']:
        content = r.content
    else:
        es_response = json.loads(r.content)
        if 'hits' in es_response.keys():
            for index, record in enumerate(es_response['hits']['hits']):
                es_type = record['_type']
                es_response['hits']['hits'][index]['_source'] = restrict_access(record['_source'], es_type, user)
        content = json.dumps(es_response)

    return HttpResponse(content, content_type="application/json")
    


