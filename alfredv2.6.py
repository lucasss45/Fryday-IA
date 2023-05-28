import datetime
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import pywhatkit
import time
import threading
import newsapi
import random

maquina = pyttsx3.init()
voz = maquina.getProperty('voices')
maquina.setProperty('voice', voz[1].id)

def executa_comando():
    try:
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            voz = recognizer.listen(source)
            comando = recognizer.recognize_google(voz, language='pt-BR')
            comando = comando.lower()
            return comando
    except sr.UnknownValueError:
        maquina.say('Não entendi o comando')
        maquina.runAndWait()
    except sr.RequestError as e:
        maquina.say('Desculpe, houve um erro ao processar o comando')
        maquina.runAndWait()
    return ''

def comando_voz_usuario():
    while True:
        comando = executa_comando()

        if 'horas' in comando:
            tempo = datetime.datetime.now().strftime('%H:%M')
            maquina.say('Agora são ' + tempo)
            maquina.runAndWait()
        elif 'procure por' in comando:
            procurar = comando.replace('procure por', '')
            wikipedia.set_lang('pt')
            resultado = wikipedia.summary(procurar, 2)
            maquina.say(resultado)
            maquina.runAndWait()
        elif 'abrir navegador' in comando:
            webbrowser.open('https://www.google.com.br/')
        elif 'pesquise por' in comando:
            pesquisar = comando.replace('pesquise por', '')
            webbrowser.open('https://www.google.com.br/search?q=' + pesquisar)
        elif 'toque' in comando:
            musica = comando.replace('toque', '')
            pywhatkit.playonyt(musica)
            maquina.say('Tocando Música ' + musica)
            maquina.runAndWait()
        elif 'clima' in comando:
            obter_clima()
        elif 'pare de escutar' in comando:
            maquina.say('Por quantos minutos você quer que eu pare de escutar?')
            maquina.runAndWait()
            resposta = executa_comando()
            try:
                tempo = int(resposta)
                maquina.say('Ok, vou parar de escutar por ' + str(tempo) + ' minutos')
                maquina.runAndWait()
                time.sleep(tempo * 60)
                maquina.say('Voltei! O que posso fazer por você?')
                maquina.runAndWait()
            except ValueError:
                maquina.say('Desculpe, não entendi o tempo que você informou')
                maquina.runAndWait()
        elif 'tchau' in comando:
            maquina.say('Tchau!, foi bom te ver')
            maquina.runAndWait()
            break
        elif 'definir alarme' in comando:
            partes = comando.split(' ')
            hora = partes[2]
            mensagem = ' '.join(partes[3:])
            definir_alarme(hora, mensagem)
            maquina.say('Alarme definido para ' + hora + '.')
            maquina.runAndWait()
        elif 'definir lembrete' in comando:
            partes = comando.split(' ')
            tempo_espera = int(partes[2])
            mensagem = ' '.join(partes[3:])
            def alerta():
                time.sleep(tempo_espera)
                maquina.say(mensagem)
                maquina.runAndWait()
            thread = threading.Thread(target=alerta)
            thread.start()
            maquina.say('Lembrete definido para daqui a ' + str(tempo_espera) + ' segundos.')
            maquina.runAndWait()
        elif 'notícias' in comando:
            obter_noticias()
        elif 'piada' in comando:
            contar_piada()
        elif 'ajuda' in comando:
            exibir_ajuda()
        else:
            maquina.say('Comando não reconhecido')
            maquina.runAndWait()

def definir_alarme(hora, mensagem):
    agora = datetime.datetime.now()
    horario_alarme = datetime.datetime.strptime(hora, '%H:%M')
    diferenca = horario_alarme - agora
    segundos = diferenca.seconds

    def alerta():
        time.sleep(segundos)
        maquina.say(mensagem)
        maquina.runAndWait()

    thread = threading.Thread(target=alerta)
    thread.start()

def obter_clima():
    maquina.say('Desculpe, ainda não posso fornecer informações sobre o clima.')
    maquina.runAndWait()

def obter_noticias():
    newsapi = NewsApiClient(api_key='YOUR_NEWS_API_KEY')
    top_headlines = newsapi.get_top_headlines(language='pt')
    articles = top_headlines['articles']
    maquina.say('Aqui estão as principais notícias:')
    maquina.runAndWait()

    for article in articles:
        title = article['title']
        maquina.say(title)
        maquina.runAndWait()

def contar_piada():
    piadas = [
        "Por que a galinha atravessou a rua? Para chegar ao outro lado.",
        "O que o pato disse para a pata? 'Vem Quá!'",
        "Qual é o cúmulo da velocidade? Levantar a mão para pedir licença ao vento.",
        "Por que o livro de matemática cometeu suicídio? Porque tinha muitos problemas.",
        "Qual é o doce preferido do átomo? Pé de moléculas."
    ]
    piada = random.choice(piadas)
    maquina.say(piada)
    maquina.runAndWait()

def exibir_ajuda():
    ajuda = "Aqui estão alguns comandos que você pode usar:\n" \
            "- Horas: para saber a hora atual.\n" \
            "- Procure por [termo]: para pesquisar informações no Wikipedia.\n" \
            "- Abrir navegador: para abrir o navegador padrão.\n" \
            "- Pesquise por [termo]: para pesquisar no Google.\n" \
            "- Toque [música]: para reproduzir uma música no YouTube.\n" \
            "- Clima: para obter informações sobre o clima.\n" \
            "- Pare de escutar: para pausar a escuta por um determinado tempo.\n" \
            "- Tchau: para encerrar o programa.\n" \
            "- Definir alarme [hora] [mensagem]: para definir um alarme.\n" \
            "- Definir lembrete [tempo] [mensagem]: para definir um lembrete.\n" \
            "- Notícias: para obter as principais notícias.\n" \
            "- Piada: para ouvir uma piada.\n" \
            "- Ajuda: para exibir esta mensagem de ajuda."
    maquina.say(ajuda)
    maquina.runAndWait()

comando_voz_usuario()
