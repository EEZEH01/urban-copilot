// Urban Copilot Frontend Application

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatContainer = document.getElementById('chatContainer');
    const questionForm = document.getElementById('questionForm');
    const questionInput = document.getElementById('questionInput');
    const submitButtonText = document.getElementById('submitButtonText');
    const loadingSpinner = document.getElementById('loadingSpinner');
    
    // Event Listeners
    questionForm.addEventListener('submit', handleQuestionSubmit);
    
    // Display initial message
    scrollToBottom();
    
    // Function to handle question submission
    async function handleQuestionSubmit(event) {
        event.preventDefault();
        
        // Get the question from the input
        const question = questionInput.value.trim();
        
        // Validate input
        if (!question) {
            displayErrorMessage('Please enter a question.');
            return;
        }
        
        // Display user message
        displayUserMessage(question);
        
        // Clear input field
        questionInput.value = '';
        
        // Show loading state
        setLoadingState(true);
        
        try {
            // Send request to the API
            const response = await fetchAnswer(question);
            
            // Display assistant message
            displayAssistantMessage(response.response || response.message);
        } catch (error) {
            console.error('Error:', error);
            displayErrorMessage('Sorry, there was an error processing your request. Please try again.');
        } finally {
            // Hide loading state
            setLoadingState(false);
        }
    }
    
    // Function to fetch answer from API
    async function fetchAnswer(question) {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question }),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
    
    // Function to display user message
    function displayUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'user-message';
        messageElement.innerHTML = `<p>${escapeHtml(message)}</p>`;
        chatContainer.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Function to display assistant message
    function displayAssistantMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'assistant-message';
        messageElement.innerHTML = `<p>${escapeHtml(message)}</p>`;
        chatContainer.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Function to display error message
    function displayErrorMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'error-message';
        messageElement.innerHTML = `<p>${escapeHtml(message)}</p>`;
        chatContainer.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Function to set loading state
    function setLoadingState(isLoading) {
        submitButtonText.textContent = isLoading ? '' : 'Send';
        loadingSpinner.classList.toggle('d-none', !isLoading);
        questionInput.disabled = isLoading;
    }
    
    // Function to scroll to bottom of chat
    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // Function to escape HTML to prevent XSS
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});
