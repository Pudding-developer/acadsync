import {
  createTask,
  finishTask,
  getProfileData,
  getClassroomData,
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

function closeCreateTaskModal() {
  const modal = document.getElementById("add-todo-modal");
  modal.style.display = "none";
}

function openCreateTaskModal() {
  const modal = document.getElementById("add-todo-modal");
  modal.style.display = "";
}

function submitTask() {
  const taskName = document.getElementById("task-input");
  const taskDue = document.getElementById("task-due");

  createTask(taskName.value, taskDue.value, () => {
    window.location.reload();
  });
}

// allow global access
window.openCreateTaskModal = openCreateTaskModal;
window.closeCreateTaskModal = closeCreateTaskModal;
window.submitTask = submitTask;
window.finishTask = finishTask;

function loadProfileData(studentData) {
  // loads the name of the student
  const namePlaceholder = document.getElementById("name-of-student");
  const welcomeNamePlaceholder = document.getElementById("welcome-name");
  const profilePlaceholder = document.getElementById("profile");

  namePlaceholder.innerText = studentData.name;
  welcomeNamePlaceholder.innerText = studentData.given_name;
  if (studentData.picture)
    profilePlaceholder.src = studentData.picture;
}

function loadSubjects(classroomData) {
  // loads the subject of the student
  const subjectRow = document.getElementById("subject-row");

  // I use the ff. as reference html code:
  /*
   * <div class="subject-card">
   *   <div class="subject-title">
   *     Subject <i class="fa fa-book-open"></i>
   *   </div>
   * <div class="subject-actions"><i class="fa fa-video"></i></div>
   * </div>
   */

  // used basic for loop instead of arrow notation
  for (let i = 0; i < classroomData.length; i++) {
    if (classroomData[i].courseState == "ACTIVE") {
        const subjectCardDiv = document.createElement("div");
        const subjectTitleDiv = document.createElement("div");
    
        // assign css values
        subjectCardDiv.className = "subject-card";
        subjectTitleDiv.className = "subject-title";
    
        // subject title and shii
        subjectTitleDiv.innerHTML = `
            ${classroomData[i].name}
            <br/><br/>
            <a href="${classroomData[i].alternateLink}" target="_blank" style="color: inherit; text-decoration: none;">
              <i title="Go to Classroom link" class="fa fa-book-open clickable"></i>
            </a>
            <i title="Go to Messenger Chatroom" class="fas fa-comment clickable"></i>
        `;

        // put elements inside their respective tags
        subjectCardDiv.appendChild(subjectTitleDiv);
        subjectRow.appendChild(subjectCardDiv);
    }
  }
}


// load all the deadlines here
function loadDeadlines(deadlinesList) {
  const deadlineContainer = document.getElementById("deadline-container");
  const todoContainer = document.getElementById("todo-container");

  const todos = [];
  const deadlines = [];

  // Separate tasks
  for (let i = 0; i < deadlinesList.length; i++) {
    if (deadlinesList[i].course === "local-acadsync") {
      todos.push(deadlinesList[i]);
    } else {
      deadlines.push(deadlinesList[i]);
    }
  }

  // Sort deadlines by due_date (if available)
  deadlines.sort((a, b) => {
    const aTime = a.due_date ? new Date(a.due_date).getTime() : Infinity;
    const bTime = b.due_date ? new Date(b.due_date).getTime() : Infinity;
    return aTime - bTime;
  });

  // Render todos
  todos.forEach((task, index) => {
    todoContainer.innerHTML += `
      <span id="task_${task.id}">
        <input type="checkbox" id="task__${index}" style="cursor: pointer;" onclick="finishTask('${task.id}', () => {
          document.getElementById('task_${task.id}').remove();
        })">
        <label>${task.task_name} ${task.due_date ? formatCustomDate(task.due_date) : "(No Due Date)"}</label>
      </span>
    `;
  });

  // Render sorted deadlines
  deadlines.forEach(task => {
    deadlineContainer.innerHTML += `
      <li onclick="(() => {window.open('${task.link}', '_blank')})();">
        ${task.course} - ${task.task_name}
        <br/>
        ${task.due_date ? formatCustomDate(task.due_date) : "No Due Date"}
      </li>
    `;
  });
}


// allows us to use async functions
(async function () {
  // retrieves student data from api
  const studentData = await getProfileData();
  const classroomData = await getClassroomData();
  const tasks = await getTasks();

  loadProfileData(studentData);
  loadSubjects(classroomData);
  loadDeadlines(tasks);

  console.log(tasks);
})();
