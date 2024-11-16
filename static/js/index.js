
let globalState = {
  value:null,
}

function updateGlobalState(newValue,name){
  console.log('updating')
  globalState.value = newValue

  console.log(globalState)
}





const selectedData = [];

// Function to toggle row selection
function toggleSelection(row, checkbox) {
    if (checkbox.checked) {
        row.classList.add('selected');
        // Collect data from row
        const rowData = {
            id:parseInt(checkbox.value),
            productName: row.cells[1].innerText,
            price: row.cells[2].innerText,
            quantity: row.cells[3].innerText
        };
        selectedData.push(rowData);
    } else {
        row.classList.remove('selected');
        // Remove deselected data
        const productName = row.cells[1].innerText;
        const index = selectedData.findIndex(data => data.productName === productName);
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
      console.log('event',event.target.value)
        const row = checkbox.parentElement.parentElement;
        toggleSelection(row, checkbox);

        // Update "Select All" checkbox state based on individual selections
        // const allChecked = [...document.querySelectorAll('.select-checkbox')].every(cb => cb.checked);
        // document.getElementById('selectAll').checked = allChecked;
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
    // Here you could send selectedData via a fetch or AJAX request
    // e.g., fetch('/your-endpoint', { method: 'POST', body: JSON.stringify(selectedData) })
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

