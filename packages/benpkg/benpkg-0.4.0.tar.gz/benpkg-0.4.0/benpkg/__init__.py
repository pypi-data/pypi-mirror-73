__version__ = "0.1.0"


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy, QSpacerItem


class CustomProgressBar(QWidget):
    def __init__(self, steps):
        super().__init__()
        self.steps = steps
        self.widgets = {}
        self.label_width = len(max(self.steps, key=len)) * 5
        self.label_spacing_width = self.label_width / 15
        self.bar_height = 15
        self.dot_width = 20
        self._build_ui()
        self.update(0)

    def _build_ui(self):
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        self.layout_bar = QHBoxLayout()
        self.layout_bar.addSpacing(self.label_width / 2 - (self.dot_width / 2))
        self.layout_main.addLayout(self.layout_bar)
        self._create_bar()
        self.layout_bar.addSpacing(self.label_width / 2 - (self.dot_width / 2))

        self.layout_labels = QHBoxLayout()
        self.layout_main.addLayout(self.layout_labels)
        self._create_labels()

    def _create_bar(self):
        for i in range(len(self.steps)):
            self.widgets[i] = []
            if i != 0:
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setLineWidth(3)
                line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                line.setFixedHeight(self.bar_height)
                self.layout_bar.addWidget(line)
                self.widgets[i].append(line)
            dot = QLabel("•")
            dot.font_size = self.bar_height * 2.6
            dot.setFixedWidth(self.dot_width)
            dot.setFixedHeight(self.bar_height)
            dot.setAlignment(Qt.AlignCenter)
            self.layout_bar.addWidget(dot)
            self.widgets[i].append(dot)

    def _create_labels(self):
        for i in range(len(self.steps)):
            if i != 0:
                spacer = QSpacerItem(self.label_spacing_width, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
                self.layout_labels.addItem(spacer)
            label = QLabel(self.steps[i])
            label.font_size = 11
            label.setWordWrap(True)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedWidth(self.label_width)
            self.layout_labels.addWidget(label)
            self.widgets[i].append(label)

    def update(self, index):
        for key in self.widgets:
            if key <= index:
                color = "#00AC94"  # greenish
            else:
                color = "#B7A99A"  # greyish
            for widget in self.widgets[key]:
                try:
                    widget.setStyleSheet("font-size:{}pt; color:{};".format(widget.font_size, color))
                except AttributeError:
                    widget.setStyleSheet("color:{};".format(color))

