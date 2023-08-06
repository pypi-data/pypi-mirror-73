/*
 * this file is part of pyliblzfse.
 *
 * Copyright (c) 2017-2020  Yogesh Khatri
 * Copyright (c) 2016, 2017 Dima Krasner
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#define PY_SSIZE_T_CLEAN
#include <lzfse.h>
#include <Python.h>

static PyObject *LzfseError;

static PyObject*
lzfse_op(PyObject* self,
         PyObject* args,
         size_t (*op)(uint8_t *__restrict,
                      size_t,
                      const uint8_t *__restrict,
                      size_t,
                      void *__restrict),
         size_t (*get_outlen)(const size_t, const uint8_t *buffer),
         size_t (*get_auxlen)(void))
{
    PyObject *str;
    const char *in;
    char *out;
    char *out_realloc;
    void *aux;
    Py_ssize_t inlen;
    size_t outlen;
    size_t op_output_len;

    if (!PyArg_ParseTuple(args, "s#", &in, &inlen))
        return NULL;

    outlen = get_outlen((size_t)inlen, (const uint8_t *)in);
    //if (op == lzfse_decode_buffer)
    //    outlen *= 4;
 
    out = (char *)malloc(outlen + 1);
    if (!out)
        return PyErr_NoMemory();

    aux = malloc(get_auxlen());
    if (!aux) {
        free(out);
        return PyErr_NoMemory();
    }
    while (1) {
        Py_BEGIN_ALLOW_THREADS
        op_output_len = op((uint8_t *)out,
                    outlen,
                    (const uint8_t *)in,
                    (size_t)inlen,
                    aux);
        Py_END_ALLOW_THREADS
        if (op == lzfse_decode_buffer) {
            if (op_output_len == 0) // output was zero, something went wrong!
                break;
            if (op_output_len == outlen) { // Dest buffer too small. Double it
                outlen *= 2;
                out_realloc = (char *)realloc(out, outlen);
                if (!out_realloc) {
                    free(out);
                    free(aux);
                    return PyErr_NoMemory();
                }
                else
                    out = out_realloc;
            }
            else
                break; // all good!
        }
        else
            break;
    }
    free(aux);

    if (!op_output_len) {
        free(out);
        PyErr_SetNone(LzfseError);
        return NULL;
    }

    out[op_output_len] = '\0';
#if PY_MAJOR_VERSION >= 3
    str = PyBytes_FromStringAndSize(out, (Py_ssize_t)op_output_len);
#else
    str = PyString_FromStringAndSize(out, (Py_ssize_t)op_output_len);
#endif
    free(out);
    if (!str)
        PyErr_SetNone(LzfseError);
    return str;
}

static size_t
get_encode_outlen(const size_t inlen, const uint8_t *buffer)
{
    /* Extra 12 bytes for start/end block magics and block length in case the
     * compressed output is larger than the input, as in lzfse_encode.c */
    return inlen + 12;
}

static PyObject*
lzfse_compress(PyObject* self, PyObject* args)
{
    return lzfse_op(self,
                    args,
                    lzfse_encode_buffer,
                    get_encode_outlen,
                    lzfse_encode_scratch_size);
}

PyDoc_STRVAR(compress_doc,
"compress(buffer) -- Compress a buffer using LZFSE.");

static size_t
get_decode_outlen(const size_t inlen, const uint8_t *buffer)
{
    // read uncompressed size from buffer, remove upper bits as size_t could be 8
    return (*(size_t*)(buffer + 4) ) & 0xFFFFFFFF;
}

static PyObject*
lzfse_decompress(PyObject* self, PyObject* args)
{
    return lzfse_op(self,
                    args,
                    lzfse_decode_buffer,
                    get_decode_outlen,
                    lzfse_decode_scratch_size);
}

PyDoc_STRVAR(decompress_doc,
"decompress(buffer) -- Decompress a LZFSE/LZVN-compressed buffer.");

static PyMethodDef LzfseMethods[] = {
    {"compress", lzfse_compress, METH_VARARGS, compress_doc},
    {"decompress", lzfse_decompress, METH_VARARGS, decompress_doc},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "liblzfse",
    "Python module for LZFSE",
    -1,
    LzfseMethods
};
#endif

PyMODINIT_FUNC
#if PY_MAJOR_VERSION >= 3
PyInit_liblzfse(void)
{
    PyObject *m = PyModule_Create(&moduledef);
    if (!m)
        return NULL;
#else
initlzfse(void)
{
    PyObject *m = Py_InitModule("liblzfse", LzfseMethods);
    if (!m)
        return;
#endif

    LzfseError = PyErr_NewException("liblzfse.error", NULL, NULL);
    if (LzfseError) {
        Py_INCREF(LzfseError);
        PyModule_AddObject(m, "error", LzfseError);
    }

#if PY_MAJOR_VERSION >= 3
    return m;
#endif
}
