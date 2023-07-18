$(document).ready(() => {
  //Sign In
  $('#login').submit((event) => {
    event.preventDefault();

    submitForm2()
  });

  function submitForm2() {
    const formData = {
      email: $('#user').val(),
      password: $('#pass').val()
    };

    $.ajax({
      url: '/api/auth/login',
      type: 'POST',
      data: formData,
      success: (response) => {
        console.log(response);
        // Redirect to the success page
        window.location.href = 'Landing-page/landing-page.html'; 
      },
      error: (error) => {
        console.error(error);
        // Show an error message to the user
        window.location.href = './index.html';
      }
    });
  }
});
