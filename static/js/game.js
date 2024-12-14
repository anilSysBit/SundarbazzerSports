
async function addGoalFromForm(e) {
    e.preventDefault();
    try {
        // Get the form element
        const form = document.getElementById('goal-alert-box');

        // Create FormData object to gather form data
        const formData = new FormData(form);

        // Convert FormData to a plain object
        const goalData = Object.fromEntries(formData.entries());
        console.log(goalData)

        if(!goalData.goal_type){
            showSnackBar(message='You need to select the goal type',type="error",position='top')
            return;
        }

        if(!goalData.goal_time){
            showSnackBar(message='Enter the time when player scored a goal, or check the add current time box',type='error',position='top')
            return;
        }
        // return;
        // Make the API request
        const response = await fetch('/match/add-goal/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': goalData.csrfmiddlewaretoken, // Include CSRF token
            },
            body: formData, // Send FormData directly for compatibility with Django
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error:', errorData.errors || errorData.message);
            snack.showSnack(message=errorData.message,type='error')

            return { success: false, errors: errorData.errors || errorData.message };
        }

        const responseData = await response.json();
        console.log('Goal added successfully:', responseData);
        // return { success: true, data: responseData };
        snack.showSnack(message=responseData.message,type='success')
        const alertbox = document.getElementById('goal-alert-box');
        alertbox.classList.remove('show')
        removeSelection()
        updateMatchData();
        
    } catch (error) {
        console.error('Unexpected error:', error);
        return { success: false, errors: 'An unexpected error occurred.' };
    }
}



async function addFoulFromForm(e) {
    e.preventDefault();
    try {
        // Get the form element
        const form = document.getElementById('foul-alert-box');

        // Create FormData object to gather form data
        const formData = new FormData(form);

        // Convert FormData to a plain object
        const goalData = Object.fromEntries(formData.entries());
        console.log(goalData)



        if(!goalData.fall_time){
            showSnackBar(message='Enter the time when player scored a goal, or check the add current time box',type='error',position='top')
            return;
        }
        // return;
        // Make the API request
        const response = await fetch('/match/add-foul/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': goalData.csrfmiddlewaretoken, // Include CSRF token
            },
            body: formData, // Send FormData directly for compatibility with Django
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error:', errorData.errors || errorData.message);
            snack.showSnack(message=errorData.message,type='error')

            return { success: false, errors: errorData.errors || errorData.message };
        }

        const responseData = await response.json();
        console.log('Goal added successfully:', responseData);
        // return { success: true, data: responseData };
        snack.showSnack(message=responseData.message,type='success')
        form.classList.remove('show')
        removeSelection()
        updateMatchData();
        
    } catch (error) {
        console.error('Unexpected error:', error);
        return { success: false, errors: 'An unexpected error occurred.' };
    }
}



// JavaScript function to update the player stats dynamically
function updateMatchData() {
    fetch(`/match/match-data-api/${matchId}/`)
        .then(response => response.json())
        .then(data => {

            document.getElementById('team1-score').textContent = data.team1.total_goals;
            document.getElementById('team2-score').textContent = data.team2.total_goals;

            // Update team 1 players' goal and foul counts
            data.team1.active_players.forEach(player => {
                const goalCells = document.querySelectorAll('.goal-count-1');
                const foulCells = document.querySelectorAll('.foul-count-1');
                
                // Loop through all goal and foul count cells for Team 1 and update based on player ID
                goalCells.forEach(cell => {
                    if (cell.closest('tr').dataset.playerId == player.id) {
                        cell.textContent = player.goal_count;
                    }
                });

                foulCells.forEach(cell => {
                    if (cell.closest('tr').dataset.playerId == player.id) {
                        cell.textContent = player.foul_count;
                    }
                });
            });

            // Update team 2 players' goal and foul counts
            data.team2.active_players.forEach(player => {
            });
        })
        .catch(error => {
            console.error('Error fetching match data:', error);
        });
}




const checkbox = document.getElementById('checkbox');
const timeInputBox = document.getElementById('time-input-box');
const timeInput = document.getElementById('custom-time')


function toggleTimeInput() {
    const prevValue = getCustomCurrentTime()
    if (checkbox.checked) {
        // timeInputBox.style.display = 'none';
        timeInput.value = prevValue
        // timeInputBox.style.display = 'block';

    } else {
        timeInput.value = prevValue;

    }
}

// Attach event listener to toggle visibility
checkbox.addEventListener('change', ()=>toggleTimeInput());



// function that handles the add match schedular 

async function handleMatchSchedular(e,id){
    e.preventDefault();



    const form = document.getElementById('match-schedule-alert-box');

    // Create FormData object to gather form data
    const formData = new FormData(form);

    // Convert FormData to a plain object
    const goalData = Object.fromEntries(formData.entries());
    console.log(goalData)

    try{
        const response = await fetch(`/match/match-schedule/${id || ''}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': goalData.csrfmiddlewaretoken, // Include CSRF token
            },
            body: formData, // Send FormData directly for compatibility with Django
        });
        const responseData = await response.json()
        console.log('Match Schedule Response',responseData)

        if(!response.ok){
            snack.showSnack(message=responseData.message,type='error')
        }else{
            snack.showSnack(message=responseData.message,type='success')
            window.location.href = `/match/game-simulation/${goalData.match}/`

        }

        form.classList.remove('show')

    }catch(error){
        console.log(error)
    }
}



const fetchSubsitutionPlayers =async(id1,id2)=>{

    const response = await fetch(`/match/substitution-players/${id1}/${id2}/`,{
      method:"get"
    })
  
    const responseData = await response.json();
    if(!response.ok){
      snack.showSnack(message=responseData.error, type='error')
    }
    
    console.log('fetch substitution resopnse',responseData)
    return responseData
  
  }

const handleOpenSubstitutionBox=async()=>{
    const data1 = selectedData[0];
    const data2 = selectedData[1]

    console.log('selecte dtaa',selectedData)



    if(selectedData.length < 2){
      showSnackBar(message="You should choose two players player of same team before adding foul",type='error')
      return;
    }else if(data1.team_name != data2.team_name){
        showSnackBar(message="Cannot Subsitutie a player of different teams. Invalid",type='error')
    }else if(selectedData.length > 2){
      showSnackBar(message="More than Two players cannot be selected at one to add a substitution",type='error')
      return;
    }
  
    const responseData = await fetchSubsitutionPlayers(data1.id,data2.id)

    const player1 = responseData?.player1;
    const player2 = responseData?.player2;

  
    const alertbox = document.getElementById('substitution-alert-box');
    alertbox.reset()
  
    const timeInput = document.getElementById('custom-time-substitution')
  
    // alertbox.remove()
  
    const timeValue = getCustomCurrentTime()
    timeInput.value = timeValue;
  
    
    // const note = document.getElementById('note')
    const header = document.getElementById('header-foul')
    // const sub_header = document.getElementById('sub-header')
    const team_name = document.getElementById('team-name');
    const jersey_no_in = document.getElementById(`jersey-noin`)
    const jersey_no_out = document.getElementById(`jersey-noout`)

    const player_name_in = document.getElementById('player-namein')
    const player_name_out = document.getElementById('player-nameout')


    const board_out_number = document.getElementById('out-numbersimu')
    const board_in_number = document.getElementById('in-numbersimu')

    board_out_number.textContent = player1.jersey_no;
    board_in_number.textContent = player2.jersey_no;
    

    
    const player_id = document.getElementById('player-foul')
    
    player_name_out.textContent = player1.name;
    player_name_in.textContent = player2.name;
  
    // player_id.value = responseData.id
  
    // header.textContent = `${responseData.name} (${responseData.team_name})`
    // sub_header.textContent = `${selected.team_name}`
  
  
    jersey_no_out.textContent = `${player1.jersey_no || '00'}`
    jersey_no_in.textContent = `${player2.jersey_no || '00'}`

    team_name.textContent = player1.team_name;
    // player_name.textContent = `${responseData.name}`
  
    alertbox.classList.add('show')


    alertbox.onsubmit =(event)=> handleSubmitSubstitution(event,player1.id,player2.id);
  }



const handleSubmitSubstitution =async(event,player_out,player_in)=>{
    event.preventDefault();
    try {
        // Get the form element
        const form = document.getElementById('substitution-alert-box');

        const formData = new FormData(form);
        formData.append("player_out",player_out)
        formData.append("player_in",player_in)

        // Convert FormData to a plain object
        const goalData = Object.fromEntries(formData.entries());
        console.log(goalData)



        if(!goalData.time){
            showSnackBar(message='Enter the time when subsitutuion occured',type='error',position='top')
            return;
        }
        // return;
        // Make the API request
        const response = await fetch('/match/add-substitution/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': goalData.csrfmiddlewaretoken, // Include CSRF token
            },
            body: formData, // Send FormData directly for compatibility with Django
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error:', errorData.errors || errorData.message);
            snack.showSnack(message=errorData.errors.__all__,type='error')

            return { success: false, errors: errorData.errors || errorData.message };
        }

        const responseData = await response.json();
        console.log('Goal added successfully:', responseData);
        // return { success: true, data: responseData };
        snack.showSnack(message=responseData.message,type='success')
        form.classList.remove('show')
        removeSelection()
        updateMatchData();
        
    } catch (error) {
        console.error('Unexpected error:', error);
        return { success: false, errors: 'An unexpected error occurred.' };
    }


}



// handle click start match


const handleRequestGameStart =async(id,type=0)=>{
    const form = document.getElementById('simulation-form');

    const formData = new FormData(form)

    const formValues = Object.fromEntries(formData.entries());


    try{
        const response = await fetch(`/match/start-match/${id}/?type=${type}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': formValues.csrfmiddlewaretoken, // Include CSRF token
                
            },
            body: formValues, // Send FormData directly for compatibility with Django
        });

        const responseData = await response.json();

        console.log('response data of start time',responseData)
        if(!response.ok){
            snack.showSnack(message="Error starting the time",type="error")
            return;
        }

        snack.showSnack(message=responseData?.message || "Success",type='success')

        updateGameTimeData(id);




    }catch(error){
        console.log(error)
    }
}

const runTimer =(start_time)=>{
    const datetime = new Date(start_time);

}
function secondsToHHSS(seconds) {
    const hours = Math.floor(seconds / 3600);
    const secs = Math.floor(seconds % 60);
    return `${String(hours).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

function secondsToHHMMSS(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}


function startStopwatchFrom(pause = false, secondsStart, element, format) {
    let seconds = secondsStart;
    let minutes = Math.floor(seconds / 60);
    let hours = Math.floor(minutes / 60);
    let days = Math.floor(hours / 24);

    seconds = seconds % 60;
    minutes = minutes % 60;
    hours = hours % 24;

    // Clear any existing stopwatch interval before starting a new one
    if (element.stopwatchInterval) {
        clearInterval(element.stopwatchInterval);
    }

    // If paused, display the time without starting the interval
    if (pause) {
        element.innerHTML = formatTime(minutes, seconds, hours, days, format);
        return;  // Exit the function without starting the interval
    }

    // Start the stopwatch interval
    const stopwatchInterval = setInterval(() => {
        seconds++;

        if (seconds === 60) {
            seconds = 0;
            minutes++;
        }

        if (minutes === 60) {
            minutes = 0;
            hours++;
        }

        if (hours === 24) {
            hours = 0;
            days++;
        }

        // Update the display with formatted time
        element.innerHTML = formatTime(minutes, seconds, hours, days, format);
    }, 1000);

    // Store the interval ID on the element for future reference (for stopping)
    element.stopwatchInterval = stopwatchInterval;

    // Return the stop function
    function stopStopwatch() {
        clearInterval(stopwatchInterval);
        delete element.stopwatchInterval; // Remove the reference to the interval
        console.log('Stopwatch stopped');
    }

    return stopStopwatch; // Return the stop function to stop the stopwatch externally
}

// Helper function to format time
function formatTime(minutes, seconds, hours, days, format) {
    let formattedTime = '';

    switch (format) {
        case 'm-s':
            formattedTime = `
                <p class="time_box">${minutes} M</p>
                <p class="time_box">${seconds} S</p>
            `;
            break;

        case 'h-m-s':
            formattedTime = `
                <p class="time_box">${hours} H</p>
                <p class="time_box">${minutes} M</p>
                <p class="time_box">${seconds} S</p>
            `;
            break;

        case 'd-h-m-s':
            formattedTime = `
                <p class="time_box">${days} D</p>
                <p class="time_box">${hours} H</p>
                <p class="time_box">${minutes} M</p>
                <p class="time_box">${seconds} S</p>
            `;
            break;

        default:
            formattedTime = `
                <p class="time_box">${hours} H</p>
                <p class="time_box">${minutes} M</p>
                <p class="time_box">${seconds} S</p>
            `;
    }

    return formattedTime;
}



// finish and end the match

const handleUpdateMatchTimeManager =async(id,newFormData)=>{
    const form = document.getElementById("simulation-form")

    const formData = new FormData(form);

    // Convert FormData to a plain object
    const data = Object.fromEntries(formData.entries());
    // console.log(data)
    const response = await fetch(`/match/match-schedule/${id}/`,
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': data.csrfmiddlewaretoken, // Include CSRF token
            },
            body: newFormData,
        }
    )
    const responseData = await response.json()
    console.log('Response of update match time manager',responseData)
    if(!response.ok){
        console.log('gonig here')
        snack.showSnack(message=responseData?.message || "Error POST request.",type='error')
        return;
    }

    snack.showSnack(message=responseData.message || 'Success',type='success')
}

let currentStopwatch;
async function updateGameTimeData (id){
    const data = await fetchGameTimeData(id)


    const game_start_time = document.getElementById('game-start-time')
    const game_total_duration = document.getElementById('game-total-duration')
    const half_duration = document.getElementById("game-half-duration")
    const total_time_running_date = document.getElementById('game-total-time-running') 
    const toal_time_remaining_date = document.getElementById('game-total-time-remaining')
    const timerType = total_time_running_date.getAttribute('data-timer-type')
    const leaked_time = document.getElementById('game-total-leakage-time')
    const remaning_time = document.getElementById('game-total-remaning-time')
    const start_button = document.getElementById("start-match-button")

    if(!data?.is_half_time_over && !data?.first_half_start_time){
        start_button.textContent = 'Start First Half'
        
    }
    else if(data?.first_half_start_time && !data?.is_half_time_over){
        start_button.textContent = 'Finish First Half'
        start_button.onclick =()=>{
            if(confirm("Are you sure you want to finish first half?")){
                const formData = new FormData();
                formData.append('is_half_time_over',true)
                handleUpdateMatchTimeManager(data?.time_manager,formData)
                updateGameTimeData(data?.match)
            }
        }
    }
    else if(data?.is_half_time_over && !data?.second_half_start_time){
        start_button.textContent = 'Start Second Half'
        start_button.onclick =()=> {
            if(confirm("Are you sure you want to finish first half?")){
                handleRequestGameStart(data?.match,type=1)
            }
        }
    }else if(data?.second_half_start_time && data?.first_half_start_time && data?.is_half_time_over){
        start_button.textContent = 'Finish Game'
        start_button.onclick =()=> {
            if(confirm("Are you sure you want to finish the Game?")){
                const formData = new FormData();
                formData.append('match_ended',true)
                handleUpdateMatchTimeManager(data?.time_manager,formData)
                updateGameTimeData(data?.match)
            }
        }
    }else{
        start_button.textContent = 'Game Already over'
        start_button.onclick = ()=> null
    }

    remaning_time.textContent = `Remaning Time : ${data?.remaning_time}`
    

    if(data?.leakage_time){
        format_leakage = secondsToHHMMSS(data?.leakage_time)
        leaked_time.textContent = `Leakage Time : ${format_leakage}`
    }




    if(data){
        if(data.first_half_start_time){
            game_start_time.textContent = `First Half Start Time : ${data.first_half_start_time}`
        }

        game_total_duration.textContent = `Duration : ${data?.game_duration}`

        if(data.first_half_start_time && !data.second_half_start_time){
            half_duration.textContent = `Running First Half : ${data?.half_time_duration}`
        }else{
            half_duration.textContent = `Second Half : ${data?.half_time_duration}`

        }


        
        // Stop the current stopwatch before starting a new one
        if (currentStopwatch) {
            currentStopwatch(); // Stop the previous stopwatch
        }

        currentStopwatch = startStopwatchFrom(
            data?.pause_running_time,
            data?.running_time,
            total_time_running_date,
            timerType
        );

        
    }
}

function handleClickStartMatch (id){
    if(confirm("Are you sure you want to start the match")){
        console.log('Game Confirmed')
        handleRequestGameStart(id);
    }else{
        console.log('Cancelled the confiramtion')
    }
}


const fetchGameTimeData =async(id)=>{

    const response = await fetch(`/match/match-time-api/${id}/`,{
        method:"GET",
    })
    const responseData = await response.json();

    console.log('fetch tiem api resopnse',responseData)
    if(!response.ok){
        snack.showSnack(message=responseData?.message || "Error Fetching the match data try again.",type='error')
        return;
    }

    return responseData.data
}





// load pause resume api time load data

const handleLoadPauseResumeData =async(match)=>{
    
    try{
        const response = await fetch(`/match/game-pause-resume-status/${match}/`,{
            method:"GET"  
        })

        const responseData = await response.json()

        console.log('Response of pause resume initial data',responseData)
        if(!response.ok){
            snack.showSnack(message=responseData.message || 'Something Went Wrong',type='error')

            return;
        }

        if(responseData.data){
            managePauseResumeDom(responseData.data)
        }


    }catch(error){
        snack.showSnack(message="Error Fetching the Pause Resume Recent Status, Try Again!",type='error')
    }
}


const managePauseResumeDom =(data)=>{
    const button = document.getElementById('pause-resume-button')

    
    if(data){
        console.log('dom data passing',data)
        if(data.recent_status == 'paused'){
            button.textContent = 'Resume Match'
            button.onclick =()=> handleResumeMatchRequest(data.match,data.recent_resume_id)
        }else if(data.recent_status == 'resumed'){
            button.textContent = 'Pause Match'
            button.onclick =()=> handlePauseMatchRequest(data.match)
        }
    }
}



// pause resume
const handlePauseMatchRequest =async(match)=>{

    console.log('match id',match)
    const formData = new FormData()
    formData.append('match',match)
    const response = await fetch(`/match/pause-match/`,{
        method:"POST",
        body:formData,        
    })

    // console.log(await response)
    const responseData = await response.json()

    console.log('responese of pause',responseData)

    if(!response.ok){
        snack.showSnack(message=responseData?.message || 'Something Went Wrong',type='error')
        return
    }

    snack.showSnack(message="Successfully Paused the Match. Time Duration between Paused and Resumed will be listed on Leakage Time.",type="success")

    // return responseData;
    handleLoadPauseResumeData(match);
    updateGameTimeData(match)
}



const handleResumeMatchRequest =async(match,resume_id)=>{
    const response = await fetch(`/match/resume-match/${resume_id}/`,{
        method:"POST",
    })
    const responseData = await response.json()

    console.log('responese of resume',responseData)

    if(!response.ok){
        snack.showSnack(message=responseData?.message || 'Something Went Wrong',type='error')
        return
    }

    snack.showSnack(message=responseData.message || 'Successfully Resumed the Match',type="success")

    handleLoadPauseResumeData(match);
    updateGameTimeData(match);
}


