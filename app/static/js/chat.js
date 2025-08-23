document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('.sidebar');
    const toggleSidebarBtn = document.querySelector('.toggle-sidebar');
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const fileUpload = document.getElementById('fileUpload');
    const chatHistory = document.getElementById('chatHistory');
    
    // Toggle sidebar
    toggleSidebarBtn.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
    });
    
    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    // File upload feedback
    fileUpload.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            const fileName = e.target.files[0].name;
            messageInput.value = `Uploaded: ${fileName}`;
            
            // Simulate sending the file
            setTimeout(() => {
                addMessage('Uploaded lecture notes for summarization...', 'user');
                
                // Simulate AI response
                setTimeout(() => {
                    addMessage('I\'ve analyzed your lecture notes on "Introduction to Machine Learning". Here\'s a summary:\n\nMachine learning is a subset of AI that focuses on systems that learn from data. Types: supervised, unsupervised, and reinforcement learning.', 'ai');
                }, 1500);
            }, 500);
        }
    });
    
    // Form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            messageInput.value = '';
            messageInput.style.height = 'auto';
            
            // Simulate AI response
            setTimeout(() => {
                addMessage('I can help you summarize lecture notes. Upload your document using the paperclip icon, or describe what you need help with.', 'ai');
            }, 1000);
        }
    });
    
    // Add message to chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender + '-message');
        messageDiv.textContent = text;
        
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    
    // Initial greeting
    setTimeout(() => {
        addMessage('Hello Joseph! I\'m ready to help summarize your lecture notes. Upload a document or ask me questions.', 'ai');
    }, 500);
});

