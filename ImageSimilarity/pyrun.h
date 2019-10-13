#ifndef PYRUN_H
#define PYRUN_H

#include <Python.h>
#include <marshal.h>

#include <QString>

#include "img_search_result.h"

class PyRun
{
public:
    PyRun(QString);
    ~PyRun();

    enum Network_Type{PCA, CONVOLUTIONAL};

    //App functionality
    Img_Search_Result* image_Search(PyObject *db, PyObject *encoder, QString filepath, int max_dist);
    PyObject* make_Neural_Network(Network_Type);
    void load_Weights(PyObject *encoder, QString filepath);
    PyObject* load_Database(QString);
    void save_Database(PyObject*, QString name, bool overwrite);
    PyObject* build_Database(PyObject *encoder, QString dir);


private:
    std::wstring execFile;
    std::wstring pythonPath;
    bool hasError();
    PyObject* importModule(const QByteArray&, const QString&);
    PyObject* callFunction(PyObject*, QString, PyObject*);
    QString ObjectToString(PyObject*);
};

#endif // PYRUN_H
