# -*- coding: utf-8; mode: python; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4; truncate-lines: 0 -*-
# vi: set fileencoding=utf-8 filetype=python expandtab tabstop=4 shiftwidth=4 softtabstop=4 cindent:
# :mode=python:indentSize=4:tabSize=4:noTabs=true:

#-----------------------------------------------------------------------------#
# Installed modules

from PyQt4 import QtGui, QtCore

#-----------------------------------------------------------------------------#

MAX_SIZE = 50 # max number of files to retain

class RecentFiles:
    def __init__(self, parent, numShown=5, debug=None):
        self.parent = parent
        self.numShown = int(numShown)
        self.debug = debug
        self.__recent_files = []
        self.__indecies = []
        self.load()
        return


    def load(self):
        settings = QtCore.QSettings()
        # PyQt-BUG: beginReadArray() should return array size but returns always 0
        # as a workaround we loop until a value is "None".
        settings.beginReadArray("RecentFiles")
        i = -1
        while True:
            i += 1
            settings.setArrayIndex(i)
            try:
                s = settings.value("Filename").toPyObject()
                if s == None:
                    break
                self.__recent_files.append(str(s))
            except Exception as e:
                print("Loading of recent file entry {0} failed.".format(i))
                if self.debug: print(e)
                settings.remove("Filename")

        settings.endArray()

        if self.debug: print("recent_files: {0}".format(self.__recent_files))

        self.addToMenu()
        return


    def save(self):
        # truncate list if necessary
        self.__recent_files = self.__recent_files[:MAX_SIZE]
        s = QtCore.QSettings()
        s.beginWriteArray("RecentFiles")
        cnt = 0
        for f in self.__recent_files:
            s.setArrayIndex(cnt)
            s.setValue("Filename", f)
            cnt += 1
        s.sync()
        return


    def add(self, filename):
        try:
            self.__recent_files.remove(filename)
        except:
            pass

        self.__recent_files.insert(0, filename)
        self.save()
        self.addToMenu()
        return


    def clearMenu(self):
        # clear each menu entry...
        for idx in self.__indecies:
            self.parent.fileMenu.removeAction(idx)

        # clear list of menu entry indecies
        self.__indecies = []
        return


    def addToMenu(self, clear=1):
        if clear: self.clearMenu()

        # add applicable items to menu
        num = min(self.numShown, len(self.__recent_files))
        for i in range(num):
            filename = self.__recent_files[i]
            idx = self.parent.fileMenu.addAction(
                QtGui.QIcon(QtGui.QPixmap(":images/document-open-recent.png")),
                filename)

            self.__indecies.insert(0, idx)
        return


    def setNumShown(self, numShown):
        ns = int(numShown)
        if ns == self.numShown: return

        # clear menu of size X then add entries of size Y
        self.clearMenu()
        self.numShown = ns
        self.addToMenu(0)
        return


    def isRecentFile(self, menuid):
        return menuid in self.__indecies


"""
    def move(self, filename, menuid):
        # fix me....
        menu = self.parent.fileMenu
        idx = menu.indexOf(self.__indecies[0])
        menu.removeItem(menuid)
        # FIXME there is no QIconSet
        menu.insertItem(QIconSet(QtGui.QPixmap(":images/document-open-recent.png")),
                        filename,
                        -1,
                        idx)
        try:
            self.__recent_files.remove(filename)
        except:
            pass
        self.__indecies.insert(0, filename)
        return
"""

#-----------------------------------------------------------------------------#
