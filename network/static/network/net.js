  

  
  document.addEventListener('DOMContentLoaded', function() {

    // likes
    document.querySelectorAll('.lik').forEach(button => {
      button.onclick = function(e) {
        // change number of likes
        fetch(`/like/${e.target.dataset.id}`)
        .then(response => response.json())
        .then(text => {
          (e.target.parentElement.children)[1].innerHTML = text['likes'];
        });
      };
  });

  // update
  document.querySelectorAll('.update').forEach(button => {
    button.onclick = function(e) {
      (e.target.parentElement.children)[1].style.display = 'none';
      (e.target.parentElement.children)[2].style.display = 'none';
      (e.target.parentElement.children)[3].style.display = 'block';
    };
});

document.querySelectorAll('.NewContent').forEach(form => {
  form.onsubmit = function() {
    pid = this.dataset.id;
    newContent = (this.children[0]).children[0].value;
    //update
    fetch('/edit', {
      method: 'POST',
      body: JSON.stringify({
          pid: pid,
          content: newContent
      })
    })
    .then(response => response.json())
    .then(result => {
      ((this.parentElement).parentElement.children)[1].style.display = 'block';
      ((this.parentElement).parentElement.children)[1].style.width= 'fit-content';
      ((this.parentElement).parentElement.children)[2].innerHTML = newContent;
      ((this.parentElement).parentElement.children)[2].style.display= 'block';
      ((this.parentElement).parentElement.children)[3].style.display= 'none';
      console.log(result);
        
    });
    return false;

  };
});

  });

  
