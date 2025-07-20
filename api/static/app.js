const submitBtn = document.getElementById('submit-btn');
const outputDiv = document.getElementById('output');
const resourcesInput = document.getElementById('resources');
const promptInput = document.getElementById('prompt');
const modelSelect = document.getElementById('model-select');

submitBtn.addEventListener('click', async () => {
  const prompt = promptInput.value.trim();
  const resources = resourcesInput.value.trim();
  const model = modelSelect.value;
  const x_api_key = "meowbaksh_abracadabra_13491"; 
  if(!prompt || !resources) {
    alert("Please fill both study content and prompt");
    return;
  }

  outputDiv.textContent = "Processing...";
  submitBtn.disabled = true;
  submitBtn.textContent = "Processing...";

  try {
    const formData = new FormData();
    formData.append('prompt', prompt);
    formData.append('resources', resources);
    formData.append('model', model);
    formData.append('x_api_key', x_api_key);

    const res = await fetch('/ask', {
      method: 'POST',
      body: formData
    });

    const data = await res.json();
    if (res.ok) {
      outputDiv.textContent = data.result;
    } else {
      outputDiv.innerHTML = `<span style="color: red;">Error: ${data.detail}</span>`;
    }
  } catch (err) {
    outputDiv.innerHTML = `<span style="color: red;">Request failed: ${err.message}</span>`;
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Process";
  }
});
