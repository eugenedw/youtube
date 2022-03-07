# -*- coding: utf-8 -*-
"""deeptranslate.py DeepL and Python
@Author: Eugene Williams
@Date: Sunday, March 6, 2022 21:09
@Links: https://deepstitch.io

This module provides an example approach to process language translation
requests and retrieval from DeepL

Example:
    Here are some examples of how the command could be run::

        $ python deepltranslate.py translate mysource_en.txt
        $ python deepltranslate.py status 483094A483B84309403940934 9483040934C83094A0039E
        $ python deepltranslate.py download 483094A483B84309403940934 9483040934C83094A0039E

Todo:
    * Parameterize to capture the source and destination language

"""
import requests
import os
import sys
import json

AUTH_KEY = os.environ["DEEPL_API_KEY"]

translate_url = "https://api-free.deepl.com/v2/document"
translate_status_url = "https://api-free.deepl.com/v2/document/{0}"
translate_download_url = "https://api-free.deepl.com/v2/document/{0}/result"

def translatedoc(path):
    """
    translates a document and prints out the subsequent 
    commands to get status and download

    :param path: the path of the file to be translated
    :return: nothing
    """ 
    up_file = open(path,"rb")
    _params = {
        "source_lang" : "EN",
        "auth_key" : AUTH_KEY,
        "target_lang" : "ZH"
    }
    response = requests.post(translate_url,params=_params,files={"file":up_file})
    print(response.text)
    jdata = json.loads(response.text)
    print("")
    print("*****************************************************")
    print("[status] => python3 deepltranslate.py status {0} {1}".format(jdata["document_id"],jdata["document_key"]))
    print("[download] => python3 deepltranslate.py download {0} {1}".format(jdata["document_id"],jdata["document_key"]))
    print("*****************************************************")
    print("")

def docstatus(docid,dockey):
    """
    collects the status of a document which has been 
    submitted for translation

    :param docid: the document id returned from the translate request
    :param dockey: the encryption key for the document
    :return: nothing
    """ 
    _params = {
        "auth_key" : AUTH_KEY,
        "document_key" : dockey
    }
    response = requests.get(translate_status_url.format(docid),params=_params)
    print(response.text)

def downloadtranslation(docid,dockey):
    """
    downloads the document using the referenced id if it is 
    ready for download 

    :param docid: the document id returned from the translate request
    :param dockey: the encryption key for the document
    :return: nothing
    """ 
    _params = {
        "auth_key" : AUTH_KEY,
        "document_key" : dockey
    }
    response = requests.get(translate_download_url.format(docid),params=_params,allow_redirects=True)
    open("{0}.txt".format(docid),"wb").write(response.content)

# the program should be run with the following structure
# python deepltranslate.py [action] [param 1] [param 2]
action = sys.argv[1]
if action == "translate":
    translatedoc(sys.argv[2])
elif action == "status":
    docstatus(sys.argv[2],sys.argv[3])
elif action == "download":
    downloadtranslation(sys.argv[2],sys.argv[3])