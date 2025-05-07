export async function getClassroomData() {
  try {
    const response = await fetch("/api/gsuite-features/classroom/courses", {
      credentials: "include",
    });
    const responseData = await response.json();
    return responseData;
  } catch (err) {
    console.error(err);
  }
}

export async function getProfileData() {
  try {
    const response = await fetch("/api/gsuite-features/profile/", {
      credentials: "include",
    });
    const responseData = await response.json();
    return responseData;
  } catch (err) {
    console.error(err);
  }
}

export async function getTasks(includeAcadsync=false) {
  try {
    const response = await fetch(`/api/gsuite-features/classroom/task?${includeAcadsync ? "include_done=true": ""}`, {
      credentials: "include",
    });
    const responseData = await response.json();
    return responseData;
  } catch (err) {
    console.error(err);
  }
}

export async function finishTask(id, afterCallback) {
  try {
    await fetch(`/api/gsuite-features/classroom/finish-task/${id}`, {
      credentials: "include",
      method: "DELETE"
    });
    afterCallback && afterCallback();
  } catch (err) {
    console.error(err);
  }

}

export async function createTask(taskName, taskDueDate, afterCallback) {
  try {
    await fetch(`/api/gsuite-features/classroom/task`, {
      credentials: "include",
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        "task_name": taskName,
        "task_due": taskDueDate
      })
    });
    afterCallback && afterCallback();
  } catch (err) {
    console.error(err);
  }
}

export async function setMessengerLink(id, link, afterCallback) {
  try {
    await fetch(`/api/gsuite-features/classroom/set-link/${id}`, {
      credentials: "include",
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        "messenger_link": link,
      })
    });
    afterCallback && afterCallback();
  } catch (err) {
    console.error(err);
  }
}