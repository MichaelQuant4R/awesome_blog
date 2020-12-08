
    
$.get("/get_notifications").then(function(data){
    
    var notifications = data["notifications"];
    
     for(var i =0; i < notifications.length; i++){
        
         if(notifications[i]["bell"] == true){
             
             bellCount += 1;
             
             console.log(notifications[i]["bell"]);
             console.log("CHeck notification!", notifications[i]["bell"] == true);
             
         }
         
     }
    
    console.log("BELL COUNT", bellCount);
    
    if(bellCount > 0){
    
        bellSpan.innerText = bellCount;
        bellSpan.style.visibility = "visible";
        
    }
});
    
    
    
function ViewNotify(e){
 
    console.log(e);
    
    if(notifyContainer.style.display != "block"){
    
        
        console.log(bellCount);
        notifyContainer.style.display = "block";
        
        
        if(bellCount > 0){
        $.ajax({
            
            
            url:"/clear_notifications",
            method:"POST",
            contentType:"application/json;charset=UTF-8",
            dataType:"json",
            headers:{
                
                "X-CSRFToken": token,
                
            },
            data:JSON.stringify({"clear": true})
       
        }).done(function(){
            
           
            
        });
            
        bellCount = 0;
        bellSpan.style.visibility = "hidden";

            
            
    }
    
    }
    else{
        
     notifyContainer.style.display = "none";
        
    }
    
    
};
    
    
    


    
$.get("/get_notifications").then(function(data){
    
    
    
    
    var notifications = data["notifications"];
    
    //console.log(notifications);
    
    
    var bell = document.getElementById("bell");
    
    
    
    
    
    for(var i =0; i < notifications.length; i++){
        
        
        
        
        
        var notify = notifications[i];
        
        var userName = notify["author"];
        
        var newName = userName[0].toUpperCase() + userName.slice(1, );
        var ID = notify["id"]; // ACTUALLY THE NOTIFY ID, NOT REPLY/COMMENT ID
        var userID = notify["user_id"];
        var timeStamp = notify["timestamp"];
        var text = notify["text"];
        var blogID = notify["blog_id"];
        var blogTitle = notify["blog_title"];
        var image = notify["image"];
        
        
    
        notifyDiv.innerHTML += "<div class='notify-container' id='notify-" + ID + "'> "

            + "<a href='/awesome_blog/one_blog/" + blogID + "/" + blogTitle +  "'>" + blogTitle + "</a>"
            + "<a href='profile/" + userName + "/" + userID + "'>"
            + "<div class='notify-author'>"
            + "<img class='author-image' src=" + image + "><br>"
            + "<span class='author-username'>" + newName + "</span><br>"
            + "</div>"
            + "</a>"
            + "<span class='delete-notification' onclick='DeleteNotify(this)' id='delete-" + ID + "' title='delete notification'><i class='fa fa-trash'></i></span>"
            + "<span class='notify-author-timestamp'>Posted: " + timeStamp + "</span>"
            + "<div class='notify-author-message'><br>"
            + text
            + "</div>"


            + "</div><br>";



    
    
    }
    
    
    
    
    
    
    
    
    
    
    
    
});
    

    

    
// function adjustNotifyContainer(){
    
//     console.log("SCROLL WIDth!!");
//     console.log(document.body.scrollWidth);
    
//     if(notifyContainer.scrollWidth <= "700"){
        
//         console.log(notifyContainer.scrollWidth);
        
//         notifyContainer.style.position = "relative";
//     }else{
//          notifyContainer.style.position = "absolute";}


// };

    
    
function DeleteNotify(e){
    
    
    
    console.log(e);
    
    
    var ID = e.id.split("-")[1];
    
    console.log(ID);
    
    var notify = document.getElementById("notify-" + ID);
    
    notify.style.display = "none";
    notify.nextElementSibling.remove();
    notify.remove();
    
    $.ajax({


        url:"/delete_notification",
        method:"POST",
        contentType:"application/json;charset=UTF-8",
        dataType:"json",
        headers:{

            "X-CSRFToken": token,

        },
        data:JSON.stringify({"notify_id": ID})

    }).done(function(){




    });
    
    
    
    
    
    
    
    
};
    