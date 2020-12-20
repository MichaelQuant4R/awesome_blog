from flask import (Blueprint, jsonify, request, flash, current_app, session)
from models import (db, csrf, User, Blog, Comment, Reply, AdminRole, Notification)
from filters import read_datetime
from flask_login import (current_user, login_required)

app_comm = Blueprint("comment_section", __name__)

COMMENT_LIST_ID = []
REPLY_LIST_ID = []

BLOG_LIST_ID = []

NOTIFY_BLOG_LIST_ID = []



# @app_comm.route("/comment_data", methods = ["GET", "POST"])
# def comment_data():
    

    
#     blog_id = session["blog_id"][-1]
    

    
#     blog = Blog.query.filter_by(id = blog_id).first()
    
#     if blog is None:
        
        
#         return "no comments!"
    
    
#     comments = blog.comments.all()
    
#     comment_list = []
#     for comm in comments[::-1]:
#         user = User.query.filter_by(id = comm.user_id).first()

#         replies = comm.replies.all()

#         if replies != []:

#             reply_list = []

#             for rep in replies:

#                 reply_list.append({"reply": rep.reply,
#                                 "id": rep.id,
#                                  "comment_id": comm.id,
#                                  "blog_id": comm.blog_id,
#                                 "user_id": rep.user.id,
#                                    "image": rep.user.get_image(),
#                                 "username": rep.user.username,
#                                 "timestamp": read_datetime(rep.timestamp)})
                
#             comment_list.append({"comment": comm.comment,
#                 "id": comm.id,
#                  "blog_id": comm.blog_id,
#                 "user_id": user.id,
#                  "image": user.get_image(),
#                 "username": user.username,
#                 "timestamp": read_datetime(comm.timestamp),
#                 "replies": reply_list})

#         else:

#             user = User.query.filter_by(id = comm.user_id).first()

#             comment_list.append({"comment": comm.comment,
#                         "id": comm.id,
#                          "blog_id": comm.blog_id,
#                         "user_id": user.id,
#                                  "image": user.get_image(),
#                         "username": user.username,
#                         "timestamp": read_datetime(comm.timestamp),
#                         "replies": []})
            
            
#     return jsonify({"comments": comment_list})





@app_comm.route("/new_comment", methods = ["GET", "POST"])
@login_required
def new_comment():
    
    
    data = request.get_json(force = True)
    
    
    
    
    print("NEW COMMENT WORKING!")
    
    if data is not None:
        
        print("Got a new comment!")
        print(data)
        
        
        text = data["comment"]
        blog_id = data["blog_id"]
        user_id = current_user.id
        commenting = Comment(text, blog_id, user_id)
        db.session.add(commenting)
        db.session.commit()
        
        comment = Comment.query.filter(Comment.user_id == user_id).filter(Comment.blog_id == blog_id)\
        .filter(Comment.comment == text).first()
        

        
        COMMENT_LIST_ID.append(comment.id)
    

    
    return "new comment saved!"



@app_comm.route("/send_comment", methods = ["GET", "POST"])
@login_required
def send_comment():
    

    comment_list = []
    
    print("Sending new comment!!!")
    
    comment_id = COMMENT_LIST_ID[-1]

    
    print(comment_id)
    
    comment = Comment.query.filter_by(id = comment_id).first()
    
    user = User.query.filter_by(id = comment.user_id).first()
    
    comment_list.append({"comment": comment.comment,
                         "timestamp": read_datetime(comment.timestamp),
                         "user_id": comment.user_id,
                         "id": comment.id,
                         "image": user.get_image(),
                         "username": User.query.filter_by(id = comment.user_id).first().username,
                         "replies": []})
    
    return jsonify({"add_comment": comment_list})









@app_comm.route("/new_reply", methods = ["GET", "POST"])
@login_required
def new_reply():
    
    data = request.get_json()
    
    
    print(data)
    
    print("Your reply data was received!")
    reply = data["reply"]
    blog_id = data["blog_id"]
    user_id = data["user_id"]
    comment_id = data["comment_id"]
    
    replying = Reply(reply, comment_id, current_user.id)
    db.session.add(replying)
    db.session.commit()
    
    reply_id = Reply.query.filter(Reply.user_id == current_user.id).filter(Reply.comment_id == comment_id).filter(Reply.reply == reply).first().id
    



    REPLY_LIST_ID.append(reply_id)
    print(REPLY_LIST_ID)
    

    return "new reply!"





@app_comm.route("/send_reply", methods = ["GET", "POST"])
@login_required
def send_reply():
    
    
    print(REPLY_LIST_ID)
    reply_id = REPLY_LIST_ID[-1]
    print("sending reply!")
   
    reply_list = []

    
    reply = Reply.query.filter_by(id = reply_id).first()
    
    user = User.query.filter_by(id = reply.user_id).first()
    
    reply_list.append({"reply": reply.reply,
                       "timestamp": read_datetime(reply.timestamp),
                       "comment_id": reply.comment_id,
                       "user_id": reply.user_id,
                       "id": reply.id,
                       "image": user.get_image(),
                       "username": user.username})
    
    return jsonify({"add_reply": reply_list})




@app_comm.route("/delete_text", methods = ["GET", "POST"])
@login_required
def delete_text():
    
    
    
    data = request.get_json()
    
    print("Delete comment or reply")
    
    if data is not None:
        
        print(data)
        
        text_type = data["text_type"]
        comment_id = data["comment_id"]
        blog_id = data["blog_id"]
        
        if text_type == "comment":
            
            
            comment = Comment.query.filter(Comment.id == comment_id).filter(Comment.blog_id == blog_id)\
            .filter(Comment.user_id == current_user.id).first()
            
            
            notify_comment = Notification.query.filter_by(text_type = "comment").filter_by(text_id = comment.id).first()
            
            if notify_comment is not None:
                
                db.session.delete(notify_comment)
                db.session.commit()
            
            
            if comment is not None:
                
                
                replies = comment.replies.all()
                if replies != []:
                    
                    
                    
                    for i in range(len(replies)):
                        

                        notify_reply = Notification.query.filter_by(text_type = "reply").filter_by(text_id = replies[i].id).first()

                        if notify_reply is not None:

                            db.session.delete(notify_reply)
                            db.session.commit()
            
                        
                        db.session.delete(replies[i])
                        db.session.commit()
                
                
                
                db.session.delete(comment)
                db.session.commit()
                
        else:
            
            reply_id = data["reply_id"]
            reply = Reply.query.filter(Reply.id == reply_id).filter(Reply.user_id == current_user.id)\
            .filter(Reply.comment_id == comment_id).first()
            
            if reply is not None:
                
                
                notify_reply = Notification.query.filter_by(text_type = "reply").filter_by(text_id = replies[i].id).first()

                if notify_reply is not None:

                    db.session.delete(notify_reply)
                    db.session.commit()

                
                db.session.delete(reply)
                db.session.commit()
                

    return "deleting a comment/reply!"





@app_comm.route("/update_text", methods = ["GET", "POST"])
@login_required
def update_text():
    
    
    
    data = request.get_json()
    
    print("Edit comment or reply")
    
    if data is not None:
        
        print(data)
        
        text_type = data["text_type"]
        
        comment_id = data["comment_id"]
        text = data["text"]
        
        if text_type == "comment":
            
            
            comment = Comment.query.filter(Comment.id == comment_id).filter(Comment.user_id == current_user.id).first()
            
            if comment is not None:
                
                comment.comment = text
                db.session.commit()
                
                print("Comment updated!")
                
            
                
        else:
            
            
            reply = Reply.query.filter(Reply.id == comment_id).filter(Reply.user_id == current_user.id).first()
            
            if reply is not None:
                
                reply.reply = text
                db.session.commit()
                
                print("Reply updated!")




        
    return "editing a comment/reply!"






























































