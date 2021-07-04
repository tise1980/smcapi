# coding: utf-8
import requests
import json
import urllib.request, urllib.error
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET

@csrf_exempt
@api_view(['GET','POST'])
def get_dataextention_info(request):
    stack = request.GET.get('stack')
    query = request.GET.get('query')
    access_token = request.GET.get('access_token')
    subdomain = request.GET.get('subdomain')
    if stack != 'S11':
        url = 'https://webservice.'+ stack +'.exacttarget.com/Service.asmx'
    elif stack == 'S11':
        url = 'https://'+ subdomain +'.soap.marketingcloudapis.com/Service.asmx'
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <soapenv:Header>
                    <fueloauth>""" + access_token + """</fueloauth>
                </soapenv:Header>
                <soapenv:Body>
                    <RetrieveRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI">
                        <RetrieveRequest>
                            <ObjectType>DataExtension</ObjectType>
                                <Properties>Name</Properties>
                                    <Filter xsi:type="SimpleFilterPart">
                                        <Property>Name</Property>
                                        <SimpleOperator>like</SimpleOperator>
                                        <Value>"""+ query +"""</Value>
                                    </Filter>
                        </RetrieveRequest>
                    </RetrieveRequestMsg>
                </soapenv:Body>
            </soapenv:Envelope>"""
    headers = {
                'SOAPAction': 'Retrieve',
                'Content-Type': 'text/xml'
            }
    resp = requests.post(url, data=body, headers=headers)
    return Response(resp.content, status=resp.status_code)

@csrf_exempt
@api_view(['GET','POST'])
def get_queryactivity_info(request):
    stack = request.GET.get('stack')
    query = request.GET.get('query')
    access_token = request.GET.get('access_token')
    subdomain = request.GET.get('subdomain')
    if stack != 'S11':
        url = 'https://webservice.'+ stack +'.exacttarget.com/Service.asmx'
    elif stack == 'S11':
        url = 'https://'+ subdomain +'.soap.marketingcloudapis.com/Service.asmx'
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <soapenv:Header>
                    <fueloauth>""" + access_token + """</fueloauth>
                </soapenv:Header>
                <soapenv:Body>
                    <RetrieveRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI">
                        <RetrieveRequest>
                            <ObjectType>QueryDefinition</ObjectType>
                                <Properties>Name</Properties>
                                <Properties>Client.ID</Properties>
                                <Properties>CategoryID</Properties>
                                    <Filter xsi:type="SimpleFilterPart">
                                        <Property>QueryText</Property>
                                        <SimpleOperator>like</SimpleOperator>
                                        <Value>"""+ query +"""</Value>
                                    </Filter>
                        </RetrieveRequest>
                    </RetrieveRequestMsg>
                </soapenv:Body>
            </soapenv:Envelope>"""
    headers = {
                'SOAPAction': 'Retrieve',
                'Content-Type': 'text/xml'
            }
    resp = requests.post(url, data=body, headers=headers)
    """フォルダーの場所を抽出するスクリプト（実行に時間がかかるので今回は見送り）
    tree = ET.fromstring(resp.content)
    root = tree[1][0]
    for category_id in root.iter('{http://exacttarget.com/wsdl/partnerAPI}CategoryID'):
        p_resp = get_folderlocation_info(category_id.text,'queryactivity',stack,access_token,subdomain)
        p_tree = ET.fromstring(p_resp.content)
        p_root = p_tree[1][0]
        for p_category_id in p_root.iter('{http://exacttarget.com/wsdl/partnerAPI}Name'):
            print(p_category_id.text)
    """
    return Response(resp.content, status=resp.status_code)

def get_folderlocation_info(id,content_type,stack,access_token,subdomain=''):
    if stack != 'S11':
        url = 'https://webservice.'+ stack +'.exacttarget.com/Service.asmx'
    elif stack == 'S11':
        url = 'https://'+ subdomain +'.soap.marketingcloudapis.com/Service.asmx'
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <soapenv:Header>
                    <fueloauth>""" + access_token + """</fueloauth>
                </soapenv:Header>
                <soapenv:Body>
                    <RetrieveRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI">
                        <RetrieveRequest>
                            <ObjectType>DataFolder</ObjectType>
                            <Properties>Name</Properties>
                            <Properties>ParentFolder.ID</Properties>
                            <Filter xsi:type="ComplexFilterPart">
                                <LeftOperand xsi:type="SimpleFilterPart">
                                    <Property>ID</Property>
                                    <SimpleOperator>equals</SimpleOperator>
                                    <Value>""" + id + """</Value>
                                </LeftOperand>
                                <LogicalOperator>AND</LogicalOperator>
                                <RightOperand xsi:type="SimpleFilterPart">
                                    <Property>ContentType</Property>
                                    <SimpleOperator>equals</SimpleOperator>
                                    <Value>""" + content_type + """</Value>
                                </RightOperand>
                            </Filter>
                        </RetrieveRequest>
                    </RetrieveRequestMsg>
                </soapenv:Body>
            </soapenv:Envelope>"""
    headers = {
                'SOAPAction': 'Retrieve',
                'Content-Type': 'text/xml'
            }
    resp = requests.post(url, data=body, headers=headers)
    return resp