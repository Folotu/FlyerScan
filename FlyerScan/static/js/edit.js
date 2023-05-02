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

window.onload = function() {
  if (checkFields()) {
    document.getElementById('cal-button').style.display = 'block';
  }
}

  let activeButton = null;
  let recognition = null;

function speechToText(button, inputID, inputType) {;
  let inputElem = document.getElementById(inputID);
    //console.log(inputElem)

  if (activeButton && (activeButton !== button)){
    recognition.stop();
    activeButton.classList.remove('active');
  }

  recognition = new webkitSpeechRecognition();
  recognition.lang = 'en-US';
  recognition.onresult = function(event) {
    var transcript = event.results[0][0].transcript;
    //console.log(transcript);
    if (inputType === 'date'){
      var transcript = event.results[0][0].transcript;
      transcript = transcript.replace(/\s/g, '')
      transcript = transcript.replace(/dash/gi, "-");
      let date = new Date(transcript);
      let year = date.getFullYear();
      let month = ('0' + (date.getMonth() + 1)).slice(-2);
      let day = ('0' + date.getDate()).slice(-2);
      //console.log('Year:', year, 'Month:', month, 'Day:', day);
      transcript = year +"-" + month + "-" + day;
      //console.log(transcript);
    }
    inputElem.value = transcript;
    //console.log(inputElem)
  };
  
  if (button.classList.contains('active')) {
    recognition.stop();
    button.classList.remove('active');
    activeButton = null;
  } else {
    recognition.start();
    button.classList.add('active');
    activeButton = button;
  }   
}

function deleteFlyer(){
  const url_string = window.location.href;
  const url_array = url_string.split("/");
  const flyer_id = parseInt(url_array[url_array.length - 1]);
  //console.log(flyer_id);
  const home_url = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port;
  var xhttp = new XMLHttpRequest();
  xhttp.open("DELETE", home_url + "/edit_file/" + flyer_id);
  xhttp.onload = function(){
    if(xhttp.status === 200){
      window.location.href = home_url + "/history";
      //alert("successfuly Deleted")
    }
  }
  xhttp.send();
}

function confirmDeletion(){
  if (confirm("Are you sure you want to delete this flyer?")){
    deleteFlyer()
  } else{
    
  }
}

function checkFields() {
  let title = document.getElementById('title');
  let date = document.getElementById('date');
  let start_time = document.getElementById('start_time');
  let location = document.getElementById('location');
  let description = document.getElementById('description');
  
  let button = document.getElementById('cal-button');

  if (title && title.value === ''){
    button.style.display = 'none';
    console.log(title.value)
    return false;
  } 
  if (date && date.value === ''){
    button.style.display = 'none';
    return false;
  }
  if (start_time && start_time.value === ''){
    button.style.display = 'none';
    return false;
  }
  if (location && location.value === ''){
    button.style.display = 'none';
    return false;
  }
  if(description && description.value === ''){
    button.style.display = 'none';
    return false;
  }

  button.style.display = 'block';
  return true;
}

