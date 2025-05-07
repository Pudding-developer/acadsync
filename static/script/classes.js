import {
    getProfileData,
    getClassroomData,
    setMessengerLink
} from "./modules/gsuitefeatures.js";

function closeCreateTaskModal() {
  const modal = document.getElementById("add-todo-modal");
  modal.style.display = "none";
}

function openCreateTaskModal(classroomId) {
  const modal = document.getElementById("add-todo-modal");
  modal.style.display = "";
  window.selectedClassId = classroomId;
}

function updateMessengerLink() {
    const link = document.getElementById("link-input").value;
    if (link === "") {
        return alert("Cannot set empty link");
    }

    setMessengerLink(window.selectedClassId, link, () => {
        window.location.reload();
    })
}

// allow global access
window.openCreateTaskModal = openCreateTaskModal;
window.closeCreateTaskModal = closeCreateTaskModal;
window.updateMessengerLink = updateMessengerLink;
window.selectedClassId = null;

function loadClasses(classroomData) {
    const subRow = document.getElementById("subjects-row");

    for (let data of classroomData) {
        subRow.innerHTML += `
            <div class="subject-card">
                <div class="subject-title">${data.name}</div>
                <div class="holder">
                    <button class="classop view-button" onclick="(() => {window.open('${data.alternateLink}')})()">Open Class</button>
                    <button class="classop view-button ${!data.messengerLink ? "disabled-button": ""}" ${data.messengerLink ? "onclick=\"(() => {window.open('" + data.messengerLink + "')})()\"" : ""}>Open Chat</button>
                    <button class="classop view-button" onclick="(() => {openCreateTaskModal(${data.id})})()">Edit Chat</button>
                </div>
            </div>
        `;
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


(async function() {
    const profileData = await getProfileData();
    const classroomData = await getClassroomData();

    loadProfileData(profileData);
    loadClasses(classroomData);
})();