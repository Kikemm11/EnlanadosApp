function buildCalendar() {
    const today = new Date();
    const currentYear = today.getFullYear();
    const currentMonth = today.getMonth(); // 0 is January, 11 is December
    const currentDay = today.getDate();
  
    // Array of month names
    const monthNames = [
      'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
      'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ];
  
    // Get the first day of the current month and the total days in the month
    const firstDay = new Date(currentYear, currentMonth, 1).getDay(); // 0 is Sunday, 6 is Saturday
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate(); // Total days in the month
  
    // Set the header with the current month and year
    document.getElementById('calendar-header').textContent = `${monthNames[currentMonth]} ${currentYear}`;
  
    const calendarBody = document.getElementById('calendar-body');
  
    // Generate the empty slots before the first day of the month
    for (let i = 0; i < firstDay; i++) {
      const emptyDiv = document.createElement('div');
      emptyDiv.classList.add('empty');
      calendarBody.appendChild(emptyDiv);
    }
  
    // Generate the days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      const dayDiv = document.createElement('div');
      dayDiv.textContent = day;
  
      // Highlight the current day
      if (day === currentDay) {
        dayDiv.classList.add('current-day');
      }
  
      calendarBody.appendChild(dayDiv);
    }
  }
  
  // Build the calendar when the page loads
  window.onload = function () {
    buildCalendar();
  };
  