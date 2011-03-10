#coding: utf-8
"""
author: hyliker@gmail.com
"""
import pprint
import os, tempfile, zipfile
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import settings

class dotdict(dict):
    """
    @author: hyliker@gmail.com
    @reference:
        http://parand.com/say/index.php/2008/10/24/python-dot-notation-dictionary-access/
        http://code.activestate.com/recipes/576586/
    >>> dd = dotdict()
    >>> dd.a
    >>> dd.a = 'one'
    >>> dd.a
    'one'
    >>> dd.keys()
    ['a']

    >>> existing = {'a':'A', 'b':'B'}
    >>> dot_existing = dotdict(existing)
    >>> dot_existing.a
    'A'
    """
    def __init__(self, d=None, **kwargs):
        if d is None:
            d = {}
        d.update(kwargs)
        for k in d:
            if isinstance(d[k], dict):
                self[k] = dotdict(d[k])
            elif isinstance(d[k], (list, tuple)):
                l = []
                for v in d[k]:
                    if isinstance(v, dict):
                        l.append(dotdict(v))
                    else:
                        l.append(v)
                self[k] = l
            else:
                self[k] = d[k]

    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

def JsonResponse(result, is_json = False):
    """返回json結果给前台"""

    from django.http import HttpResponse
    import json

    if result and is_json:
        result = {"success": True, "data": result }
    elif result and not is_json:
        result = {"success": True }
    else:
        result = {"success": False }
    return HttpResponse(json.dumps(result))

def menu(filepath, mnode):
    import yaml
    #yaml_file = file('course/config.yml', 'r')
    yaml_file = file(filepath, 'r')
    config = yaml.load(yaml_file)
    menu = config["menu"]
    for k, v in enumerate(menu):
        if mnode in v.values():
            menu[k].update({"current":True})
    menu = [dotdict(m) for m in menu] 
    return menu

def send_file(request, fileobj, filename=None):
    """
    reference: http://www.djangosnippets.org/snippets/365/
    sumaary: Send a file through Django without loading the whole file into
             memory at once. The FileWrapper will turn the file object into an
             iterator for chunks of 8KB.
             支持中文附件名
    author: hyliker@gmail.com
    """
    wrapper = FileWrapper(fileobj)
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    if filename:
        content_disp =u'attachment; filename="%s"' % filename
        response['Content-Disposition'] = content_disp.encode('utf-8')
    return response

def send_zipfile(request):
    """
    http://www.djangosnippets.org/snippets/365/
    Create a ZIP file on disk and transmit it in chunks of 8KB,
    without loading the whole file into memory. A similar approach can
    be used for large dynamic PDF files.
    """
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    for index in range(10):
        filename = __file__ # Select your files here.                           
        archive.write(filename, 'file%d.txt' % index)
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response

def debug(info):
    """测试专用函数， 用来代替print"""

    if settings.DEBUG:
        print "\ndebug: %s \n"  % info
