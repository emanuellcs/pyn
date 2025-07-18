const originalFetch = window.fetch;

window.fetch = function (url, options) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    if (options && options.headers) {
        options.headers['X-CSRFToken'] = csrfToken;
    } else if (options) {
        options.headers = { 'X-CSRFToken': csrfToken };
    } else {
        options = { headers: { 'X-CSRFToken': csrfToken } };
    }

    return originalFetch(url, options);
};
document.addEventListener('DOMContentLoaded', function() {
    const generateButton = document.getElementById('generate-password-button');
    const passwordGeneratorForm = document.getElementById('password-generator-form');
    const passwordOutput = document.getElementById('password-output');
    const analysisContainer = document.querySelector('.analysis-container');
    const resultContainer = document.querySelector('.result-container');

    if (generateButton && passwordGeneratorForm) {
        generateButton.addEventListener('click', function() {
            const url = passwordGeneratorForm.dataset.url;
            const length = document.getElementById('length').value;
            const useUpper = document.getElementById('use_upper').checked;
            const useLower = document.getElementById('use_lower').checked;
            const useDigits = document.getElementById('use_digits').checked;
            const useSpecial = document.getElementById('use_special').checked;

            const formData = {
                length: parseInt(length),
                use_upper: useUpper,
                use_lower: useLower,
                use_digits: useDigits,
                use_special: useSpecial
            };

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Response data:', data);
                if (data.error) {
                    alert('Error: ' + data.error);
                    if (resultContainer) resultContainer.style.display = 'none';
                    return;
                }
                
                console.log('Password output element:', passwordOutput);
                if (passwordOutput) {
                    passwordOutput.value = data.password_result;
                    console.log('Set password value to:', data.password_result);
                } else {
                    console.error('Could not find password output element');
                }

                if (resultContainer) {
                    resultContainer.style.display = 'block';
                    console.log('Result container display set to block');
                } else {
                    console.error('Could not find result container element');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during password generation.');
                if (resultContainer) resultContainer.style.display = 'none';
            });
        });
    }
});