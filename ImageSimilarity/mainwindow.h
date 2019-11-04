#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "pyrun.h"
#include "img_search_result.h"

#include <QMainWindow>
#include <QStandardItemModel>
#include <QFileDialog>
#include <QMessageBox>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(PyRun *pyrun, QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void onPushButtonBuildDBClicked();
    void onPushButtonLoadDBClicked();
    void onPushButtonSaveDBClicked();
    void onPushButtonLoadWeightsClicked();
    void onPushButtonLoadIMGClicked();
    void onPushButtonSearchClicked();
    void onRadioButtonPCAChecked();
    void onRadioButtonConvolutionalChecked();

private:
    Ui::MainWindow *ui;
    PyRun *pyRun;
    Img_Search_Result *result;
    QStandardItemModel *model;

    QString applicationDirPath;
    QString searchImagePath;
    PyObject *po_Encoder;
    PyObject *po_DB;
};

#endif // MAINWINDOW_H
