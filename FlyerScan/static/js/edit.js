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

  let recognition;

  function speechToText(button, inputID) {;
    let inputElem = document.getElementById(inputID);
    console.log(inputElem)
      recognition = new webkitSpeechRecognition();
      recognition.lang = 'en-US';
      recognition.onresult = function(event) {
        inputElem.value = event.results[0][0].transcript;
        console.log(inputElem)
      };
    
    if (button.classList.contains('active')) {
      recognition.stop();
      button.classList.remove('active');
    } else {
      recognition.start();
      button.classList.add('active');
    }
  }