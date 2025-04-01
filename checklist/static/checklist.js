function toggleChecklist(event, checklistId) {
    event.preventDefault();
    
    const options = document.getElementById(checklistId);
    const toggleButton = document.querySelector(`button[onclick="toggleChecklist('${checklistId}')"]`);
    
    if (options.style.maxHeight === '0px' || options.style.maxHeight === '') {
        options.style.maxHeight = '500px'; // Adjust to fit content
        options.style.opacity = '1';
        toggleButton.classList.add('expanded');
    } else {
        options.style.maxHeight = '0';
        options.style.opacity = '0';
        toggleButton.classList.remove('expanded');
    }
}

// Function to toggle the checklist items
function toggleChecklist(checklistId) {
    const options = document.getElementById(checklistId);
    const toggleButton = document.querySelector(`button[onclick="toggleChecklist('${checklistId}')"]`);
    
    if (options.style.maxHeight === '0px' || options.style.maxHeight === '') {
        options.style.maxHeight = '500px'; // Adjust to fit content
        options.style.opacity = '1';
        toggleButton.classList.add('expanded');
    } else {
        options.style.maxHeight = '0';
        options.style.opacity = '0';
        toggleButton.classList.remove('expanded');
    }

    // Call updateProgressBar function whenever a checklist is toggled
    updateProgressBar();
}

// Function to update progress bar
function updateProgressBar() {
    // Get the total number of checkboxes
    const totalCheckboxes = document.querySelectorAll('.checklist-item input[type="checkbox"]').length;
    
    // Get the number of checked checkboxes
    const checkedCheckboxes = document.querySelectorAll('.checklist-item input[type="checkbox"]:checked').length;
    
    // Calculate the percent completed
    const percentage = (checkedCheckboxes / totalCheckboxes) * 100;

    // Update progress bar width
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = percentage + '%';
}

document.addEventListener('DOMContentLoaded', () => {
    // Add an event listener to each checkbox
    const checkboxes = document.querySelectorAll('.checklist-item input[type="checkbox"]');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            // Call updateProgressBar function whenever a checkbox is changed
            updateProgressBar();
        });
    });
    
    // Initialize the progress bar
    updateProgressBar();
});

