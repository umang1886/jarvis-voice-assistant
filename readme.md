# JARVIS Voice Assistant
A Flask-based web application for a voice command assistant similar to JARVIS. It supports both voice and text input, and responds with voice output and displayed text.

## Features
- Voice and text input options.
- Text-to-speech (TTS) responses.
- Commands like:
  - Search Wikipedia
  - Search Google
  - Play Music
  - Say Time and Date
  - Manage To-Do List
  - Open Applications
  - Send WhatsApp Messages
  - Send Emails

  ## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/jarvis-voice-assistant.git
   ```
2. Navigate to the project directory:
   ```bash
   cd jarvis-voice-assistant
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask application:
   ```bash
   python app.py
   ```
5. Open your browser and go to `http://127.0.0.1:5000`.

## Usage
- Use the microphone button to give voice commands.
- Type commands in the text input field and click "Submit".
- The assistant will respond with voice output and display the response on the webpage.

## Available Commands
| Command                 | Function                                      | Example Usage                   |
|-------------------------|-----------------------------------------------|---------------------------------|
| "Search Wikipedia {q}"  | Fetches a short summary from Wikipedia       | "Search Wikipedia Albert Einstein" |
| "Search Google {q}"     | Opens Google search for the given query      | "Search Google latest tech news" |
| "Play Music"            | Opens a random YouTube music video           | "Play Music"                     |
| "Send WhatsApp"         | Sends a WhatsApp message (asks for input)    | "Send WhatsApp"                  |
| "Send Email"            | Sends an email (asks for input)              | "Send Email"                     |
| "Open {app}"            | Opens a specified application                | "Open Notepad"                   |

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credits
- [Flask](https://flask.palletsprojects.com/) - Web framework.
- [pyttsx3](https://pypi.org/project/pyttsx3/) - Text-to-speech library.
- [Bootstrap](https://getbootstrap.com/) - Frontend styling.



http://127.0.0.1:5000/