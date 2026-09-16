// Mobile nav toggle
document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.primary-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var isOpen = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }

  // On small screens, tapping a "has-dropdown" label toggles its submenu
  // instead of navigating immediately.
  document.querySelectorAll('.has-dropdown > a').forEach(function (link) {
    link.addEventListener('click', function (e) {
      if (window.matchMedia('(max-width: 940px)').matches) {
        var parent = link.parentElement;
        if (!parent.classList.contains('is-open')) {
          e.preventDefault();
          parent.classList.add('is-open');
        }
      }
    });
  });

  // Close mobile nav after choosing a leaf link
  document.querySelectorAll('.primary-nav a:not(.has-dropdown > a)').forEach(function (link) {
    link.addEventListener('click', function () {
      nav.classList.remove('is-open');
    });
  });

  // Lead form -> opens the visitor's email client with a prefilled message.
  // This site has no backend, so this is a lightweight, honest fallback
  // until the form is wired to a real CRM/email service.
  var leadForm = document.querySelector('#lead-form');
  if (leadForm) {
    leadForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = new FormData(leadForm);
      var name = [data.get('first_name'), data.get('last_name')].filter(Boolean).join(' ');
      var program = data.get('program') || 'Not specified';
      var phone = data.get('phone') || 'Not provided';
      var email = data.get('email') || '';
      var subject = encodeURIComponent('Free trial request — ' + (name || 'New lead'));
      var body = encodeURIComponent(
        'Name: ' + name + '\n' +
        'Phone: ' + phone + '\n' +
        'Email: ' + email + '\n' +
        'Program of interest: ' + program + '\n'
      );
      window.location.href = 'mailto:scottsdalemartialartscenter@gmail.com?subject=' + subject + '&body=' + body;
      leadForm.reset();
      var note = leadForm.querySelector('.form-status');
      if (note) note.textContent = 'Opening your email app to send this to SMAC…';
    });
  }
});
