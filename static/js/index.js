
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
    alertboxDeleteTeam.showAlert(message,note,()=>handleDeleteTeam(id))
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