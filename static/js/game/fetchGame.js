document.addEventListener('DOMContentLoaded',()=>{
    const path = window.location.pathname; // Get the path like "/match/game-simulation/1/"
    const parts = path.split('/').filter(Boolean); // Split by '/' and remove empty parts
    const id = parts[parts.length - 1]; // Get the last part of the path (which is the ID)    fetchGameTimeData()

    handleLoadGameRecentData(id)
    handleLoadPauseResumeData(id)
})