document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      // ... do something else with emails ...
      emails.forEach((email) => {
        const element = document.createElement('div');
        // Add a class to the element
        element.classList.add('mail-item');
        
        email.read ? element.style.backgroundColor='gray' : element.style.backgroundColor='white';

        element.innerHTML = `<p><span class="sender">${email.sender}</span> ${email.subject}</p>
        <p class='time'>${email.timestamp}</p>`;
        element.addEventListener('click', () => load_email(email.id));
        document.querySelector('#emails-view').append(element);  
      })

  });

}

function send_email(event){
  event.preventDefault();
  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;
  
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });
  load_mailbox('sent')

}

function load_email(id){
  document.querySelector('#emails-view').innerHTML = "";
  
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      // ... do something else with email ...
      const element = document.createElement('div');
      // Add a class to the element
      element.classList.add('email-view');
      element.innerHTML = `<p><b>From: </b>${email.sender}</p>
      <p><b>To: </b>${email.recipients}</p>
      <p><b>Subject: </b>${email.subject}</p>
      <p><b>Timestamp: </b>${email.timestamp}</p>
      <hr>
      <p>${email.body}</p>`;
      document.querySelector('#emails-view').append(element);
  });
  //Mark the email as read
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}