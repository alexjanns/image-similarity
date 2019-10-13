#include "pyrun.h"

#include <QString>
#include <QStringList>
#include <QDir>
#include <QFileInfo>
#include <QDebug>

PyRun::PyRun(QString execFile)
{
    this->execFile = execFile.toStdWString();

    QStringList pythonPath;
    pythonPath << QDir::toNativeSeparators(QFileInfo(QFileInfo(execFile).absoluteDir(), "libpy34.zip").canonicalFilePath());

    this->pythonPath = pythonPath.join(":").toStdWString();

    // Path of our executable
    Py_SetProgramName((wchar_t*) this->execFile.c_str());

    // Set module search path
    Py_SetPath(this->pythonPath.c_str());

    Py_NoSiteFlag = 1;

    // Initialize the Python interpreter
    Py_InitializeEx(0);

    qDebug() << "Python interpreter version:" << QString(Py_GetVersion());
    qDebug() << "Python standard library path:" << QString::fromWCharArray(Py_GetPath());

    QFile f("://res/ImageSimilarity.py.codeobj");

    if(f.open(QIODevice::ReadOnly))
    {
        QByteArray codeObj = f.readAll();
        f.close();
        importModule(codeObj, "ImageSimilarity");
    }
}

PyRun::~PyRun()
{
    Py_Finalize();
}

PyObject* PyRun::importModule(const QByteArray& codeObj, const QString& moduleName)
{
    PyObject *poModule = nullptr;

    // Get reference to main module
    PyObject *mainModule = PyImport_AddModule("__main__");

    // De-serialize Python code object
    PyObject *poCodeObj = PyMarshal_ReadObjectFromString((char*)codeObj.data(), codeObj.size());

    if(!hasError())
    {
        // Load module from code object
        poModule = PyImport_ExecCodeModule(moduleName.toUtf8().data(), poCodeObj);

        if(!hasError())
        {
            // Add module to main module as moduleName
            PyModule_AddObject(mainModule, moduleName.toUtf8().data(), poModule);
        }

        // Release object reference (Python cannot track references automatically in C++!)
        Py_XDECREF(poCodeObj);
    }

    return poModule;
}

PyObject* PyRun::callFunction(PyObject *poModule, QString funcName, PyObject *poArgs)
{
    PyObject *poRet = nullptr;

    // Get reference to function funcName in module poModule
    PyObject *poFunc = PyObject_GetAttrString(poModule, funcName.toUtf8().data());

    if(!hasError())
    {
        // Call function with arguments poArgs
        poRet = PyObject_CallObject(poFunc, poArgs);

        if(hasError())
        {
            poRet = nullptr;
        }

        // Release reference to function
        Py_XDECREF(poFunc);
    }

    // Release reference to arguments
    Py_XDECREF(poArgs);

    return poRet;
}

//Returns a list of dictionaries with keys 'path', 'code' and 'distance'
Img_Search_Result* PyRun::image_Search(PyObject *db, PyObject *encoder, QString filepath, int max_dist)
{
    PyObject *poRet = nullptr;

    // Get reference to ImageSimilarity module
    PyObject *poModule = PyImport_AddModule("ImageSimilarity");

    if(!hasError())
    {
        poRet = callFunction(poModule, "similarity_search", Py_BuildValue("uooi", filepath.toUtf8().constData(), db, encoder, max_dist));
    }

    // Release references to database and encoder
    Py_XDECREF(db);
    Py_XDECREF(encoder);

    return new Img_Search_Result(poRet);
}

PyObject* PyRun::make_Neural_Network(Network_Type mode){
    PyObject *poRet = nullptr;

    // Get reference to ImageSimilarity module
    PyObject *poModule = PyImport_AddModule("ImageSimilarity");

    if(!hasError())
    {
        if(mode == Network_Type::PCA){
            poRet = callFunction(poModule, "build_pca_autoencoder", nullptr);
        } else if (mode == Network_Type::CONVOLUTIONAL) {
            poRet = callFunction(poModule, "build_deep_autoencoder", nullptr);
        }
    }

    return poRet;
}

void PyRun::load_Weights(PyObject* encoder, QString filepath){
    PyObject *poRet = nullptr;

    // Get reference to ImageSimilarity module
    PyObject *poModule = PyImport_AddModule("ImageSimilarity");

    if(!hasError())
    {
        poRet = callFunction(poModule, "load_NN_weights", Py_BuildValue("ou", encoder, filepath.toUtf8().constData()));
    }

    // Release reference to encoder
    Py_XDECREF(encoder);
}

PyObject* PyRun::build_Database(PyObject* encoder, QString dir){
    PyObject *poRet = nullptr;

    // Get reference to ImageSimilarity module
    PyObject *poModule = PyImport_AddModule("ImageSimilarity");

    if(!hasError())
    {
        poRet = callFunction(poModule, "build_code_database", Py_BuildValue("ou", encoder, dir.toUtf8().constData()));
    }

    // Release reference to encoder
    Py_XDECREF(encoder);

    return poRet;
}

PyObject* PyRun::load_Database(QString file){
    PyObject *poRet = nullptr;

    // Get reference to ImageSimilarity module
    PyObject *poModule = PyImport_AddModule("ImageSimilarity");

    if(!hasError())
    {
        poRet = callFunction(poModule, "load_database", Py_BuildValue("u", file.toUtf8().constData()));
    }

    return poRet;
}

void PyRun::save_Database(PyObject *db, QString name, bool overwrite){
    PyObject *poRet = nullptr;

    // Get reference to ImageSimilarity module
    PyObject *poModule = PyImport_AddModule("ImageSimilarity");

    if(!hasError())
    {
        poRet = callFunction(poModule, "save_database", Py_BuildValue("ouO", db, name.toUtf8().constData(), overwrite ? Py_True : Py_False));
    }
}

QString PyRun::ObjectToString(PyObject *poVal)
{
    QString val;

    if(poVal != nullptr)
    {
        if(PyUnicode_Check(poVal))
        {
            // Convert Python Unicode object to UTF8 and return pointer to buffer
            const char *str = PyUnicode_AsUTF8(poVal);

            if(!hasError())
            {
                val = QString(str);
            }
        }

        // Release reference to object
        Py_XDECREF(poVal);
    }

    return val;
}

bool PyRun::hasError()
{
    bool error = false;

    if(PyErr_Occurred())
    {
        // Output error to stderr and clear error indicator
        PyErr_Print();
        error = true;
    }

    return error;
}
