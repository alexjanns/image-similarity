#-------------------------------------------------
#
# Project created by QtCreator 2019-09-07T16:56:28
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = ImageSimilarity
TEMPLATE = app

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

CONFIG += c++11

SOURCES += \
        img_search_result.cpp \
        main.cpp \
        mainwindow.cpp \
        pyrun.cpp

HEADERS += \
        img_search_result.h \
        mainwindow.h \
        pyrun.h

FORMS += \
        mainwindow.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

win32: LIBS += -LC:/Users/Alex/Anaconda3/envs/tensorflow-gpu/libs/ -lpython36

INCLUDEPATH += C:/Users/Alex/Anaconda3/envs/tensorflow-gpu/include
DEPENDPATH += C:/Users/Alex/Anaconda3/envs/tensorflow-gpu/libs

win32:!win32-g++: PRE_TARGETDEPS += C:/Users/Alexander/Anaconda3/envs/tensorflow-gpu/libs/python36.lib
#else:win32-g++: PRE_TARGETDEPS += C:/Users/Alexander/Anaconda3/envs/tensorflow-gpu/libs/libpython36.a
