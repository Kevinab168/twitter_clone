post_content = document.querySelector('#id_content')

post_container = document.querySelector('.post_container')




document.querySelector('.btn').addEventListener('click', (e) => {
    e.preventDefault() 
    console.log('clicked the button')
    post_add = post_content.value
    new_post = `
    <a href='#' data-test="post-info">${post_add}</a>
    `
    post_container.innerHTML += new_post
})

