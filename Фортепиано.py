import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6 import QtMultimedia


class PianoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Виртуальное пианино")
        self.setFixedSize(800, 400)
        self._audio_output = QtMultimedia.QAudioOutput()
        self._player = QtMultimedia.QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)
        self._audio_output.setVolume(50)

        self.sounds = {}
        self.init_sounds()

        self.init_ui()

    def init_sounds(self):
        notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B',
                 'C#', 'D#', 'F#', 'G#', 'A#']

        for note in notes:
            sound = QSoundEffect()
            sound.setSource(QUrl.fromLocalFile(f"sounds/{note}.wav"))
            self.sounds[note] = sound

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.white_keys = {}
        self.black_keys = {}

        white_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        black_notes = ['C#', 'D#', 'F#', 'G#', 'A#']

        black_positions = [1, 2, 4, 5, 6]

        keys_layout = QHBoxLayout()
        keys_layout.setSpacing(0)

        for i, note in enumerate(white_notes):
            btn = QPushButton(note)
            btn.setFixedSize(80, 300)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white; 
                    border: 1px solid black;
                }
                QPushButton:pressed {
                    background-color: #ddd;
                }
            """)
            btn.clicked.connect(lambda checked, n=note: self.play_note(n))
            self.white_keys[note] = btn
            keys_layout.addWidget(btn)

        for i, note in enumerate(black_notes):
            btn = QPushButton(note)
            btn.setFixedSize(50, 180)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: black; 
                    color: white;
                }
                QPushButton:pressed {
                    background-color: #555;
                }
            """)
            btn.clicked.connect(lambda checked, n=note: self.play_note(n))
            self.black_keys[note] = btn

            keys_layout.insertWidget(black_positions[i], btn)
            btn.raise_()

        main_layout.addLayout(keys_layout)

        label = QPushButton("Используйте клавиши A,S,D,F,G,H,J для белых клавиш и W,E,T,Y,U для черных")
        label.setStyleSheet("background-color: lightgray; border: none;")
        label.setFlat(True)
        label.clicked.connect(self.show_help)
        main_layout.addWidget(label)

    def play_note(self, note):
        if note in self.sounds:
            self.sounds[note].play()

    def show_help(self):
        help_text = ("Управление:\n"
                     "Белые клавиши: A (C), S (D), D (E), F (F), G (G), H (A), J (B)\n"
                     "Черные клавиши: W (C#), E (D#), T (F#), Y (G#), U (A#)")

        msg = QMessageBox()
        msg.setWindowTitle("Справка")
        msg.setText(help_text)
        msg.exec()

    def keyPressEvent(self, event):
        key = event.key()

        key_to_note = {
            Qt.Key.Key_A: 'C',
            Qt.Key.Key_S: 'D',
            Qt.Key.Key_D: 'E',
            Qt.Key.Key_F: 'F',
            Qt.Key.Key_G: 'G',
            Qt.Key.Key_H: 'A',
            Qt.Key.Key_J: 'B',
            Qt.Key.Key_W: 'C#',
            Qt.Key.Key_E: 'D#',
            Qt.Key.Key_T: 'F#',
            Qt.Key.Key_Y: 'G#',
            Qt.Key.Key_U: 'A#'
        }

        if key in key_to_note:
            note = key_to_note[key]
            self.play_note(note)

            if note in self.white_keys:
                self.white_keys[note].setStyleSheet("background-color: #ddd; border: 1px solid black;")
            elif note in self.black_keys:
                self.black_keys[note].setStyleSheet("background-color: #555; color: white;")

    def keyReleaseEvent(self, event):
        key = event.key()
        key_to_note = {
            Qt.Key.Key_A: 'C',
            Qt.Key.Key_S: 'D',
            Qt.Key.Key_D: 'E',
            Qt.Key.Key_F: 'F',
            Qt.Key.Key_G: 'G',
            Qt.Key.Key_H: 'A',
            Qt.Key.Key_J: 'B',
            Qt.Key.Key_W: 'C#',
            Qt.Key.Key_E: 'D#',
            Qt.Key.Key_T: 'F#',
            Qt.Key.Key_Y: 'G#',
            Qt.Key.Key_U: 'A#'
        }

        if key in key_to_note:
            note = key_to_note[key]
            if note in self.white_keys:
                self.white_keys[note].setStyleSheet("""
                    QPushButton {
                        background-color: white; 
                        border: 1px solid black;
                    }
                    QPushButton:pressed {
                        background-color: #ddd;
                    }
                """)
            elif note in self.black_keys:
                self.black_keys[note].setStyleSheet("""
                    QPushButton {
                        background-color: black; 
                        color: white;
                    }
                    QPushButton:pressed {
                        background-color: #555;
                    }
                """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PianoApp()
    window.show()
    sys.exit(app.exec())