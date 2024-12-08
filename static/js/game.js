
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
  }



const handleSubmitSubstitution =async(event)=>{
    e.preventDefault();
    try {
        // Get the form element
        const form = document.getElementById('substitution-alert-box');

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

