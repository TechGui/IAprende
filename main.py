import streamlit as st
from dotenv import load_dotenv
import os
import pyaudio
import speech_recognition as sr
import google.generativeai as gen_ai

# Configure Streamlit page settings
st.set_page_config(
    page_title="IAprende - Aprenda Inglês com a Inteligência do Futuro.",
    page_icon="src/assets/IAprende.ico",
    layout="centered",
)

# Defining  variables
load_dotenv()
IAprende_logo = "src/assets/e.png"
IAprende_Teacher = "src/assets/IAprendeTeacher1.jpg"
IAprende_img = "src/assets/IAprendeTeacher2.jpg"
user_img = "src/assets/user.png"
microphone = ("src/assets/microphone.png")

# Set up Google Gemini model
gen_ai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]
system_instruction = "-Se passe por um professor robôzinho Brasileiro de Inglês, chamado Shemuiya e que responde formalmente e corrige o usuário quando necessário, para ensina-lo inglês e realizar práticas de estudos. E as vezes use poucas palavras e seja direto para não poluir a interface.\n-Ao usuário digitar qualquer coisa pela primeira vez, você dê boas vindas, se introduza dizendo somos da IAprende, com uma variação dizendo que é um robô virtual Brasileiro e que irá servir como seu guia para destravar seu inglês, falando de que poderá falar com a IAprende de qualquere lugar e qualquer horário que desejar. Só use um emoji e de vez em quando somente.\n-Outro exemplo: Se o usuário escrever uma frase incorreta gramaticalmente, você corrija-o em português como que se escreve corretamente.\n-Se o usuário perguntar sobre conversar por ex: Vamos praticar, quero conversar, quero treinar, você responde que tipo de conversa, informal ou formal? e inicie uma conversa sobre qualquer assunto com ele após a escolha, até ele dizer que não quer mais como: Ok, Pare, Vamos parar.\n-Se o usuário pedir uma lista de exercícios, você pergunta sobre o que você quer a prova e após a escolha, crie uma lista com 10 exercícios e 10 respostas mas que só mostre as respostas se o usuário pedir.\n-Se ele pedir seu nome, responda que você é a IAprende, uma Inteligência Artificial, explicando seu propósito.\n-Jamais use palavras agressivas ou de baixo calão, porém mantenha um certo nível de humor com um toque de futurismo em relação a atualidade com o futuro do usuário de vez em quando.\n-As vezes, você pode perguntar se o usuário está gostando de conversar com você e se está aprendendo algo, para manter a conversa mais interativa."


model = gen_ai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

# Function to translate roles between Gemini and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    
# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[{'role':'model', 'parts': [model.generate_content("Você pode falar: Como posso te ajudar hoje, humano..?").text]}])
    
# Display the chatbot's title on the page
with open("style.css") as css:
  st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

## Display the header
st.markdown("<h2 id='title' style='font-family: Michroma; font-weight: 100;'><span id='title-style'>IA</span>prende - Aprenda Inglês com a Inteligência do Futuro.</h2>", unsafe_allow_html=True)

## Espaçamento
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")

# Load text
text = "Olá <span id='subtitle-style'>humano!</span> Eu faço parte da monitoria da IAprende e tô animado(a) pra te apresentar o nosso incrível Professor logo abaixo! Seja você um expert experiente ou esteja começando sua jornada de aprendizado, nosso Professor tá aqui pra te guiar em cada passo. P.s.: Não precisa ter medo! É só chamá-lo a qualquer momento, ele vai adorar te ajudar."

# Create card layout with columns
col1, col2 = st.columns([1, 2])

# Display image in the left column
with col1:
    st.image(IAprende_img, width=200, caption="IAprende's Teacher")

# Display text in the right column
with col2:
  st.markdown(f"<p style='font-family: Montserrat;'>{text}</p>", unsafe_allow_html=True)

# Display the divider
st.divider()

# Display the chat history
for message in st.session_state.chat_session.history:
    avatar = IAprende_Teacher if translate_role_for_streamlit(message.role) == "assistant" else user_img
    with st.chat_message(translate_role_for_streamlit(message.role), avatar=avatar):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Digite aqui sua mensagem...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user", avatar=user_img).markdown(user_prompt)

    # Send user's message to Gemini and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini's response
    with st.chat_message("assistant", avatar=IAprende_Teacher):
        st.markdown(gemini_response.text)

# Function to convert speech to text
def speech_to_text():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    st.write("Listening...")
    audio = r.listen(source)
  try:
    text = r.recognize_google(audio, language="pt-BR,en-US")
    return text
  except sr.UnknownValueError:
    st.write("Sorry, I could not understand your speech.")
    return ""
  except sr.RequestError as e:
    st.write(f"Sorry, an error occurred while processing your speech: {e}")
    return ""


# Get user's speech input
if st.button("Speak 🎙", key="speak_button"):
    user_speech = speech_to_text()
else:
    user_speech = ""

# Add user's speech to chat and display it
if user_speech:
  st.chat_message("user", avatar=user_img).markdown(user_speech)

  # Send user's speech to Gemini and get the response
  gemini_response = st.session_state.chat_session.send_message(user_speech)

  # Display Gemini's response
  with st.chat_message("assistant", avatar=IAprende_Teacher):
    st.markdown(gemini_response.text)

# Display the footer
st.markdown(f"<p id='footer' style='font-family: Montserrat; font-size: 12px; color: #8c8c8c;'>Desenvolvido por <a href='https://github.com/TechGui' target='_blank'>Guilherme da Rosa Silva</a> com a ajuda da <a href='https://www.linkedin.com/school/aluracursos/?originalSubdomain=br' target='_blank'>Alura</a> e <a href='https://www.linkedin.com/company/google/' target='_blank'>Google</a>.</p>", unsafe_allow_html=True)
