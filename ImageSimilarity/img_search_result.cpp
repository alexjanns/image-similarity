#include "img_search_result.h"

Img_Search_Result::Img_Search_Result(PyObject *poDicts)
{
    result = std::vector<DB_Entry>();

    if(PyList_Check(poDicts)){
        for(int i = 0; i < PyList_Size(poDicts); i++){
            if(PyDict_Check(PyList_GetItem(poDicts,i))){
                wchar_t *name = PyUnicode_AsWideCharString(PyDict_GetItemString(PyList_GetItem(poDicts,i), "name"), nullptr);
                wchar_t *path = PyUnicode_AsWideCharString(PyDict_GetItemString(PyList_GetItem(poDicts,i), "path"), nullptr);
                long dist = PyLong_AsLong(PyDict_GetItemString(PyList_GetItem(poDicts,i), "distance"));
                result.push_back(DB_Entry(QString(*name), QString(*path), dist));
            }
        }
    }

    // Release reference to result
    Py_XDECREF(poDicts);
}
