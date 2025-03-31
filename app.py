from flask import Flask, render_template, request, jsonify
import pyttsx3
import wikipedia
import pywhatkit
import pyautogui
import webbrowser
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
tasks = []

# Initialize TTS engine
engine = pyttsx3.init()


@app.route('/open_app', methods=['POST'])
def open_app():
    data = request.json
    app_name = data.get("app", "").lower()

    app_links = {
        "youtube": "vnd.youtube://",
        "play store": "https://play.google.com/store",
        "instagram": "instagram://user?username=yourusername",  # Replace with actual username
        "whatsapp": "whatsapp://send?phone=+918888888888",  # Replace with actual number
        "snapchat": "snapchat://",
        "chrome": "googlechrome://"
    }

    if app_name in app_links:
        webbrowser.open(app_links[app_name])
        return jsonify({"message": f"Opening {app_name}..."})
    else:
        return jsonify({"error": "App not supported"}), 400


def speak(text):
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Reset the engine after speaking

# Email configuration (update with your email credentials)
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"

def send_email(to_email, subject, message):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    command = request.json['command']
    response = ""

    if "search wikipedia about" in command.lower():
        query = command.lower().replace("search wikipedia about", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            response = summary
        except wikipedia.exceptions.PageError:
            response = "Sorry, I couldn't find anything on Wikipedia."
        except wikipedia.exceptions.DisambiguationError as e:
            response = f"Multiple results found. Please be more specific. {e}"

    elif "search wikipedia" in command.lower():
        query = command.lower().replace("search wikipedia", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            response = summary
        except wikipedia.exceptions.PageError:
            response = "Sorry, I couldn't find anything on Wikipedia."
        except wikipedia.exceptions.DisambiguationError as e:
            response = f"Multiple results found. Please be more specific. {e}"

    elif "search google" in command.lower():
        query = command.lower().replace("search google", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        response = f"Searching Google for {query}."

    elif "play music" in command.lower():
        pywhatkit.playonyt("random music")
        response = "Playing music on YouTube."

    elif "say time" in command.lower():
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The time is {current_time}."

    elif "say date" in command.lower():
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        response = f"Today's date is {current_date}."

    elif "new task" in command.lower():
        task = command.lower().replace("new task", "").strip()
        tasks.append(task)
        response = f"Added task: {task}."

    elif "speak task" in command.lower():
        if tasks:
            response = "Your tasks are: " + ", ".join(tasks)
        else:
            response = "You have no tasks."

    
    elif "who made you" in command.lower() or "who created you" in command.lower():
        response = "I was created by Umang Vaghela."

    elif "who are you" in command.lower():
        response = "I am a Jarvis Assistant."

    elif "hello" in command.lower() or "hi" in command.lower() or "hey" in command.lower():
        response = "Hello, How can I help you?"

    elif "who is the special person for umang" in command.lower():
        response = "His Mom and Dad"

    elif "where does umang study?" in command.lower():
        response = "New LJ Institute of engineering and technology"

    elif "who is the male best friends of umang" in command.lower():
        response = "Madhav, Ansh, Krish, Chandan"

    elif "who is the female best friends of umang" in command.lower():
        response = "Shrushti, Maansi"

    elif "which game umang likes to play?" in command.lower():
        response = "Umang likes to play cricket with friends"

    elif "what does umang like?" in command.lower():
        response = "Playing badminton with special person"


    elif "send whatsapp" in command.lower():
        response = "Please enter the mobile number and message."

    elif "send email" in command.lower():
        response = "Please enter the recipient email, subject, and message."

    elif "open" in command.lower():
        app_name = command.lower().replace("open", "").strip()
        pyautogui.press('win')
        pyautogui.write(app_name)
        pyautogui.press('enter')
        response = f"Opening {app_name}."

    elif "who made you" in command.lower() or "who created you" in command.lower():
        response = "I was created by Umang Vaghela."

    elif "hey how are you" in command.lower() or "how are you" in command.lower():
        response = "Hello, I am fine, how can I help you."

    # else:
    #     response = "Sorry, I didn't understand that command."

    else:  # Agar koi bhi function match nahi hota, to Google pe search karega
        webbrowser.open("https://www.google.com/search?q=" + command)
        response = f"Searching Google for {command}."


    return jsonify({"response": response})

@app.route('/send_whatsapp', methods=['POST'])
def send_whatsapp():
    data = request.json
    mobile_number = data['mobile_number']
    message = data['message']
    try:
        pywhatkit.sendwhatmsg_instantly(mobile_number, message)
        return jsonify({"status": "success", "message": "WhatsApp message sent successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/send_scheduled_whatsapp', methods=['POST'])
def send_scheduled_whatsapp():
    data = request.json
    mobile_number = data['mobile_number']
    message = data['message']
    hours = int(data['hours'])
    minutes = int(data['minutes'])
    try:
        pywhatkit.sendwhatmsg(mobile_number, message, hours, minutes)
        return jsonify({"status": "success", "message": f"WhatsApp message scheduled for {hours}:{minutes}!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/send_email', methods=['POST'])
def send_email_route():
    data = request.json
    to_email = data['to_email']
    subject = data['subject']
    message = data['message']
    if send_email(to_email, subject, message):
        return jsonify({"status": "success", "message": "Email sent successfully!"})
    else:
        return jsonify({"status": "error", "message": "Failed to send email."})

if __name__ == '__main__':
    app.run(debug=True)