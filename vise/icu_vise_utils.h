/*
 * Copyright (C) 2015 Kovid Goyal <kovid at kovidgoyal.net>
 *
 * Distributed under terms of the GPL3 license.
 */

#pragma once

#define UNICODE
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <unicode/uversion.h>
#include <unicode/utypes.h>
#include <unicode/uclean.h>
#include <unicode/utf16.h>
#include <unicode/ucol.h>
#include <unicode/ucoleitr.h>
#include <unicode/ustring.h>
#include <unicode/usearch.h>
#include <unicode/utrans.h>
#include <unicode/unorm.h>
#include <unicode/ubrk.h>

#if PY_VERSION_HEX < 0x03030000 
#error Not implemented for python < 3.3
#endif

// Roundtripping will need to be implemented differently for python 3.3+ where strings are stored with variable widths

#ifndef NO_PYTHON_TO_ICU
static UChar* python_to_icu(PyObject *obj, int32_t *osz, uint8_t do_check) {
    UChar *ans = NULL;
    Py_ssize_t sz = 0, i = 0;
    UErrorCode status = U_ZERO_ERROR;
	int kind = 0;
	void *data = NULL;
	PyObject *temp = NULL;

    if (do_check && !PyUnicode_CheckExact(obj)) {
        PyErr_SetString(PyExc_TypeError, "Not a unicode string");
        goto end;
    }
	if (PyUnicode_READY(obj) != 0) goto end;
	kind = PyUnicode_KIND(obj);

	switch (kind) {
		case PyUnicode_1BYTE_KIND:
			sz = PyUnicode_GET_LENGTH(obj);
			ans = (UChar*) calloc(sz+1, sizeof(UChar));  // Ensure null termination
			if (ans == NULL) { PyErr_NoMemory(); goto end; }
			data = PyUnicode_DATA(obj);
			for (i = 0; i < sz; i++) ans[i] = (UChar)PyUnicode_READ(kind, data, i);
			if (osz != NULL) *osz = (int32_t)sz;
			break;
		case PyUnicode_2BYTE_KIND:
			sz = PyUnicode_GET_LENGTH(obj);
			ans = (UChar*) calloc(sz+1, sizeof(UChar));  // Ensure null termination
			if (ans == NULL) { PyErr_NoMemory(); goto end; }
			memcpy(ans, PyUnicode_2BYTE_DATA(obj), sz);
			if (osz != NULL) *osz = (int32_t)sz;
			break;
		case PyUnicode_4BYTE_KIND:
			sz = PyUnicode_GET_LENGTH(obj);
			ans = (UChar*) calloc(2*(sz+1), sizeof(UChar));  // Ensure null termination
			if (ans == NULL) { PyErr_NoMemory(); goto end; }
			u_strFromUTF32(ans, (int32_t)(2*(sz+1)), osz, (UChar32*)PyUnicode_4BYTE_DATA(obj), (int32_t)sz, &status);
			if (U_FAILURE(status)) { PyErr_SetString(PyExc_ValueError, u_errorName(status)); free(ans); ans = NULL; goto end; }
			break;
		default:
			temp = PyUnicode_AsUTF16String(obj);
			if (temp == NULL) goto end;
			sz = PyBytes_GET_SIZE(temp);
			ans = (UChar*) calloc(sz+1, sizeof(UChar));  // Ensure null termination
			if (ans == NULL) { Py_DECREF(temp); temp = NULL; PyErr_NoMemory(); goto end; }
			memcpy(ans, PyBytes_AS_STRING(obj), sz);
			Py_DECREF(temp); temp = NULL;
			if (osz != NULL) *osz = (int32_t)PyUnicode_GET_LENGTH(obj);
	}
end:
    return ans;
}
#endif


#ifndef NO_ICU_TO_PYTHON
static PyObject* icu_to_python(UChar *src, int32_t sz) {
    return PyUnicode_DecodeUTF16((const char*)src, sz*sizeof(UChar), "strict", 0);
}
#endif


