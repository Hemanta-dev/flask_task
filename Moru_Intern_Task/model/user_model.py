import mysql.connector
import json
import jwt
from flask import make_response
from datetime import datetime,timedelta
class user_model():
    def __init__(self):
        try:
            self.conn=mysql.connector.connect(host="localhost",user="root",password="root",database="flask_task")
            self.conn.autocommit=True
            self.cur=self.conn.cursor(dictionary=True)
            print("connection successfuly done")
        except:
            print("some error")
    def user_getall_model(self):
        self.cur.execute("SELECT * FROM users")
        result=self.cur.fetchall()
  
        if len(result)>0:
            return make_response({"payload":result},200)
        else:
            return make_response({"message":"No Data Found"},204)
        
    def user_addone_model(self,data):
        self.cur.execute(f"INSERT INTO users(name,email,phone,role,password) VALUES('{data['name']}','{data['email']}','{data['phone']}','{data['role']}','{data['password']}')")
        print(data)
        return make_response({"message":"User Created Successfully"},201)
    
    def user_update_model(self,data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}',role='{data['role']}',password='{data['password']}' WHERE id={data['id']}")
        if self.cur.rowcount>0:
            return make_response({"message":"User Updated Successfully"},201)
        else:
            return make_response({"message":"No Data Updated"},202)
        
    def user_delete_model(self,id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"User Deleted Successfully"},200)
        else:
            return make_response({"message":"Deleted not"},202)
    
    def user_patch_model(self,data,id):
        qry="UPDATE users SET "
        for key in data:
            qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id={id}"
        self.cur.execute(qry)
        if self.cur.rowcount>0:
            return make_response({"message":"User Updated Successfully"},201)
        else:
            return make_response({"message":"No Data Updated"},202)    

#pagination process of user model      
    def user_pagination_model(self,limit,page):
        limit=int(limit)
        page=int(page)
        start=(page*limit)-limit
        qry=f"SELECT * FROM users LIMIT {start},{limit}"
        self.cur.execute(qry)
        result=self.cur.fetchall()
        print(result)
        if len(result)>0:
            return make_response({"payload":result,"page_number":page,"limit_value":limit},200)
        else:
            return make_response({"message":"No Data Found"},204)
        
    def upload_avatar_model(self, uid, finalFilePath):
        self.cur.execute(f"UPDATE users SET avatar='{finalFilePath}' WHERE id={uid}")
        if self.cur.rowcount>0:
            return make_response({"message":"FILE_UPLOADED_SUCCESSFULLY", "path":finalFilePath},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)    
    
    def user_login_model(self,data):
        self.cur.execute(f"SELECT id, role_id, avatar, email, name, phone from users WHERE email='{data['email']}' and password='{data['password']}'")
        result = self.cur.fetchall()
        userdata=result[0]
        exp_time=datetime.now()+timedelta(minutes=15)
        exp_epoch_time=int(exp_time.timestamp())
        payload={
            "payload":userdata,
            "exp":exp_epoch_time
        }
        token=jwt.encode(payload,"Emcee",algorithm="HS256")
        print(result)
        return make_response({"token":token},200)   
        
#blog page 
    def blog_getall_model(self):
        self.cur.execute("SELECT * FROM blogs")
        result=self.cur.fetchall()

        if len(result)>0:
          return make_response({"payload":result},200)
        else:
          return make_response({"message":"No Data Found"},204)
      
          
    def blog_addone_model(self,data):
        self.cur.execute(f"INSERT INTO blogs(title,description,date) VALUES('{data['title']}','{data['description']}','{data['date']}')")
        return make_response({"message":"blog Created Successfully"},201)  
    
    def blog_update_model(self,data):
        result=self.cur.execute(f"UPDATE blogs SET title='{data['title']}', description='{data['description']}', date='{data['date']}' WHERE id={data['id']}")
        print(result)
        if self.cur.rowcount>0:
            return make_response({"message":"User Updated Successfully"},201)
        else:
            return make_response({"message":"No Data Updated"},202)  
        
    def blog_delete_model(self,id):
        self.cur.execute(f"DELETE FROM blogs WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"Blog Deleted Successfully"},200)
        else:
            return make_response({"message":"Deleted not"},202) 
        
#pagination process of blog  model      
    def blog_pagination_model(self,limit,page):
        limit=int(limit)
        page=int(page)
        start=(page*limit)-limit
        qry=f"SELECT * FROM blogs LIMIT {start},{limit}"
        self.cur.execute(qry)
        result=self.cur.fetchall()
        print(result)
        if len(result)>0:
            return make_response({"payload":result,"page_number":page,"limit_value":limit},200)
        else:
            return make_response({"message":"No Data Found"},204)
        
#logout user model
    def user_logout_model():
        return make_response({"message":"Successfully user logout"},200)   
                     