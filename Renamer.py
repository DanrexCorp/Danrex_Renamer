import os
import sys
from pathlib import Path
from typing import Optional

from PySide6.QtCore import (
    Qt, QObject, QSettings, QSize,
)
from PySide6.QtGui import (
    QAction, QKeySequence, QFont,
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QListWidget,
    QListWidgetItem, QFileDialog, QMessageBox, QStatusBar,
    QMenuBar, QMenu, QSizePolicy, QStyleFactory,
    QGroupBox, QFrame, QToolBar, QStackedWidget, QSpinBox,
)

ORGANIZATION_NAME = "Danrex Corp"
APPLICATION_NAME = "Danrex Renamer"
APPLICATION_VERSION = "2.0.0"

ACCENT_COLOR = "#0078D4"
FONT_FAMILY = "Segoe UI"
MONOSPACE_FONT = "Consolas"
BASE_FONT_SIZE = 9

DARK_STYLE = f"""
QWidget {{
    font-family: "{FONT_FAMILY}";
    font-size: {BASE_FONT_SIZE}pt;
    color: #cccccc;
}}
QMainWindow, QDialog {{
    background-color: #1e1e1e;
}}
QMenuBar {{
    background-color: #2d2d2d;
    color: #cccccc;
    border-bottom: 1px solid #3e3e3e;
    padding: 0;
    spacing: 0;
}}
QMenuBar::item {{
    padding: 5px 10px;
    background: transparent;
}}
QMenuBar::item:selected {{
    background-color: #3e3e3e;
}}
QMenuBar::item:pressed {{
    background-color: #094771;
}}
QMenu {{
    background-color: #2d2d2d;
    color: #cccccc;
    border: 1px solid #3e3e3e;
    padding: 2px;
}}
QMenu::item {{
    padding: 5px 28px 5px 18px;
}}
QMenu::item:selected {{
    background-color: #094771;
    color: #ffffff;
}}
QMenu::separator {{
    height: 1px;
    background: #3e3e3e;
    margin: 3px 8px;
}}
QToolBar {{
    background-color: #252526;
    border-bottom: 1px solid #3e3e3e;
    spacing: 2px;
    padding: 2px 4px;
}}
QToolBar::separator {{
    width: 1px;
    background: #3e3e3e;
    margin: 3px 3px;
}}
QToolButton {{
    background-color: transparent;
    color: #cccccc;
    border: none;
    padding: 4px 10px;
    margin: 1px;
}}
QToolButton:hover {{
    background-color: #3e3e3e;
}}
QToolButton:pressed {{
    background-color: #094771;
}}
QGroupBox {{
    color: #cccccc;
    font-weight: bold;
    border: 1px solid #3e3e3e;
    background-color: #252526;
    margin-top: 14px;
    padding-top: 14px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    top: 0px;
    padding: 0 4px;
    color: #8fc9ff;
    background-color: #252526;
}}
QListWidget {{
    background-color: #1e1e1e;
    color: #cccccc;
    border: 1px solid #3e3e3e;
    outline: none;
    font-family: "{MONOSPACE_FONT}";
    font-size: {BASE_FONT_SIZE}pt;
}}
QListWidget::item {{
    padding: 3px 6px;
    border: none;
}}
QListWidget::item:selected {{
    background-color: #094771;
    color: #ffffff;
}}
QListWidget::item:hover:!selected {{
    background-color: #2a2d2e;
}}
QLineEdit {{
    background-color: #1e1e1e;
    color: #cccccc;
    border: 1px solid #3e3e3e;
    padding: 4px 8px;
    min-height: 22px;
}}
QLineEdit:focus {{
    border-color: {ACCENT_COLOR};
}}
QLineEdit:read-only {{
    background-color: #252526;
    color: #888888;
}}
QComboBox {{
    background-color: #3a3a3a;
    color: #cccccc;
    border: 1px solid #555555;
    padding: 4px 8px;
    min-height: 22px;
}}
QComboBox:hover {{
    border-color: #666666;
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox QAbstractItemView {{
    background-color: #2d2d2d;
    color: #cccccc;
    selection-background-color: #094771;
    border: 1px solid #3e3e3e;
    outline: none;
}}
QSpinBox {{
    background-color: #1e1e1e;
    color: #cccccc;
    border: 1px solid #3e3e3e;
    padding: 4px 8px;
    min-height: 22px;
}}
QSpinBox:focus {{
    border-color: {ACCENT_COLOR};
}}
QPushButton {{
    background-color: #3a3a3a;
    color: #cccccc;
    border: 1px solid #555555;
    padding: 4px 14px;
    min-height: 22px;
}}
QPushButton:hover {{
    background-color: #4a4a4a;
    border-color: #666666;
}}
QPushButton:pressed {{
    background-color: #2a2a2a;
}}
QPushButton:disabled {{
    background-color: #2d2d2d;
    color: #555555;
    border-color: #3a3a3a;
}}
QPushButton#AccentButton {{
    background-color: {ACCENT_COLOR};
    color: #ffffff;
    border: none;
    font-weight: bold;
    padding: 5px 18px;
    min-height: 26px;
}}
QPushButton#AccentButton:hover {{
    background-color: #1a8ad4;
}}
QPushButton#AccentButton:pressed {{
    background-color: #006cbe;
}}
QPushButton#AccentButton:disabled {{
    background-color: #2a4a6a;
    color: #666666;
}}
QStatusBar {{
    background-color: #2d2d2d;
    color: #cccccc;
    border-top: 1px solid #3e3e3e;
    padding: 0 8px;
    min-height: 20px;
    max-height: 20px;
}}
QStatusBar::item {{
    border: none;
}}
QStatusBar QLabel {{
    color: #cccccc;
    font-size: 8pt;
    padding: 0;
    background: transparent;
}}
QLabel {{
    color: #cccccc;
    background: transparent;
}}
QLabel#TitleLabel {{
    font-size: 16pt;
    font-weight: 300;
    color: #e0e0e0;
}}
QLabel#SubtitleLabel {{
    font-size: 8pt;
    color: #888888;
}}
QFrame#TopLine {{
    background-color: {ACCENT_COLOR};
    max-height: 2px;
}}
"""

LIGHT_STYLE = f"""
QWidget {{
    font-family: "{FONT_FAMILY}";
    font-size: {BASE_FONT_SIZE}pt;
    color: #1e1e1e;
}}
QMainWindow, QDialog {{
    background-color: #f0f0f0;
}}
QMenuBar {{
    background-color: #ffffff;
    color: #1e1e1e;
    border-bottom: 1px solid #d0d0d0;
    padding: 0;
    spacing: 0;
}}
QMenuBar::item {{
    padding: 5px 10px;
    background: transparent;
}}
QMenuBar::item:selected {{
    background-color: #e5e5e5;
}}
QMenuBar::item:pressed {{
    background-color: #cce4f7;
}}
QMenu {{
    background-color: #ffffff;
    color: #1e1e1e;
    border: 1px solid #c0c0c0;
    padding: 2px;
}}
QMenu::item {{
    padding: 5px 28px 5px 18px;
}}
QMenu::item:selected {{
    background-color: #cce4f7;
    color: #1e1e1e;
}}
QMenu::separator {{
    height: 1px;
    background: #e0e0e0;
    margin: 3px 8px;
}}
QToolBar {{
    background-color: #fafafa;
    border-bottom: 1px solid #d0d0d0;
    spacing: 2px;
    padding: 2px 4px;
}}
QToolBar::separator {{
    width: 1px;
    background: #d0d0d0;
    margin: 3px 3px;
}}
QToolButton {{
    background-color: transparent;
    color: #1e1e1e;
    border: none;
    padding: 4px 10px;
    margin: 1px;
}}
QToolButton:hover {{
    background-color: #e5e5e5;
}}
QToolButton:pressed {{
    background-color: #cce4f7;
}}
QGroupBox {{
    color: #1e1e1e;
    font-weight: bold;
    border: 1px solid #c8c8c8;
    background-color: #ffffff;
    margin-top: 14px;
    padding-top: 14px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    top: 0px;
    padding: 0 4px;
    color: {ACCENT_COLOR};
    background-color: #ffffff;
}}
QListWidget {{
    background-color: #ffffff;
    color: #1e1e1e;
    border: 1px solid #c8c8c8;
    outline: none;
    font-family: "{MONOSPACE_FONT}";
    font-size: {BASE_FONT_SIZE}pt;
}}
QListWidget::item {{
    padding: 3px 6px;
    border: none;
}}
QListWidget::item:selected {{
    background-color: #cce4f7;
    color: #1e1e1e;
}}
QListWidget::item:hover:!selected {{
    background-color: #f0f0f0;
}}
QLineEdit {{
    background-color: #ffffff;
    color: #1e1e1e;
    border: 1px solid #adadad;
    padding: 4px 8px;
    min-height: 22px;
}}
QLineEdit:focus {{
    border-color: {ACCENT_COLOR};
}}
QLineEdit:read-only {{
    background-color: #f5f5f5;
    color: #888888;
}}
QComboBox {{
    background-color: #ffffff;
    color: #1e1e1e;
    border: 1px solid #adadad;
    padding: 4px 8px;
    min-height: 22px;
}}
QComboBox:hover {{
    border-color: #999999;
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox QAbstractItemView {{
    background-color: #ffffff;
    color: #1e1e1e;
    selection-background-color: #cce4f7;
    border: 1px solid #c0c0c0;
    outline: none;
}}
QSpinBox {{
    background-color: #ffffff;
    color: #1e1e1e;
    border: 1px solid #adadad;
    padding: 4px 8px;
    min-height: 22px;
}}
QSpinBox:focus {{
    border-color: {ACCENT_COLOR};
}}
QPushButton {{
    background-color: #ffffff;
    color: #1e1e1e;
    border: 1px solid #adadad;
    padding: 4px 14px;
    min-height: 22px;
}}
QPushButton:hover {{
    background-color: #e9e9e9;
    border-color: #999999;
}}
QPushButton:pressed {{
    background-color: #d9d9d9;
}}
QPushButton:disabled {{
    background-color: #f5f5f5;
    color: #aaaaaa;
    border-color: #d0d0d0;
}}
QPushButton#AccentButton {{
    background-color: {ACCENT_COLOR};
    color: #ffffff;
    border: none;
    font-weight: bold;
    padding: 5px 18px;
    min-height: 26px;
}}
QPushButton#AccentButton:hover {{
    background-color: #1a8ad4;
}}
QPushButton#AccentButton:pressed {{
    background-color: #006cbe;
}}
QPushButton#AccentButton:disabled {{
    background-color: #a8cce8;
    color: #ffffff;
}}
QStatusBar {{
    background-color: #ffffff;
    color: #1e1e1e;
    border-top: 1px solid #d0d0d0;
    padding: 0 8px;
    min-height: 20px;
    max-height: 20px;
}}
QStatusBar::item {{
    border: none;
}}
QStatusBar QLabel {{
    color: #1e1e1e;
    font-size: 8pt;
    padding: 0;
    background: transparent;
}}
QLabel {{
    color: #1e1e1e;
    background: transparent;
}}
QLabel#TitleLabel {{
    font-size: 16pt;
    font-weight: 300;
    color: #1e1e1e;
}}
QLabel#SubtitleLabel {{
    font-size: 8pt;
    color: #888888;
}}
QFrame#TopLine {{
    background-color: {ACCENT_COLOR};
    max-height: 2px;
}}
"""

RENAME_MODES = [
    "Добавить префикс",
    "Добавить суффикс",
    "Заменить текст",
    "Нумерация",
    "Удалить символы",
]


class RenameLogic(QObject):

    @staticmethod
    def scan_files(folder_path: str) -> list[str]:
        files = []
        try:
            for entry in os.scandir(folder_path):
                if entry.is_file():
                    files.append(entry.name)
        except OSError:
            pass
        files.sort()
        return files

    @staticmethod
    def get_new_name(old_name: str, mode: str, params: dict, index: int = 0) -> str:
        name, ext = os.path.splitext(old_name)

        if mode == "Добавить префикс":
            return params.get("prefix", "") + old_name

        elif mode == "Добавить суффикс":
            return name + params.get("suffix", "") + ext

        elif mode == "Заменить текст":
            find_text = params.get("find", "")
            replace_text = params.get("replace", "")
            if find_text:
                return old_name.replace(find_text, replace_text)
            return old_name

        elif mode == "Нумерация":
            start = params.get("start", 1)
            fmt = params.get("format", "001")
            num = start + index
            if fmt.isdigit():
                num_str = str(num).zfill(len(fmt))
            else:
                num_str = f"{fmt}{num}"
            return f"{num_str}{ext}"

        elif mode == "Удалить символы":
            start = params.get("start_pos", 1) - 1
            end = params.get("end_pos", 0)
            if start < 0:
                start = 0
            if end > len(name):
                end = len(name)
            new_name = name[:start] + name[end:]
            return new_name + ext if new_name else old_name

        return old_name

    @staticmethod
    def get_unique_filename(folder_path: str, filename: str) -> str:
        name, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        while os.path.exists(os.path.join(folder_path, new_filename)):
            new_filename = f"{name}_{counter}{ext}"
            counter += 1
        return new_filename

    @staticmethod
    def rename_files(folder_path: str, preview_data: list[tuple[str, str]]) -> tuple[int, int]:
        renamed = 0
        errors = 0
        for old_name, new_name in preview_data:
            if old_name == new_name:
                continue
            old_path = os.path.join(folder_path, old_name)
            new_path = os.path.join(folder_path, new_name)
            if os.path.exists(new_path):
                new_name = RenameLogic.get_unique_filename(folder_path, new_name)
                new_path = os.path.join(folder_path, new_name)
            try:
                os.rename(old_path, new_path)
                renamed += 1
            except OSError:
                errors += 1
        return renamed, errors


class ThemeController:
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"

    @staticmethod
    def _is_system_dark() -> bool:
        if sys.platform != "win32":
            return False
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return value == 0
        except Exception:
            return False

    @staticmethod
    def apply_theme(app: QApplication, theme_name: str) -> None:
        if theme_name == ThemeController.DARK:
            app.setStyleSheet(DARK_STYLE)
        elif theme_name == ThemeController.LIGHT:
            app.setStyleSheet(LIGHT_STYLE)
        else:
            sheet = DARK_STYLE if ThemeController._is_system_dark() else LIGHT_STYLE
            app.setStyleSheet(sheet)


class DanrexRenamerWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.qsettings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
        self.current_folder: str = ""
        self.files: list[str] = []
        self.preview_data: list[tuple[str, str]] = []
        self.theme: str = self.qsettings.value("theme", ThemeController.SYSTEM)

        self.setWindowTitle(APPLICATION_NAME)
        self.setMinimumSize(640, 600)

        self._build_actions()
        self._build_menubar()
        self._build_central()
        self._build_statusbar()

        self._restore_geometry()
        self._apply_theme()
        self._sync_theme_actions()

    def _build_actions(self) -> None:
        self.act_open = QAction("&Выбрать папку...", self)
        self.act_open.setShortcut(QKeySequence("Ctrl+O"))
        self.act_open.setStatusTip("Выбрать папку с файлами (Ctrl+O)")
        self.act_open.triggered.connect(self._do_select_folder)

        self.act_preview = QAction("&Предпросмотр", self)
        self.act_preview.setShortcut(QKeySequence("F5"))
        self.act_preview.setStatusTip("Обновить предпросмотр (F5)")
        self.act_preview.triggered.connect(self._do_preview)

        self.act_rename = QAction("&Переименовать", self)
        self.act_rename.setShortcut(QKeySequence("Ctrl+R"))
        self.act_rename.setStatusTip("Выполнить переименование (Ctrl+R)")
        self.act_rename.triggered.connect(self._do_rename)
        self.act_rename.setEnabled(False)

        self.act_exit = QAction("&Выход", self)
        self.act_exit.setShortcut(QKeySequence("Alt+F4"))
        self.act_exit.triggered.connect(self.close)

        self.act_light = QAction("&Светлая", self, checkable=True)
        self.act_dark = QAction("&Тёмная", self, checkable=True)
        self.act_system = QAction("&Системная", self, checkable=True)
        self.act_light.triggered.connect(lambda: self._change_theme(ThemeController.LIGHT))
        self.act_dark.triggered.connect(lambda: self._change_theme(ThemeController.DARK))
        self.act_system.triggered.connect(lambda: self._change_theme(ThemeController.SYSTEM))

        self.act_about = QAction("&О программе...", self)
        self.act_about.triggered.connect(self._do_about)

    def _build_menubar(self) -> None:
        mb = self.menuBar()

        m_file = mb.addMenu("&Файл")
        m_file.addAction(self.act_open)
        m_file.addSeparator()
        m_file.addAction(self.act_exit)

        m_tools = mb.addMenu("&Инструменты")
        m_tools.addAction(self.act_preview)
        m_tools.addAction(self.act_rename)

        m_view = mb.addMenu("&Вид")
        m_theme = m_view.addMenu("&Тема")
        m_theme.addAction(self.act_light)
        m_theme.addAction(self.act_dark)
        m_theme.addAction(self.act_system)

        m_help = mb.addMenu("&Справка")
        m_help.addAction(self.act_about)

    def _build_central(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(20, 16, 20, 14)
        layout.setSpacing(10)

        top_line = QFrame()
        top_line.setObjectName("TopLine")
        layout.addWidget(top_line)

        title_label = QLabel(APPLICATION_NAME)
        title_label.setObjectName("TitleLabel")
        layout.addWidget(title_label)

        subtitle_label = QLabel("Массовое переименование файлов")
        subtitle_label.setObjectName("SubtitleLabel")
        layout.addWidget(subtitle_label)

        folder_group = QGroupBox("Папка с файлами")
        folder_layout = QHBoxLayout(folder_group)
        folder_layout.setContentsMargins(10, 18, 10, 10)
        folder_layout.setSpacing(8)

        self.folder_path_edit = QLineEdit()
        self.folder_path_edit.setReadOnly(True)
        self.folder_path_edit.setPlaceholderText("Папка не выбрана")
        folder_layout.addWidget(self.folder_path_edit, stretch=1)

        browse_button = QPushButton("Обзор...")
        browse_button.clicked.connect(self._do_select_folder)
        folder_layout.addWidget(browse_button)

        layout.addWidget(folder_group)

        mode_group = QGroupBox("Режим переименования")
        mode_layout = QVBoxLayout(mode_group)
        mode_layout.setContentsMargins(10, 18, 10, 10)
        mode_layout.setSpacing(8)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(RENAME_MODES)
        self.mode_combo.currentTextChanged.connect(self._on_mode_changed)
        mode_layout.addWidget(self.mode_combo)

        self.params_stack = QStackedWidget()
        self.params_stack.addWidget(self._build_prefix_params())
        self.params_stack.addWidget(self._build_suffix_params())
        self.params_stack.addWidget(self._build_replace_params())
        self.params_stack.addWidget(self._build_numbering_params())
        self.params_stack.addWidget(self._build_remove_params())
        mode_layout.addWidget(self.params_stack)

        layout.addWidget(mode_group)

        preview_group = QGroupBox("Предпросмотр")
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setContentsMargins(10, 18, 10, 10)
        preview_layout.setSpacing(6)

        self.preview_list = QListWidget()
        self.preview_list.setMinimumHeight(120)
        preview_layout.addWidget(self.preview_list)

        self.preview_count_label = QLabel("0 файлов")
        self.preview_count_label.setObjectName("SubtitleLabel")
        self.preview_count_label.setAlignment(Qt.AlignRight)
        preview_layout.addWidget(self.preview_count_label)

        layout.addWidget(preview_group, stretch=1)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)

        self.preview_button = QPushButton("Предпросмотр")
        self.preview_button.clicked.connect(self._do_preview)
        buttons_layout.addWidget(self.preview_button, stretch=1)

        self.rename_button = QPushButton("Переименовать")
        self.rename_button.setObjectName("AccentButton")
        self.rename_button.setEnabled(False)
        self.rename_button.clicked.connect(self._do_rename)
        buttons_layout.addWidget(self.rename_button, stretch=1)

        layout.addLayout(buttons_layout)

    def _build_prefix_params(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.addWidget(QLabel("Префикс:"))
        self.prefix_edit = QLineEdit()
        self.prefix_edit.setPlaceholderText("Например: backup_")
        l.addWidget(self.prefix_edit)
        return w

    def _build_suffix_params(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.addWidget(QLabel("Суффикс (перед расширением):"))
        self.suffix_edit = QLineEdit()
        self.suffix_edit.setPlaceholderText("Например: _final")
        l.addWidget(self.suffix_edit)
        return w

    def _build_replace_params(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(4)
        l.addWidget(QLabel("Найти:"))
        self.find_edit = QLineEdit()
        self.find_edit.setPlaceholderText("Текст для поиска")
        l.addWidget(self.find_edit)
        l.addWidget(QLabel("Заменить на:"))
        self.replace_edit = QLineEdit()
        self.replace_edit.setPlaceholderText("Текст для замены")
        l.addWidget(self.replace_edit)
        return w

    def _build_numbering_params(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(4)
        l.addWidget(QLabel("Начальный номер:"))
        self.start_spin = QSpinBox()
        self.start_spin.setRange(0, 999999)
        self.start_spin.setValue(1)
        l.addWidget(self.start_spin)
        l.addWidget(QLabel("Формат номера:"))
        self.format_edit = QLineEdit()
        self.format_edit.setText("001")
        l.addWidget(self.format_edit)
        return w

    def _build_remove_params(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(4)
        l.addWidget(QLabel("Удалить с позиции (начиная с 1):"))
        self.start_pos_spin = QSpinBox()
        self.start_pos_spin.setRange(1, 999)
        self.start_pos_spin.setValue(1)
        l.addWidget(self.start_pos_spin)
        l.addWidget(QLabel("Удалить до позиции:"))
        self.end_pos_spin = QSpinBox()
        self.end_pos_spin.setRange(1, 999)
        self.end_pos_spin.setValue(5)
        l.addWidget(self.end_pos_spin)
        return w

    def _build_statusbar(self) -> None:
        sb = QStatusBar()
        self.setStatusBar(sb)
        self.status_label = QLabel("")
        sb.addWidget(self.status_label, 1)

    def _restore_geometry(self) -> None:
        geom = self.qsettings.value("geometry")
        maximized = self.qsettings.value("maximized", False, type=bool)
        if geom:
            self.restoreGeometry(geom)
        else:
            self.resize(680, 640)
            self._center_on_screen()
        if maximized:
            self.showMaximized()

    def _center_on_screen(self) -> None:
        screen = QApplication.primaryScreen()
        if screen:
            center = screen.availableGeometry().center()
            fg = self.frameGeometry()
            fg.moveCenter(center)
            self.move(fg.topLeft())

    def _apply_theme(self) -> None:
        app = QApplication.instance()
        if app:
            ThemeController.apply_theme(app, self.theme)

    def _sync_theme_actions(self) -> None:
        self.act_light.setChecked(self.theme == ThemeController.LIGHT)
        self.act_dark.setChecked(self.theme == ThemeController.DARK)
        self.act_system.setChecked(self.theme == ThemeController.SYSTEM)

    def _change_theme(self, theme: str) -> None:
        self.theme = theme
        self.qsettings.setValue("theme", theme)
        self._apply_theme()
        self._sync_theme_actions()

    def _on_mode_changed(self) -> None:
        mode = self.mode_combo.currentText()
        index = RENAME_MODES.index(mode)
        self.params_stack.setCurrentIndex(index)
        if self.current_folder:
            self._do_preview()

    def _get_params(self) -> dict:
        mode = self.mode_combo.currentText()
        params = {}
        if mode == "Добавить префикс":
            params["prefix"] = self.prefix_edit.text()
        elif mode == "Добавить суффикс":
            params["suffix"] = self.suffix_edit.text()
        elif mode == "Заменить текст":
            params["find"] = self.find_edit.text()
            params["replace"] = self.replace_edit.text()
        elif mode == "Нумерация":
            params["start"] = self.start_spin.value()
            params["format"] = self.format_edit.text()
        elif mode == "Удалить символы":
            params["start_pos"] = self.start_pos_spin.value()
            params["end_pos"] = self.end_pos_spin.value()
        return params

    def _do_select_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с файлами")
        if folder:
            self.current_folder = folder
            self.folder_path_edit.setText(folder)
            self.files = RenameLogic.scan_files(folder)
            self.status_label.setText(f"Найдено файлов: {len(self.files)}")
            self._do_preview()

    def _do_preview(self) -> None:
        if not self.current_folder:
            QMessageBox.warning(self, "Предупреждение", "Сначала выберите папку.")
            return

        self.files = RenameLogic.scan_files(self.current_folder)
        mode = self.mode_combo.currentText()
        params = self._get_params()

        self.preview_list.clear()
        self.preview_data = []

        for idx, old_name in enumerate(self.files):
            new_name = RenameLogic.get_new_name(old_name, mode, params, idx)
            self.preview_data.append((old_name, new_name))
            self.preview_list.addItem(f"{old_name}  →  {new_name}")

        self.preview_count_label.setText(f"{len(self.files)} файлов")
        self.rename_button.setEnabled(len(self.files) > 0)
        self.act_rename.setEnabled(len(self.files) > 0)
        self.status_label.setText(f"Предпросмотр: {len(self.files)} файлов")

    def _do_rename(self) -> None:
        if not self.preview_data:
            QMessageBox.warning(self, "Предупреждение", "Сначала выполните предпросмотр.")
            return

        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Переименовать {len(self.files)} файлов?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        renamed, errors = RenameLogic.rename_files(self.current_folder, self.preview_data)
        self.status_label.setText(f"Переименовано: {renamed}, ошибок: {errors}")

        if renamed > 0:
            self.files = RenameLogic.scan_files(self.current_folder)
            self._do_preview()

    def _do_about(self) -> None:
        QMessageBox.about(
            self,
            f"О программе {APPLICATION_NAME}",
            f"{APPLICATION_NAME}  {APPLICATION_VERSION}\n\n"
            "Массовое переименование файлов.\n"
            "Режимы: префикс, суффикс, замена, нумерация, удаление символов.\n\n"
            f"© 2026 {ORGANIZATION_NAME}",
        )

    def closeEvent(self, event) -> None:
        self.qsettings.setValue("geometry", self.saveGeometry())
        self.qsettings.setValue("maximized", self.isMaximized())
        event.accept()


def main() -> None:
    app = QApplication(sys.argv)
    app.setOrganizationName(ORGANIZATION_NAME)
    app.setApplicationName(APPLICATION_NAME)
    if sys.platform == "win32":
        app.setStyle(QStyleFactory.create("windowsvista"))
    else:
        app.setStyle(QStyleFactory.create("Fusion"))
    app.setFont(QFont(FONT_FAMILY, BASE_FONT_SIZE))
    window = DanrexRenamerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
