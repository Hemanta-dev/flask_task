import mysql.connector
import json
import jwt
import re
from flask import make_response,request
from datetime import datetime,timedelta
from functools import wraps
class auth_model():
    def __init__(self):
        try:
            self.conn=mysql.connector.connect(host="localhost",user="root",password="root",database="flask_task")
            self.conn.autocommit=True
            self.cur=self.conn.cursor(dictionary=True)
            print("connection successfuly done")
        except:
            print("some error")
            
    def token_auth(self,endpoint):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                authorization=request.headers.get("authorization")   
                if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                    token = authorization.split(" ")[1] 
                    try:
                       jwtdecoded=jwt.decode(token, "Emcee",algorithms="HS256")  
                    except jwt.ExpiredSignatureError:
                        return make_response({"ERROR":"Token Expired"},401)
                         
                    role_id=jwtdecoded['payload']['role_id']
                    self.cur.execute(f"SELECT roles FROM new_view WHERE endpoint='{endpoint}'")
                    result=self.cur.fetchall()
                  
                    if len(result)>0:
                        allowedroles=json.loads(result[0]['roles'])
                        print(allowedroles)
                        if role_id in  allowedroles:
                            return func(*args)
                        else:
                            return make_response({"ERROR":"INVALID ROLE"},404)
                    else:
                        return make_response({'ERROR':"UNKNOWN ENDPOINT"},404)    
                    
                else:
                    return make_response({"ERROR":"Invalid_token"},401)     
              
                
            return inner2
        return inner1       