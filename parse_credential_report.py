#!/usr/bin/env python

from sys import stdin

import json
import base64
import time
import datetime

report = json.loads(stdin.read())
table = base64.b64decode(report["Content"]).splitlines()
generated = report["GeneratedTime"].splitlines()
generated = generated[0].encode("ascii")
head = table[0].split(",")
table = table[1:]

currentdateraw = datetime.datetime.strptime(generated,"%Y-%m-%dT%H:%M:%SZ")
currentdate = currentdateraw.strftime("%Y-%m-%d %H:%M:%S")
currentd = time.mktime(datetime.datetime.strptime(currentdate, "%Y-%m-%d %H:%M:%S").timetuple())

print "Username,Created Date,Password Enabled,Password Age,Access Key 1 Active,Access Key 1 Age,Access 2 Active,Access Key 2 Age,Last Activity,MFA enabled, Report Generated",currentdateraw.strftime("%c"),"UTC"
for row in iter(table):
  user = dict(zip(head, row.split(",")))
  try:
    usercreatedate = datetime.datetime.strptime(user["user_creation_time"],"%Y-%m-%dT%H:%M:%S+00:00")
    usercreatedate = usercreatedate.strftime("%Y-%m-%d %H:%M:%S")
  except ValueError:
    usercreatedate = "None"
  try:
    pwdlastused = datetime.datetime.strptime(user["password_last_used"],"%Y-%m-%dT%H:%M:%S+00:00")
    pwdlastused = pwdlastused.strftime("%Y-%m-%d %H:%M:%S")
    pwdlastusedd = time.mktime(datetime.datetime.strptime(pwdlastused, "%Y-%m-%d %H:%M:%S").timetuple())
    pwd_activedays = int(round(((currentd - pwdlastusedd)/60/60/24)))
  except ValueError:
    pwd_activedays = "None"
  try:
    pwdlastchanged = datetime.datetime.strptime(user["password_last_changed"],"%Y-%m-%dT%H:%M:%S+00:00")
    pwdlastchanged = pwdlastchanged.strftime("%Y-%m-%d %H:%M:%S")
    pwdlastchangedd = time.mktime(datetime.datetime.strptime(pwdlastchanged, "%Y-%m-%d %H:%M:%S").timetuple())
    pwd_age = int(round(((currentd - pwdlastchangedd)/60/60/24)))
  except ValueError:
    pwd_age = "None"
  try: 
    acckey1lastused = datetime.datetime.strptime(user["access_key_1_last_used_date"],"%Y-%m-%dT%H:%M:%S+00:00")
    acckey1lastused = acckey1lastused.strftime("%Y-%m-%d %H:%M:%S")
    acckey1lastusedd = time.mktime(datetime.datetime.strptime(acckey1lastused, "%Y-%m-%d %H:%M:%S").timetuple())
    acckey1_activedays = int(round(((currentd - acckey1lastusedd)/60/60/24)))
  except ValueError:
    acckey1_activedays = "None"
  try:
    acckey1_lastrotated = datetime.datetime.strptime(user["access_key_1_last_rotated"],"%Y-%m-%dT%H:%M:%S+00:00")
    acckey1_lastrotated = acckey1_lastrotated.strftime("%Y-%m-%d %H:%M:%S")
    acckey1_lastrotatedd = time.mktime(datetime.datetime.strptime(acckey1_lastrotated, "%Y-%m-%d %H:%M:%S").timetuple())
    acckey1_age = int(round(((currentd - acckey1_lastrotatedd)/60/60/24)))
  except ValueError:
    acckey1_age = "None"
  try:
    acckey2lastused = datetime.datetime.strptime(user["access_key_2_last_used_date"],"%Y-%m-%dT%H:%M:%S+00:00")
    acckey2lastused = acckey2lastused.strftime("%Y-%m-%d %H:%M:%S")
    acckey2lastusedd = time.mktime(datetime.datetime.strptime(acckey2lastused, "%Y-%m-%d %H:%M:%S").timetuple())
    acckey2_activedays = int(round((currentd - acckey2lastusedd)/60/60/24))
  except ValueError:
    acckey2_activedays = "None"
  try:
    acckey2_lastrotated = datetime.datetime.strptime(user["access_key_2_last_rotated"],"%Y-%m-%dT%H:%M:%S+00:00")
    acckey2_lastrotated = acckey2_lastrotated.strftime("%Y-%m-%d %H:%M:%S")
    acckey2_lastrotatedd = time.mktime(datetime.datetime.strptime(acckey2_lastrotated, "%Y-%m-%d %H:%M:%S").timetuple())
    acckey2_age = int(round(((currentd - acckey2_lastrotatedd)/60/60/24)))
  except ValueError:
    acckey2_age = "None"
#
# Work out lowest access key
#
  if type(acckey1_activedays) is int and type(acckey2_activedays) is int:
    acckey_activedays = min(acckey1_activedays,acckey2_activedays)
  if type(acckey1_activedays) is int and type(acckey2_activedays) is str:
    acckey_activedays = acckey1_activedays
  if type(acckey1_activedays) is str and type(acckey2_activedays) is int:
    acckey_activedays = acckey2_activedays 
  if type(acckey1_activedays) is str and type(acckey2_activedays) is str:
    acckey_activedays = "None"
#
# Work out Last Activity
#
  if type(pwd_activedays) is int and type(acckey_activedays) is int:
    last_activity = min(pwd_activedays,acckey_activedays)
  if type(pwd_activedays) is int and type(acckey_activedays) is str:
    last_activity = pwd_activedays
  if type(pwd_activedays) is str and type(acckey_activedays) is int:
    last_activity = acckey_activedays
  if type(pwd_activedays) is str and type(acckey_activedays) is str:
    last_activity = "None"
#
# Formating
#
  if last_activity == 0 : last_activity = "Today"
  if last_activity == 1 : last_activity = "Yesterday"
  if type(last_activity) is int: last_activity = str(last_activity) + " days"
#
  if acckey1_age == 0 : acckey1_age = "Today"
  if acckey1_age == 1 : acckey1_age = "Yesterday"
  if type(acckey1_age) is int: acckey1_age = str(acckey1_age) + " days"
#
  if acckey2_age == 0 : acckey2_age = "Today"
  if acckey2_age == 1 : acckey2_age = "Yesterday"
  if type(acckey2_age) is int: acckey2_age = str(acckey2_age) + " days"
#
  if pwd_age == 0 : pwd_age = "Today"
  if pwd_age == 1 : pwd_age = "Yesterday"
  if type(pwd_age) is int: pwd_age = str(pwd_age) + " days"
# Output
  print "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (user["user"], usercreatedate, user["password_enabled"], pwd_age, user["access_key_1_active"], acckey1_age, user["access_key_2_active"], acckey2_age, last_activity, user["mfa_active"])
