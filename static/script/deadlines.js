import {
  getProfileData,
  getTasks
} from "./modules/gsuitefeatures.js";

function formatCustomDate(dateStr) {
  const date = new Date(dateStr);

  const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

  const month = months[date.getUTCMonth()];
  const day = date.getUTCDate();
  const year = date.getUTCFullYear();

  let hours = date.getUTCHours();
  const minutes = String(date.getUTCMinutes()).padStart(2, '0');
  const suffix = hours >= 12 ? "pm" : "am";

  if (hours === 0) {
    hours = "00";
  } else {
    hours = String(hours % 12 || 12).padStart(2, '0');
  }

  // return `(${month} ${day}, ${year} - ${hours}:${minutes}${suffix})`;
  return `(${month} ${day}, ${year})`;
}

function loadDeadlines(tasks) {
  const taskContainer = document.getElementById("task-container");
  const finishedContainer = document.getElementById("finished-container");

  for (let task of tasks) {
    console.log(task);

    if (["CREATED", "NEW"].includes(task.status)) {
      taskContainer.innerHTML += `
        <div class="todo-item">
            <div class="todo-icon"><i class="fa fa-pencil"></i> ${task.task_name}</div>
            <div class="todo-details">
                <div></div>
                <div></div>
            </div>
            <div class="todo-due">Due Date: ${formatCustomDate(task.due_date)}</div>
        </div>
      `;
    } else {
      finishedContainer.innerHTML += `
        <div class="completed-item">
          <div class="completed-icon"><i class="fa fa-check-circle"></i> ${task.task_name}</div>
          <div class="completed-details">
              <div></div>
              <div></div>
          </div>
        </div>
      `;
    }
  }
}

function loadProfileData(studentData) {
    // loads the name of the student
    const namePlaceholder = document.getElementById("name-of-student");
    const profilePlaceholder = document.getElementById("profile");
  
    namePlaceholder.innerText = studentData.name;
    if (studentData.picture)
      profilePlaceholder.src = studentData.picture;
}

// allows us to use async functions
(async function () {
  // retrieves student data from api
  const studentData = await getProfileData();
  const tasks = await getTasks(true);

  loadProfileData(studentData);
  loadDeadlines(tasks);
})();
