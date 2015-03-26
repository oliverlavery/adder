#ifndef ADDER_API_INCLUDED
#define ADDER_API_INCLUDED

#if defined(SWIG)
#define ADDERAPI
#elif defined(ADDER_EXPORTS)
#define ADDERAPI __declspec(dllexport) 
#else
#define ADDERAPI __declspec(dllimport) 
#endif
#pragma warning(disable:4311)
#pragma warning(disable:4312)

//#define ADDER_TRACE
#ifdef ADDER_TRACE
#define TRACE( a ) a
#else
#define TRACE( a )
#endif

#endif