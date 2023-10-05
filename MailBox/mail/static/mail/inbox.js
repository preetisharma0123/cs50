document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', submit);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}


function load_email(id){
   fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {

    console.log(email);

    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
 
    document.querySelector('#email-view').innerHTML = `
    <div>
    <ul class=" list-group-item " style="list-style-type:none;">
      <li ><strong>From:</strong> ${email.sender}</li>
      <li><strong>To:</strong> ${email.recipients}</li>
      <li><strong>Subject:</strong> ${email.subject}</li>      
      <li><strong>Timestamp:</strong> ${email.timestamp}</li>
      </br>
      <li>${email.body}</li>
      </br></ul>
      </div>
    
    `

      // mark as read 
    if(!email.read){
      fetch(`/emails/${email['id']}`, {
        method: 'PUT',
        body: JSON.stringify({
        read: true
        })
      });
      }

    // mark as unread 

    const buttonUnread = document.createElement('button');
    buttonUnread.innerHTML = "Unread";
    buttonUnread.className = "btn btn-primary";
    buttonUnread.addEventListener('click', function() {
      fetch(`/emails/${email['id']}`, {
        method: 'PUT',
        body: JSON.stringify({ read : false })
      })

        .then(response => {
          console.log(response);
          load_mailbox('inbox');
      })
      });
    document.querySelector('#email-view').append(buttonUnread);
   

    // Archive/Unarchive logic
    const buttonArchive = document.createElement('button');
    buttonArchive.innerHTML = email.archived ? "Unarchive" : "Archive";
    buttonArchive.className = email.archived ? "d-grid gap-2 d-md-flex justify-content-md-end btn btn-outline-info my-2 " : "d-grid gap-2 d-md-flex justify-content-md-end btn btn-danger my-2";
    buttonArchive.addEventListener('click', function() {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !email.archived
        })
      })
      .then(() => {load_mailbox('archive')})
    });
    document.querySelector('#email-view').append(buttonArchive);


    // Reply logic
    const buttonReply = document.createElement('button');
    buttonReply.innerHTML = "Reply"
    buttonReply.className = "btn btn-success my-2 d-grid gap-2 d-md-block"
    buttonReply.addEventListener('click', function() {
      compose_email();

      document.querySelector('#compose-recipients').value = email['sender'];
      let subject = email['subject'];
      if(subject.split(' ', 1)[0] != "Re:") {
        subject =  `Re: ${email['subject']}`;  
      }
      document.querySelector('#compose-subject').value = subject;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email['sender']} wrote: ${email['body']}`;
    });
    document.querySelector('#email-view').append(buttonReply);
    
  })
}

  

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
 
  const view = document.querySelector('#emails-view');   


  // Show the mailbox name
  view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
       
  // get the emails from the mailbox 
    
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {






  // loop through each email

    emails.forEach(email => {
      const newEmail = document.createElement('div');
      newEmail.className = "row border border-black"; 
      const otherHTML =  `
  <div class="col-3"><strong>From: ${email['sender']}</strong></div>
  <div class="col-6"><div class="row">${email['subject']}</div></div>
  <div class="col-3">${email['timestamp']}</div>

      `;
      const sentHTML = `
  <div class="col-3"><strong>To: ${email['recipients']}</strong></div>
  <div class="col-6"><div class="row">${email['subject']}</div></div>
  <div class="col-3">${email['timestamp']}</div>

      `;

      newEmail.innerHTML = mailbox == 'sent' ? sentHTML: otherHTML;

  // change background color 
      newEmail.className = email.read ? 'row border border-black  read': 'row border border-black unread';


  // add click event to email

      view.append(newEmail);
      newEmail.addEventListener('click', () => load_email(email['id']));

    })
    });
  }

function submit(event){

  event.preventDefault();

  fetch('/emails', {
  method: 'POST',
  body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
   })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent')
  });
}