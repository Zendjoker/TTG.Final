document.addEventListener('DOMContentLoaded', function() {
    var tabs = document.querySelectorAll('ul.tabs li');
    var nextTabButtons = document.querySelectorAll('.next-tab-btn');
    var prevTabButtons = document.querySelectorAll('.back-tab-btn');
  
    // Function to switch tabs
    function switchTab(tabId) {
        tabs.forEach(function(item) {
            item.classList.remove('current');
        });
        var tabContents = document.querySelectorAll('.tab-content');
        tabContents.forEach(function(content) {
            content.classList.remove('current');
        });
  
        var selectedTab = document.querySelector('ul.tabs li[data-tab="' + tabId + '"]');
        selectedTab.classList.add('current');
        document.getElementById(tabId).classList.add('current');
    }
  
    // Event listener for tab clicks
    tabs.forEach(function(tab) {
        tab.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default action (switching tabs)
        });
    });
  
    // Event listener for next tab buttons
    nextTabButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var currentTab = document.querySelector('ul.tabs li.current');
            var currentIndex = Array.from(tabs).indexOf(currentTab);
            var nextIndex = (currentIndex + 1) % tabs.length;
            var nextTabId = tabs[nextIndex].getAttribute('data-tab');
            switchTab(nextTabId);
        });
    });
  
    // Event listener for previous tab buttons
    prevTabButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var currentTab = document.querySelector('ul.tabs li.current');
            var currentIndex = Array.from(tabs).indexOf(currentTab);
            var prevIndex = (currentIndex - 1 + tabs.length) % tabs.length;
            var prevTabId = tabs[prevIndex].getAttribute('data-tab');
            switchTab(prevTabId);
        });
    });
  });
  

form = document.querySelector(".sessionForm")
submitButton = document.querySelector(".DoneSubmit")

submitButton.addEventListener("click", function (event) {
    event.preventDefault();
    formData = new FormData(form);

    let isValid = true;

    // Check if any required fields are empty
    for (const input of form.querySelectorAll("input[required]")) {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add("error");
        } else {
            input.classList.remove("error");
        }
    }

    // Check for empty values in formData
    for (const entry of formData.entries()) {
        if (entry[1].trim() === '') {
            isValid = false;
            break; // Exit the loop if any empty value found
        }
    }

    if (!isValid) {
        popupMessage.classList.remove('success'); // Ensure class is correctly managed
        popupSpan.textContent = "Please fill in all fields!";
        popupMessage.classList.add('popup-show');
                // Close button functionality
                document.getElementById('popUpCloseButton').addEventListener('click', function() {
                    popupMessage.classList.remove('popup-show');
                });
        return;
    }

    $.ajax({
        type: 'POST',
        url: '/schedulePrivateSession/',
        data: formData,
        processData: false,
        contentType: false,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
        },
        success: function(response) {
            console.log(response);
            replaceScheduleBodyWithDoneContent();
        },
        error: function(error) {
            console.error('Error filtering products:', error);
        }
    });

});

// Function First Name is emtpy
function EmptyFirstName(){
    var input = document.getElementById("id_first_name");
    input.style.border = "1px solid #ff3f3f";
    input.style.backgroundColor = "#2020201c";
}
function EmptyLastName(){
    var input = document.getElementById("id_last_name");
    input.style.border = "1px solid #ff3f3f";
    input.style.backgroundColor = "#2020201c";
}
function EmptyEmail(){
    var input = document.getElementById("id_email");
    input.style.border = "1px solid #ff3f3f";
    input.style.backgroundColor = "#2020201c";
}
function EmptyPhone(){
    var input = document.getElementById("id_phone_number");
    input.style.border = "1px solid #ff3f3f";
    input.style.backgroundColor = "#2020201c";
}

// Function to get the value of a cookie

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  // Sample unavailable days (you can replace this with your logic)
// Sample unavailable days (you can replace this with your logic)
const unavailableDays = [2, 5, 8, 12, 15];

const calendar = document.querySelector('.calendar');
const selectedDateInput = document.getElementById('selectedDateInput');
const selectedDateForm = document.getElementById('selectedDateForm');

// // Generate calendar days
// function generateCalendar() {
//     const daysInMonth = 31; // You can adjust this based on the actual month
//     for (let i = 1; i <= daysInMonth; i++) {
//         const dayElement = document.createElement('div');
//         dayElement.textContent = i;
//         dayElement.classList.add('calendar-day');

//         if (unavailableDays.includes(i)) {
//             dayElement.classList.add('unavailable');
//         } else {
//             // Add event listener only if the day is available
//             dayElement.addEventListener('click', function() {
//                 if (!this.classList.contains('unavailable')) {
//                     // Clear previously selected day
//                     const selectedDay = document.querySelector('.calendar-day.selected');
//                     if (selectedDay) {
//                         selectedDay.classList.remove('selected');
//                     }

//                     // Mark current day as selected
//                     this.classList.add('selected');
//                     selectedDateInput.value = i;
//                 }
//             });
//         }

//         calendar.appendChild(dayElement);
//     }
// }

// Call the function to generate the calendar
// generateCalendar();


function replaceScheduleBodyWithDoneContent() {
    const scheduleBody = document.querySelector('.schedule-body');
    if (scheduleBody) {
        // Clear existing content
        scheduleBody.innerHTML = '';

        // Create the new content
        const doneBody = document.createElement('div');
        doneBody.classList.add('schedule-body', 'done-body');

        const scheduleBodyLeft = document.createElement('div');
        scheduleBodyLeft.classList.add('schedule-body-left');
        const doneImg = document.createElement('img');
        doneImg.src = "/static/assets/done.svg";
        doneImg.width = "340px";
        doneImg.height = "340px";
        doneImg.alt = "Schedule Done";
        doneImg.classList.add('jello-horizontal');
        scheduleBodyLeft.appendChild(doneImg);

        const scheduleBodyRight = document.createElement('div');
        scheduleBodyRight.classList.add('schedule-body-right');
        const doneContainer = document.createElement('div');
        doneContainer.classList.add('done-container');
        const span1 = document.createElement('span');
        span1.textContent = "Thank you for expressing interest in a private session";
        const span2 = document.createElement('span');
        span2.textContent = "We're excited to connect with you! Expect a follow-up from us in 3 to 5 business days. Thanks for reaching out!";
        const goBackLink = document.createElement('a');
        goBackLink.href = "#";
        goBackLink.classList.add('next-tab-btn');
        goBackLink.textContent = "Go Back";
        doneContainer.appendChild(span1);
        doneContainer.appendChild(span2);
        doneContainer.appendChild(goBackLink);
        scheduleBodyRight.appendChild(doneContainer);

        doneBody.appendChild(scheduleBodyLeft);
        doneBody.appendChild(scheduleBodyRight);

        // Replace the schedule-body content with the new content
        scheduleBody.appendChild(doneBody);

        // Prevent default action and handle go back functionality
        goBackLink.addEventListener('click', function(event) {
            event.preventDefault();
            // Call a function to handle what happens when "Go Back" is clicked
            handleGoBack();
        });
    }
}

function handleGoBack() {
    // Example function to revert to the previous view or perform another action
    const scheduleBody = document.querySelector('.schedule-body');
    if (scheduleBody) {
        // Code to restore the previous content or switch views
        // This needs to be adapted based on how you manage views/states in your application
    }
}




