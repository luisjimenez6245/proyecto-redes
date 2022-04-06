export const API_URL = getApiUrl();


function getApiUrl() {
    let url = process.env.REACT_APP_API_URL;
    if(!url){
        if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
            return 'http://localhost:80';
        } else {
            return 'https://plants-server.finalsa.app';
        }
    }
    return url
}

