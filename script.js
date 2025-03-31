document.addEventListener('DOMContentLoaded', function() {
    const tasks = [];
    
    // Voice recognition setup
    document.getElementById('voice-btn').addEventListener('click', () => {
        const listeningIndicator = document.getElementById('listening-indicator');
        const voiceBtn = document.getElementById('voice-btn');
        
        // Show listening state
        voiceBtn.innerHTML = '<i class="fas fa-microphone-slash"></i> Listening...';
        voiceBtn.classList.remove('btn-primary');
        voiceBtn.classList.add('btn-warning');
        listeningIndicator.style.display = 'flex';
        
        // Check if browser supports speech recognition
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert("Speech recognition not supported in your browser. Try Chrome or Edge.");
            resetVoiceButton();
            return;
        }
        
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.start();
        
        recognition.onresult = (event) => {
            const command = event.results[0][0].transcript;
            document.getElementById('command-input').value = command;
            sendCommand(command);
            resetVoiceButton();
        };
        
        recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            alert("Error occurred in recognition: " + event.error);
            resetVoiceButton();
        };
        
        recognition.onend = () => {
            resetVoiceButton();
        };
        
        function resetVoiceButton() {
            voiceBtn.innerHTML = '<i class="fas fa-microphone"></i> Speak';
            voiceBtn.classList.remove('btn-warning');
            voiceBtn.classList.add('btn-primary');
            listeningIndicator.style.display = 'none';
        }
    });
    
    // Submit command
    document.getElementById('submit-btn').addEventListener('click', () => {
        const command = document.getElementById('command-input').value.trim();
        if (command) {
            sendCommand(command);
        }
    });
    
    // Enter key to submit (but allow Shift+Enter for new lines)
    document.getElementById('command-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            document.getElementById('submit-btn').click();
        }
    });
    
    // Show/hide schedule time fields
    document.querySelectorAll('input[name="whatsappOption"]').forEach(radio => {
        radio.addEventListener('change', function() {
            document.getElementById('schedule-time').style.display = 
                this.value === 'scheduled' ? 'block' : 'none';
        });
    });
    
    // Handle WhatsApp message sending
    document.getElementById('send-whatsapp-btn').addEventListener('click', sendWhatsAppMessage);
    
    // Handle Email sending
    document.getElementById('send-email-btn').addEventListener('click', sendEmail);
});

function sendCommand(command) {
    fetch('/process_command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command: command }),
    })
    .then(response => response.json())
    .then(data => {
        const responseDiv = document.getElementById('response');
        responseDiv.innerHTML = `<strong>Response:</strong> ${data.response}`;

        const utterance = new SpeechSynthesisUtterance(data.response);
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);

        if (command.toLowerCase().includes("send whatsapp")) {
            document.getElementById('whatsapp-form').style.display = 'block';
            document.getElementById('email-form').style.display = 'none';
        }

        if (command.toLowerCase().includes("send email")) {
            document.getElementById('email-form').style.display = 'block';
            document.getElementById('whatsapp-form').style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing the command.');
    });
}

function sendWhatsAppMessage() {
    const mobileNumber = document.getElementById('mobile-number').value;
    const message = document.getElementById('whatsapp-message').value;
    const isScheduled = document.getElementById('scheduledWhatsapp').checked;
    
    if (!mobileNumber || !message) {
        alert('Please enter both mobile number and message');
        return;
    }

    if (isScheduled) {
        const hours = document.getElementById('schedule-hours').value;
        const minutes = document.getElementById('schedule-minutes').value;
        
        if (!hours || !minutes) {
            alert('Please enter both hours and minutes for scheduling');
            return;
        }

        fetch('/send_scheduled_whatsapp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                mobile_number: mobileNumber, 
                message: message,
                hours: hours,
                minutes: minutes
            }),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            document.getElementById('whatsapp-form').style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to schedule WhatsApp message');
        });
    } else {
        fetch('/send_whatsapp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                mobile_number: mobileNumber, 
                message: message 
            }),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            document.getElementById('whatsapp-form').style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to send WhatsApp message');
        });
    }
}

function sendEmail() {
    const toEmail = document.getElementById('to-email').value;
    const subject = document.getElementById('email-subject').value;
    const message = document.getElementById('email-message').value;

    if (!toEmail || !subject || !message) {
        alert('Please fill all email fields');
        return;
    }

    fetch('/send_email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ to_email: toEmail, subject: subject, message: message }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('email-form').style.display = 'none';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to send email');
    });
}