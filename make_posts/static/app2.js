const commentContainer = document.querySelector('#comment-container')

document.querySelector('#create_comment').addEventListener('click', (e) => { 
    e.preventDefault();
    const formDataValues = document.querySelector('#comment-add-form');
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
        const commentUser = document.createElement('p');
        commentUser.setAttribute('class', 'badge badge-danger');
        commentUser.textContent = responseData.user
        cardBody.appendChild(commentUser);       
        const commentCreationDate = document.createElement('p');
        commentCreationDate.setAttribute('data-test', 'comment_creation_date');
        commentCreationDate.textContent = `Created: ${responseData.comment_creation}`;
        cardBody.appendChild(commentCreationDate);       
        const commentUpdateDate = document.createElement('p');
        commentUpdateDate.setAttribute('data-test', 'comment_updated_date');
        commentUpdateDate.textContent = `Updated: ${responseData.comment_updated}`;
        cardBody.appendChild(commentUpdateDate);       
        const commentTextContent = document.createElement('p');
        commentTextContent.setAttribute('data-test', 'user-comment');
        commentTextContent.textContent = responseData.comment_content
        cardBody.appendChild(commentTextContent); 
        
        const editBtn = document.createElement('a');
        editBtn.setAttribute('href', `/posts/comments/${responseData.comment_pk}/edit`);
        editBtn.setAttribute('class', 'btn btn-block btn-primary');
        editBtn.setAttribute('data-test', 'edit_button')
        editBtn.textContent = 'Edit Post'
        cardBody.appendChild(editBtn)

        const commentCard = document.createElement('div');
        commentCard.setAttribute('class', 'card mt-3');
        commentCard.appendChild(cardBody);
        commentContainer.appendChild(commentCard)
    }

})