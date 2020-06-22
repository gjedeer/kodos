# -*- coding: utf-8; mode: python; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4; truncate-lines: 0 -*-
# vi: set fileencoding=utf-8 filetype=python expandtab tabstop=4 shiftwidth=4 softtabstop=4 cindent:
# :mode=python:indentSize=4:tabSize=4:noTabs=true:

#-----------------------------------------------------------------------------#
# Installed modules

from PyQt4 import QtGui, QtCore

#-----------------------------------------------------------------------------#
# Kodos modules

from .prefsBA import Ui_PrefsBA
from .help import Help

#-----------------------------------------------------------------------------#

class Preferences(QtGui.QDialog, Ui_PrefsBA):

    prefsSaved = QtCore.pyqtSignal()

    def __init__(self, autoload=0, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QDialog.__init__(self, parent, f)
        self.setupUi(self)

        self.parent = parent
        self.settings = QtCore.QSettings()
        if autoload:
            self.load()
        return


    def load(self):
        for preference in self.settings.childKeys():
            try:
                setting = self.settings.value(preference)
                if preference == 'Font':
                    self.parent.setfont(setting.toPyObject())
                if preference == 'Match Font':
                    self.parent.setMatchFont(setting.toPyObject())
                if preference == 'Email Server':
                    self.emailServerEdit.setText(setting.toPyObject())
                if preference == 'Recent Files Count':
                    self.recentFilesSpinBox.setValue(int(setting.toPyObject()))
            except Exception:
                print("Loading of configuration key {0} failed.".format(preference))
                self.settings.remove(preference)
        return


    def save(self):
        self.settings.setValue('Font', self.parent.getfont())
        self.settings.setValue('Match Font', self.parent.getMatchFont())
        self.settings.setValue('Email Server', self.emailServerEdit.text())
        self.settings.setValue('Recent Files Count', self.recentFilesSpinBox.text())

        self.settings.sync()
        self.prefsSaved.emit()
        return


    def setFontButtonText(self, button, font):
        #self.fontButton.setText("{0} {1}".format(str(font.family()), font.pointSize()))
        button.setText("{0} {1}".format(str(font.family()), font.pointSize()))
        return


    def showPrefsDialog(self):
        f = self.parent.getfont()
        self.fontButton.setFont(f)
        self.setFontButtonText(self.fontButton, f)

        f = self.parent.getMatchFont()
        self.fontButtonMatch.setFont(f)
        self.setFontButtonText(self.fontButtonMatch, f)

        self.show()
        return


    def font_slot(self):
        (font, ok) = QtGui.QFontDialog.getFont(self.fontButton.font())
        if ok:
            self.fontButton.setFont(font)
            self.setFontButtonText(self.fontButton, font)
        return


    def match_font_slot(self):
        (font, ok) = QtGui.QFontDialog.getFont(self.fontButtonMatch.font())
        if ok:
            self.fontButtonMatch.setFont(font)
            self.setFontButtonText(self.fontButtonMatch, font)
        return


    def apply_slot(self):
        self.parent.setfont(self.fontButton.font())
        self.parent.setMatchFont(self.fontButtonMatch.font())
        self.save()
        return


    def accept(self):
        self.apply_slot()
        QtGui.QDialog.accept(self)
        return


    def help_slot(self):
        self.helpWindow = Help(filename="prefs.html", parent=self)
        return

#-----------------------------------------------------------------------------#
