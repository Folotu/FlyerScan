
    var upvoteCommentElements = document.getElementsByClassName('fa fa-arrow-up comment');
    var downvoteCommentElements = document.getElementsByClassName('fa fa-arrow-down comment');
    
    var upvotePostElements = document.getElementsByClassName('fa fa-arrow-up post');
    var downvotePostElements = document.getElementsByClassName('fa fa-arrow-down post');

    function delayedLog() {
        console.log('This message is delayed by 2 seconds');
    }

    // Loop through the elements
    for (var i = 0; i < upvoteCommentElements.length; i++) 
    {
        
        (function(i) 
        {
            upvoteCommentElements[i].addEventListener("click", function() 
            {
                upvoteCommentElements[i].classList.add("active");
                console.log(upvoteCommentElements[i].style.backgroundColor)
         
                if (upvoteCommentElements[i].style.backgroundColor == "rgb(204, 204, 204)") 
                {
                    upvoteCommentElements[i].style = "background-color: ''" 
                    downvoteCommentElements[i].style = "background-color: ''" 

                    var commentId = $(this).data('commentid');

                    //Make an AJAX request to update the up vote count for the comment
                        $.ajax({
                            url: `/comment/${commentId}/vote/unvote/`,
                            type: 'POST',
                            success: function(response) {
                                if (response.redirect) {
                                    // Update the URL in the browser to the new location
                                    window.location.href = response.redirect;
                                }else {
                                    // Update the display to show the updated vote count
                                    setTimeout(delayedLog, 20000);
                                    if(response.votes >= 0)
                                    {
                                        $(upvoteCommentElements[i]).next().text(response.votes + ' Upvotes ');
                                    }else
                                    {
                                        $(upvoteCommentElements[i]).next().text(response.votes + ' Downvotes ');
                                    }

                                }
                                
                                console.log("comment unvoted")
                            }
                        });
                   
                }
                else
                {
                    upvoteCommentElements[i].style = "background-color: #ccc;";
                    downvoteCommentElements[i].style = "background-color: ''";
                    var commentId = $(this).data('commentid');

                    //Make an AJAX request to update the up vote count for the comment
                        $.ajax({
                            url: `/comment/${commentId}/vote/add`,
                            type: 'POST',
                            success: function(response) {
                                if (response.redirect) {
                                    // Update the URL in the browser to the new location
                                    window.location.href = response.redirect;
                                }else {
                                    // Update the display to show the updated vote count
                                    setTimeout(delayedLog, 20000);
                                    if(response.votes >= 0)
                                    {
                                        $(upvoteCommentElements[i]).next().text(response.votes + ' Upvotes ');
                                    }else
                                    {
                                        $(upvoteCommentElements[i]).next().text(response.votes + ' Downvotes ');
                                    }

                                }
                                
                                console.log("it updates")
                            }
                        });

                        // Remove the "active" class from the current element
                        //upvoteCommentElements[i].className = upvoteCommentElements[i].className.replace("active", "");
                        upvoteCommentElements[i].classList.toggle("active");

                }

            });

            downvoteCommentElements[i].addEventListener("click", function() 
            {
                downvoteCommentElements[i].classList.add("active");
                if (downvoteCommentElements[i].style.backgroundColor == "rgb(204, 204, 204)") {
                    //add active class
                    downvoteCommentElements[i].style = "background-color: ''" 
                    upvoteCommentElements[i].style = "background-color: ''" 
                    
                    var commentId = $(this).data('commentid');
                    console.log(commentId)
                    //Make an AJAX request to update the up vote count for the comment
                    $.ajax({
                        url: `/comment/${commentId}/vote/unvote`,
                        type: 'POST',
                        success: function(response) {
                            if (response.redirect) {
                                // Update the URL in the browser to the new location
                                window.location.href = response.redirect;
                            }
                            // Update the display to show the updated vote count
                            setTimeout(delayedLog, 2000);
                            if(response.votes >= 0)
                            {
                                $(upvoteCommentElements[i]).next().text(response.votes + ' Upvotes ');
                            }else{
                                $(upvoteCommentElements[i]).next().text(response.votes + ' Downvotes ');
                            }

                            console.log("unvoted")
                        }
                    });

                } 
                else{
                    downvoteCommentElements[i].style = "background-color: #ccc;";
                    upvoteCommentElements[i].style = "background-color: ''";
                    
                    
                    var commentId = $(this).data('commentid');
                    console.log(commentId)
                    //Make an AJAX request to update the up vote count for the comment

                    $.ajax({
                        url: `/comment/${commentId}/vote/subtract`,
                        type: 'POST',
                        success: function(response) {
                            if (response.redirect) {
                                // Update the URL in the browser to the new location
                                window.location.href = response.redirect;
                            }
                            // Update the display to show the updated vote count
                            setTimeout(delayedLog, 2000);
                            if(response.votes >= 0)
                            {
                                $(upvoteCommentElements[i]).next().text(response.votes + ' Upvotes ');
                            }else{
                                $(upvoteCommentElements[i]).next().text(response.votes + ' Downvotes ');
                            }
                        }
                    });

                    // Remove the "active" class from the current element
                    downvoteCommentElements[i].classList.toggle("active");
                }
            });
        })(i)   

    }

    // post element functionality 
    for (var i = 0; i < upvotePostElements.length; i++) 
    {
        
        (function(i) 
        {
            upvotePostElements[i].addEventListener("click", function() 
            {
                // Add the "active" class to the current element
                //upvotePostElements[i].className += " active";
                upvotePostElements[i].classList.add("active");
                console.log(upvotePostElements[i].style.backgroundColor)
                if (upvotePostElements[i].style.backgroundColor == "rgb(204, 204, 204)" )
                {
                    upvotePostElements[i].style = "background-color: ''" 
                    downvotePostElements[i].style = "background-color: ''" 

                    var postId = $(this).data('postid');

                    //Make an AJAX request to unvote for post
                    $.ajax({
                        url: `/post/${postId}/vote/unvote/`,
                        type: 'POST',
                        success: function(response) {
                            if (response.redirect) {
                                // Update the URL in the browser to the new location
                                window.location.href = response.redirect;
                            }
                            // Update the display to show the updated vote count
                            setTimeout(delayedLog, 2000);
                            if(response.votes >= 0)
                            {
                                $(upvotePostElements[i]).next().text(response.votes + ' Upvotes ');
                            }else
                            {
                                $(upvotePostElements[i]).next().text(response.votes + ' Downvotes ');
                            }

                            console.log("post unvoted")
                        }
                    });
                }
                else
                {
                    upvotePostElements[i].style = "background-color: #ccc;";
                    downvotePostElements[i].style = "background-color: ''";
                    
                    console.log(upvotePostElements[i].className)
                    
                    var postId = $(this).data('postid');

                    //Make an AJAX request to update the up vote count for the comment
                        $.ajax({
                            url: `/post/${postId}/vote/add/`,
                            type: 'POST',
                            success: function(response) {
                                if (response.redirect) {
                                    // Update the URL in the browser to the new location
                                    window.location.href = response.redirect;
                                }
                                // Update the display to show the updated vote count
                                setTimeout(delayedLog, 2000);
                                if(response.votes >= 0)
                                {
                                    $(upvotePostElements[i]).next().text(response.votes + ' Upvotes ');
                                }else
                                {
                                    $(upvotePostElements[i]).next().text(response.votes + ' Downvotes ');
                                }


                                console.log("voted add")
                            }
                        });

                }

                    // Remove the "active" class from the current element
                    //upvotePostElements[i].className = upvotePostElements[i].className.replace("active", "");
                    upvotePostElements[i].classList.toggle("active");
                
            });
        

            downvotePostElements[i].addEventListener("click", function() 
            {
                //add active class
                //upvotePostElements[i].className += " active";
                downvotePostElements[i].classList.add("active");
                
                if (downvotePostElements[i].style.backgroundColor == "rgb(204, 204, 204)")
                {
                    downvotePostElements[i].style = "background-color: ''" 
                    upvotePostElements[i].style = "background-color: ''" 

                    var postId = $(this).data('postid');

                    //Make an AJAX request to unvote for post
                    $.ajax({
                        url: `/post/${postId}/vote/unvote/`,
                        type: 'POST',
                        success: function(response) {
                            if (response.redirect) {
                                // Update the URL in the browser to the new location
                                window.location.href = response.redirect;
                            }
                            // Update the display to show the updated vote count
                            setTimeout(delayedLog, 2000);
                            if(response.votes >= 0)
                            {
                                $(upvotePostElements[i]).next().text(response.votes + ' Upvotes ');
                            }else
                            {
                                $(upvotePostElements[i]).next().text(response.votes + ' Downvotes ');
                            }

                            console.log("unvoted")
                        }
                    });

                }
                else
                {
                    downvotePostElements[i].style = "background-color: #ccc;";
                    upvotePostElements[i].style = "background-color: ''";
                    
                    console.log(upvotePostElements[i].className)
                    
                    var postId = $(this).data('postid');

                    //Make an AJAX request to update the up vote count for the post
                    $.ajax({
                        url: `/post/${postId}/vote/subtract/`,
                        type: 'POST',
                        success: function(response) {
                            if (response.redirect) {
                                // Update the URL in the browser to the new location
                                window.location.href = response.redirect;
                            }
                            setTimeout(delayedLog, 2000);
                            // Update the display to show the updated vote count

                            if(response.votes >= 0)
                            {
                                $(upvotePostElements[i]).next().text(response.votes + ' Upvotes ');
                            }else
                            {
                                $(upvotePostElements[i]).next().text(response.votes + ' Downvotes ');
                            }


                            console.log("it updates")
                        }
                    });
            }
                // Remove the "active" class from the current element
                //downvotePostElements[i].className = upvotePostElements[i].className.replace("active", "");
                downvotePostElements[i].classList.toggle("active");

            });

        })(i) 

    }


    // reply element functionality 
    
    var upvoteReplyElements = document.getElementsByClassName('fa fa-arrow-up reply');
    var downvoteReplyElements = document.getElementsByClassName('fa fa-arrow-down reply');

    
    for (var i = 0; i < upvoteReplyElements.length; i++) 
    {
        (function(i) 
        {
            upvoteReplyElements[i].addEventListener("click", function() 
            {
                upvoteReplyElements[i].classList.add("active");
                console.log(upvoteReplyElements[i].style.backgroundColor)
                if (upvoteReplyElements[i].style.backgroundColor == "rgb(204, 204, 204)") 
                {
                    // Add the "active" class to the current element
                    upvoteReplyElements[i].style = "background-color: ''" 
                    downvoteReplyElements[i].style = "background-color: ''" 
                   
                   var replyId = $(this).data('replyid');

                    //Make an AJAX request to update the up vote count for the comment
                        $.ajax({
                            url: `/reply/${replyId}/vote/unvote/`,
                            type: 'POST',
                            success: function(response) {
                                if (response.redirect) {
                                    // Update the URL in the browser to the new location
                                    window.location.href = response.redirect;
                                }
                                setTimeout(delayedLog, 2000);
                                // Update the display to show the updated vote count

                                if(response.votes >= 0)
                                {
                                    $(upvoteReplyElements[i]).next().text(response.votes + ' Upvotes ');
                                }else
                                {
                                    $(upvoteReplyElements[i]).next().text(response.votes + ' Downvotes ');
                                }

                                console.log("reply unvoted")
                            }
                        });
          
                }
                else
                {
                    upvoteReplyElements[i].style = "background-color: #ccc;";
                    downvoteReplyElements[i].style = "background-color: ''";

                    var replyId = $(this).data('replyid');

                    $.ajax({
                        url: `/reply/${replyId}/vote/add/`,
                        type: 'POST',
                        success: function(response) {
                            if (response.redirect) {
                                // Update the URL in the browser to the new location
                                window.location.href = response.redirect;
                            }
                            setTimeout(delayedLog, 2000);
                            // Update the display to show the updated vote count

                            if(response.votes >= 0)
                            {
                                $(upvoteReplyElements[i]).next().text(response.votes + ' Upvotes ');
                            }else
                            {
                                $(upvoteReplyElements[i]).next().text(response.votes + ' Downvotes ');
                            }


                            console.log("it updates")
                        }
                    });


                    upvoteReplyElements[i].classList.toggle("active");
                }

            });

            downvoteReplyElements[i].addEventListener("click", function() 
            {
                downvoteReplyElements[i].classList.add("active");
                
                if (downvoteReplyElements[i].style.backgroundColor == "rgb(204, 204, 204)") {
                    //add active class
                    downvoteReplyElements[i].style = "background-color: ''" 
                    upvoteReplyElements[i].style = "background-color: ''" 
                    
                    var replyId = $(this).data('replyid');
                    
                    //Make an AJAX request to update the up vote count for the post
                    $.ajax({
                        url: `/reply/${replyId}/vote/unvote/`,
                        type: 'POST',
                        success: function(response) {
                            if (response.redirect) {
                                // Update the URL in the browser to the new location
                                window.location.href = response.redirect;
                            }
                            setTimeout(delayedLog, 2000);
                            // Update the display to show the updated vote count

                            if(response.votes >= 0)
                            {
                                $(upvoteReplyElements[i]).next().text(response.votes + ' Upvotes ');
                            }else
                            {
                                $(upvoteReplyElements[i]).next().text(response.votes + ' Downvotes ');
                            }


                            console.log("reply unvoted")
                        }
                    });    
                } 
                else
                {
                    downvoteReplyElements[i].style = "background-color: #ccc;";
                    upvoteReplyElements[i].style = "background-color: ''";

                    var replyId = $(this).data('replyid');

                    //Make an AJAX request to update the up vote count for the post
                    $.ajax({
                        url: `/reply/${replyId}/vote/subtract/`,
                        type: 'POST',
                        success: function(response) {
                            if (response.redirect) {
                                // Update the URL in the browser to the new location
                                window.location.href = response.redirect;
                            }
                            setTimeout(delayedLog, 2000);
                            // Update the display to show the updated vote count

                            if(response.votes >= 0)
                            {
                                $(upvoteReplyElements[i]).next().text(response.votes + ' Upvotes ');
                            }else
                            {
                                $(upvoteReplyElements[i]).next().text(response.votes + ' Downvotes ');
                            }

                        }
                    });

                    // Remove the "active" class from the current element
                    downvoteReplyElements[i].classList.toggle("active");
                }

            });

        })(i) 

    }

    //nested reply functionality 
    
    var upvoteNestReplyElements = document.getElementsByClassName('fa fa-arrow-up nestreply');
    var downvoteNestReplyElements = document.getElementsByClassName('fa fa-arrow-down nestreply');

    
    for (var i = 0; i < upvoteNestReplyElements.length; i++) 
    {
        (function(i) 
        {
            upvoteNestReplyElements[i].addEventListener("click", function() 
            {
                upvoteNestReplyElements[i].classList.add("active");
                console.log(upvoteNestReplyElements[i].style.backgroundColor)
                if (upvoteNestReplyElements[i].style.backgroundColor == "rgb(204, 204, 204)") 
                {
                    // Add the "active" class to the current element
                    upvoteNestReplyElements[i].style = "background-color: ''" 
                    downvoteNestReplyElements[i].style = "background-color: ''" 
                   
                   var nestreplyId = $(this).data('nestreply');

                    //Make an AJAX request to update the up vote count for the comment
                        $.ajax({
                            url: `/reply/${nestreplyId}/vote/unvote/`,
                            type: 'POST',
                            success: function(response) {
                                // Update the display to show the updated vote count
                                console.log(response)
                                if (response.redirect) {
                                    // Update the URL in the browser to the new location
                                    window.location.href = response.redirect;
                                }
                                setTimeout(delayedLog, 2000);
                                if(response.votes >= 0)
                                {
                                    $(upvoteNestReplyElements[i]).next().text(response.votes + ' Upvotes ');
                                }else
                                {
                                    $(upvoteNestReplyElements[i]).next().text(response.votes + ' Downvotes ');
                                }

                                console.log("nestedreply unvoted")
                            }
                        });
                        
                }
                else{

                    upvoteNestReplyElements[i].style = "background-color: #ccc;";
                    downvoteNestReplyElements[i].style = "background-color: ''";

                    var nestreplyId = $(this).data('nestreply');

                    $.ajax({
                        url: `/reply/${nestreplyId}/vote/add/`,
                        type: 'POST',
                        success: function(response) {
                            // Update the display to show the updated vote count
                            console.log(response)
                            if (response.redirect) {
                                // Update the URL in the browser to the new location
                                window.location.href = response.redirect;
                            }
                            setTimeout(delayedLog, 2000);
                            if(response.votes >= 0)
                            {
                                $(upvoteNestReplyElements[i]).next().text(response.votes + ' Upvotes ');
                            }else
                            {
                                $(upvoteNestReplyElements[i]).next().text(response.votes + ' Downvotes ');
                            }

                            console.log("it updates")
                        }
                    });

                    upvoteNestReplyElements[i].classList.toggle("active");

                }

            });

            downvoteNestReplyElements[i].addEventListener("click", function() 
            {
                downvoteNestReplyElements[i].classList.add("active");

                if (downvoteNestReplyElements[i].style.backgroundColor == "rgb(204, 204, 204)") {
                    //add active class
                    downvoteNestReplyElements[i].style = "background-color: ''" 
                    upvoteNestReplyElements[i].style = "background-color: ''" 
                    
                    var nestreplyId = $(this).data('nestreply');

                    //Make an AJAX request to update the up vote count for the post
                    $.ajax({
                        url: `/reply/${nestreplyId}/vote/unvote/`,
                        type: 'POST',
                        success: function(response) {
                            // Update the display to show the updated vote count
                            if (response.redirect) {
                                // Update the URL in the browser to the new location
                                window.location.href = response.redirect;
                            }
                            setTimeout(delayedLog, 2000);

                            if(response.votes >= 0)
                            {
                                $(upvoteNestReplyElements[i]).next().text(response.votes + ' Upvotes ');
                            }else
                            {
                                $(upvoteNestReplyElements[i]).next().text(response.votes + ' Downvotes ');
                            }


                            console.log("nestedreply unvoted")
                        }
                    });
                } 

                else
                {
                    downvoteNestReplyElements[i].style = "background-color: #ccc;";
                    upvoteNestReplyElements[i].style = "background-color: ''";

                    var nestreplyId = $(this).data('nestreply');

                    //Make an AJAX request to update the up vote count for the post
                    $.ajax({
                        url: `/reply/${nestreplyId}/vote/subtract/`,
                        type: 'POST',
                        success: function(response) {
                            // Update the display to show the updated vote count
                            if (response.redirect) {
                                // Update the URL in the browser to the new location
                                window.location.href = response.redirect;
                            }
                            setTimeout(delayedLog, 2000);

                            if(response.votes >= 0)
                            {
                                $(upvoteNestReplyElements[i]).next().text(response.votes + ' Upvotes ');
                            }else
                            {
                                $(upvoteNestReplyElements[i]).next().text(response.votes + ' Downvotes ');
                            }


                            console.log("it updates")
                        }
                    });

                    // Remove the "active" class from the current element
                    downvoteNestReplyElements[i].classList.toggle("active");

                }

            });

        })(i) 

    }