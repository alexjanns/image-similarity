/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.12.5
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTableView>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QTableView *tableView;
    QRadioButton *radioButton_PCA;
    QRadioButton *radioButton_CONV;
    QPushButton *pushButton_build;
    QLabel *label;
    QPushButton *pushButton_ldDB;
    QPushButton *pushButton_ldIMG;
    QPushButton *pushButton_ldWTH;
    QPushButton *pushButton_saveDB;
    QPushButton *pushButton_search;
    QSpinBox *spinBox;
    QLabel *label_2;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(1095, 590);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        tableView = new QTableView(centralWidget);
        tableView->setObjectName(QString::fromUtf8("tableView"));
        tableView->setGeometry(QRect(10, 100, 1071, 381));
        radioButton_PCA = new QRadioButton(centralWidget);
        radioButton_PCA->setObjectName(QString::fromUtf8("radioButton_PCA"));
        radioButton_PCA->setGeometry(QRect(20, 70, 82, 17));
        radioButton_CONV = new QRadioButton(centralWidget);
        radioButton_CONV->setObjectName(QString::fromUtf8("radioButton_CONV"));
        radioButton_CONV->setGeometry(QRect(80, 70, 91, 17));
        pushButton_build = new QPushButton(centralWidget);
        pushButton_build->setObjectName(QString::fromUtf8("pushButton_build"));
        pushButton_build->setGeometry(QRect(10, 500, 91, 23));
        label = new QLabel(centralWidget);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(20, 40, 47, 13));
        pushButton_ldDB = new QPushButton(centralWidget);
        pushButton_ldDB->setObjectName(QString::fromUtf8("pushButton_ldDB"));
        pushButton_ldDB->setGeometry(QRect(120, 500, 91, 23));
        pushButton_ldIMG = new QPushButton(centralWidget);
        pushButton_ldIMG->setObjectName(QString::fromUtf8("pushButton_ldIMG"));
        pushButton_ldIMG->setGeometry(QRect(200, 60, 131, 23));
        pushButton_ldWTH = new QPushButton(centralWidget);
        pushButton_ldWTH->setObjectName(QString::fromUtf8("pushButton_ldWTH"));
        pushButton_ldWTH->setGeometry(QRect(340, 500, 131, 23));
        pushButton_saveDB = new QPushButton(centralWidget);
        pushButton_saveDB->setObjectName(QString::fromUtf8("pushButton_saveDB"));
        pushButton_saveDB->setGeometry(QRect(230, 500, 91, 23));
        pushButton_search = new QPushButton(centralWidget);
        pushButton_search->setObjectName(QString::fromUtf8("pushButton_search"));
        pushButton_search->setGeometry(QRect(1000, 500, 75, 23));
        spinBox = new QSpinBox(centralWidget);
        spinBox->setObjectName(QString::fromUtf8("spinBox"));
        spinBox->setGeometry(QRect(920, 500, 42, 22));
        spinBox->setMaximum(9999);
        spinBox->setDisplayIntegerBase(10);
        label_2 = new QLabel(centralWidget);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(840, 500, 71, 21));
        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 1095, 21));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        MainWindow->setStatusBar(statusBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", nullptr));
        radioButton_PCA->setText(QApplication::translate("MainWindow", "PCA", nullptr));
        radioButton_CONV->setText(QApplication::translate("MainWindow", "Convolutional", nullptr));
        pushButton_build->setText(QApplication::translate("MainWindow", "Build Database", nullptr));
        label->setText(QApplication::translate("MainWindow", "Method:", nullptr));
        pushButton_ldDB->setText(QApplication::translate("MainWindow", "Load Database", nullptr));
        pushButton_ldIMG->setText(QApplication::translate("MainWindow", "Load Image to Compare", nullptr));
        pushButton_ldWTH->setText(QApplication::translate("MainWindow", "Load Other NN Weights", nullptr));
        pushButton_saveDB->setText(QApplication::translate("MainWindow", "Save Database", nullptr));
        pushButton_search->setText(QApplication::translate("MainWindow", "Search!", nullptr));
        label_2->setText(QApplication::translate("MainWindow", "Max Distance:", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
