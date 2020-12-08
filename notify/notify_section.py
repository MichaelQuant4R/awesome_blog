from flask import (Blueprint, request, jsonify)
from models import (db, User, Blog, Comment, Reply, Notification)
from flask_login import (login_required, current_user)
from filters import read_datetime


app_bell = Blueprint("notify_section", __name__)



@app_bell.route("/get_notifications", methods = ["GET", "POST"])
@login_required
def get_noticiations():
    
    user = User.query.filter_by(id = current_user.id).first()

    notifications = user.notifications.all()

    notify_list = []

    if notifications != []:

        notifications = notifications[::-1]


        for msg in notifications:


            if msg.text_type == "comment":


                ## only for blog author

                comment = Comment.query.filter_by(id = msg.text_id).first()

                text_author = User.query.filter_by(id = comment.user_id).first()

                notify_list.append({"text_type": "comment",
                                   "author": text_author.username,
                                   "user_id": text_author.id,
                                   "image": text_author.get_image(),
                                   "id": msg.id,
                                    "text": comment.comment,
                                   "timestamp": read_datetime(msg.timestamp),
                                   "blog_id": comment.blog_id,
                                   "blog_title": comment.blog.title,
                                   "bell": msg.bell})

            else:

                ### reply for user or blog author

                reply = Reply.query.filter_by(id = msg.text_id).first()

                text_author = User.query.filter_by(id = reply.user_id).first()

                notify_list.append({"text_type": "comment",
                                   "author": text_author.username,
                                   "user_id": text_author.id,
                                   "image": text_author.get_image(),
                                   "id": msg.id,
                                    "text": reply.reply,
                                   "timestamp": read_datetime(msg.timestamp),
                                   "blog_id": reply.comment.blog_id,
                                   "blog_title": reply.comment.blog.title,
                                   "bell": msg.bell})
    
    return jsonify({"notifications": notify_list})


@app_bell.route("/send_notification_comment", methods = ["GET", "POST"])
@login_required
def send_notification_comment():
    
    print("SEND NEW NOTIFICATION!!!")
    
    data = request.get_json()
    
    print(data)
    
    if data is not None:
    
    
        #  Notification(text_type, text_id, user_id)

        blog_id = int(data["notified"][0])
        text_id = int(data["notified"][1])

        blog = Blog.query.filter_by(id = blog_id).first()

        if blog.user_id != current_user.id:

            notify = Notification("comment", text_id, blog.user_id)
            db.session.add(notify)
            db.session.commit()
    
    return "Got new notification data!"
    
    
@app_bell.route("/send_notification_reply", methods = ["GET", "POST"])
@login_required
def send_notification_reply():
    
    print("SEND NEW NOTIFICATION!!!")
    
    data = request.get_json()
    
    print(data)
    
    if data is not None:
    
    
        #  Notification(text_type, text_id, user_id)
        #  data:JSON.stringify({"notified": [blogID, commentID, replyID, notifyUserID]})

        blog_id = int(data["notified"][0])
        comment_id = int(data["notified"][1])
        reply_id = int(data["notified"][2])
        user_id = int(data["notified"][3])
        
        text_id = reply_id

        blog = Blog.query.filter_by(id = blog_id).first()
        
        comment = Comment.query.filter_by(id = comment_id).first()
        reply = Reply.query.filter_by(id = reply_id).first()
        
        if current_user.id != user_id:

            notify = Notification("reply", text_id, user_id)
            db.session.add(notify)
            db.session.commit()

    return "Got new reply notification data!"
    
    
    
    
    
@app_bell.route("/receive_notifications", methods = ["GET", "POST"])
@login_required
def receive_notifications():
    
    
    
    notifications = current_user.notifications.all()
    
    notify_list = []
    
    if notifications != []:
        
        pass
        
#         notifications = notifications[::-1]
        
#         for msg in messages:

#             print(msg)

#             user = User.query.filter
#             notify_list.append({"text_type": "reply",
#                                "author": msg.user.username,
#                                 "user_id": msg.user.id,
#                                 "image": msg.user.get_image(),
#                                "id": msg.id,
#                                "text": msg.reply,
#                                "blog_id": msg.comment.blog_id,
#                                 "blog_title": msg.comment.blog.title,
#                                "timestamp": read_datetime(msg.timestamp)})


        
        
        
        
    return jsonify({"notify_list": notify_list})
    
    
    
    
    
    
    
@app_bell.route("/clear_notifications", methods = ["GET", "POST"])
@login_required
def clear_notifications():
    
    
    data = request.get_json()
    
    print("CLEAR NOTIFICATIONS!!!")
    
    if data is not None:
        
        print(data)
    
        notifications = current_user.notifications.all()

        if notifications != []:


            for notify in notifications:

                print(notify)

                notify.bell = False
                db.session.commit()

            
    return "Cleared notifications!"
    
    
    
    
    
    
    
@app_bell.route("/delete_notification", methods = ["GET", "POST"])
@login_required
def delete_notification():
    
    
    data = request.get_json()
    
    print("DELETE NOTIFICATION!!!")
    
    if data is not None:
        
        print(data)
        
        notify_id = data["notify_id"]
        
        
        notify = Notification.query.filter_by(id = notify_id).first()
        db.session.delete(notify)
        db.session.commit()
        
        print("DELETED!!")

    return "Cleared notifications!"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    