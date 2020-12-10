var commentDiv = document.getElementById("comment-id");

var commentCount = document.getElementById("comment-count");


    
function DeleteBlog(e){
    
    var authorID = e.id.split("-")[2];
    var authorName = e.id.split("-")[3];
    
    
    var absPath = window.location.href;
    
    console.log(absPath);
    
    
        alert("Deleted your blog");
    window.location.reload();
            window.location = window.location.origin;
        
    
    $.ajax({
        
        
        url:"/delete_blog",
        method:"POST",
        dataType:"json",
        contentType:"application/json;charset=UTF-8",
        headers:{
            
            "X-CSRFToken": token,
        },
        data:JSON.stringify({"blog_id": blogID, "author_id": authorID, "author_name": authorName})
        
        
        
        
        
    }).done(function(){
        
        console.log("DELETED BLOG!");

        
    });

    
    
    
};



















// $.get("/comment_data").then(function(data){

    var repCount = 0;
//     var comm = data["comments"];
    
    for(var c = 0; c < comm.length; c++){

        repCount += comm[c]["replies"].length;

    };
    
    
    commentCount.innerText = comm.length + repCount;
    
    
// });
    

    
    
    
// $.get("/comment_data").then(function(data){

//     var comm = data["comments"];
    
for(var i =0; i < comm.length; i++){

        console.log(comm[i]);
        
        
        var userName = comm[i]["username"];
        var newName = userName[0].toUpperCase() + userName.slice(1,);
        
        var comment = comm[i]["comment"];
        var userID = comm[i]["user_id"];
        var commentID = comm[i]["id"];
        var timeStamp = comm[i]["timestamp"];
        var image = comm[i]["image"];
        
        var interact = "";
        
        
        if(currentUserID == userID){
  
            
            interact = "<span class='interact-tooltip'>"+
                
                "<button onclick='EditText(this)' class='edit-text' id='edit-comment-" 
                + commentID  + "-" + userID
                +"'>Edit</button><br><br>"
            
                + "<button onclick='DeleteText(this)' class='delete-text' id='delete-comment-" 
                + commentID + "-" + userID
                
                +"'>Delete</button>"
            
            
            
            +"</span>"
           
            
            
        }else{
            
            
            interact = "<span class='interact-tooltip'>" + 
                
                "<button onclick='ReportText(this)' class='report-text' id='report-comment-"
            + commentID + "-" + userID
        
            + "'>Report</button><br>"
                
                +"</span>"
            
           
            
        }
        
        
        commentDiv.innerHTML += "<div class='comment-container' id='comment-container-" + commentID + "-" +  userID + "'>"
        
        + "<span class='timestamp-container-comment'><span class='timestamp-comment'>" + timeStamp + "</span>"
        
        + "<div class='interact-dots'>"
        + "..."
       
        +interact
    
        + "</div>"

        
        
        + "<span class='comment-info'><img src='" + image + "' class='user-image'> </span>"
        
        + "<a class='commenter-info' href='/profile/" + userName + "/"
        + userID + "'><span class='username'>" + newName + "</span></a><br>"
        
        + "<span id='comment-text-" + commentID + "' class='comment-text'>" + comment + "</span>"
        + "<div class='comment-interact' id='comment-interact-" + commentID + "'>"
    
        + "<button class='reply-button' onclick='ToggleReplyForm(this)' id='toggle-comment-button-" + commentID + "'> reply</button><br>"
    
    
    + "</div>"
        
        
        
         + "<form method = 'POST' class='comment-form' id='form-comment-" + commentID + "'>"
        
        + "<input type='hidden' name='csrf_token' value='" + token + "'>"
        + "<textarea class='textarea-comment' placeholder='add a reply to the conversation...' id='textarea-comment-" + commentID + "'></textarea><br>"
        
        + "<input class='submit-textarea' type='button' onclick='ReplyButton(this)' id='submit-comment-" + commentID + "-" + userID + "' value='add reply'>"
        
        
        + "</form>"
   
        + "<div id='comment-break-" + commentID + "'></div>"
        
        
        + "</div><br>";
        
         var form = document.getElementById("form-comment-" + commentID);
        form.style.display = "none";

        var replies = comm[i]["replies"];
        
        if(replies.length > 0){
            
            
            
            var repliesList = document.createElement("DIV");
            
            
            var interactive = document.getElementById("comment-interact-" + commentID);
            
            repliesList.setAttribute("onclick", "ToggleReplies(this)");
            repliesList.id = "toggle-replies-" + commentID;
            repliesList.className = "toggle-replies";
            
            repliesList.innerText = "view " + replies.length + " Replies";
            interactive.appendChild(repliesList);
            
            
            
            
            for(var r = 0; r < replies.length; r++){
                
                
                 var userName = replies[r]["username"];
                var newName = userName[0].toUpperCase() + userName.slice(1,);

                var reply = replies[r]["reply"];
                var userID = replies[r]["user_id"];
                var replyID = replies[r]["id"];
                var timeStamp = replies[r]["timestamp"];
                var image = replies[r]["image"];

                var interact = "";
                
             if(currentUserID == userID){
  
            
                             
            interact = "<span class='interact-tooltip'>"+
                
                "<button onclick='EditText(this)' class='edit-text' id='edit-reply-" 
                 +
                replyID + "-" + commentID + "-" + userID
                +"'>Edit</button><br><br>"
            
                + "<button onclick='DeleteText(this)' class='delete-text' id='delete-reply-" 
                 +replyID + "-" + commentID + "-" + userID
                
                +"'>Delete</button>"
            
            
            
            +"</span>"
           
            
            
        }else{
            
            
            interact = "<span class='interact-tooltip'>" + 
                
                "<button onclick='ReportText(this)' class='report-text' id='report-reply-"
            + replyID + "-" + commentID + "-" + userID
        
            + "'>Report</button><br>"
                
                +"</span>"
            
           
            
        }
                


                replyDiv = document.createElement("DIV");
                replyDiv.id = "full-reply-" +replyID;
                replyDiv.className = "reply-list";
                
               
                
                replyDiv.innerHTML += "<div class='reply-container' id='reply-container-"  + replyID + "-" +  commentID + "-" +  userID + "'>"

                + "<span class='timestamp-container-reply'><span class='timestamp-reply'>" + timeStamp + "</span>"

                + "<div class='interact-dots'>"
                + "..."

                +interact

                + "</div>"


                + "<span class='reply-info'><img src='" + image + "' class='user-image'> </span>"

                + "<a class='reply-info' href='/profile/" + userName + "/"
                + userID + "'><span class='username'>" + newName + "</span></a><br>"

                + "<span id='reply-text-" + replyID + "-" +  commentID + "' class='reply-text'>" 
                    
                + reply + "</span><br>"
                + "<button class='reply-button' onclick='ToggleReplyForm(this)' id='toggle-reply-button-" 
                    + replyID + "-" + commentID + "'> reply</button>"
                
                + "<form method = 'POST' class='reply-form' id='form-reply-" +  replyID + "-" + commentID + "'>"

                + "<input type='hidden' name='csrf_token' value='" + token + "'>"
                + "<textarea class='textarea-reply' placeholder='add a reply to the conversation...' id='textarea-reply-"
                + replyID + "-" + commentID + "'></textarea><br>"

                + "<input class='submit-textarea' type='button' onclick='ReplyButton(this)' id='submit-reply-" + replyID + "-"
                    + commentID + "-" + userID + "' value='add reply'>"


                + "</form>"




                + "</div><br>";

                
        
                var commentBreak = document.getElementById("comment-break-" + commentID);
                
                commentBreak.appendChild(replyDiv);
                
                
                
                var form = document.getElementById("form-reply-" + replyID + "-" + commentID);
                form.style.display = "none";
  
            };
            
            

            
            
        };
        

        
    };
    
    
    
    var repList = document.getElementsByClassName("reply-list");
    
    
for(var i =0; i < repList.length; i++){
    
    console.log("Hide replies!");
    
    
    repList[i].style.display = "none";

  
};
    
    
// });
    
    
    
    
function ToggleReplyForm(e){
    
    
    
    console.log(e);
    
    
    var check = e.id.split("-")[1];
    
    if(check == "comment"){
        
        var ID = e.id.split("-")[3];
        
        
        var form = document.getElementById("form-comment-" + ID);
        
        if(form.style.display != "block"){
            form.style.display = "block";
            e.innerText = "cancel";
            
            
        }
        else{
            
             form.style.display = "none";
            e.innerText = "reply";
            document.getElementById("textarea-comment-"  + ID).value = "";
            
            
            
        }
        
        
    }else{
        
        
         
        var ID = e.id.split("-")[4];
        var repID = e.id.split("-")[3];
        
        
        
        var form = document.getElementById("form-reply-" + repID + "-" + ID);
        
        if(form.style.display != "block"){
            form.style.display = "block";
            e.innerText = "cancel";
            
            
        }
        else{
            
             form.style.display = "none";
            e.innerText = "reply";
            document.getElementById("textarea-reply-" +  repID + "-" + ID).value = "";

        }

    }

    
    
};

    

function ToggleReplies(e){
    
    console.log("Toggle replies!");
    var text;
    var ID = e.id.split("-")[2];
    
    console.log(e);
    console.log(e.id);
    console.log(e.id);
    
    var containers = document.getElementById("comment-break-" + ID).getElementsByClassName("reply-list");
    
    
    
    var toggleText = document.getElementById("toggle-replies-" + ID);
    var i =0;
    var length = containers.length;
    for(i; i < length; i++){
        
        
        if(containers[i].style.display != "block"){
            
            containers[i].style.display = "block";
            text = toggleText.innerText.replace("view", "hide");
            
            toggleText.innerText = text;
            
        }else{
            
            containers[i].style.display = "none";
            text = toggleText.innerText.replace("hide", "view");
            toggleText.innerText = text;
 
        }

    };
     
};
    

    
    
function ToggleComments(e){

    var commentDiv = document.getElementById("comment-id");
    var comm = document.getElementsByClassName("comment-container");
    var commList = [];
    
    for(var i = comm.length - 1; i > -1; i--){
        
        commList.push(comm[i]);

    };
    
    commentDiv.innerHTML = "";
    
    for(var t = 0; t < commList.length; t++){

        commentDiv.appendChild(commList[t]);
        
        
        commList[t].insertAdjacentHTML("afterend", "<br>");

        
    };
   
};
    

    
    
    
function NewComment(){
    
    
     $.get("/send_comment").then(function(data){
            
            
            
            console.log(data);
            
            var comm = data["add_comment"][0];
            
            
            
         
             var comment = comm["comment"];
            var userID = comm["user_id"];
            var userName = comm["username"];
            var image = comm["image"];
            
            var newName = userName[0].toUpperCase() + userName.slice(1,);
            
            var timeStamp = comm["timestamp"];
            
            var commentID = comm["id"];
            
            var eleComment = document.createElement("DIV");

            var interact = "";
         
         sendNotificationComment(blogID, commentID);
    
         
         
          interact = "<span class='interact-tooltip'>"+
                
                "<button onclick='EditText(this)' class='edit-text' id='edit-comment-" 
                + commentID  + "-" + userID
                +"'>Edit</button><br><br>"
            
                + "<button onclick='DeleteText(this)' class='delete-text' id='delete-comment-" 
                + commentID + "-" + userID
                
                +"'>Delete</button>"
            
            
            
            +"</span>"
           
        
        
        eleComment.innerHTML += "<div class='comment-container' id='comment-container-" + commentID + "-" +  userID + "'>"
        
        + "<span class='timestamp-container-comment'><span class='timestamp-comment'>" + timeStamp + "</span>"
        
        + "<div class='interact-dots'>"
        + "..."
       
        +interact
    
        + "</div>"

        
        
        + "<span class='comment-info'><img src='" + image + "' class='user-image'> </span>"
        
        + "<a class='commenter-info' href='/profile/" + userName + "/"
        + userID + "'><span class='username'>" + newName + "</span></a><br>"
        
        + "<span id='comment-text-" + commentID + "'>" + comment + "</span>"
        + "<div class='comment-interact' id='comment-interact-" + commentID + "'>"
    
        + "<button class='reply-button' onclick='ToggleReplyForm(this)' id='toggle-comment-button-" + commentID + "'> reply</button><br>"
    
    
    + "</div>"
        
        
        
         + "<form method = 'POST' class='comment-form' id='form-comment-" + commentID + "'>"
        
        + "<input type='hidden' name='csrf_token' value='" + token + "'>"
        + "<textarea class='textarea-comment' placeholder='add a reply to the conversation...' id='textarea-comment-" + commentID + "'></textarea><br>"
        
        + "<input class='submit-textarea' type='button' onclick='ReplyButton(this)' id='submit-comment-" + commentID + "-" + userID + "' value='add reply'>"
        
        
        + "</form>"
   
        + "<div id='comment-break-" + commentID + "'></div>"
        
        
        + "</div><br>";
        
         
            
            
            
        commentDiv.insertBefore(eleComment, commentDiv.childNodes[0]);
            
         var form = document.getElementById("form-comment-" + commentID);
        form.style.display = "none";   
            
            
            
            
        });
        
    
    
};
    
    

function sendNotificationComment(blogID, commentID){
    
    $.ajax({
        
        url:"/send_notification_comment",
        method:"POST",
        contentType:"application/json;charset=UTF-8",
        dataType:"json",
        headers:{
            
            "X-CSRFToken": token,
        },
        data:JSON.stringify({"notified": [blogID, commentID]})
    
    }).done(function(){
        
        console.log("SENT NOTIFICATION !!!!");
        
    });
  
    
};

    
    
$("#submit").click(function(e){
    
  
//     NOT FINISHED YET
    
    var comment = document.getElementById("comment");
    
    var text = comment.value;
    console.log(text);
    
    
    
    
    
    if(text.length >= 3 && text.length <= 300){
        
        
        comment.value = "";
    
    
    $.ajax({
        
        
        url:"/new_comment",
        method:"POST",
        dataType:"json",
        contentType:"application/json;charset=UTF-8",
        headers:{
            "X-CSRFToken": token,
        },
        data:JSON.stringify({"comment":text, "blog_id": blogID})
        
  
        
    }).done(function(){
        
        
        
        NewComment();
       
        
        
    }).fail(function(){
        
        
        
        
        NewComment();
        

        

    });
    
    

    
    }else{
        
        
        console.log("The comment must be between 3 and 300 characters long!");
        
        
        
        var error = document.getElementById("comment-error");
        
        error.style.display = "block";
        
        error.innerHTML = "<span><center>Comment must be betweeen 3 and 300 characters long <span id='delete-error' onclick='DeleteError()'>X</span></center></span>";
        
    }
    
    e.preventDefault();
    
});



function DeleteError(){
    
    
      var error = document.getElementById("comment-error");
        
        error.style.display = "none";
    
    
    
    
};
    
    
    

    
function getReplyData(check, notifyUserID){
    
    
    
    console.log("GETTING REPLY DATA!");
    
    $.get("/send_reply").then(function(data){
        
        console.log(data);
        
        
        var rep = data["add_reply"][0];
        var eleReply = document.createElement("DIV");
        var reply = rep["reply"];
        var commentID = rep["comment_id"];
        var timeStamp = rep["timestamp"];
        var userID = rep["user_id"];
        var replyID = rep["id"];
        var userName = rep["username"];
        
        var newName = userName[0] + userName.slice(1,);
        var image = rep["image"];
        
        
        var commentBreak = document.getElementById("comment-break-" + commentID);
        
        replyDiv.className = "reply-list";
        replyDiv.id = "full-reply-" + replyID;

       var interact = "";

        
        
        //         REPLY NOTIFICATION

        sendNotificationReply(blogID, commentID,  replyID, notifyUserID);

        eleReply = document.createElement("DIV");
        eleReply.id = "full-reply-" +replyID;
        eleReply.className = "reply-list";



        eleReply.innerHTML += "<div class='reply-container' id='reply-container-" + "-" + replyID + "-" +  commentID + "-" +  userID + "'>"

        + "<span class='timestamp-container-reply'><span class='timestamp-reply'>" + timeStamp + "</span>"

        + "<div class='interactive-box'>"

        +interact

        + "</div>"


        + "<span class='reply-info'><img src='" + image + "' class='user-image'> </span>"

        + "<a class='reply-info' href='/profile/" + userName + "/"
        + userID + "'><span class='username'>" + newName + "</span></a><br>"

        + "<span id='reply-text-" + "-" + replyID + "-" +  commentID + "'>" 

        + reply + "</span><br>"
        + "<button class='reply-button' onclick='ToggleReplyForm(this)' id='toggle-reply-button-" 
            + replyID + "-" + commentID + "'> reply</button>"

        + "<form method = 'POST' class='reply-form' id='form-reply-" +  replyID + "-" + commentID + "'>"

        + "<input type='hidden' name='csrf_token' value='" + token + "'>"
        + "<textarea class='textarea-reply' placeholder='add a reply to the conversation...' id='textarea-reply-"
        + replyID + "-" + commentID + "'></textarea><br>"

        + "<input class='submit-textarea' type='button' onclick='ReplyButton(this)' id='submit-reply-" + replyID + "-"
            + commentID + "-" + userID + "' value='add reply'>"


        + "</form>"




        + "</div><br>";


         
        
        commentBreak.appendChild(eleReply);
        
        var form = document.getElementById("form-reply-" + replyID + "-" + commentID);
        form.style.display = "none";
        
        
        if(check == "comment"){
            
            
            var formAbove = document.getElementById("form-comment-" + commentID);
            formAbove.style.display = "none";
            
            
        }else{
            
            
            
            
            var formAbove = document.getElementById("form-reply-" + replyIdAbove + "-" + commentID);
            formAbove.style.display = "none";
            
            
            
            
        }
    
    
        
    });
    
    
    
};

    

function sendNotificationReply(blogID, commentID,  replyID, notifyUserID){
    
    $.ajax({
        
        url:"/send_notification_reply",
        method:"POST",
        contentType:"application/json;charset=UTF-8",
        dataType:"json",
        headers:{
            
            "X-CSRFToken": token,
        },
        data:JSON.stringify({"notified": [blogID, commentID, replyID, notifyUserID]})
    
    }).done(function(){
        
        console.log("SENT NOTIFICATION !!!!");
        
    });
  
    
};

    
    
    
function ReplyButton(e){

    console.log(e);
    
    
    var check = e.id.split("-")[1];
    
    //var replyIdAbove;
    
    var notifyUserID;
    
    if(check == "comment"){
        
        console.log("This is a reply to a comment!");
        
        var ID = e.id.split("-")[2];
        
        var userID = e.id.split("-")[3];
        
        notifyUserID = userID;
        
        var text = document.getElementById("textarea-comment-" +ID);
        var newText = text.value;
        
    }else{
        
        
        console.log("This is a reply to a reply!");
        
        var ID = e.id.split("-")[3];
        var replyID = e.id.split("-")[2];
        
        var userID = e.id.split("-")[4];
        
        notifyUserID = userID;
        
        var text = document.getElementById("textarea-reply-" + replyID + "-" + ID);
        var newText = text.value;
        //replyIdAbove = replyID;
        
        
        
    }
        
        
        
    if(newText.length >=3 && newText.length <= 300){



        text.value = "";

        $.ajax({


            url:"/new_reply",
            method:"POST",
            dataType:"json",
            contentType:"application/json;charset=UTF-8",
            headers:{


                "X-CSRFToken": token,
            },
            data:JSON.stringify({"reply": newText, "blog_id": blogID,
                                 "user_id": userID, "comment_id": ID})


        }).done(function(){

                
                
            getReplyData(check, notifyUserID);
                
                
                
            }).fail(function(){
                
                
            getReplyData(check, notifyUserID);

            });
        
        
        
        
      }else{
        
        
        console.log("The reply must be between 3 and 300 characters long!");
        
          alert("The reply must be between 3 and 300 characters long!");
        
     
        }
    

};
    
    

    
function postTextData(commentID, replyID, textType, interactType, text){
    
    
    var urlPath = "/" + interactType;
    

    $.ajax({
        
        
        url:urlPath,
        method:"POST",
        dataType:"json",
        contentType:"application/json;charset=UTF-8",
        headers:{
            
            "X-CSRFToken": token,
            
        },
        data:JSON.stringify({"comment_id": commentID, "reply_id": replyID,
                             "text_type":textType, "text": text,
                            "blog_id": blogID})
        

        
    });
    

};
    
    
    
    
    
    
    
    
    
    
function DeleteText(e){
    
    
    console.log(e);
    
    var check = e.id.split("-")[1];
    
    var text = null;
    
    var replyID = null;
    
    
    console.log(e.id);
    
    if(check == "comment"){
        
        console.log("Deleting a comment!");
        
        var ID = e.id.split("-")[2]; 
        var userID = e.id.split("-")[3];
        
        
        var del = document.getElementById("comment-container-" + ID + "-" +  userID);
        
        del.style.display = "none";

        
         postTextData(ID, replyID, check, "delete_text", text);       

        
    }else{
        
        console.log("Deleting a reply!");
        
        var replyID = e.id.split("-")[2];
        var ID = e.id.split("-")[3];
        var userID = e.id.split("-")[4];
        
        var del = document.getElementById("reply-container-" + replyID + "-" + ID + "-" + userID);
        
        
        del.style.display = "none";
        
        
        
        postTextData(ID, replyID, check, "delete_text", text);
        
        
    }
        
        
        
        
};
    
    
    
function UpdateText(e){

    console.log(e);
    
    var check = e.id.split("-")[1];
    
    console.log(e.id);

    var text = null;
    
    var replyID = null;
  
    
    if(check == "comment"){
        
        console.log("Updated a comment!");
        var ID = e.id.split("-")[2]; 
        var userID = e.id.split("-")[3];

        
        var edit = document.getElementById("comment-container-" + ID + "-" +  currentUserID);
        var form = document.getElementById("form-comment-" + ID);
        var textArea = form.getElementsByTagName("textarea")[0];
        text = textArea.value;
        
//         GIVE NEW TEXTAREA VALUE TO COMMENT TEXT, THEN SET TEXTAREA TO NONE AND HIDE FORM
        var updatedText = document.getElementById("comment-text-" + ID);
        updatedText.innerText = text;
        textArea.value = "";
        form.style.display = "none";
        
//         REMOVE CANCEL BUTTON HERE
        var cancelButton = document.getElementById("cancel-comment-" + ID);
        cancelButton.remove();
        
//         SWAP UPDATETEXT BUTTON FOR REPLYBUTTON
        var changeButton = document.getElementById("submit-comment-" + ID  + "-" + currentUserID);
        changeButton.setAttribute("onclick", "ReplyButton(this)");
        changeButton.value = "add reply";
        

         postTextData(ID, replyID, check, "update_text", text);    
        
        

        
    }else{
        
        console.log("Updated a reply!");
        
         var replyID = e.id.split("-")[2];
        var ID = e.id.split("-")[3];
        var userID = e.id.split("-")[4];
        
        var edit = document.getElementById("reply-container-" + replyID + "-" + ID + "-" + currentUserID);
        var form = document.getElementById("form-reply-" + replyID + "-" + ID);
        var textArea = form.getElementsByTagName("textarea")[0];
        text = textArea.value;
        
        console.log(text);
        
        var updatedText = document.getElementById("reply-text-" + replyID + "-" + ID);
        updatedText.innerText = text;

        textArea.value = "";
        form.style.display = "none";
        
        var cancelButton = document.getElementById("cancel-reply-" + replyID + "-" +ID);
        cancelButton.remove();
        
        var changeButton = document.getElementById("submit-reply-" + replyID + "-" + ID + "-" + currentUserID);
        changeButton.setAttribute("onclick", "ReplyButton(this)");
        changeButton.value = "add reply";
       
 
        postTextData(ID, replyID, check, "update_text", text);
    
    }
        
        
        
        
};
    
    
    
    
    
    
function EditText(e){
    
    
    console.log(e);
    
    var check = e.id.split("-")[1];
    
    console.log(e.id);

    
    var text;
    if(check == "comment"){
        
        console.log("Editing a comment!");
        
        
        var ID = e.id.split("-")[2]; 
        var userID = e.id.split("-")[3];

        edit = document.getElementById("comment-text-" + ID);
        console.log(edit.innerText);
        
        
        var form = document.getElementById("form-comment-" + ID);
        
        form.style.display = "block";
        var textArea = form.getElementsByTagName("textarea")[0];
        console.log(textArea);
        textArea.value = edit.innerText;
        text = edit.innerText;
        
        
        var cancelButton = "<button type='button' onclick='CancelEditText(this)' class='cancel-edit' " +
            " id='cancel-comment-" + ID + "'>cancel</button>";
        
        
      var sub = document.getElementById("submit-comment-" + ID + "-" + currentUserID);
        
        sub.setAttribute("onclick", "UpdateText(this)");
        sub.value = "update";
        sub.insertAdjacentHTML("afterend", cancelButton);
        
        var cancel = document.getElementById("cancel-comment-" + ID);
        cancel.value = text;
        
        
    }else{
        
        console.log("Editing a reply!");
        
         var replyID = e.id.split("-")[2];
        var ID = e.id.split("-")[3];
        var userID = e.id.split("-")[4];
        
        edit = document.getElementById("reply-text-" + replyID + "-" + ID);
        console.log(edit);
        
        var form = document.getElementById("form-reply-" + replyID + "-" + ID);
        form.style.display = "block";
        var textArea = form.getElementsByTagName("textarea")[0];
        textArea.value = edit.innerText;
        text = edit.innerText;
        
        
        var cancelButton = "<button type='button' onclick='CancelEditText(this)' class='cancel-edit' " +
            " id='cancel-reply-" + replyID + "-" + ID + "'>cancel</button>";
        
        
        var sub = document.getElementById("submit-reply-" + replyID + "-" +  ID + "-" + currentUserID);
        sub.setAttribute("onclick", "UpdateText(this)");
        sub.value = "update";
        sub.insertAdjacentHTML("afterend", cancelButton);
        var cancel = document.getElementById("cancel-reply-" + replyID + "-" + ID);
        cancel.value = text;
        

    }
  
        
};
    
    
    
    
    
    
    
    
    
    
    
function ReportText(e){
    
    
    console.log(e);
    
    
    alert("This comment/reply has been reported. Thank you.")
    
    
};
    
    
    
    
function CancelEditText(e){
    
    console.log(e);
    
    
    var check = e.id.split("-")[1];
    
    if(check == "comment"){
        
        
        var ID = e.id.split("-")[2];
        
        var form = document.getElementById("form-comment-" + ID);
        
        var sub = document.getElementById("submit-comment-" + ID + "-" + currentUserID);
        
        
        sub.setAttribute("onclick", "ReplyButton(this)");
        
        sub.value = "add reply";
        
        var textArea = form.getElementsByTagName("textarea")[0];
        textArea.value = "";
        form.style.display = "none";
        
        var cancel = document.getElementById("cancel-comment-" + ID);
        cancel.remove();
        

        
    }else{
        
        
         var ID = e.id.split("-")[3];
        
        var replyID = e.id.split("-")[2];
        
        var form = document.getElementById("form-reply-" + replyID + "-" + ID);
        
        var sub = document.getElementById("submit-reply-" + replyID + "-" + ID + "-" + currentUserID);
        
        
        sub.setAttribute("onclick", "ReplyButton(this)");
        
        sub.value = "add reply";
        
        var textArea = form.getElementsByTagName("textarea")[0];
        textArea.value = "";
        form.style.display = "none";
        
        var cancel = document.getElementById("cancel-reply-" + replyID + "-" + ID);
        cancel.remove();

    }
    
    
};
    
    
    
    
    
    
    
