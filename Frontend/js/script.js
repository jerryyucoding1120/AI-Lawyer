document.addEventListener('DOMContentLoaded', () => {
    const summarizeButton = document.getElementById('summarizeButton');
    const caseTextInput = document.getElementById('caseTextInput');
    const summaryContainer = document.getElementById('summaryOutput');
    const summaryOutput = summaryContainer.querySelector('p');

    summarizeButton.addEventListener('click', async () => {
        const textToSummarize = caseTextInput.value;

        if (!textToSummarize.trim()) {
            summaryOutput.textContent = 'Please enter some text to analyze.';
            summaryContainer.style.display = 'block'; // Show the container even for an error
            return;
        }

        // Show a loading message
        summaryContainer.style.display = 'block'; // Make container visible
        summaryOutput.textContent = 'Analyzing...';
        summaryContainer.querySelector('h3').style.display = 'none'; // Hide "Summary" title while loading

        try {
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
            summaryContainer.querySelector('h3').style.display = 'block'; // Show title again
            summaryOutput.textContent = data.summary;

        } catch (error) {
            console.error('Error during summarization:', error);
            summaryOutput.textContent = 'Failed to get summary. Make sure the backend server is running.';
        }
    });
});