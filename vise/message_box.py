#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from gettext import gettext as _

from PyQt5.Qt import (
    QDialog, QIcon, QApplication, QSize, QKeySequence, QAction, Qt,
    QDialogButtonBox, QGridLayout, QLabel, QPlainTextEdit, QCheckBox,
    pyqtSignal, QStyle
)

from .constants import appname, str_version
from .resources import get_icon
from .settings import gprefs


class MessageBox(QDialog):  # {{{

    ERROR = 0
    WARNING = 1
    INFO = 2
    QUESTION = 3

    resize_needed = pyqtSignal()

    def setup_ui(self):
        self.setObjectName("Dialog")
        self.resize(497, 235)
        self.gridLayout = l = QGridLayout(self)
        l.setObjectName("gridLayout")
        self.icon_label = la = QLabel('')
        la.setMaximumSize(QSize(68, 68))
        la.setScaledContents(True)
        la.setObjectName("icon_label")
        l.addWidget(la)
        self.msg = la = QLabel(self)
        la.setWordWrap(True), la.setMinimumWidth(400)
        la.setOpenExternalLinks(True)
        la.setObjectName("msg")
        l.addWidget(la, 0, 1, 1, 1)
        self.det_msg = dm = QPlainTextEdit(self)
        dm.setReadOnly(True)
        dm.setObjectName("det_msg")
        l.addWidget(dm, 1, 0, 1, 2)
        self.bb = bb = QDialogButtonBox(self)
        bb.setStandardButtons(QDialogButtonBox.Ok)
        bb.setObjectName("bb")
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        l.addWidget(bb, 3, 0, 1, 2)
        self.toggle_checkbox = tc = QCheckBox(self)
        tc.setObjectName("toggle_checkbox")
        l.addWidget(tc, 2, 0, 1, 2)

    def __init__(self, type_, title, msg,
                 det_msg='',
                 q_icon=None,
                 show_copy_button=True,
                 parent=None, default_yes=True,
                 yes_text=None, no_text=None, yes_icon=None, no_icon=None):
        QDialog.__init__(self, parent)
        if q_icon is None:
            icon = {
                self.ERROR: QStyle.SP_MessageBoxCritical,
                self.WARNING: QStyle.SP_MessageBoxWarning,
                self.INFO:    QStyle.SP_MessageBoxInformation,
                self.QUESTION: QStyle.SP_MessageBoxQuestion,
            }[type_]
            self.icon = self.style().standardIcon(icon)
        else:
            self.icon = q_icon if isinstance(q_icon, QIcon) else get_icon(q_icon)
        self.setup_ui()

        self.setWindowTitle(title)
        self.setWindowIcon(self.icon)
        self.icon_label.setPixmap(self.icon.pixmap(128, 128))
        self.msg.setText(msg)
        self.det_msg.setPlainText(det_msg)
        self.det_msg.setVisible(False)
        self.toggle_checkbox.setVisible(False)

        if show_copy_button:
            self.ctc_button = self.bb.addButton(_('&Copy to clipboard'),
                                                self.bb.ActionRole)
            self.ctc_button.clicked.connect(self.copy_to_clipboard)

        self.show_det_msg = _('Show &details')
        self.hide_det_msg = _('Hide &details')
        self.det_msg_toggle = self.bb.addButton(self.show_det_msg, self.bb.ActionRole)
        self.det_msg_toggle.clicked.connect(self.toggle_det_msg)
        self.det_msg_toggle.setToolTip(
            _('Show detailed information about this error'))

        self.copy_action = QAction(self)
        self.addAction(self.copy_action)
        self.copy_action.setShortcuts(QKeySequence.Copy)
        self.copy_action.triggered.connect(self.copy_to_clipboard)

        self.is_question = type_ == self.QUESTION
        if self.is_question:
            self.bb.setStandardButtons(self.bb.Yes | self.bb.No)
            self.bb.button(self.bb.Yes if default_yes else self.bb.No
                           ).setDefault(True)
            self.default_yes = default_yes
            if yes_text is not None:
                self.bb.button(self.bb.Yes).setText(yes_text)
            if no_text is not None:
                self.bb.button(self.bb.No).setText(no_text)
            if yes_icon is not None:
                self.bb.button(self.bb.Yes).setIcon(yes_icon if isinstance(yes_icon, QIcon) else get_icon(yes_icon))
            if no_icon is not None:
                self.bb.button(self.bb.No).setIcon(no_icon if isinstance(no_icon, QIcon) else get_icon(no_icon))
        else:
            self.bb.button(self.bb.Ok).setDefault(True)

        if not det_msg:
            self.det_msg_toggle.setVisible(False)

        self.resize_needed.connect(self.do_resize, type=Qt.QueuedConnection)
        self.do_resize()

    def sizeHint(self):
        ans = QDialog.sizeHint(self)
        ans.setWidth(max(min(ans.width(), 500), self.bb.sizeHint().width() + 100))
        ans.setHeight(min(ans.height(), 500))
        return ans

    def toggle_det_msg(self, *args):
        vis = self.det_msg.isVisible()
        self.det_msg.setVisible(not vis)
        self.det_msg_toggle.setText(self.show_det_msg if vis else self.hide_det_msg)
        self.resize_needed.emit()

    def do_resize(self):
        self.resize(self.sizeHint())

    def copy_to_clipboard(self, *args):
        QApplication.clipboard().setText(
            '%s, version %s\n%s: %s\n\n%s' %
            (appname, str_version, self.windowTitle(),
             self.msg.text(),
             self.det_msg.toPlainText()))
        if hasattr(self, 'ctc_button'):
            self.ctc_button.setText(_('Copied'))

    def showEvent(self, ev):
        ret = QDialog.showEvent(self, ev)
        if self.is_question:
            try:
                self.bb.button(self.bb.Yes if self.default_yes else self.bb.No
                               ).setFocus(Qt.OtherFocusReason)
            except:
                pass  # Buttons were changed
        else:
            self.bb.button(self.bb.Ok).setFocus(Qt.OtherFocusReason)
        return ret

    def set_details(self, msg):
        if not msg:
            msg = ''
        self.det_msg.setPlainText(msg)
        self.det_msg_toggle.setText(self.show_det_msg)
        self.det_msg_toggle.setVisible(bool(msg))
        self.det_msg.setVisible(False)
        self.resize_needed.emit()
# }}}


def warning_dialog(parent, title, msg, det_msg='', show=False, show_copy_button=True):
    d = MessageBox(MessageBox.WARNING, _('WARNING:') + ' ' +
                   title, msg, det_msg, parent=parent, show_copy_button=show_copy_button)
    return d.exec_() if show else d


def error_dialog(parent, title, msg, det_msg='', show=True, show_copy_button=True):
    d = MessageBox(MessageBox.ERROR, _('ERROR:') + ' ' +
                   title, msg, det_msg, parent=parent, show_copy_button=show_copy_button)
    return d.exec_() if show else d


def question_dialog(
        parent, title, msg, det_msg='', show_copy_button=False,
        default_yes=True,
        # Skippable dialogs
        # Set skip_dialog_name to a unique name for this dialog
        # Set skip_dialog_msg to a message displayed to the user
        skip_dialog_name=None, skip_dialog_msg=_('Show this confirmation again'),
        skip_dialog_skipped_value=True, skip_dialog_skip_precheck=True,
        # Override icon (QIcon to be used as the icon for this dialog or string for I())
        override_icon=None,
        # Change the text/icons of the yes and no buttons.
        # The icons must be QIcon objects or strings for I()
        yes_text=None, no_text=None, yes_icon=None, no_icon=None,
):

    auto_skip = set(gprefs.get('questions_to_auto_skip', []))
    if (skip_dialog_name is not None and skip_dialog_name in auto_skip):
        return bool(skip_dialog_skipped_value)

    d = MessageBox(MessageBox.QUESTION, title, msg, det_msg, parent=parent,
                   show_copy_button=show_copy_button, default_yes=default_yes,
                   q_icon=override_icon, yes_text=yes_text, no_text=no_text,
                   yes_icon=yes_icon, no_icon=no_icon)

    if skip_dialog_name is not None and skip_dialog_msg:
        tc = d.toggle_checkbox
        tc.setVisible(True)
        tc.setText(skip_dialog_msg)
        tc.setChecked(bool(skip_dialog_skip_precheck))
        d.resize_needed.emit()

    ret = d.exec_() == d.Accepted

    if skip_dialog_name is not None and not d.toggle_checkbox.isChecked():
        auto_skip.add(skip_dialog_name)
        gprefs.set('questions_to_auto_skip', list(auto_skip))

    return ret
