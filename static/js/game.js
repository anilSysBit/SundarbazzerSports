
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