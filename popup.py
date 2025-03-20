try:
    from PySide6.QtWidgets import QLabel, QPushButton, QLineEdit, QDialog, QVBoxLayout, QHBoxLayout
    from PySide6.QtGui import QPixmap, QMovie
    from PySide6.QtCore import Qt, QSize
except:
    from PySide2.QtWidgets import QLabel, QPushButton, QLineEdit, QDialog, QVBoxLayout, QHBoxLayout
    from PySide2.QtGui import QPixmap, QMovie
    from PySide2.QtCore import Qt, QSize

class PublishComplete:
    """퍼블리쉬가 완료되면 메시지 창을 띄우는 클래스"""
    
    @staticmethod
    def pub_complete(parent):
        
        dialog = QDialog(parent)
        dialog.setWindowTitle("Complete")
        dialog.setFixedSize(350, 160)  # 크기 조절
        
        dialog.setStyleSheet("background-color: #1c1c1c; border-radius: 10px;")  # 다이얼로그 배경색 적용
        
        img_path = "/nas/Batz_Maru/pingu/imim/gif/B_scissor.gif"
        movie = QMovie(img_path)
        movie.setScaledSize(QSize(100, 100))  # GIF 크기 조정
        
        gif_label = QLabel(dialog)
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()  # GIF 애니메이션 시작
        
        movie.finished.connect(movie.start)
        
        text_label = QLabel("<p style='color: #FFF8DC; font-size: 14px; font-weight: bold;'>"
                            "Publish Complete!! <br> </p>", dialog)
        text_label.setAlignment(Qt.AlignVCenter)
        
        ok_button = QPushButton("  Go to Home!  ", dialog)
        ok_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #fdcb01;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
                background-color: #feeca4;
                color: #333333;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #fdd835;
                border: 2px solid #fbc02d;
            }
            QPushButton:pressed {
                background-color: #fdcb01;
                border: 2px solid #fbc02d;
            }
        """)
        ok_button.clicked.connect(dialog.accept)
        
        main_layout = QVBoxLayout()
        content_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        
        content_layout.addWidget(gif_label)
        content_layout.addWidget(text_label)
        content_layout.setAlignment(Qt.AlignCenter)
        
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        
        main_layout.addLayout(content_layout)
        main_layout.addLayout(button_layout)
        
        dialog.setLayout(main_layout)
        dialog.exec_()





class ABCError:
    """오류 메시지 창을 스타일링하고 표시하는 클래스"""

    @staticmethod
    def show_error_message(parent=None):
        """Maya의 메인 윈도우를 부모로 설정하여 오류 메시지 창을 띄우는 함수"""

        dialog = QDialog(parent)
        dialog.setWindowTitle("Error")
        dialog.setFixedSize(350, 180)

        dialog.setStyleSheet("background-color: #1c1c1c; border-radius: 10px;")

        img_path = "/nas/Batz_Maru/pingu/imim/gif/sorry.gif"
        movie = QMovie(img_path)
        movie.setScaledSize(QSize(100, 100))

        gif_label = QLabel(dialog)
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()

        text_label = QLabel(
            "<p style='color: #FFF8DC; font-size: 14px; font-weight: bold; text-align: center;'>"
            "Alembic cache ( .abc )를 내보낼<br>오브젝트가 선택되지 않았습니다."
            "</p>", 
            dialog
        )
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        text_label.setFixedWidth(300)
        text_label.setFixedHeight(50)
        
        ok_button = QPushButton("  확인  ", dialog)
        ok_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #fdcb01;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
                background-color: #feeca4;
                color: #333333;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #fdd835;
                border: 2px solid #fbc02d;
            }
            QPushButton:pressed {
                background-color: #fdcb01;
                border: 2px solid #fbc02d;
            }
        """)
        ok_button.clicked.connect(dialog.accept)

        main_layout = QVBoxLayout()
        gif_layout = QHBoxLayout()
        text_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        gif_layout.addWidget(gif_label)
        gif_layout.setAlignment(Qt.AlignCenter)

        text_layout.addWidget(text_label)
        text_layout.setAlignment(Qt.AlignCenter)

        button_layout.addStretch()
        button_layout.addWidget(ok_button)

        main_layout.addLayout(gif_layout)
        main_layout.addLayout(text_layout)
        main_layout.addLayout(button_layout)

        dialog.setLayout(main_layout)
        dialog.exec_()



class CameraError:
    """오류 메시지 창을 스타일링하고 표시하는 클래스"""

    @staticmethod
    def show_error_message(parent=None):
        """Maya의 메인 윈도우를 부모로 설정하여 오류 메시지 창을 띄우는 함수"""

        dialog = QDialog(parent)
        dialog.setWindowTitle("Error")
        dialog.setFixedSize(350, 180)

        dialog.setStyleSheet("background-color: #1c1c1c; border-radius: 10px;")

        img_path = "/nas/Batz_Maru/pingu/imim/gif/sorry.gif"
        movie = QMovie(img_path)
        movie.setScaledSize(QSize(100, 100))

        gif_label = QLabel(dialog)
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()

        text_label = QLabel(
            "<p style='color: #FFF8DC; font-size: 14px; font-weight: bold; text-align: center;'>"
            "Playblast ( .mov )를 보내기 위한<br>카메라가 선택되지 않았습니다."
            "</p>", 
            dialog
        )
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        text_label.setFixedWidth(300)
        text_label.setFixedHeight(50)
        
        ok_button = QPushButton("  확인  ", dialog)
        ok_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #fdcb01;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
                background-color: #feeca4;
                color: #333333;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #fdd835;
                border: 2px solid #fbc02d;
            }
            QPushButton:pressed {
                background-color: #fdcb01;
                border: 2px solid #fbc02d;
            }
        """)
        ok_button.clicked.connect(dialog.accept)

        main_layout = QVBoxLayout()
        gif_layout = QHBoxLayout()
        text_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        gif_layout.addWidget(gif_label)
        gif_layout.setAlignment(Qt.AlignCenter)

        text_layout.addWidget(text_label)
        text_layout.setAlignment(Qt.AlignCenter)

        button_layout.addStretch()
        button_layout.addWidget(ok_button)

        main_layout.addLayout(gif_layout)
        main_layout.addLayout(text_layout)
        main_layout.addLayout(button_layout)

        dialog.setLayout(main_layout)
        dialog.exec_()




