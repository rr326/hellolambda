function baseURL() {
    return (window.useLocalhost)
        ? HLCONFIG.API_LOCAL_BASE
        : `http://localhost:${HLCONFIG.API_AWS_BASE}`
}

function apiURL(path) {
    const separator = path.slice(0,1) === '/' ? '' : '/'
    const href = baseURL() + separator + path
    return href
}

function apiCall(path, method, data, options = {}){
    const href = apiURL(path)

    $.ajax({
        url: href,
        method: method,
        data: (method.toLowerCase() === 'post') ? JSON.stringify(data): data,
        contentType: "text/plain",

        success: (data, textStatus, jqXHR) => {
            if (options.debug) {
                console.log("apiCall success", data, textStatus, jqXHR)
            }

            if (options.successFn) {
                options.successFn(data, textStatus, jqXHR)
            }
        },
        error: (jqXHR, textStatus, errorThrown) => {
            if (options.debug) {
                console.log('apiCall Error', jqXHR, textStatus, errorThrown)
            }

            if (options.errorFn) {
                options.errorFn(jqXHR, textStatus, errorThrown)
            }
        }
    })
}