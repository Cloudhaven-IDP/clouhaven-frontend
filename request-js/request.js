document.getElementById('requestForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const name = document.getElementById('name').value.trim();
  const email = document.getElementById('email').value.trim();
  const resource = document.getElementById('resource').value.trim();
  const reason = document.getElementById('reason').value.trim();

  const data = { name, email, resource, reason };

  try {
    const response = await fetch('https://your-api-gateway-or-backend.com/request', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    document.getElementById('statusMessage').textContent =
      result.message || 'Request submitted successfully!';
    document.getElementById('requestForm').reset();
  } catch (error) {
    console.error(error);
    document.getElementById('statusMessage').textContent =
      'There was a problem submitting your request. Please try again.';
  }
});
