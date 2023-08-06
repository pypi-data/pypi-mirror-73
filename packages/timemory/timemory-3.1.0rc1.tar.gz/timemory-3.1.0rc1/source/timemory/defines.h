// MIT License
//
// Copyright (c) 2020, The Regents of the University of California,
// through Lawrence Berkeley National Laboratory (subject to receipt of any
// required approvals from the U.S. Dept. of Energy).  All rights reserved.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#pragma once

/// \file timemory/defines.h
/// \brief Provides the definitions for the installation if not using cmake

#if !defined(TIMEMORY_SOURCE) && !defined(TIMEMORY_CMAKE)

/* #undef DYNINST_API_RT */
#define TIMEMORY_PYTHON_PLOTTER "/opt/local/bin/python3.7"
/* #undef TIMEMORY_USE_ALLINEA_MAP */
#define TIMEMORY_USE_ARCH
/* #undef TIMEMORY_USE_CALIPER */
/* #undef TIMEMORY_USE_CRAYPAT */
/* #undef TIMEMORY_USE_CUDA */
/* #undef TIMEMORY_USE_CUPTI */
/* #undef TIMEMORY_USE_GOTCHA */
#define TIMEMORY_USE_GPERFTOOLS
/* #undef TIMEMORY_USE_LIKWID */
#define TIMEMORY_USE_MPI
#define TIMEMORY_USE_MPI_INIT
/* #undef TIMEMORY_USE_NVTX */
/* #undef TIMEMORY_USE_OMPT */
/* #undef TIMEMORY_USE_PAPI */
#define TIMEMORY_USE_PYTHON
#define TIMEMORY_USE_STATISTICS
/* #undef TIMEMORY_USE_TAU */
/* #undef TIMEMORY_USE_UPCXX */
/* #undef TIMEMORY_USE_VTUNE */
/* #undef TIMEMORY_USE_XRAY */
#define TIMEMORY_VEC 256

#endif
