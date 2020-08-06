const postContent = document.querySelector('#id_content');
const postContainer = document.querySelector('.post_container');


document.querySelector('#create_post').addEventListener('click', (e) => {
    e.preventDefault();
    const formDataValues = document.querySelector('#image_add_form');
    const formDataObj = new FormData(formDataValues);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '');
    xhr.setRequestHeader('X-CSRFTOKEN', csrftoken);
    xhr.send(formDataObj); 
    xhr.onload = () => { 
        const responseData = JSON.parse(xhr.response); 
        const cardBody = document.createElement('div');
        cardBody.setAttribute('class', 'card-body');
        const postCreatedDate = document.createElement('p');
        postCreatedDate.setAttribute('data-test', 'created_date');
        postCreatedDate.textContent = `Created: ${responseData.created_date}`;
        cardBody.appendChild(postCreatedDate);       
        const postUpdatedDate = document.createElement('p');
        postUpdatedDate.setAttribute('data-test', 'updated_date');
        postUpdatedDate.textContent = `Updated: ${responseData.updated_date}`;
        cardBody.appendChild(postUpdatedDate);       
        const postTextContent = document.createElement('p');
        postTextContent.setAttribute('data-test', 'created-post');
        postTextContent.textContent = responseData.post_content
        cardBody.appendChild(postTextContent);   
        for (let i = 0; i < (responseData.images.length); i++) { 
            const imageURL = responseData.images[i];
            const image = document.createElement('img');
            image.setAttribute('data-test', 'post_img_preview');
            image.setAttribute('src', `/static/${imageURL}`);
            cardBody.appendChild(image);
        }
        const editBtn = document.createElement('a');
        editBtn.setAttribute('href', `/posts/${responseData.post_pk}/edit`);
        editBtn.setAttribute('class', 'btn btn-block btn-primary');
        editBtn.setAttribute('data-test', 'edit_button');
        editBtn.textContent = 'Edit Post';
        cardBody.appendChild(editBtn);

        const postCard = document.createElement('div');
        postCard.setAttribute('class', 'card mt-3');
        postCard.appendChild(cardBody); 
        const postLinkElement = document.createElement('a');
        postLinkElement.setAttribute('href', `/posts/${responseData.post_pk}`);
        postLinkElement.appendChild(postCard);
        postContainer.appendChild(postLinkElement);
    }

})
