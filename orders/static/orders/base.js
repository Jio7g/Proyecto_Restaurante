document.addEventListener('DOMContentLoaded', () => {

    let basknum = document.querySelector('#basketnum');
    let basketnum = JSON.parse(localStorage.getItem('basknum'));
    
    if (basketnum > 0) {
        basknum.innerHTML = basketnum;
        basknum.hidden = false;
    } else {
        basknum.innerHTML = 0;
        basknum.hidden = true;
    }
});