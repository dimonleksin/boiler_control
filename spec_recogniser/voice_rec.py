#from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import wave  # создание и чтение аудиофайлов формата wav
import json  # работа с json-файлами и json-строками
import os  # работа с файловой системой
import requests
import settings
import voice_rec as vr


def record_and_recognize_audio(*args: tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""

        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        # использование online-распознавания через Google 
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит попытка 
        # использовать offline-распознавание через Vosk
        except speech_recognition.RequestError:
            print("Trying to use offline recognition...")

        return recognized_data

def listen_comand(recognized_data):
    print("Слушаю Вас")
    comand = record_and_recognize_audio()
    match comand:
        case "Какая температура":
            resultGetTemp = requests.get(f"{settings.main_url}/gettemp")
            pars = json.loads(BeautifulSoup(resultGetTemp.text, "html.parser").string)
            tempBoiler = pars["tempBoiler"]    
            vr.play(f"Current temperature in boiler room {tempBoiler}")
        case "Что с первым котлом":
            result = requests.get(f"{settings.main_url}/get-status?number=1")
            pars = json.loads(BeautifulSoup(resultGetTemp.text, "html.parser").string)
            vr.play(pars["boiler_1_status"])
        case "Что со вторым котлом":
            result = requests.get(f"{settings.main_url}/get-status?number=2")
            pars = json.loads(BeautifulSoup(resultGetTemp.text, "html.parser").string)
            vr.play(pars["boiler_2_status"])
        case "Включи первый котел":
            result = requests.get(f"{settings.main_url}/set-status?number=1,status=1")
            pars = json.loads(BeautifulSoup(resultGetTemp.text, "html.parser").string)
            vr.play(pars["boiler_1_status"])
        case "Включи второй котел":
            result = requests.get(f"{settings.main_url}/set-status?number=2,status=1")
            pars = json.loads(BeautifulSoup(resultGetTemp.text, "html.parser").string)
            vr.play(pars["boiler_2_status"])
        case "Выключи первый котел":
            result = requests.get(f"{settings.main_url}/set-status?number=1,status=0")
            pars = json.loads(BeautifulSoup(resultGetTemp.text, "html.parser").string)
            vr.play(pars["boiler_1_status"])
        case "Выключи второй котел":
            result = requests.get(f"{settings.main_url}/set-status?number=2,status=0")
            pars = json.loads(BeautifulSoup(resultGetTemp.text, "html.parser").string)
            vr.play(pars["boiler_2_status"])
    return

if __name__ == "__main__":

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    while True:
        # старт записи речи с последующим выводом распознанной речи
        # и удалением записанного в микрофон аудио
        voice_input = record_and_recognize_audio()
        os.remove("microphone-results.wav")
        if voice_input == 'дом':
            print(voice_input)
            vr.play("listening for you")
            listen_comand(voice_input)
        print(voice_input)
        