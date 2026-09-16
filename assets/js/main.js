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

  initLeadForm();
});

// ---------------------------------------------------------------------------
// Lead form
//
// The form is marked up to work out of the box the moment this site is
// deployed on Netlify (data-netlify="true" + a hidden form-name field is
// all Netlify Forms needs — no account setup beyond hosting there, and
// submissions show up in the Netlify dashboard and can be emailed to you).
//
// Until then, or if you deploy somewhere else, this script tries a plain
// form POST first; if that has nowhere to land (any host without form
// handling), it falls back to opening the visitor's email client with the
// details pre-filled, so a submission is never silently lost.
//
// To switch to a different form backend (Formspree, a CRM endpoint, etc.),
// just change the form's `action` attribute in build/build.py — this
// script's fetch-then-fallback logic will keep working unchanged.
// ---------------------------------------------------------------------------
function initLeadForm() {
  var form = document.querySelector('#lead-form');
  if (!form) return;

  var statusEl = form.querySelector('.form-status');
  var submitBtn = form.querySelector('button[type="submit"]');

  function setStatus(text) {
    if (statusEl) statusEl.textContent = text;
  }

  function mailtoFallback(data) {
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
    setStatus('Opening your email app to send this to SMAC…');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var data = new FormData(form);
    var action = form.getAttribute('action') || '/';

    if (submitBtn) submitBtn.disabled = true;
    setStatus('Sending…');

    fetch(action, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(data).toString(),
    })
      .then(function (res) {
        if (res.ok) {
          form.reset();
          setStatus('Thanks! We’ll be in touch soon.');
        } else {
          mailtoFallback(data);
        }
      })
      .catch(function () {
        // No form backend at this URL (e.g. not hosted on Netlify yet) —
        // fall back to email so the lead still reaches SMAC.
        mailtoFallback(data);
      })
      .finally(function () {
        if (submitBtn) submitBtn.disabled = false;
      });
  });
}
