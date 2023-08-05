#include <Python.h>
#include <datetime.h>
#include <stdio.h>
#include <plist/plist.h>


#define FMT_XML "xml"
#define FMT_BINARY "binary"

// object used to hold error information for backtrace
typedef struct _err_ctx err_ctx;
struct _err_ctx {
    char msg[256];
    err_ctx *next;
};

static err_ctx *err_append(err_ctx *ctx, const char *format, ...) {
    va_list ap;
    err_ctx *newctx = calloc(sizeof(err_ctx), 1);

    va_start(ap, format);

    size_t n = vsnprintf(newctx->msg, sizeof(newctx->msg), format, ap);
    if (n > sizeof(newctx->msg) - 3) {
        newctx->msg[sizeof(newctx->msg)-4] = '.';
        newctx->msg[sizeof(newctx->msg)-3] = '.';
        newctx->msg[sizeof(newctx->msg)-2] = '.';
        newctx->msg[sizeof(newctx->msg)-1] = 0;
    }
    if (ctx) {
        if (ctx->next) {
            free(ctx->next);
        }
        ctx->next = newctx;
    }
    return newctx;
    va_end(ap);
}

static void err_format(err_ctx *ctx, char *msg, size_t start, size_t length) {
    start += snprintf(msg + start, length - start, "%s", ctx->msg);
    if (ctx->next && length - start > 2) {
        msg[start] = ':';
        msg[start+1] = ' ';
        start += 2;
        
        err_format(ctx->next, msg, start, length);
    }
}

static void err_free(err_ctx *ctx) {
    if (ctx) {
        err_free(ctx->next);
    }
    free(ctx);
}

static PyObject *plistToPython(plist_t node, err_ctx *ctx);

static PyObject *plistArrayToPython(plist_t node, err_ctx *ctx) {
    PyObject *result = NULL;
    PyObject *item = NULL;
    plist_array_iter iter;
    plist_t next = NULL;
    size_t length = plist_array_get_size(node);
    result = PyList_New(length);

    if (!result) {
        err_append(ctx, "failed creating array of length %zu", length);
        return NULL;
    }
    plist_array_new_iter(node, &iter);

    for (size_t i = 0; i < length; i++) {
        plist_array_next_item(node, iter, &next);
        item = plistToPython(next, ctx);
        if (!next || !item) {
            err_append(ctx, "[%d]", i);
            Py_DECREF(result);
            result = NULL;
            break;
        }
        PyList_SetItem(result, i, item);
    }

    return result;
}

static PyObject *plistDictToPython(plist_t node, err_ctx *ctx) {
    plist_dict_iter iter;
    char *key;
    plist_t value;
    PyObject *result = PyDict_New();
    plist_dict_new_iter(node, &iter);
    plist_dict_next_item(node, iter, &key, &value);
    while (key && value) {
        PyObject *key_obj = Py_BuildValue("s", key);
        PyObject *value_obj = plistToPython(value, ctx);
        if (key_obj && value_obj) {
            PyDict_SetItem(result, key_obj, value_obj);
            free(key);
        } else {
            Py_DECREF(result);
            err_append(ctx, "%s", key);
            result = NULL;
            break;
        }
        plist_dict_next_item(node, iter, &key, &value);
    }
    return result;
}

static PyObject *plistToPython(plist_t node, err_ctx *ctx) {
    union {
        uint8_t boolean;
        uint64_t uint;
        double real;
        uint64_t uid;
        char *cstring;
        struct {
            uint64_t length;
            const void *ptr;
        } buf;
        struct {
            int32_t sec;
            int32_t usec;
        } datetime;
    } value;

    PyObject *result = NULL;

    switch (plist_get_node_type(node)) {
    case PLIST_ARRAY:
        result = plistArrayToPython(node, ctx);
        break;

    case PLIST_DICT:
        result = plistDictToPython(node, ctx);
        break;

    case PLIST_BOOLEAN:
        plist_get_bool_val(node, &value.boolean);
        result = PyBool_FromLong(value.boolean);
        break;

    case PLIST_UINT:
        plist_get_uint_val(node, &value.uint);
        result = Py_BuildValue("k", value.uint);
        break;

    case PLIST_REAL:
        plist_get_real_val(node, &value.real);
        result = Py_BuildValue("d", value.real);
        break;

    case PLIST_UID:
        plist_get_uid_val(node, &value.uid);
        result = Py_BuildValue("k", value.uid);
        break;

    case PLIST_DATE:
        plist_get_date_val(node, &value.datetime.sec, &value.datetime.usec);
// #define SEC_PER_DAY (24 * 3600)
        PyObject *delta = PyDelta_FromDSU(0, value.datetime.sec, value.datetime.usec);
        PyObject *ref = PyDateTime_FromDateAndTime(2001, 1, 1, 0, 0, 0, 0);
        if (ref && delta) {
            result = PyNumber_Add(ref, delta);
        }
        Py_XDECREF(delta);
        Py_XDECREF(ref);
        break;

    case PLIST_DATA:
        value.buf.ptr = plist_get_data_ptr(node, &value.buf.length);
        result = Py_BuildValue("y#", value.buf.ptr, value.buf.length);
        break;

    case PLIST_STRING:
        value.buf.ptr = plist_get_string_ptr(node, &value.buf.length);
        result = Py_BuildValue("s#", value.buf.ptr, value.buf.length);
        break;

    case PLIST_KEY:
        plist_get_key_val(node, &value.cstring);
        result = Py_BuildValue("s", value.cstring);
        break;

    case PLIST_NONE:
    default:
        Py_RETURN_NONE;
        break;
    }

    if (!result) {
        err_append(ctx, "invalid field value");
    }

    return result;
}

static plist_t plistFromPython(PyObject *obj, err_ctx *err);

static plist_t plistFromList(PyListObject *obj, err_ctx *err) {
    plist_t array = plist_new_array();
    ssize_t size = PyList_GET_SIZE(obj);
    for (ssize_t i = 0; i < size; i++) {
        plist_t item = plistFromPython(PyList_GET_ITEM(obj, i), err);
        if (!item) {
            err_append(err, "item %d", i);
            plist_free(item);
            return NULL;
        }
        plist_array_append_item(array, item);
    }
    return array;
}

static plist_t plistFromDict(PyObject *obj, err_ctx *err) {
    plist_t dict = plist_new_dict();
    ssize_t pos = 0;
    PyObject *key = NULL;
    PyObject *value = NULL;

    while (PyDict_Next(obj, &pos, &key, &value)) {
        if (!PyUnicode_Check(key)) {
            err_append(err, "invalid type for property list key: %s", key->ob_type->tp_name);
            plist_free(dict);
            return NULL;
        }
        const char *key_string = PyUnicode_AsUTF8(key);
        plist_t pvalue = plistFromPython(value, err);
        if (!pvalue) {
            err_append(err, "%s", key_string);
            plist_free(dict);
            return NULL;
        }
        plist_dict_set_item(dict, key_string, pvalue);
    }
    return dict;
}

static plist_t plistFromPython(PyObject *obj, err_ctx *err) {
    if (PyBytes_Check(obj)) {
        return plist_new_data(PyBytes_AS_STRING(obj), PyBytes_GET_SIZE(obj));

    } else if (PyByteArray_Check(obj)) {
        return plist_new_data(PyByteArray_AS_STRING(obj), PyByteArray_GET_SIZE(obj));

    } else if (PyDateTime_Check(obj)) {
        PyObject *ref = PyDateTime_FromDateAndTime(2001, 1, 1, 0, 0, 0, 0);
        if (ref) {
            PyObject *delta = PyNumber_Subtract(obj, ref);
            Py_DECREF(ref);
            if (delta) {
                int seconds = PyDateTime_DELTA_GET_SECONDS(delta) + PyDateTime_DELTA_GET_DAYS(delta) * 24 * 3600;
                int usecs = PyDateTime_DELTA_GET_MICROSECONDS(delta);
                PyObject_Print(delta, stdout, 0);
                Py_DECREF(delta);
                return plist_new_date(seconds, usecs);
            }
        }

    } else if (PyUnicode_Check(obj)) {
        return plist_new_string(PyUnicode_AsUTF8(obj));

    } else if (PyFloat_Check(obj)) {
        return plist_new_real(PyFloat_AsDouble(obj));

    } else if (PyBool_Check(obj)) {
        return plist_new_bool(PyLong_AsLong(obj));

    } else if (PyLong_Check(obj)) {
        return plist_new_uint(PyLong_AsUnsignedLong(obj));

    } else if (PyDict_Check(obj)) {
        return plistFromDict(obj, err);

    } else if (PyList_Check(obj)) {
        return plistFromList((PyListObject *)obj, err);
    }

    err_append(err, "can't serialize `%s`", obj->ob_type->tp_name);
    return NULL;
}


static PyObject *unserialize(Py_buffer *buffer) {
    plist_t plist = NULL;
    plist_from_memory(buffer->buf, buffer->len, &plist);
    PyBuffer_Release(buffer);
    if (plist) {
        err_ctx *root = err_append(NULL, "Error parsing plist");
        PyObject *value = plistToPython(plist, root);
        if (!value) {
            char err_str[4096] = {0};
            err_format(root, err_str, 0, 4095);
            PyErr_SetString(PyExc_ValueError, err_str);
        }
        plist_free(plist);
        err_free(root);
        return value;
    } else {
        return NULL;
    }
}

static PyObject *load(PyObject * self, PyObject * args) {
    PyObject *fobj = NULL;
    Py_buffer buffer;
    PyObject *result = NULL;
    if (!PyArg_ParseTuple(args, "O", &fobj)) {
        return NULL;
    }
    PyObject *read = PyObject_GetAttrString(fobj, "read");
    PyObject *read_args = Py_BuildValue("()");
    PyErr_SetString(PyExc_TypeError, "file object is not readable");
    if (read && PyCallable_Check(read) && read_args) {
        PyErr_Clear();
        PyObject *data = PyObject_Call(read, read_args, NULL);
        if (data && !PyObject_GetBuffer(data, &buffer, PyBUF_SIMPLE)) {
            result = unserialize(&buffer);
        }
        Py_XDECREF(data);
    }
    Py_XDECREF(read);
    Py_XDECREF(read_args);
    return result;
}

static PyObject *loads(PyObject * self, PyObject * args) {
    Py_buffer buffer;
    if (!PyArg_ParseTuple(args, "s*", &buffer)) {
        return NULL;
    }
    return unserialize(&buffer);
}

static PyObject *serialize(PyObject *obj, int xml) {
    err_ctx *err = err_append(NULL, "Error serializing plist");
    plist_t plist = plistFromPython(obj, err);
    
    if (!plist) {
        char err_str[4096] = {0};
        err_format(err, err_str, 0, 4095);
        PyErr_SetString(PyExc_ValueError, err_str);
        err_free(err);
        return NULL;
    }
    err_free(err);
    char *buf = NULL;
    uint32_t size = 0;
    PyObject *result = NULL;
    if (xml) {
        plist_to_xml(plist, &buf, &size);
        result = Py_BuildValue("s#", buf, size);
        plist_to_xml_free(buf);
    } else {
        plist_to_bin(plist, &buf, &size);
        result = Py_BuildValue("y#", buf, size);
        plist_to_bin_free(buf);
    }
    return result;
}

static PyObject *dumps(PyObject *self, PyObject *args, PyObject *kwargs) {
    PyObject *obj = NULL;
    const char *fmt = FMT_XML;
    static char *kwlist[] = {"object", "fmt",NULL};
    int xml = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|s", kwlist,
                                     &obj, &fmt)) {
        return NULL;
    }

    if (strcasecmp(fmt, FMT_XML) == 0) {
        xml = 1;
    } else if (strcasecmp(fmt, FMT_BINARY) == 0) {
        xml = 0;
    } else {
        PyErr_Format(PyExc_ValueError, "Unknown plist format: %s", fmt);
        return NULL;
    }
    return serialize(obj, xml);
}

static PyObject *dump(PyObject *self, PyObject *args, PyObject *kwargs) {
    PyObject *obj = NULL;
    PyObject *fobj = NULL;
    const char *fmt = FMT_XML;
    static char *kwlist[] = {"object", "fobj", "fmt",NULL};
    int xml = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|s", kwlist,
                                     &obj, &fobj, &fmt)) {
        return NULL;
    }

    if (strcasecmp(fmt, FMT_XML) == 0) {
        xml = 1;
    } else if (strcasecmp(fmt, FMT_BINARY) == 0) {
        xml = 0;
    } else {
        PyErr_Format(PyExc_ValueError, "Unknown plist format: %s", fmt);
        return NULL;
    }  

    PyObject *data = serialize(obj, xml);
    PyObject *result = NULL;

    if (data) {
        PyObject *write = PyObject_GetAttrString(fobj, "write");
        PyObject *write_args = Py_BuildValue("(O)", data);
        PyErr_SetString(PyExc_TypeError, "file object is not writeable");
        if (write && PyCallable_Check(write) && write_args) {
            PyErr_Clear();
            result = PyObject_Call(write, write_args, NULL);
        }
        Py_XDECREF(write);
        Py_XDECREF(write_args);
        Py_DECREF(data);
    }
    return result;
}

static PyMethodDef cplist_methods[] = {
    {
        "loads",
        loads,
        METH_VARARGS,
        "loads(data: <str or bytes>, /) -> object\n"
        "\n"
        "Load a plist from an XML or bytes"
    },
    {
        "load",
        load,
        METH_VARARGS,
        "load(fobj, /) -> object\n"
        "\n"
        "Load a plist from a file"
    },
    {
        "dumps",
        (PyCFunction)dumps,
        METH_VARARGS | METH_KEYWORDS,
        "dumps(object, fmt=FMT_XML, /) -> <str or bytes>\n"
        "\n"
        "Dump a plist to an XML or binary format"
    },
    {
        "dump",
        (PyCFunction)dump,
        METH_VARARGS | METH_KEYWORDS,
        "dump(object, fobj, fmt=FMT_XML, /)\n"
        "\n"
        "Dump a plist to a file"
    },
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef cplist_module = {
	PyModuleDef_HEAD_INIT,
	"cplist",
	"plist parser",
	-1,
	cplist_methods
};

PyMODINIT_FUNC PyInit_cplist(void) {
    PyObject * mod = PyModule_Create(&cplist_module);
    PyDateTime_IMPORT;

    PyObject *format_xml = Py_BuildValue("s", FMT_XML);
    PyObject *format_binary = Py_BuildValue("s", FMT_BINARY);
    Py_INCREF(format_xml);
    Py_INCREF(format_binary);

    if (PyModule_AddObject(mod, "FMT_XML", format_xml) < 0
        || PyModule_AddObject(mod, "FMT_BINARY", format_binary) < 0) {
        Py_XDECREF(format_xml);
        Py_XDECREF(format_binary);
        Py_DECREF(mod);
        return NULL;
    }
    return mod;
};
