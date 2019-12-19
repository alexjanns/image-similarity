"""**************************************************************************
**
** Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
** All rights reserved.
** Contact: Nokia Corporation (qt-info@nokia.com)
**
** This file is part of the examples of the Qt Toolkit.
**
** You may use this file under the terms of the BSD license as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
**     the names of its contributors may be used to endorse or promote
**     products derived from this software without specific prior written
**     permission.
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
*****************************************************************************"""

from PyQt5.QtCore import (Qt, QAbstractTableModel, QModelIndex)
import operator

class TableModel(QAbstractTableModel):

    def __init__(self, results=None, parent=None):
        super(TableModel, self).__init__(parent)

        if results is None:
            self.results = []
        else:
            self.results = results

    def rowCount(self, index=QModelIndex()):
        """ Returns the number of rows the model holds. """
        return len(self.results)

    def columnCount(self, index=QModelIndex()):
        """ Returns the number of columns the model holds. """
        return 3

    def data(self, index, role=Qt.DisplayRole):
        """ Depending on the index and role given, return data. If not 
            returning data, return None (PyQt equivalent of QT's 
            "invalid QVariant").
        """
        if not index.isValid() or not 0 <= index.row() < len(self.results):
            return None

        if role == Qt.DisplayRole:
            name = self.results[index.row()]["name"]
            path = self.results[index.row()]["path"]
            distance = self.results[index.row()]["distance"]

            if index.column() == 0:
                if isinstance(name, bytes):
                    return name.decode('UTF-8')
                else:
                    return name
            elif index.column() == 1:
                if isinstance(path, bytes):
                    return path.decode('UTF-8')
                else:
                    return path
            elif index.column() == 2:
                return str(distance)

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """ Set the headers to be displayed. """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return "Name"
            elif section == 1:
                return "Path"
            elif section == 2:
                return "Distance"
        
        return None

    def sort(self, col, order):
        """Sort table by given column number. """
        self.layoutAboutToBeChanged.emit()
        self.results = sorted(self.results, key=operator.itemgetter(self.headerData(col, Qt.Horizontal).lower()))
        if order == Qt.DescendingOrder:
            self.results.reverse()
        self.layoutChanged.emit()
    
    def insertRows(self, position, rows=1, index=QModelIndex()):
        """ Insert a row into the model. """
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)

        for row in range(rows):
            self.results.insert(position + row, {"name":"", "path":"", "distance":0})

        self.endInsertRows()
        return True

    def appendRow(self, row, index=QModelIndex()):
        """ Append a row to the model. """
        self.beginInsertRows(QModelIndex(), len(self.results), len(self.results))
        
        self.results.append(row)
        
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        """ Remove a row from the model. """
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)

        del self.results[position:position+rows]

        self.endRemoveRows()
        return True

    def flags(self, index):
        """ Set the item flags at the given index. Seems like we're 
            implementing this function just to see how it's done, as we 
            manually adjust each tableView to have NoEditTriggers.
        """
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index))