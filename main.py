import datetime
import os

from google.cloud import texttospeech
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QMainWindow,
    QProgressDialog,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

if not os.path.exists("tts"):
    os.makedirs("tts")


class TTSApp(QMainWindow):
    def __init__(self):
        super().__init__()

        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"
        ] = "your_api_key.json" # https://cloud.google.com/speech-to-text/docs/before-you-begin#create_a_service_account

        self.client = texttospeech.TextToSpeechClient()

        self.media_player = QMediaPlayer(self)
        self.media_playlist = QMediaPlaylist(self.media_player)
        self.media_player.setPlaylist(self.media_playlist)

        self.setWindowTitle("Text-to-Speech")
        self.setGeometry(100, 100, 500, 200)
        self.setCentralWidget(QWidget(self))

        layout = QVBoxLayout()
        self.centralWidget().setLayout(layout)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.text_field = QTextEdit(self)
        self.synth_button = QPushButton("Synthesize", self)
        self.synth_button.clicked.connect(self.synthesize)
        self.synth_button.setMinimumHeight(30)
        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play)
        self.play_button.setMinimumHeight(30)
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setMinimumHeight(30)

        layout.addWidget(self.text_field)
        layout.addWidget(self.synth_button)
        layout.addWidget(self.play_button)
        layout.addWidget(self.stop_button)

        self.file_path = ""

    def synthesize(self):
        progress_dialog = QProgressDialog(
            "Synthesizing speech...", "Cancel", 0, 0, self
        )
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.show()
        text = self.text_field.toPlainText()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-J",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        now = datetime.datetime.now()
        timestamp = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
        filename = f"output_{timestamp}.mp3"
        self.file_path = os.path.join("tts", filename)
        with open(self.file_path, "wb") as out:
            out.write(response.audio_content)
            print(f'Audio content written to file "{filename}"')
        self.play_button.setEnabled(True)
        self.media_playlist.clear()
        self.media_playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.file_path)))
        progress_dialog.close()

    def play(self):
        self.media_playlist.clear()
        self.media_playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.file_path)))
        self.media_player.play()

    def stop(self):
        self.media_player.stop()


if __name__ == "__main__":
    app = QApplication([])
    tts_app = TTSApp()
    tts_app.show()
    app.exec_()
