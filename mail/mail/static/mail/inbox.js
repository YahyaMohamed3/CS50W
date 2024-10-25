document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#new-email').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';


  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Clear previous event listener to avoid multiple submissions
  const composeForm = document.querySelector('#compose-form').addEventListener('submit', send_email);
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#new-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //get emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email =>{
    const newEmail = document.createElement('div');
    newEmail.id = email.id
    newEmail.innerHTML = `
    <h6>Sender: ${email.sender}</h6>
    <p>Subject: ${email.subject}</p>
    <p>Timestamp:${email.timestamp}</p>
    `;
    newEmail.className = email.read ? 'read' : 'unread'
    document.querySelector('#emails-view').append(newEmail);
    newEmail.addEventListener('click',()=> email_view(email.id));
  });
    })

}

function send_email(event) {
  event.preventDefault();

  // Gather email details
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  // Send email using fetch
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
    console.log(result);
    load_mailbox('sent');
  })
}

function email_view(email_id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#new-email').style.display = 'block';

  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      const view_email = document.createElement('div');
      document.querySelector('#new-email').innerHTML = '';

      view_email.innerHTML = `
        <h4>Sender: ${email.sender}</h4>
        <h4>Recipient: ${email.recipients}</h4>
        <h6>Subject: ${email.subject}</h6>
        <p>${email.body}</p>
        <p>${email.timestamp}</p>
        <button class="btn btn-sm btn-outline-primary" id="archive">
          ${email.archived ? 'Unarchive' : 'Archive'}
        </button>
        <button class="btn btn-sm btn-outline-primary"  id="reply">Reply</button>
      `;

      document.querySelector('#new-email').append(view_email);
      document.querySelector('#reply').addEventListener('click' ,()=> reply_email(email.id));
      // Add event listener for archive/unarchive button
      document.querySelector('#archive').addEventListener('click', () => {
        if (!email.archived) {
          // Archive the email
          fetch(`/emails/${email_id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: true
            })
          })
          .then(() => {
            document.querySelector('#archive').innerText = 'Unarchive';
            load_mailbox('inbox')
          });
        } else {
          fetch(`/emails/${email_id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: false
            })
          })
          .then(() => {
            document.querySelector('#archive').innerText = 'Archive';
            load_mailbox('inbox')

          });
        }
      });

      // Mark the email as read if not already read
      if (!email.read) {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        });
      }
    });
}

function reply_email(email_id) {
  fetch(`emails/${email_id}`)
    .then(response => response.json())
    .then(email => {

      // Show the compose view
      compose_email();

      // Pre-fill the recipient field
      document.querySelector("#compose-recipients").value = email.sender;

      // Pre-fill the subject, adding "Re:" if necessary
      const subject_prefix = email.subject.startsWith("Re:") ? "" : "Re: ";
      document.querySelector("#compose-subject").value = `${subject_prefix}${email.subject}`;

      // Pre-fill the body with the original message and details
      const body_content = `On ${email.timestamp}, ${email.sender} wrote:\n${email.body}\n\n`;
      document.querySelector("#compose-body").value = body_content;
    });
}

