class ABCError:
    """오류 메시지 창을 스타일링하고 표시하는 클래스"""
    
    @staticmethod
    def show_error_message(parent):
        """스타일이 적용된 오류 메시지 창을 띄우는 함수"""
        
        dialog = QDialog(parent)
        dialog.setWindowTitle("입력 오류")
        dialog.setFixedSize(350, 160)  # 크기 조절
        
        dialog.setStyleSheet("background-color: #1c1c1c; border-radius: 10px;")  # 다이얼로그 배경색 적용
        
        img_path = "/nas/Batz_Maru/pingu/imim/gif/sorry.gif"
        movie = QMovie(img_path)
        movie.setScaledSize(QSize(100, 100))  # GIF 크기 조정
        
        gif_label = QLabel(dialog)
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()  # GIF 애니메이션 시작
        
        movie.finished.connect(movie.start)
        
        text_label = QLabel("<p style='color: #FFF8DC; font-size: 14px; font-weight: bold;'>"
                            " Please select the object to Publish!</p>", dialog)   # 멘트만 다르게
        text_label.setAlignment(Qt.AlignVCenter)
        
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