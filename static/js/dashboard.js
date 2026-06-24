const role =localStorage.getItem("role")

if(!(localStorage.getItem("access"))){
    window.location.href = "/"
}

document.getElementById("loggedRole").innerHTML = role

function logout() {
    localStorage.clear()
    window.location.href = "/"
}

let currentUserPage = 1;
let currentTaskPage = 1;


// load users includes search,filter and paginations
async function loadUsers(page = 1) {
    currentUserPage = page;

    let search = document.getElementById("searchUser").value;
    let role = document.getElementById("filterRole").value;

    let response = await authFetch(`/api/users/?page=${page}&search=${search}&role=${role}`);
    let data = await response.json();

    renderUserTable(data.data.results);
    renderUserPagination(data.data);
}


// RENDER USER TABLE
function renderUserTable(users){

    let tableHead = ""
    let tableBody = ""

    // ADMIN
    if(role === "admin"){

        tableHead = `
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Total Tasks</th>
            <th>Actions</th>
        
        `
        users.forEach(user => {
            tableBody += `
                <tr data-role="${user.role}">
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td>
                        <select
                            class="form-select form-select-sm"
                            onchange="updateRole(${user.id}, this.value)">
                            <option
                                value="employee"
                                ${user.role === "employee" ? "selected" : ""}>
                                Employee
                            </option>
                            <option
                                value="manager"
                                ${user.role === "manager" ? "selected" : ""}>
                                Manager
                            </option>
                            <option
                                value="admin"
                                ${user.role === "admin" ? "selected" : ""}>
                                Admin
                            </option>

                        </select>

                    </td>

                    <td>${user.total_tasks}</td>
                    <td>
                        <button
                            class="btn btn-info btn-sm"
                            onclick="viewUser(${user.id})">
                            View
                        </button>

                        <button
                            class="btn btn-danger btn-sm"
                            onclick="deleteUser(${user.id}, '${user.username}')">
                            Delete
                        </button>
                    </td>
                </tr>
            `
        })
    }


    // MANAGER
    else if(role === "manager"){
        tableHead = `
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Total Tasks</th>
            <th>Actions</th>

        `
        users.forEach(user => {
            tableBody += `
                <tr data-role="${user.role}">
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td>${user.role}</td>
                    <td>${user.total_tasks}</td>
                    <td>
                        <button
                            class="btn btn-info btn-sm"
                            onclick="viewUser(${user.id})">
                            View
                        </button>
                    </td>
                </tr>
          `
      })
    }


    // EMPLOYEE
    else{
        tableHead = `
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Total Tasks</th>
            <th>Actions</th>
        `
        users.forEach(user => {
            tableBody += `
                <tr>
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td>${user.total_tasks}</td>
                     <td>
                        <button
                            class="btn btn-info btn-sm"
                            onclick="viewUser(${user.id})">
                            View
                        </button>
                    </td>
                </tr>
             `
        })
    }
    document.getElementById("userTableHead").innerHTML = tableHead
    document.getElementById("userTableBody").innerHTML = tableBody
}
// end table render

// start function for user table

// pagination function
function renderUserPagination(data){

    let html = "";
    if(data.previous){
        html += `
            <button class="btn btn-secondary me-1" onclick="loadUsers(${data.current_page - 1})">
                Previous
            </button>
        `;
    }

    for(let i = 1; i <= data.total_pages; i++){

        html += `
            <button
                class="btn ${
                    i === data.current_page
                    ? "btn-primary"
                    : "btn-outline-primary"
                } me-1"
                onclick="loadUsers(${i})">
                ${i}
            </button>
        `;
    }

    if(data.next){
        html += `
            <button class="btn btn-secondary" onclick="loadUsers(${data.current_page + 1})">
                Next
            </button>
        `;
    }
    document.getElementById("userPagination").innerHTML = html;
}






// UPDATE ROLE
function updateRole(userId, role){
    authFetch(`/api/users/${userId}/`, {
        method: "PATCH",
        headers: {
            "Content-Type":
            "application/json",
        },
        body: JSON.stringify({
            role: role
        })
    })
    .then(response => response.json())
    .then(data => {
        alert("Role Updated")
        location.reload()
    })
}



// DELETE USER
function deleteUser(userId, username){
    const confirmDelete = confirm(`Delete ${username}?`)
    if(!confirmDelete){
        return
    }
    authFetch(`/api/users/${userId}/`, {
        method: "DELETE",
        headers: {
            "Authorization":
            `Bearer ${localStorage.getItem("access")}`
        }
    })
    .then(() => {
        alert("User Deleted")
        location.reload()
    })
}



// VIEW USER
function viewUser(userId){
    window.location.href = `/user-detail/?id=${userId}`
}




//  Start Task Table 


//  RENDER TASK TABLE
function renderTaskTable(tasks){
    let tableHead = ""
    let tableBody = ""

    // ADMIN
    if(role === "admin"){
         document.getElementById("createTaskBtn").innerHTML = `<a href="/tasks/create/" class="btn btn-primary">
            + Create Task
        </a>
       
    `
        tableHead = `
            <th>ID</th>
            <th>Title</th>
            <th>Created By</th>
            <th>Assigned To</th>
            <th>Status</th>
            <th>Priority</th>
            <th>Submission</th>
            <th>Actions</th>
            
        `

        tasks.forEach(task => {
            tableBody += `
                <tr data-status="${task.status}">
                    <td>
                        <span>${task.id}</span>
                    </td>

                    <td>${task.title}</td>

                    <td>${task.created_by_name}</td>

                    <td>${task.assigned_to_names.join(", ")}</td>

                    <td>
                        <span  id="task-status-${task.id}" class="badge bg-primary">${task.status}</span>
                    </td>

                    <td>
                        <span class="badge bg-danger">${task.priority}</span>
                    </td>

                     <td>
                        ${
                            task.submission
                            ? `<button class="btn btn-info btn-sm"
                                    onclick="viewSubmission('${task.submission}')">
                                    View File
                            </button>`
                            : `<span class="text-muted">No submission</span>`
                        }
                    </td>

                    <td>
                        <div class="d-flex gap-2">
                            <button class="btn btn-info btn-sm" onclick="viewTask(${task.id})">
                                View
                            </button>

                            <button class="btn btn-warning btn-sm" onclick="editTask(${task.id})">
                                Edit
                            </button>

                            <button class="btn btn-danger btn-sm" onclick="deleteTask(${task.id})">
                                Delete
                            </button>
                        
                        </div>
                    </td>
                    
                </tr>
            `
        })
    }



    // MANAGER 
    else if(role === "manager"){

        document.getElementById("createTaskBtn").innerHTML = `
        <a href="/tasks/create/" class="btn btn-primary">
            + Create Task
        </a>
    `
        tableHead = `
            <th>ID</th>
            <th>Title</th>
            <th>Assigned To</th>
            <th>Status</th>
            <th>Priority</th>
            <th>Submission</th>
            <th>Actions</th>
            <th>Chat</th>
        `

        tasks.forEach(task => {
            tableBody += `
                <tr data-status="${task.status}">
                    <td>${task.id}</td>
                    <td>${task.title}</td>
                    <td>${task.assigned_to_names.join(", ")}</td>
                    <td>
                        <span  id="task-status-${task.id}" class="badge bg-primary">${task.status}</span>
                    </td>

                    <td>
                        <span class="badge bg-danger">${task.priority}</span>
                    </td>

                     <td>
                        ${
                            task.submission
                            ? `<button class="btn btn-info btn-sm" onclick="viewSubmission('${task.submission}')">
                                    View File
                            </button>`
                            : `<span class="text-muted">No submission</span>`
                        }
                    </td>

                    <td>
                        <button class="btn btn-info btn-sm" onclick="viewTask(${task.id})">
                            View
                        </button>

                        <button class="btn btn-warning btn-sm" onclick="editTask(${task.id})">
                            Edit
                        </button>
                         <button class="btn btn-danger btn-sm" onclick="deleteTask(${task.id})">
                            Delete
                        </button>
                    </td>

                    <td>
                        <button
                            class="btn btn-success btn-sm"
                            onclick="openChat(${task.id})">
                            Chat
                        </button>
                    </td>
                </tr>
            `
        })
    }


    //EMPLOYEE 
    else{
         document.getElementById("createTaskBtn").innerHTML = `  `
        tableHead = `
            <th>ID</th>
            <th>Title</th>
            <th>Assigned By</th>
            <th>Status</th>
            <th>Priority</th>
            <th>Submission</th>
            <th>Actions</th>
            <th>Chat</th>
        `

        tasks.forEach(task => {
            tableBody += `
                <tr data-status="${task.status}">

                    <td>${task.id}</td>
                    <td>${task.title}</td>
                    <td>${task.created_by_name}</td>
                    <td>
                        <span  id="task-status-${task.id}"  class="badge bg-primary">${task.status}</span>
                    </td>
                    <td>
                        <span class="badge bg-danger">${task.priority}</span>
                    </td>

                    <td>
                        ${
                            task.submission
                            ? `<button class="btn btn-info btn-sm" onclick="viewSubmission('${task.submission}')">
                                    View File
                            </button>`
                            : `<span class="text-muted">No submission</span>`
                        }
                    </td>

                    <td>
                        <button class="btn btn-info btn-sm" onclick="viewTask(${task.id})">
                            View
                        </button>
                        <button class="btn btn-warning btn-sm" onclick="editTask(${task.id})">
                            Edit
                        </button>
                    </td>
                    <td>
                        <button
                            class="btn btn-success btn-sm"
                            onclick="openChat(${task.id})">
                            Chat
                        </button>
                    </td>
                </tr>
         `
       })

    }
    document.getElementById("taskTableHead").innerHTML = tableHead
    document.getElementById("taskTableBody").innerHTML = tableBody
}

// end the task table render

// start function for task table


// task pagination function
function renderTaskPagination(data){

    let html = "";
    if(data.previous){
        html += `
            <button class="btn btn-secondary me-1" onclick="loadTasks(${data.current_page - 1})">
                Previous
            </button>
        `;
    }
    for(let i = 1; i <= data.total_pages; i++){

        html += `
            <button
                class="btn ${
                    i === data.current_page
                    ? "btn-primary"
                    : "btn-outline-primary"
                } me-1"
                onclick="loadTasks(${i})">
                ${i}
            </button>
        `;
    }
    if(data.next){
        html += `
            <button class="btn btn-secondary" onclick="loadTasks(${data.current_page + 1})">
                Next
            </button>
        `;
    }
    document.getElementById("taskPagination").innerHTML = html;
}



// view attachment and submission files
function viewAttachment(url) {
    window.open(url, "_blank");
}


function viewSubmission(url) {
    if (!url) {
        alert("No file uploaded");
        return;
    }
    window.open(url, "_blank");
}



// load tasks includes serach,filter and paginations 
async function loadTasks(page = 1) {
    currentTaskPage = page;

    let search = document.getElementById("searchTask").value;
    let status = document.getElementById("filterTaskStatus").value;

    let response = await authFetch(`/api/tasks/?page=${page}&search=${search}&status=${status}`);
    let data = await response.json();

    renderTaskTable(data.data.results);
    renderTaskPagination(data.data);
}


//  VIEW TASK
function viewTask(taskId){
    window.location.href = `/task-detail/?id=${taskId}`
}


// EDIT TASK 
function editTask(taskId){
    window.location.href = `/task-edit/?id=${taskId}`
}


//DELETE TASK 
function deleteTask(taskId){
    const confirmDelete = confirm(
        `Delete Task ${taskId}?`
    )
    if(!confirmDelete){
        return
    }
    authFetch(`/api/tasks/${taskId}/`, {
        method: "DELETE",
        headers: {
            "Authorization":
            `Bearer ${localStorage.getItem("access")}`
        }
    })
    .then(response => {
        if(response.ok){
            alert("Task Deleted")
            location.reload()
        }
    })
}

function openChat(taskId){
    window.location.href = `/chat/?task=${taskId}`;
}



// create task
function createTask(){

    let formData = new FormData()
    formData.append("title", document.getElementById("title").value)
    formData.append("description", document.getElementById("description").value)
    formData.append("due_date", document.getElementById("due_date").value)
    formData.append("assigned_to", document.getElementById("assigned_to").value)

    let file = document.getElementById("file").files[0]

    if(file){
        formData.append("attachment", file)
    }

    authFetch("/api/tasks/", {
        method: "POST",
        body: formData
    })

    .then(res => res.json())
    .then(data => {
        alert("Task Created Successfully")
        window.location.href = "/dashboard/"

    })

}

loadUsers();
