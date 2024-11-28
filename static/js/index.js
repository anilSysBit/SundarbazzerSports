
let globalState = {
  value:null,
}

function updateGlobalState(newValue,name){
  console.log('updating')
  globalState.value = newValue

  console.log(globalState)  
}





const selectedData = [];

function removeSelection(){
  selectedData.splice(0, selectedData.length);
  document.querySelectorAll('.select-checkbox').forEach((checkbox) => {
    const row = checkbox.parentElement.parentElement;
    row.classList.remove('selected');
    checkbox.checked = false
    // Remove deselected data
    const id = parseInt(checkbox.value);
    
});
}
function toggleSelection(row, checkbox) {
  const id = parseInt(checkbox.value);
  if (checkbox.checked) {
      row.classList.add('selected');

      // Dynamically create row data with variable names based on the <td> id
      const rowData = {
        id:id,
      };
      Array.from(row.cells).forEach(cell => {
          if (cell.id) { // Use the `id` of the cell if it exists
              rowData[cell.id] = cell.innerText;
          }
      });

      selectedData.push(rowData);
  } else {
      row.classList.remove('selected');

      // Remove deselected data
      const id = parseInt(checkbox.value);
      const index = selectedData.findIndex(data => data.id === id);
      if (index > -1) selectedData.splice(index, 1);
  }
}

// // Function to handle "Select All" checkbox
// document.getElementById('selectAll').addEventListener('change', function () {
//     const isChecked = this.checked;
//     const checkboxes = document.querySelectorAll('.select-checkbox');

//     checkboxes.forEach((checkbox) => {
//         checkbox.checked = isChecked;
//         const row = checkbox.parentElement.parentElement;
//         toggleSelection(row, checkbox);
//     });
// });

// Event listener for individual row checkboxes
document.querySelectorAll('.select-checkbox').forEach((checkbox) => {
    checkbox.addEventListener('click', function (event) {
      // console.log('event',event.target.value)
        const row = checkbox.parentElement.parentElement;
        toggleSelection(row, checkbox);

    });
});

document.querySelectorAll('.select-checkbox-row').forEach((row) => {
  row.addEventListener('click', function (event) {
      // Get the checkbox inside the clicked row
      const checkbox = row.querySelector('.select-checkbox');

      // If the click is on the checkbox itself, skip toggling to avoid double-trigger
      if (event.target === checkbox) return;

      // Trigger the checkbox click
      checkbox.click();
  });
});

// Function to handle selected data submission
function sendSelectedData() {
    console.log("Selected Data for Request:", selectedData);
}



// for sidebar toggle
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  sidebar.classList.toggle('collapsed');
}


function previewImage(event, previewId) {
  var reader = new FileReader();
  reader.onload = function(){
      var output = document.getElementById(previewId);
      output.src = reader.result;
      output.style.display = 'block';
  };
  reader.readAsDataURL(event.target.files[0]);
}


// function for snack bar

function showSnackBar() {
  const snackBar = document.getElementById("snackbar");
  snackBar.classList.add("show");

  // Hide the snackbar after 3 seconds
  setTimeout(() => {
    snackBar.classList.remove("show");
  }, 8000);
}



function closeSnackBar() {
  const snackBar = document.getElementById("snackbar");
  snackBar.classList.remove("show");
}



// sidebar

document.addEventListener('DOMContentLoaded', function () {
  let dropdown = document.getElementById('dropdown-content');
  var dropdownbox = document.getElementById('team-dropdown');
  if (dropdown) {
    // Create the icon span
    let icon = document.createElement('span');
    icon.className = 'material-symbols-outlined dropdown-arrow';
    icon.id = 'team-dropdown-toggle'
    icon.textContent = 'keyboard_arrow_down'; // The icon text
    
    dropdown.onclick =()=>{
      dropdownbox.classList.toggle('show');

      // Toggle the arrow direction
      if (dropdownbox.classList.contains('show')) {
        icon.textContent = 'keyboard_arrow_up'; // Change to "up" arrow when open
      } else {
        icon.textContent = 'keyboard_arrow_down'; // Change to "down" arrow when closed
}
    }
    // Append the icon to the link
    let link = dropdown.querySelector('a');
    link.appendChild(icon);
  }
});




function startCountdown(id) {
  const timerElement = document.getElementById(id);
  const targetDate = new Date(timerElement.textContent)

  console.log('targetDate',timerElement.textContent)

  function updateTimer() {
    const now = new Date().getTime();
    const timeDifference = targetDate.getTime() - now;

    if (timeDifference <= 0) {
      clearInterval(interval);
      timerElement.textContent = "Countdown Completed!";
      return;
    }

    const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);


    timerElement.innerHTML = `
                      <p class="time_box">${days} D</p>
                      <p class="time_box">${hours} H</p>
                      <p class="time_box">${minutes} M</p>
                      <p class="time_box">${seconds} S</p>

    `;
  }

  const interval = setInterval(updateTimer, 1000);
  updateTimer(); // Initial call to display immediately
}


startCountdown("timer");


startCountdown("timer2")


// startCountdown1("timer3")

// for custom time

function handleFetchTestData(){
  const button = document.getElementById('fetchButton');
  button.classList.add('loading');
  const spinner = document.createElement('span')
  spinner.classList.add('spinner')



  // Simulate an API call
  fetch('https://jsonplaceholder.typicode.com/todos/1') // Replace with your API URL
    .then(response => response.json())
    .then(data => {
      console.log(data); // Log the response data
      alert("Data fetched successfully!");
    })
    .catch(error => {
      console.error('Error:', error);
      alert("Failed to fetch data.");
    })
    .finally(() => {
      button.classList.remove('loading');
    });
}