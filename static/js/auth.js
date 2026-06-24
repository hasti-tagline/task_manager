async function refreshAccessToken() {

    const refresh = localStorage.getItem("refresh");

    if (!refresh) return null;

    const response = await fetch("/api/token/refresh/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ refresh })
    });

    const data = await response.json();


    if (response.ok && data.data.access) {
        localStorage.setItem("access", data.data.access);
        return data.data.access;
    }
    return null;
}


async function authFetch(url, options = {}) {

    let token = localStorage.getItem("access");

    options.headers = {
        ...options.headers,
        "Authorization": `Bearer ${token}`
    };

    let response = await fetch(url, options);

   if (response.status === 401 || response.status === 403) {

        const newToken = await refreshAccessToken();

        if (!newToken) {
            localStorage.clear();
            window.location.href = "/";
            return;
        }

        options.headers["Authorization"] = `Bearer ${newToken}`;

        response = await fetch(url, options);
    }

    return response;
}