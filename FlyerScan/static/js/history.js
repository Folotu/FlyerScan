const form = document.querySelector(".search-box");
const input = form.querySelector('input[type="text"]');
const searchBtn = form.querySelector('button[type="submit"]');
const micBtn = form.querySelector(".microphone-btn");

// get SpeechRecognition object for web speech api
console.log("SpeechRecognition" in window);

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

micBtn.addEventListener("click", () => {
  recognition.start();
});

recognition.addEventListener("result", (e) => {
  const transcript = e.results[0][0].transcript;
  input.value = transcript;
});

form.addEventListener("submit", (e) => {
  e.preventDefault();
  searchFunction(input.value);
});

input.addEventListener("keyup", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    searchFunction(input.value);
  }
});

function searchFunction(searchTerm) {
  // your search function here
  console.log(`Searching for ${searchTerm}...`);
}

/* function that grabs scan id and reroutes to edit page with clicked flyer */
var editLinks = document.querySelectorAll('a[data-url]')
for (var i =0; i < editLinks.length; i++ ){
  var editLink = editLinks[i];
  editLink.addEventListener('click', function(event){
    event.preventDefault();
    var flyerURL = this.getAttribute('data-url');
    window.location.href = flyerURL;
  });
}

// display_file.html functions
// time conversion function from 12 hr time to 24 hr time for display
function timeConversion(time){
  //console.log(time);
  var timeArray = time.split(/[: ]/);
  var hours = timeArray[0];
  var minutes = timeArray[1];
  var meridian = timeArray[2];
  if (meridian === "PM" && hours != 12){
    hours = parseInt(hours) + 12;
  } else if (meridian === "AM" && hours == 12){
    hours = 0;
  } 
  
  if (hours){
    hours = hours.toString().padStart(2,'0');
  } else{
    hours ='00';
  }

  if(minutes){
    minutes = minutes.toString().padStart(2,'0');
  } else{
    minutes='00';
  }

  convertedTime = hours + ":" + minutes;
  //console.log(convertedTime);
  return convertedTime;
}
// onload function, grabs start_time/end_time from html page
function displayConvertedTime(){
htmlStartTime = document.getElementById("start_time");
htmlEndTime = document.getElementById("end_time");

htmlStartTime.value = timeConversion(start_time);
htmlEndTime.value = timeConversion(end_time);
}
