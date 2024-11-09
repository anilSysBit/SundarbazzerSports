
let globalState = {
  value:null,
}

function updateGlobalState(newValue,name){
  console.log('updating')
  globalState.value = newValue

  console.log(globalState)
}


class AlertBox {
    constructor (containerId){

        this.container = document.getElementById(containerId)
        this.containerId = containerId;
        // this.buttonBox = document.getElementById('button-box')
        // this.btnYes.addEventListener('click', () => this.handleYes());
        // this.btnNo.addEventListener('click', () => this.handleNo());

            // Create the dialog content
        const dialog = document.createElement('div');
        dialog.classList.add('size_manager', 'dialog');
        
        // Create the icon box
        const iconBox = document.createElement('div');
        iconBox.classList.add('icon_box');
        const icon = document.createElement('span');
        icon.classList.add('icon', 'material-symbols-outlined');
        icon.textContent = 'info';
        iconBox.appendChild(icon);
        
        // Create the detail box
        this.detailBox = document.createElement('div');
        this.detailBox.classList.add('detail_box');
        this.detailBox.id = 'alert-details';


        // Create the button box
        const buttonBox = document.createElement('div');
        buttonBox.classList.add('button_box');
        const btnYes = document.createElement('button');
        btnYes.classList.add('global_btn');
        btnYes.id = 'btn-yes';
        btnYes.type = 'submit'
        btnYes.textContent = 'Yes';
        const btnNo = document.createElement('button');
        btnNo.classList.add('global_btn', 'outline');
        btnNo.id = 'btn-no';
        btnNo.textContent = 'NO';
        btnNo.type = 'button'

         // Append buttons to the button box
        buttonBox.appendChild(btnYes);
        buttonBox.appendChild(btnNo);
        
        dialog.appendChild(iconBox)
        dialog.appendChild(this.detailBox)
        dialog.appendChild(buttonBox)
        
        this.container.appendChild(dialog)
        

        // Bind event listeners
        // btnYes.addEventListener('click', () => this.handleYes());
        btnNo.addEventListener('click', () => this.handleNo());
    }


    showAlert(message,note,onYesCallback,onNoCallback){

        this.container.classList.add('dialog-overlay','show')
        
        this.detailBox.innerHTML = `<p class="alert-header">${message}</p>`

        if (note) {
          this.detailBox.innerHTML += `<p class="note">${note}</p>`;
        }


        this.onYesCallback = onYesCallback;
        this.onNoCallback = onNoCallback;

    }

     // Hide the alert box
  hideAlert() {
    this.container.classList.remove('show')
  }


     // Handle "Yes" button click
  // handleYes() {
  //   if (this.onYesCallback) {
  //     this.onYesCallback();  // Call the provided callback
  //   }
  //   this.hideAlert();  // Hide the alert box
  // }


  handleNo() {
    if(this.onNoCallback){
      this.onNoCallback();
    }
    this.hideAlert();  // Simply hide the alert box
  }
}




const alertboxDeleteTeam = new AlertBox('alert-box-delete-team')


const handleDeleteTeam =async(event)=>{
  event.preventDefault()
  const form = document.getElementById('team-form')
  const formData = new FormData(form)

  const data = Object.fromEntries(formData.entries());

  console.log(data)
  try{
    const response = await fetch(`/team-delete/${globalState.value}/`,{
      method:"post",
      headers:{
        'X-CSRFToken':data.csrfmiddlewaretoken
      }
    })
    window.location.reload()
    console.log(response)
  }catch(error){
    console.log(error)
  }
}

function handleOpenAlert (id,message,note) {
    updateGlobalState(id)
    alertboxDeleteTeam.showAlert(message,note)
}




// Team table checkbox

const alertBoxTeamActive = new AlertBox('alert-box-team-active')

const handleSubmitVerifyTeam =async(event)=>{
  event.preventDefault();

  const form = document.getElementById('team-form')
  const formData = new FormData(form)

  const data = Object.fromEntries(formData.entries());

  console.log(data)
  try{
    const response = await fetch(`/change-team-status/${globalState.value}/`,{
      method:"post",
      headers:{
        'X-CSRFToken':data.csrfmiddlewaretoken
      }
    })
    window.location.reload()
    console.log('response',await response.json())
  }catch(error){
    console.log('error',error)
  }
}


function handleChangeTeamCheckbox(id,teamName){
    updateGlobalState(id)
    const checkbox = document.getElementById(`team_checkbox${id}`);
    let text = `Do you want to ${checkbox.checked ? 'activate' : 'deactivate'} this team ${teamName}?`
    
    alertBoxTeamActive.showAlert(text,'',null,()=>{
      console.log('clicked no')
      if(checkbox.checked){
        checkbox.checked = false
      }else{
        checkbox.checked = true

      }
    })
    
}


const selectedData = [];

// Function to toggle row selection
function toggleSelection(row, checkbox) {
    if (checkbox.checked) {
        row.classList.add('selected');
        // Collect data from row
        const rowData = {
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

// Function to handle "Select All" checkbox
document.getElementById('selectAll').addEventListener('change', function () {
    const isChecked = this.checked;
    const checkboxes = document.querySelectorAll('.select-checkbox');

    checkboxes.forEach((checkbox) => {
        checkbox.checked = isChecked;
        const row = checkbox.parentElement.parentElement;
        toggleSelection(row, checkbox);
    });
});

// Event listener for individual row checkboxes
document.querySelectorAll('.select-checkbox').forEach((checkbox) => {
    checkbox.addEventListener('change', function () {
        const row = checkbox.parentElement.parentElement;
        toggleSelection(row, checkbox);

        // Update "Select All" checkbox state based on individual selections
        const allChecked = [...document.querySelectorAll('.select-checkbox')].every(cb => cb.checked);
        document.getElementById('selectAll').checked = allChecked;
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