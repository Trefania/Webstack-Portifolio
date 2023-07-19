$(document).ready(() => {
  $('#form1').submit((event) => {
    event.preventDefault();

    submitForm()
  });

  $('#signup').click(() => {
    submitForm()
  });

  function submitForm() {
    const formData = {
      username: $('#username').val(),
      email: $('#email').val(),
      password: $('#password').val()
    };

    $.ajax({
      url: '/api/auth/signup',
      type: 'POST',
      data: formData,
      success: (response) => {
        console.log(response);
        // Redirect to the success page
        window.location.href = 'Login-page/index.html'; 
      },
      error: (error) => {
        console.error(error);
        // Show an error message to the user
        window.location.href = '../main.html';
      }
    });
  }

  //Sign In
  $('#form2').submit((event) => {
    event.preventDefault();

    submitForm2()
  });

  $('#signin').click(() => {
    submitForm2()
  });

  function submitForm2() {
    const formData = {
      email: $('#email2').val(),
      password: $('#password2').val()
    };

    $.ajax({
      url: '/api/auth/login',
      type: 'POST',
      data: formData,
      success: (response) => {
        console.log(response);
        // Redirect to the success page
        window.location.href = 'Login-page/Landing-page/landing-page.html'; 
      },
      error: (error) => {
        console.error(error);
        // Show an error message to the user
        window.location.href = 'Login-page/index.html';
      }
    });
  }
});
