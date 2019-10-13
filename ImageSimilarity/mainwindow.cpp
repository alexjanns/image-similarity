#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(PyRun *pyrun, QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    //Connect signals and slots
    connect(ui->pushButton_build, &QPushButton::clicked, this, &MainWindow::on_pushButton_buildDB_clicked);
    connect(ui->pushButton_ldDB, &QPushButton::clicked, this, &MainWindow::on_pushButton_loadDB_clicked);
    connect(ui->pushButton_saveDB, &QPushButton::clicked, this, &MainWindow::on_pushButton_saveDB_clicked);
    connect(ui->pushButton_ldWTH, &QPushButton::clicked, this, &MainWindow::on_pushButton_loadWeights_clicked);
    connect(ui->pushButton_ldIMG, &QPushButton::clicked, this, &MainWindow::on_pushButton_loadIMG_clicked);
    connect(ui->pushButton_search, &QPushButton::clicked, this, &MainWindow::on_pushButton_Search_clicked);
    connect(ui->radioButton_PCA, &QRadioButton::clicked, this, &MainWindow::on_radioButton_PCA_checked);
    connect(ui->radioButton_CONV, &QRadioButton::clicked, this, &MainWindow::on_radioButton_Convolutional_checked);

    //Prepare table
    this->model =  new QStandardItemModel(0, 3);
    model->setHeaderData(0, Qt::Orientation::Horizontal, "Name", Qt::EditRole);
    model->setHeaderData(1, Qt::Orientation::Horizontal, "Distance", Qt::EditRole);
    model->setHeaderData(2, Qt::Orientation::Horizontal, "Path", Qt::EditRole);
    ui->tableView->setModel(model);

    //Prepare Python
    this->pyRun = pyrun;
    this->po_Encoder = pyRun->make_Neural_Network(pyRun->PCA);
    this->po_DB = nullptr;
    this->searchImagePath = "";
}

MainWindow::~MainWindow()
{
    delete ui;
    delete model;
}

void MainWindow::on_pushButton_buildDB_clicked(){
    QFileDialog dirdialog(this);
    dirdialog.setFileMode(QFileDialog::FileMode::Directory);
    dirdialog.setViewMode(QFileDialog::ViewMode::List);
    QStringList dirnames;
    if(dirdialog.exec()){
        dirnames = dirdialog.selectedFiles();
        this->po_DB = pyRun->build_Database(this->po_Encoder, dirnames.first());
    }
}

void MainWindow::on_pushButton_loadDB_clicked(){
    QString filename = QFileDialog::getOpenFileName(this, "Load Database", QDir::currentPath(), "Image Database (*.p)");
    if(!filename.isNull()){
        this->po_DB = pyRun->load_Database(filename);
    }
}

void MainWindow::on_pushButton_saveDB_clicked(){
    QString filename = QFileDialog::getSaveFileName(this, "Save Database", QDir::currentPath(), "Image Database (*.p)");
    if(!filename.isNull()){
        if(QFileInfo::exists(filename)){
            QMessageBox::StandardButton reply;
            reply = QMessageBox::question(this, "Overwrite?",
                                          "The selected file already exists. Are you sure you want to overwrite it?",
                                          QMessageBox::Yes | QMessageBox::No);
            if(reply == QMessageBox::Yes){
                pyRun->save_Database(po_DB, filename, true);
            }
        } else {
            pyRun->save_Database(po_DB, filename, false);
        }
    }

}

void MainWindow::on_pushButton_loadWeights_clicked(){
    QString filename = QFileDialog::getOpenFileName(this, "Load Weights", QDir::currentPath(), "Neural Network Weights (*.h5)");
    if(!filename.isNull()){
        pyRun->load_Weights(this->po_Encoder, filename);
    }
}

void MainWindow::on_pushButton_loadIMG_clicked(){
    QString filename = QFileDialog::getOpenFileName(this, "Load Image", QDir::currentPath(), "Images (*.jpg, *.jpeg, *.png, *.tga, *.bmp)");
    if(!filename.isNull()){
        this->searchImagePath = filename;
    }
}

void MainWindow::on_pushButton_Search_clicked(){
    if (this->searchImagePath != ""){
        this->result = pyRun->image_Search(this->po_DB, this->po_Encoder, this->searchImagePath, ui->spinBox->value());

        //Fill TableView with result
        std::vector<DB_Entry> entries = result->get_result();
        this->model->setRowCount(static_cast<int>(entries.size()));
        for(uint i = 0; i != static_cast<uint>(model->rowCount()); i++){
            QStandardItem *name = new QStandardItem(entries.at(i).get_name());
            QStandardItem *dist = new QStandardItem(entries.at(i).get_dist());
            QStandardItem *path = new QStandardItem(entries.at(i).get_path());
            model->setItem(static_cast<int>(i), 0, name);
            model->setItem(static_cast<int>(i), 1, dist);
            model->setItem(static_cast<int>(i), 2, path);
        }
    }
}

void MainWindow::on_radioButton_PCA_checked(){
    this->po_Encoder = pyRun->make_Neural_Network(pyRun->PCA);
}

void MainWindow::on_radioButton_Convolutional_checked(){
    this->po_Encoder = pyRun->make_Neural_Network(pyRun->CONVOLUTIONAL);
}
