const token = localStorage.getItem("access")

// load employees
fetch("/api/users/", {
    headers: {
        "Authorization": `Bearer ${localStorage.getItem("access")}`
    }
})
.then(res => res.json())
.then(users => {

    let select = document.getElementById("assigned_to")

    users.forEach(user => {

        let option = document.createElement("option")

        option.value = user.id
        option.text = `${user.username} (${user.role})`

        select.appendChild(option)
    })

})


// create task
function createTask(){

    let formData = new FormData()

    formData.append("title", document.getElementById("title").value)
    formData.append("description", document.getElementById("description").value)
    formData.append("due_date", document.getElementById("due_date").value)
    formData.append("file", document.getElementById("file").files[0])

    // MULTI SELECT USERS
    let selectedUsers = Array.from(
        document.getElementById("assigned_to").selectedOptions
    ).map(option => option.value)

    selectedUsers.forEach(id => {
        formData.append("assigned_to", id)
    })

    fetch("/api/tasks/", {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("access")}`
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        alert("Task Created Successfully")
        window.location.href = "/dashboard/"
    })
}