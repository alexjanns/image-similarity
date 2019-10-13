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
    void on_pushButton_buildDB_clicked();
    void on_pushButton_loadDB_clicked();
    void on_pushButton_saveDB_clicked();
    void on_pushButton_loadWeights_clicked();
    void on_pushButton_loadIMG_clicked();
    void on_pushButton_Search_clicked();
    void on_radioButton_PCA_checked();
    void on_radioButton_Convolutional_checked();

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
