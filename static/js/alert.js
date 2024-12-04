class AlertBox {
    constructor (containerId){
        
        this.container = document.getElementById(containerId)
        this.containerId = containerId;

        if(!this.container) return;
        console.log('container id',this.containerId)
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


class SnackBar{
      constructor() {
        // Create a container for all snackbars if it doesn't exist
        if (!document.querySelector('.snackbar-container')) {
            const container = document.createElement('div');
            container.classList.add('snackbar-container');
            document.body.appendChild(container);
        }
        this.container = document.querySelector('.snackbar-container');
    }

    showSnack(message, type) {
      // Create a new snackbar element
      const snackbar = document.createElement('div');
      snackbar.classList.add('snackbar');
      if (type) {
          snackbar.classList.add(type); // Add type-specific class (e.g., success, error)
      }
      snackbar.textContent = message;

      // Append snackbar to the container
      this.container.appendChild(snackbar);

      // Trigger fade-in effect
      setTimeout(() => {
          snackbar.classList.add('show');
      }, 10);

      // Automatically hide the snackbar after 3 seconds
      setTimeout(() => {
          this.hide(snackbar);
      }, 3000);
  }
      hide(snackbar) {
        // snackbar.classList.remove('show');
        snackbar.classList.add('hide');
        // snackbar.style.display = 'none'

        setTimeout(()=>{
          snackbar.remove()
        },500)
    }
}

const snack = new SnackBar();


function showSnackBar(message='Testing the javascript snackbar',type='success'){


    snack.showSnack(message,type)
    setTimeout(()=>{
        snack.hide()
    },4000)
}




console.log('Hello')
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

const alertBoxTeamActive = new AlertBox('alert-box-active')


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


// handling alert box of delete player




const alertBoxDeletePlayer = new AlertBox('alert-box-delete-player')

const deletePlayerSubmit =async(event)=>{
    event.preventDefault()
    const form = document.getElementById('alert-box-delete-player')
    const formData = new FormData(form)
    const data = Object.fromEntries(formData.entries());

    const response = await fetch(`/delete-player/${globalState.value}/`,{
        method:"post",
        headers:{
            'X-CSRFToken':data.csrfmiddlewaretoken
        }
    })

    window.location.reload();

    console.log(response)
}

function handleDeletePlayer(id,message,note){
    updateGlobalState(id)
    alertBoxDeletePlayer.showAlert(message,note)
}


// function that changes the status of the player

const handleChangePlayerStatus =async(event)=>{
    event.preventDefault();

    const form = document.getElementById('alert-box-active')
    const formData = new FormData(form)
  
    const data = Object.fromEntries(formData.entries());
  
    try{
      const response = await fetch(`/change-player-status/${globalState.value}/`,{
        method:"post",
        headers:{
          'X-CSRFToken':data.csrfmiddlewaretoken
        }
      })
      window.location.reload()
    //   console.log('response',await response.json())
    }catch(error){
      console.log('error',error)
    }
}




const handleDeleteMatch =async(event)=>{
  event.preventDefault();

  const form = document.getElementById('alert-box-delete-team')
  const formData = new FormData(form)

  const data = Object.fromEntries(formData.entries());

  try{
    const response = await fetch(`/delete-match/${globalState.value}/`,{
      method:"post",
      headers:{
        'X-CSRFToken':data.csrfmiddlewaretoken
      }
    })
    // console.log('response',await response.json())
    window.location.reload()

    
  }catch(error){
    console.log('error',error)
  }
}

const getCustomCurrentTime =()=>{
  const now = new Date();
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  return `${hours}:${minutes}:${seconds}`
}


const handleOpenGoalAlert =()=>{
  const selected = selectedData[0];
  // console.log('selecte dtaa',selectedData)
  if(selectedData.length < 1){
    showSnackBar(message="You should choose player before adding goal",type='error')
    return;
  }else if(selectedData.length > 1){
    showSnackBar(message="Two players cannot be selected at one to add a goal",type='error')
    return;
  }
  const alertbox = document.getElementById('goal-alert-box');
  alertbox.reset()

  const timeInput = document.getElementById('custom-time')

  // alertbox.remove()

  const timeValue = getCustomCurrentTime()
  timeInput.value = timeValue;

  
  const note = document.getElementById('note')
  const header = document.getElementById('header')
  const sub_header = document.getElementById('sub-header')
  const jersey_no = document.getElementById('jersey-no')
  const player_name = document.getElementById('player-name')
  const player_id = document.getElementById('player')

  player_id.value = selected.id


  header.textContent = `${selected.name} (${selected.team_name})`
  // sub_header.textContent = `${selected.team_name}`

  jersey_no.textContent = `${selected.jersey}`
  player_name.textContent = `${selected.team_name}`

  alertbox.classList.add('show')
}


const fetchPlayerData =async(id)=>{

  const response = await fetch(`/player-data-api/${id}/`,{
    method:"get"
  })

  return response.json()

}

const handleOpenFoulAlert =async()=>{
  const selected = selectedData[0];



  console.log('selecte dtaa',selectedData)
  if(selectedData.length < 1){
    showSnackBar(message="You should choose player before adding foul",type='error')
    return;
  }else if(selectedData.length > 1){
    showSnackBar(message="Two players cannot be selected at one to add a foul",type='error')
    return;
  }

  const responseData = await fetchPlayerData(selected.id)

  const alertbox = document.getElementById('foul-alert-box');
  alertbox.reset()

  const timeInput = document.getElementById('custom-time-foul')

  // alertbox.remove()

  const timeValue = getCustomCurrentTime()
  timeInput.value = timeValue;

  
  // const note = document.getElementById('note')
  const header = document.getElementById('header-foul')
  // const sub_header = document.getElementById('sub-header')
  const jersey_no = document.getElementById(`jersey-nofoul`)
  const player_name = document.getElementById('player-namefoul')
  const player_id = document.getElementById('player-foul')
  

  player_id.value = responseData.id

  header.textContent = `${responseData.name} (${responseData.team_name})`
  // sub_header.textContent = `${selected.team_name}`


  jersey_no.textContent = `${responseData.jersey_no}`
  player_name.textContent = `${responseData.name}`

  alertbox.classList.add('show')
}




const handleCloseAlerts =()=>{
  const boxes = document.querySelectorAll('.dialog-overlay')
  const alertbox = document.getElementById('goal-alert-box');
  

  // alertbox.remove()
  boxes.forEach((item,index)=>{
    item.classList.remove('show')
  })
}



// match schedular

const handleOpenMatchSchedular=()=>{
  const alertbox = document.getElementById('match-schedule-alert-box')
  alertbox.classList.add('show')
}