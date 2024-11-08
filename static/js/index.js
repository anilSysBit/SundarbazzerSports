

class AlertBox {
    constructor (containerId){

        this.container = document.getElementById(containerId)
        this.containerId = containerId;
    }


    showAlert(message,note,onYesCallback){

        this.container.classList.add('dialog-overlay','show')
        this.container.innerHTML = `
    <div class="size_manager dialog" id="dialog">

        <div class="icon_box">
        <span class="icon material-symbols-outlined">
          info
          </span>

        </div>

        <div class="detail_box">
            <p class="alert-header">${message}</p>
            ${note && `<p class="note">${note}</p>`}
        </div>

        <div class="button_box">
        <button class="global_btn" id="btn-yes" type="submit">Yes</button>
        <button class="global_btn outline" id="btn-no" onclick="handleHide('${this.containerId}')" type="button">NO</button>
      </div>
      </div>
        `
        // this.dialog.append(detail)

        this.onYesCallback = onYesCallback;

    }

     // Hide the alert box
  hideAlert() {
    this.container.classList.remove('show')
  }


     // Handle "Yes" button click
  handleYes() {
    if (this.onYesCallback) {
      this.onYesCallback();  // Call the provided callback
    }
    this.hideAlert();  // Hide the alert box
  }


  handleNo() {
    this.hideAlert();  // Simply hide the alert box
  }
}




const alertboxDeleteTeam = new AlertBox('alert-box-delete-team')

function handleOpenAlert (message,note) {
    alertboxDeleteTeam.showAlert(message,note,()=>{
        console.log('Box Deleted')
    })
}


function handleHide(id){
    const element = document.getElementById(id)
    element.classList.remove('show')
}


// Team table checkbox

const alertBoxTeamActive = new AlertBox('alert-box-team-active')

function handleChangeTeamCheckbox(id,teamName){
    const checkbox = document.getElementById(id);
    console.log('checkedd',checkbox.checked)
    let text = `Do you want to ${checkbox.checked ? 'activate' : 'deactivate'} this team ${teamName}?`
    
    alertBoxTeamActive.showAlert(text,'',()=>{
        console.log('callback')
    })

    
}