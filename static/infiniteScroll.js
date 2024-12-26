const container = document.getElementById('Container');
const button = document.getElementById('x');

async function getImages(n) {
    for (let i = 0; i < n; i++) {
        let response = await fetch("https://picsum.photos/200");
        let url = response.url;

        const img = document.createElement('img');
        img.src = url;
        container.appendChild(img);

        img.addEventListener('click', () => {
            img.classList.add('enlarged');
            button.style.display = 'inline-block';
        });
    }
}

getImages(9);

button.addEventListener('click', () => {
    const imageArray = document.getElementsByTagName("img");
    for (let i = 0; i < imageArray.length; i++) {
        imageArray[i].classList.remove('enlarged');
        imageArray[i].classList.add('imgs');
    }
    button.style.display = 'none';
});


window.addEventListener('scroll', (e) => {
    let { clientHeight, scrollHeight, scrollTop } = e.target.documentElement
    console.log(clientHeight)
    let scrolltop = scrollTop
    console.log(scrolltop)
    console.log(scrollHeight)


    if (clientHeight + scrolltop + 1 >= scrollHeight) {
        getImages(3);
    }
})





