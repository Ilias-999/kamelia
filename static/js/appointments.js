$(document).on('submit','#appointments',function(e){

        e.preventDefault() // this prevent the page from reloading

        $.ajax({
            type:'POST',
            url: "/appointments_form_view/",
            data:{
                date:$('#selected_date').val(),
                service_id:$('#service').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(data){
                // console.log(data['appointment_times_and_timing'])
                goToButtons()
                selected_service_id = parseInt(data['selected_service_id'])
                // console.log('selcted service id', selected_service_id)
                chosenDate = $('#selected_date').val()
                showBottons(data['appointment_times_and_timing'], data)
            },
        })

    })
let nonAvailableAppointments = []
let AvailableAppointments = []
let selected_service_id = 0
function showBottons(array, data){
    nonAvailableAppointments = []
    AvailableAppointments = []
    for(let element of array){
        // console.log(element['appointment_time'])
        nonAvailableAppointments.push(element['appointment_time'])
        add_corresponding_timing_to_time(element['appointment_time'], element['appointment_timing'])
        considering_service_timing(element['appointment_time'], data['service_timing'])
    }
    AvailableAppointments = generateAvailableTimes(nonAvailableAppointments)
    createAppointmentButtons(AvailableAppointments)

    // console.log('nonAvailableAppointments',nonAvailableAppointments)
    // console.log('AvailableAppointments',AvailableAppointments)
}

function createAppointmentButtons(array) {
    const chooseAppointmentsDiv = document.getElementById('choose-appointments');
    chooseAppointmentsDiv.innerHTML = ""
    for (const time of array) {
        const button = document.createElement('button');
        button.textContent = time;
        button.setAttribute('data-time', time);
        button.addEventListener('click', goToFormConfirmation);
        chooseAppointmentsDiv.appendChild(button);
    }
}

function add_corresponding_timing_to_time(time, timing){
  let totalMinutes = string_to_minuts(time)
  const steps = (timing/30)
  for (i=1; i<steps; i++){
    totalMinutes += 30
    nonAvailableAppointments.push(minuts_to_string(totalMinutes))
  }
}

function string_to_minuts(time){
    const [hours, minutes] = time.split(':');
    return parseInt(hours) * 60 + parseInt(minutes);
}

function considering_service_timing(time, service_timing){
  const [hours, minutes] = time.split(':')
  let totalMinutes = parseInt(hours) * 60 + parseInt(minutes);
  const steps = (service_timing/30)
  for (i=1; i<steps; i++){
    totalMinutes -= 30
    nonAvailableAppointments.push(minuts_to_string(totalMinutes))
  }
}
function minuts_to_string(minutes){
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  const formattedHours = ('0' + hours).slice(-2);
  const formattedMinutes = ('0' + remainingMinutes).slice(-2);
  return formattedHours + ':' + formattedMinutes;
}
function generateAvailableTimes(unavailableTimes) {
    const possibleTimes = [];
    for (let hour = 9; hour < 19; hour++) {
        for (let minute = 0; minute < 60; minute += 30) {
            const formattedHour = ('0' + hour).slice(-2);
            const formattedMinute = ('0' + minute).slice(-2);
            possibleTimes.push(formattedHour + ':' + formattedMinute);
        }
    }
    const availableTimes = possibleTimes.filter(time => !unavailableTimes.includes(time));
    return availableTimes;
}

$(document).on('submit','#client',function(e){
        e.preventDefault() // this prevent the page from reloading
        $.ajax({
            type:'POST',
            url: "/create_appointment_client/",
            data:{
                name:$('#name').val(),
                email:$('#email').val(),
                telephone:$('#telephone').val(),
                clickedTime: clickedTime,
                chosenDate: chosenDate,
                service_id: selected_service_id,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(data) {
            // Handle success response
             window.location.href = "/thank_you_page_view/";
            },
            error: function(error) {
                // Handle error response
            }
        })
    })

let chooseAppointmentsDiv = document.getElementById("choose-appointments");
let clientsForm = document.getElementById("client")
let displayTime = document.getElementById("display-time")
let chosenDate = ""

let clickedTime = ""
function goToFormConfirmation() {
    clickedTime = this.getAttribute("data-time");
    // console.log("Clicked time:", clickedTime);
    chooseAppointmentsDiv.classList.add("hide")
    clientsForm.classList.remove("hide")
    displayTime.textContent = clickedTime
}

function goToButtons() {
    chooseAppointmentsDiv.classList.remove("hide")
    clientsForm.classList.add("hide")
    displayTime.textContent = ''
}
