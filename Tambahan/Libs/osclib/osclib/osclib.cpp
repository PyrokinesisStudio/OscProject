// osclib.cpp : Defines the exported functions for the DLL application.
//

#include "Python.h"
#include "stdafx.h"
#include <utility>
#include "osclib.h"
#include <iostream>
#include <stdio.h>
#include <float.h>


using namespace std;


int kali(int a, int b)
{
	return a * b;
}

//double kali2(double x, double y)
//{
//	printf("%f", x);
//	return x;
//}

//PyObject *
//kali2(PyObject *a, PyObject *b)
float
kali2(float a, float b)
{
	//PyFloatObject hasil;
	//hasil = a * b;
	//int kembalian = *hasil;
	//return kembalian;
	//int* h;
	//float x, y;
	//x = 3.5f;
	//y = 2.1f;
	cout << "test fungsi dari c++ ss" << endl;
	//cout << x << end;

	float y[2];
	float x;
	x = 23.2f;
	float c = x * b + a;
	printf("testlah %f", b);
	cout << endl;
	printf("testlah2 %f", x);
	cout << endl;
	printf("hasilnya %f", c);
	cout << endl;



	//return Py_BuildValue("f", x);
	return c;
}



PyObject 
kali3(float a, PyObject b)
{
	//PyFloatObject hasil;
	//hasil = a * b;
	//int kembalian = *hasil;
	//return kembalian;
	//int* h;
	//float x, y;
	//x = 3.5f;
	//y = 2.1f;


	printf("hasil kali3 ialah %f", a);
	double dd;
	dd = 5.2;


	//return Py_BuildValue("f", a);
	PyObject po;
	//po = new PyObject();
	po = PyFloat_FromDouble(dd);
	return po;
	//return PyFloat_FromDouble(dd);
	//return Py_BuildValue("d", dd);
	//return Py_RETURN_NONE;
}


//#define LIBDLL extern C __declspec(dllexport)
//
//
//LIBDLL int kali(int a, int b)
//{
//	return a * b;
//}


//int kali(int a, int b)
//{
//	return a * b;
//}

