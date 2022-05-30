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
    for(let i = 0; i < 10; i++){
        titles[i].innerHTML = ``;
        urls[i].innerHTML = ``;
        question_body[i].innerHTML = ``;
    }

    loading_div.innerHTML = `Loading...`;

    // fetch
    try{
        const res = await fetch(`/search?question=${question}`, { method : "GET", 
        });
        const data = await res.json();

        loading_div.innerHTML = ``;


        for(let i = 0; i < 10; i++){
            titles[i].innerHTML = `<h3>${data[i].title}</h3>`;
            urls[i].innerHTML = `<a href=${data[i].url} target="_blank">${data[i].url}</a>`;
            question_body[i].innerHTML = `<p>${data[i].question_body}</p>`;
        }

    } catch(error){
        alert(error);
    }
});