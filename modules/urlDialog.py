# -*- coding: utf-8; mode: python; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4; truncate-lines: 0 -*-
# vi: set fileencoding=utf-8 filetype=python expandtab tabstop=4 shiftwidth=4 softtabstop=4 cindent:
# :mode=python:indentSize=4:tabSize=4:noTabs=true:

#-----------------------------------------------------------------------------#
# Built-in modules

import urllib

#-----------------------------------------------------------------------------#
# Installed modules

from PyQt4 import QtGui, QtCore

#-----------------------------------------------------------------------------#
# Kodos modules

from .urlDialogBA import Ui_URLDialogBA
from . import help

#-----------------------------------------------------------------------------#

class URLDialog(QtGui.QDialog, Ui_URLDialogBA):

    urlImported = QtCore.pyqtSignal(str, str)

    def __init__(self, url=None, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QDialog.__init__(self, parent, f)
        self.setupUi(self)

        if url:
            self.URLTextEdit.setPlainText(url)
        self.show()
        return


    def help_slot(self):
        self.helpWindow = help.Help(self, "importURL.html")
        return


    def ok_slot(self):
        url = str(self.URLTextEdit.toPlainText())
        try:
            fp = urllib.urlopen(url)
            lines = fp.readlines()
        except Exception as e:
            QtGui.QMessageBox.information(
                None,
                "Failed to open URL",
                "Could not open the specified URL.  Please check to ensure \
                that you have entered the correct URL.\n\n{0}".format(str(e))
            )
            return


        html = ''.join(lines)

        self.urlImported.emit(html, url)

        self.accept()
        return

#-----------------------------------------------------------------------------#
