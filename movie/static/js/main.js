function request(url, method) {
    fetch(url, { method })
        .then((res) => {
            window.location.reload();
        })
        .catch((error) => console.error(error));
}