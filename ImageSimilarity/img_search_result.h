#ifndef IMG_SEARCH_RESULT_H
#define IMG_SEARCH_RESULT_H

#include <vector>
#include <QString>

#include <Python.h>

/*
 * This class is merely used for display purposes in the TableView
 */

struct DB_Entry{
public:
    DB_Entry(QString n, QString p, long d){
        name = n;
        path = p;
        distance = d;
    }
    QString get_name(){
        return name;
    }
    void set_name(QString n){
        name = n;
    }
    QString get_path(){
        return path;
    }
    void set_path(QString p){
        path = p;
    }
    long get_dist(){
        return distance;
    }
    void set_dist(int d){
        distance = d;
    }

private:
    QString name;
    QString path;
    long distance;
};

class Img_Search_Result
{
public:
    Img_Search_Result(PyObject* poDicts);
    ~Img_Search_Result();
    std::vector<DB_Entry> get_result();

private:
    std::vector<DB_Entry> result;
};

#endif // IMG_SEARCH_RESULT_H
