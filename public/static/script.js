const form = document.querySelector('form');
const questionElement = form.question;

const question = document.querySelectorAll('.question');
const titles = document.querySelectorAll('.title');
const urls = document.querySelectorAll('.url');
const question_body = document.querySelectorAll('.question_body');
const loading_div = document.querySelector('.loading');

form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const question = questionElement.value;
    for(let i = 0; i < 5; i++){
        titles[i].innerHTML = ``;
        // urls[i].innerHTML = ``;
    }

    loading_div.innerHTML = `Loading...`;

    // fetch
    try{
        const res = await fetch(`/search?question=${question}`, { method : "GET", 
        });
        const data = await res.json();

        loading_div.innerHTML = ``;


        // titles.innerHTML = `<h3>${myJson.title}</h3>`;
        
        for(let i = 0; i < 5; i++){
            titles[i].innerHTML = `<h3>${data[i].title}</h3>`;
            // urls[i].innerHTML = `<p>${data[i].url}</p>`;
        }

    } catch(error){
        alert(error);
    }
});