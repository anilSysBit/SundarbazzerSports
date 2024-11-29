
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
        const response = await fetch('/add-goal/', {
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



// JavaScript function to update the player stats dynamically
function updateMatchData() {
    fetch(`/match-data-api/${matchId}/`)
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

