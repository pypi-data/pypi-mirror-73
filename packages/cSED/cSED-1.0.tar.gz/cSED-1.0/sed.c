#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
#define MIN(X, Y) ((X) < (Y) ? (X) : (Y))

static PyObject *SED(PyObject *self, PyObject *args)
{
  const char *q;
  const char *r;

  if (!PyArg_ParseTuple(args, "ss", &q, &r))
    return NULL;

  int m = strlen(q);
  int n = strlen(r);

  int *mem_prev = (int *)malloc(sizeof(int) * (m + 1));
  int *mem = (int *)malloc(sizeof(int) * (m + 1));
  int *tmp_ptr;
  int sed = m;

  int i, j;

  for (i = 0; i <= m; i++)
  {
    mem_prev[i] = i;
  }

  for (j = 1; j <= n; j++)
  {
    mem[0] = 0;
    for (i = 1; i <= m; i++)
    {
      if (q[i - 1] == r[j - 1])
      {
        mem[i] = mem_prev[i - 1];
      }
      else
      {
        mem[i] = MIN(mem_prev[i], mem_prev[i - 1]);
        mem[i] = MIN(mem[i], mem[i - 1]) + 1;
      }
    }
    sed = MIN(sed, mem[m]);

    tmp_ptr = mem_prev;
    mem_prev = mem;
    mem = tmp_ptr;
  }

  free(mem_prev);
  free(mem);

  return PyLong_FromLong(sed);
}

static PyObject *SED_tmp(PyObject *self, PyObject *args)
{
  const char *q;
  const char *r;

//  printf("tmp");

  if (!PyArg_ParseTuple(args, "ss", &q, &r))
    return NULL;

  int m = strlen(q);
  int n = strlen(r);
//  printf("q=%s\n", q);
//  printf("r=%s\n", r);

  int *mem_prev = (int *)malloc(sizeof(int) * (m + 1));
  int *mem = (int *)malloc(sizeof(int) * (m + 1));
  int mem_idx[1000][1000];
//  int **mem_idx = (int **)malloc(sizeof(int) * (m+1));
  int i, j;
//  for(i =0 ; i < m+1 ; ++i){
//    mem_idx[i] = (int *)malloc(sizeof(int) * (n+1));
//  }
  char str[1000];
//  char* str = (char *)malloc(sizeof(char) * (n + 3));
//  for (i =0 ; i <m +1; ++i){
//      free(mem_idx[i]);
//  }
//  printf("free done\n");
//  free(mem_idx);
//  printf("free done\n");
//  free(str);
//  printf("free done\n");

  int *tmp_ptr;
  int sed = m;

//  printf("aaaaaaaaa\n");

  for (i = 0; i <= m; i++)
  {
    mem_prev[i] = i;
  }

//  printf("bbbbb\n");
  int min_pos = 0;
  for (j = 1; j <= n; j++)
  {
    mem[0] = 0;
    for (i = 1; i <= m; i++)
    {
      if (q[i - 1] == r[j - 1])
      {
        mem[i] = mem_prev[i - 1];
        mem_idx[i][j] = 3;
      }
      else
      {
        if (mem_prev[i] < mem_prev[i-1] && mem_prev[i] < mem[i-1]){
            mem_idx[i][j] = 1;
        }
        else if (mem_prev[i-1] < mem_prev[i] && mem_prev[i-1] < mem[i-1]){
            mem_idx[i][j] = 3;
        }
        else{
            mem_idx[i][j] = 2;
        }
        mem[i] = MIN(mem_prev[i], mem_prev[i - 1]);
        mem[i] = MIN(mem[i], mem[i - 1]) + 1;
      }
    }
    if (sed >= mem[m]){
        min_pos = j;
    }
//    printf("%d row ", j);
//    for (k=0; k<=m; k++) {
//        printf("%d", mem[k]);
//    }
//    printf("\n");
    sed = MIN(sed, mem[m]);
//    printf("aaa");

    tmp_ptr = mem_prev;
    mem_prev = mem;
    mem = tmp_ptr;
  }


  int cond;
  int curr_i = m;
  int curr_j = min_pos;
  int count = 0;
  while (curr_i > 0 && curr_j >0){
      cond = mem_idx[curr_i][curr_j];
      if (cond == 1){
          str[count] = r[curr_j-1];
//          printf("1:%d, %d\n" , curr_i, curr_j);
          count++;
          curr_j--;
      }else if (cond == 2){
//          printf("2:%d, %d\n" , curr_i, curr_j);
          curr_i--;
      }else if (cond == 3){
          str[count] = r[curr_j-1];
//          printf("3:%d, %d\n" , curr_i, curr_j);
          count++;
          curr_i--;
          curr_j--;
      }else{
          printf("asser\n");
          assert(true);
      }
  }
  str[count] = '\0';
  printf("q=%s\n", q);
  printf("r=%s\n", r);
//  printf("minpos=%d\n", min_pos);
  printf("x=");
  int len = strlen(str);
  for (i=len-1; i>=0; --i){
    printf("%c", str[i]);
  }
  printf("\n");
  free(mem_prev);
//  printf("free done\n");
  free(mem);
//  printf("free done\n");
//  for (i =0 ; i <=m; ++i){
//      free(mem_idx[i]);
//  }
//  printf("free done\n");
//  free(mem_idx);
//  printf("free done\n");
//  free(str);
//  printf("free done\n");
  return PyLong_FromLong(sed);
}
static PyObject *SED_D(PyObject *self, PyObject *args)
{
  const char *q;
  const char *r;
  int d;

  if (!PyArg_ParseTuple(args, "ssi", &q, &r, &d))
    return NULL;

  int m = strlen(q);
  int n = strlen(r);

  int *mem_prev = (int *)malloc(sizeof(int) * (m + 1));
  int *mem = (int *)malloc(sizeof(int) * (m + 1));
  int *tmp_ptr;

  int i;
  int j;
  for (i = 0; i <= m; i++)
  {
    mem_prev[i] = i;
  }

  for (j = 0; j <= n; j++)
  {
    mem[0] = 0;
    for (i = 1; i <= m; i++)
    {
      if (q[i - 1] == r[j - 1])
      {
        mem[i] = mem_prev[i - 1];
      }
      else
      {
        mem[i] = MIN(mem_prev[i], mem_prev[i - 1]);
        mem[i] = MIN(mem[i], mem[i - 1]) + 1;
      }
    }

    if (mem[m] <= d)
    {
      free(mem_prev);
      free(mem);
      Py_RETURN_TRUE;
    }

    tmp_ptr = mem_prev;
    mem_prev = mem;
    mem = tmp_ptr;
  }

  free(mem_prev);
  free(mem);
  Py_RETURN_FALSE;
}

static PyMethodDef SEDMethods[] = {
    {"SED", SED, METH_VARARGS, "Substring Edit Distance"},
    {"SED_tmp", SED_tmp, METH_VARARGS, "Substring Edit Distance print"},
    {"SED_D", SED_D, METH_VARARGS, "Substring Edit Distance with delta"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef cSEDPy = {
    PyModuleDef_HEAD_INIT,
    "cSED",
    "",
    -1,
    SEDMethods};

PyMODINIT_FUNC PyInit_cSED(void)
{
  return PyModule_Create(&cSEDPy);
}
