document.addEventListener('DOMContentLoaded', () => {
    const summarizeButton = document.getElementById('summarizeButton');
    const caseTextInput = document.getElementById('caseTextInput');
    const summaryOutput = document.getElementById('summaryOutput').querySelector('p');

    summarizeButton.addEventListener('click', async () => {
        const textToSummarize = caseTextInput.value;

        // Basic validation: Check if there is text to summarize
        if (!textToSummarize.trim()) {
            summaryOutput.textContent = 'Please enter some text to summarize.';
            return;
        }

        // Show a loading message
        summaryOutput.textContent = 'Summarizing...';

        try {
            // This is the URL of your local Flask backend.
            const response = await fetch('http://127.0.0.1:5001/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: textToSummarize }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Display the summary received from the backend
            summaryOutput.textContent = data.summary;

        } catch (error) {
            console.error('Error during summarization:', error);
            summaryOutput.textContent = 'Failed to get summary. Make sure the backend server is running.';
        }
    });
});