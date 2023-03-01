// Get a reference to the button and the container for the text field

// const button = document.getElementById('my-button');
// const textFieldContainer = document.getElementById('text-field-container');



// // Add an event listener that listens for a click event on the button
// button.addEventListener('click', function() {
//     // Check if the container already contains a text field
//     if (textFieldContainer.children.length > 0) {
//         // If the container already contains a text field, then return without adding another one
//         return;
//     }

//     // Create the text field
//     const textField = document.createElement('input');
//     textField.type = 'text';

//     // Add the text field to the container
//     textFieldContainer.appendChild(textField);

//     // Show the container
//     textFieldContainer.style.display = 'block';
// });


// const button = document.getElementsByClassName('btn btn-primary comm');

// const textFieldContainer = document.getElementsByClassName('btn btn-primary commfield');

// console.log(button)
// for (i = 0; i < button.length; i++) {
// // Add an event listener that listens for a click event on the button
// button.addEventListener('click', 
// function() 
// {
//     button[i].addEventListener
//     ('click', function()
//         {
//             console.log(this)
//     // Check if the container already contains a text field
//     // if (textFieldContainer.children.length > 0) {
//     //     // If the container already contains a text field, then return without adding another one
//     //     return;
//     // }

//     // Create the text field
//     // const textField = document.createElement('input');
//     // textField.type = 'text';

//     // Add the text field to the container
//     // textFieldContainer.appendChild(textField);



//     // Show the container
//     textFieldContainer.style.display = 'block';
//         }
//     )
// })};


//  const button = document.getElementById('comment-button');

//  const textFieldContainer = document.getElementById('comment-text');



// // Add an event listener that listens for a click event on the button
// button.addEventListener('click', function() {
//     // Check if the container already contains a text field
//     if (textFieldContainer.children.length > 0) {
//         // If the container already contains a text field, then return without adding another one
//         return;
//     }

//     // Create the text field
//     const textField = document.createElement('input');
//     textField.type = 'text';

//     // Add the text field to the container
//     textFieldContainer.appendChild(textField);

//     // Show the container
//     textFieldContainer.style.display = 'block';
// });

$("#comment-button").click(function() 
{
   
    $("#comDiv").toggle();

});


// Get elements by class name
var ReplyElements = document.getElementsByClassName('btn btn-primary reply');
var divv = document.getElementsByClassName('repDiv');
console.log(ReplyElements)
// console.log(divve)

// Loop through the elements
for (var i = 0; i < ReplyElements.length; i++) 
{
    (function(i) 
    {
        ReplyElements[i].addEventListener("click", function() 
        {
   
            if (divv[i].className.indexOf("active") > -1) {
                // Remove the "active" class from the current element
                divv[i].className = divv[i].className.replace("active", "");
                divv[i].style.display = 'none';
              } 
              else 
              {
                // Add the "active" class to the current element
                divv[i].className += " active";
                divv[i].style.display = 'block';
              }

        });

    })(i)   

}


// Get elements by class name
var nestReplyElements = document.getElementsByClassName('btn btn-primary nestreply');
var nestdivv = document.getElementsByClassName('NestrepDiv');
console.log(nestReplyElements)


// Loop through the elements
for (var k = 0; k < nestReplyElements.length; k++) 
{
    (function(k) 
    {
        nestReplyElements[k].addEventListener("click", function() 
        {
   
            if (nestdivv[k].className.indexOf("active") > -1) {
                // Remove the "active" class from the current element
                nestdivv[k].className = nestdivv[k].className.replace("active", "");
                nestdivv[k].style.display = 'none';
              } 
              else 
              {
                // Add the "active" class to the current element
                nestdivv[k].className += " active";
                nestdivv[k].style.display = 'block';
              }

        });

    })(k)   

}

