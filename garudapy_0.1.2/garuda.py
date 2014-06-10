# -*- coding:utf-8 -*-

"""
Garuda API

Version 0.1.* is compatible with Garuda protocol version 0.1
"""

HOST = 'localhost'
PORT = 9000

__author__ = 'Garuda Alliance'
__version__ = '0.1.2'
__date__ = '22 Feb 2013'

import ConfigParser
import socket
import json

__ini = ConfigParser.SafeConfigParser()
__ini.read('./garuda.ini')
GADGETUUID    = __ini.get('main','gadgetUUID')
GADGETNAME    = __ini.get('main','gadgetName')
CATEGORYLIST  = __ini.get('main','categories')
DESCRIPTION   = __ini.get('main','description')
ICONPATH      = __ini.get('main','iconPath')
LAUNCHCOMMAND = __ini.get('main','launchCommand')
PROVIDER      = __ini.get('main','providerName')
SCREENSHOTS   = __ini.get('main','screenshots')
INPUTFILEFORMATS  = __ini.get('main','inFFs')
OUTPUTFILEFORMATS = __ini.get('main','outFFs')

def connect():
  """
  Create Socket Connection
  Return: socket
  """
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((HOST, PORT))
  return sock

def register(sock):
  """
  Send RegisterGadgetRequest & Receive RegisterGadgetRequest
  Return: dictionary('json','result')
  """
  # SEND RegisterGadgetRequest
  sock.sendall(__register1())
  # RECEIVE RegisterGadgetRequest
  v_json = json.loads(sock.recv(1024))
  v_result = v_json.get('body').get('result')
  # RETURN
  ret = {
    'json':v_json,
    'result':v_result
  }
  return ret 

def __register1():
  json_register = {
    'header':{ 'id':'RegisterGadgetRequest', 'version':'0.1' },
    'body':{
      'name':GADGETNAME,
      'gadgetUUID':GADGETUUID,
      'categoryList':CATEGORYLIST.split(','),
      'description':DESCRIPTION,
      'iconPath':ICONPATH,
      'launchCommand':LAUNCHCOMMAND,
      'inputFileFormats':__formats(INPUTFILEFORMATS),
      'outputFileFormats':__formats(OUTPUTFILEFORMATS),
      'provider':PROVIDER,
      'screenshots':SCREENSHOTS.split(','),
    },
  }
  return json.dumps(json_register) + '\n'

def __formats(str_formats):
  formats = []
  for str_format in str_formats.split(','):
    item = str_format.split(':')
    format = { 'fileExtension':item[0], 'fileFormat':item[1] }
    formats.append(format)
  return formats

def activate(sock):
  """
  Send ActivateGadgetRequest & Receive ActivateGadgetResponse
  Return: dictionary('json','result')
  """
  # SEND ActivateGadgetRequest
  sock.sendall(__activate1())
  # RECEIVE ActivateGadgetResponse
  v_json = json.loads(sock.recv(1024))
  v_result = v_json.get('body').get('result')
  # RETURN
  ret = {
    'json':v_json,
    'result':v_result
  }
  return ret

def __activate1():
  json_activate = {
    'header':{'id':'ActivateGadgetRequest','version':'0.1'},
    'body':{
      'gadgetName':GADGETNAME,
      'gadgetUUID':GADGETUUID
    }
  }
  return json.dumps(json_activate) + '\n'

def load(sock):
  """
  Receive LoadDataRequest & Send LoadDataResponse
  Return: dictionary('json','path')
  """
  # RECEIVE LoadDataRequest
  v_json = json.loads(sock.recv(1024))
  v_path = v_json.get('body').get('data')
  v_originGadgetName = v_json.get('body').get('originGadgetName')
  v_originGadgetUUID = v_json.get('body').get('originGadgetUUID')
  v_id = v_json.get('header').get('id')
  v_version = v_json.get('header').get('version')
  # SEND LoadDataResponse
  sock.sendall(__load1(v_originGadgetName, v_originGadgetUUID))
  # RETURN
  ret = {
    'json':v_json,
    'path':v_path
  }
  return ret

def __load1(originGadgetName, originGadgetUUID):
  json_load = {
    'body':{
      'gadgetName':GADGETNAME,
      'gadgetUUID':GADGETUUID,
      'result':'Success',
      'targetGadgetName':originGadgetName,
      'targetGadgetUUID':originGadgetUUID
    },
    'header':{'id':'LoadDataResponse','version':'0.1'}
  }
  return json.dumps(json_load) + '\n'

def getlist(sock, fileExtension, fileType):
  """
  Send GetCompatibleGadgetListRequest & Receive GetCompatibleGadgetListResponse
  Return: dictionary('json','result','gadgets')
  """
  # SEND GetCompatibleGadgetListRequest
  sock.sendall(__getlist1(fileExtension, fileType))
  # RECEIVE GetCompatibleGadgetListResponse
  v_json = json.loads(sock.recv(1024))
  v_id = v_json.get('header').get('id')
  v_version = v_json.get('header').get('version')
  v_result = v_json.get('body').get('result')
  v_gadgets = v_json.get('body').get('gadgets')
  # RETURN
  ret = {
    'json':v_json,
    'result':v_result,
    'gadgets':v_gadgets
  }
  return ret 

def __getlist1(fileExtension, fileType):
  json_getlist = {
    "body":{
      "fileExtension":fileExtension,
      "fileType":fileType,
      "gadgetName":GADGETNAME,
      "gadgetUUID":GADGETUUID
    },
    "header": { "id":"GetCompatibleGadgetListRequest", "version":"0.1" }
  }
  return json.dumps(json_getlist) + '\n'

def send(sock, data, targetGadgetName, targetGadgetUUID):
  """
  Send SentDataToGadgetRequest & Receive SentDataToGadgetResponse
  Return: dictionary('json','result')
  """
  # SEND SentDataToGadgetRequest
  sock.sendall(__send1(data, targetGadgetName, targetGadgetUUID))
  # RECEIVE SentDataToGadgetResponse
  v_json = json.loads(sock.recv(1024))
  v_id = v_json.get('header').get('id')
  v_version = v_json.get('header').get('version')
  v_result = v_json.get('body').get('result')
  # RETURN
  ret = {
    'json':v_json,
    'result':v_result,
  }
  return ret

def __send1(data, targetGadgetName, targetGadgetUUID):
  json_send = {
    'header': { 'id': 'SentDataToGadgetRequest', 'version': '0.1' },
    'body':{
      'data':data,
      'gadgetName':GADGETNAME,
      'gadgetUUID':GADGETUUID,
      'targetGadgetName':targetGadgetName,
      'targetGadgetUUID':targetGadgetUUID
    }
  }
  return json.dumps(json_send) + '\n'
