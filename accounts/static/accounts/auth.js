window.switchTo = function switchTo(mode) {
  document.getElementById('auth-box').classList.toggle('signup-mode', mode === 'signup');
}

document.addEventListener('DOMContentLoaded', () => {
  const passwordInput = document.querySelector('input[name="password1"]');
  const confirmPasswordInput = document.querySelector('input[name="password2"]');

  if (passwordInput) {
    passwordInput.addEventListener('focus', () => {
      document.getElementById('password-conditions').classList.remove('hidden');
    });
    passwordInput.addEventListener('input', validatePassword);
  }
  if (confirmPasswordInput) {
    confirmPasswordInput.addEventListener('blur', () => {
      const p1 = passwordInput.value;
      const p2 = confirmPasswordInput.value;
      if (p1 !== p2) {
        confirmPasswordInput.value = '';
        document.getElementById('password-match-error').classList.remove('hidden');
      } else {
        document.getElementById('password-match-error').classList.add('hidden');
      }
    });
    confirmPasswordInput.addEventListener('input', () => {
      document.getElementById('password-match-error').classList.add('hidden');
    });
  }

  const signupEmailInput = document.getElementById('signup-email');
  if (signupEmailInput) {
    signupEmailInput.addEventListener('blur', async () => {
      const email = signupEmailInput.value;
      if (!email) return;
      try {
        const response = await fetch(`/check-email/?email=${encodeURIComponent(email)}`);
        if (response.ok) {
          const data = await response.json();
          document.getElementById('email-error').classList.toggle('hidden', !data.exists);
        }
      } catch (e) {
        console.error(e);
      }
    });
  }
});

function validatePassword() {
  const password = this.value;
  const conditions = {
    length: password.length >= 8,
    letter: /[a-zA-Z]/.test(password),
    number: /\d/.test(password),
    special: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)
  };
  Object.keys(conditions).forEach(key => {
    const element = document.getElementById(key);
    if (element) {
      element.className = conditions[key] ? 'text-green-500' : 'text-red-500';
    }
  });
}

// Auto-switch if URL hash is #signup
if (window.location.hash === '#signup') switchTo('signup');
