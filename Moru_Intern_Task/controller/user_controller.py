from app import app
from model.user_model import user_model
from model.auth_model import auth_model
from flask import request,send_file,Flask, session, jsonify, request
from datetime import datetime
obj=user_model()
auth=auth_model()
 
#login authentication and authorization using jwt token with CRUD Operation
@app.route("/user/getall")
@auth.token_auth("/user/getall")
def user_getall_controller():
    return obj.user_getall_model()

@app.route("/user/addone",methods=["POST"])
@auth.token_auth("/user/addone")
def user_addone_controller():
    return obj.user_addone_model(request.form)

@app.route("/user/update",methods=["PUT"])
@auth.token_auth("/user/update")
def user_update_controller():
    return obj.user_update_model(request.form)

@app.route("/user/delete/<id>",methods=["DELETE"])

def user_delete_controller(id):
    return obj.user_delete_model(id)

@app.route("/user/patch/<id>",methods=["PATCH"])
def user_patch_controller(id):
    return obj.user_patch_model(request.form,id)

#user pagination
@app.route("/user/getall/limit/<limit>/page/<page>",methods=["GET"])
def user_pagination_controller(limit,page):
    return obj.user_pagination_model(limit,page)

@app.route("/user/<uid>/avatar/upload", methods=["PATCH"])
def upload_avatar(uid):
    file = request.files['avatar']
    # file.save(f"uploads/{file.filename}")
    uniqueFileName= str(datetime.now().timestamp()).replace(".","")
    fileNameSplit=file.filename.split(".")
    extension=fileNameSplit[len(fileNameSplit)-1]
    finalFilePath=f"uploads/{uniqueFileName}.{extension}"
    file.save(finalFilePath)
    
    return obj.upload_avatar_model(uid,finalFilePath)

@app.route("/uploads/<filename>")
def user_getavatar_controller(filename):
    return send_file(f"uploads/{filename}")

@app.route("/user/login",methods=["POST"])
def user_login_controller():
    return obj.user_login_model(request.form)


#blog page
@app.route("/blog/getall")
@auth.token_auth("/blog/getall")
def blog_getall_controller():
    return obj.blog_getall_model()

@app.route("/blog/addone",methods=["POST"])
@auth.token_auth("/blog/addone")
def blog_addone_controller():
    return obj.blog_addone_model(request.form)

@app.route("/blog/update",methods=["PUT"])
@auth.token_auth("/blog/update")
def blog_update_controller():
    return obj.blog_update_model(request.form)

@app.route("/blog/delete/<id>",methods=["DELETE"])
def blog_delete_controller(id):
    return obj.blog_delete_model(id)


#blog pagination
@app.route("/blog/getall/limit/<limit>/page/<page>",methods=["GET"])
def blog_pagination_controller(limit,page):
    return obj.blog_pagination_model(limit,page)

#user logout
@app.route('/user/logout', methods=['POST'])
def user_logout():
    # clear the session data
    session.clear()
    return obj.user_logout_model()






