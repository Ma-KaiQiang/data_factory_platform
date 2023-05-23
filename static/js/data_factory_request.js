export function request(method, url, data = null, callback) {

    const p = new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        console.log(url)
        xhr.open(method, url)
        xhr.send(data);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status >= 200 && xhr.status < 300) {
                    resolve(xhr.response);
                } else {
                    reject(xhr.status)
                }
            }
        }
    });
    p.then(function (value) {
        const res = JSON.parse(value);
        callback(res);
    }, function (reason) {
        console.error(reason);
    })
}
