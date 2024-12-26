document.addEventListener('DOMContentLoaded', function() {
    function updateDateTime() {
        const now = new Date();
        const dateElement = document.getElementById('date');
        const timeElement = document.getElementById('time');

        const optionsDate = { year: 'numeric', month: 'long', day: 'numeric' };
        const optionsTime = { hour: '2-digit', minute: '2-digit', second: '2-digit' };

        dateElement.textContent = now.toLocaleDateString(undefined, optionsDate);
        timeElement.textContent = now.toLocaleTimeString(undefined, optionsTime);
    }

    updateDateTime();
    setInterval(updateDateTime, 1000); // Update time every second
});
