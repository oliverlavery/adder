%module(directors="1") adder

%{
#include "adder.h"
%}
%include "typemaps.i"
%include "cpointer.i"
%include "cdata.i"

// Typemaps for better int handling with python 2.3
%typemap(in,parse="i") int "";
%typemap(in,parse="h") short "";
%typemap(in,parse="l") long "";
%typemap(in,parse="b") signed char "";

%typemap(in,parse="I") unsigned int "";
%typemap(in,parse="H") unsigned short "";
%typemap(in,parse="k") unsigned long "";
%typemap(in,parse="B") unsigned char "";

%typemap(in) 
             const unsigned int & (unsigned int temp),
             const unsigned long & (unsigned long temp)
{             
	temp = ($*1_ltype) PyInt_AsUnsignedLongMask($input);
    if (PyErr_Occurred()) SWIG_fail;
    $1 = &temp;
}        

%typemap(out)  unsigned int, unsigned long {
	// expand to long if we can't store it in an int
	if ( ( $1 & 1<<31 ) != 0) {
		$result = PyLong_FromUnsignedLong($1);
	} else {
		$result = PyInt_FromLong($1);
	}	
}

%typemap(out) const unsigned int &,
              const unsigned long & {
	if ( ( *($1) & 1<<31 ) != 0) {
		$result = PyLong_FromUnsignedLong(*($1));
	} else {
		$result = PyInt_FromLong(*($1));
	}	
}	

%typemap(varin) unsigned int, unsigned long
{
  unsigned long temp = PyInt_AsUnsignedLongMask($input);
  if (PyErr_Occurred()) {
    PyErr_SetString(PyExc_TypeError, "C variable '$name ($1_ltype)'");
    return 1;
  }
  $1 = ($1_type) temp;
}

%typemap(varout)      unsigned int,
                      unsigned long {
	// expand to long if we can't store it in an int
	if ( ( $1 & 1<<31 ) != 0) {
		$result = PyLong_FromUnsignedLong($1);
	} else {
		$result = PyInt_FromLong($1);
	}	
}


// From SWIG docs.
// These typemaps handle reading and writing arrays of chars as 
// Python strings

// typemap for an outgoing buffer
%typemap(in) (void *wbuffer, size_t len) {
   if (!PyString_Check($input)) {
       PyErr_SetString(PyExc_ValueError, "Expecting a string");
       return NULL;
   }
   $1 = (void *) PyString_AsString($input);
   $2 = PyString_Size($input);
}

// typemap for an incoming buffer
%typemap(in) (void *rbuffer, size_t len) {
   if (!PyInt_Check($input)) {
       PyErr_SetString(PyExc_ValueError, "Expecting an integer");
       return NULL;
   }
   $2 = PyInt_AsLong($input);
   if ($2 < 0) {
       PyErr_SetString(PyExc_ValueError, "Positive integer expected");
       return NULL;
   }
   $1 = (void *) malloc($2);
}

// Return the buffer.  Discarding any previous return result
%typemap(argout) (void *rbuffer, size_t len) {
   Py_XDECREF($result);   /* Blow away any previous result */
   if (result < 0) {      /* Check for I/O error */
       free($1);
       PyErr_SetFromErrno(PyExc_IOError);
       return NULL;
   }
   $result = PyString_FromStringAndSize((char *)$1, (int)result);
   free($1);
}

// typemap for an incoming wide char buffer
%typemap(in) (wchar_t *urbuffer, size_t len) {
   if (!PyInt_Check($input)) {
       PyErr_SetString(PyExc_ValueError, "Expecting an integer");
       return NULL;
   }
   $2 = PyInt_AsLong($input);
   if ($2 < 0) {
       PyErr_SetString(PyExc_ValueError, "Positive integer expected");
       return NULL;
   }
   $1 = (wchar_t *) malloc($2 * sizeof(wchar_t) );
}

// Typemap for unicode string output
%typemap(argout) (wchar_t *urbuffer, size_t len) {
   Py_XDECREF($result);   /* Blow away any previous result */
   if (result < 0) {      /* Check for I/O error */
       free($1);
       PyErr_SetFromErrno(PyExc_IOError);
       return NULL;
   }
   $result = PyUnicode_FromWideChar($1, (int)result);
   free($1);
}

// Typemap for string + length input
%apply (char *STRING, int LENGTH) { (char *in_str, int len) };



// This macro expands the python registers object with helpers so that
// we can use syntax like 'regs.eax' instead of 'regs.r32.eax'.
// Cleans up the python and saves typing...
%define %registers_pseudomember(NAME, SIZE)
%extend registers{
	uint##SIZE NAME;	
}
%{
uint##SIZE registers_##NAME##_get(registers *r) {
	return r->r##SIZE##.##NAME;
}
void registers_##NAME##_set(registers *r, uint##SIZE val) {
	r->r##SIZE##.##NAME = val;
}
%}
%enddef

%define %constant_pseudomember(CLASS, NAME, TYPE)
%extend CLASS {
	const TYPE NAME;	
}
%{
TYPE CLASS##_##NAME##_get(CLASS *c) {
	return c->##NAME;
}
%}
%enddef


// Turn on exception handling for ptr class
%exception {
	try {
		$action
	} catch ( char *s ) {
		PyErr_SetString( PyExc_RuntimeError, s );
		return NULL;
	} catch (...) {
		return NULL;
	} 
}

%inline %{
#include <windows.h>

#define ACCESS_ERROR_STR "Access Violation"
#define PROTECTION_ERROR_STR "Unable to change memory page protection"
#define NOTFOUND_ERROR_STR "Search item not found"

class ptr {
public:

	ptr() 
		: pvoid( NULL ), auto_write( false ), never_write( false ) {} ;
	ptr( const ptr &cpy ) 
		: pvoid( cpy.pvoid ), auto_write( cpy.auto_write ), never_write( cpy.never_write ) {} ;

	ptr( PyObject *p ) 
		: auto_write( false ), never_write( false ) {
//		puts("Ptr() with PyObject argument.");
		
		// Integer PyObject. value == address
        if ( PyInt_Check( p ) || PyLong_Check( p ) ) {
//		  puts("PyObject argument is int.");
		  unsigned long temp = PyInt_AsUnsignedLongMask(p);
		  if (PyErr_Occurred()) {
		    PyErr_SetString(PyExc_TypeError, "Unable to convert int argument to C type");
//			puts("bad conversion. throwing.");
		    throw 0;
		  }
		  pvoid = (void *)temp;
        } 
        // Convert SWIG pointer type to void * directly
        else if (SWIG_ConvertPtr(p, (void **) &pvoid, 0, 0) != -1) {                
//        		puts("PyObject argument is a SWIG C-ptr.");
                PyErr_Clear();
        }
        // Not an integer and not a SWIG pointer. Try the Python buffer interface
        else if ( PyObject_CheckReadBuffer(p) ) {
			int foo;
//            puts("Argument supports buffer interface");
            if ( PyObject_AsWriteBuffer( p, (void**)&pvoid, &foo ) == -1 ) {
//	            puts("no write buffer interface");
	            PyErr_Clear();
	            if ( PyObject_AsReadBuffer( p, (const void**)&pvoid, &foo ) == -1 ) {
//		            puts("no read buffer interface");
		            throw 0;
		        }
				// We got a read buffer so the object is immutable.
				// never allow writes through this pointer.
				never_write = true;
            } 
        }
		else {
			PyErr_SetString(PyExc_TypeError, "Invalid argument to ptr() ctor.");
//			puts("invalid. throwing.");
			throw 0;
		}
	}

	// These get shadowed by the PyObject* ctor when called from python.
	// They are only used from C++
	ptr( unsigned int i ) 
		: pvoid( (void *)i ), auto_write( false ), never_write( false ) {} ;
	ptr( void *p ) 
		: pvoid( p ), auto_write( false ), never_write( false ) {} ;
	ptr( void *p, bool autow, bool never ) 
		: pvoid( p ), auto_write( autow ), never_write( never ) {} ;

	
	~ptr() {};
	
	ptr operator+(const unsigned int c) const{
		return ptr( (void *)( (char*)pvoid + c ), auto_write, never_write );
	};
	ptr operator-(const unsigned int c) const{
		return ptr( (void *)( (char*)pvoid - c ), auto_write, never_write );
	};
	bool operator>(const ptr &p) const{
		return pvoid > p.pvoid;
	};
	bool operator>(const unsigned int c) const{
		return pvoid > (void*)c;
	};
	bool operator>=(const ptr &p) const{
		return pvoid >= p.pvoid;
	};
	bool operator>=(const unsigned int c) const{
		return pvoid >= (void*)c;
	};
	bool operator<(const ptr &p) const{
		return pvoid < p.pvoid;
	};
	bool operator<(const unsigned int c) const{
		return pvoid < (void*)c;
	};
	bool operator<=(const ptr &p) const{
		return pvoid <= p.pvoid;
	};
	bool operator<=(const unsigned int c) const{
		return pvoid <= (void*)c;
	};
	bool operator==(const ptr &p) const{
		return p.pvoid == pvoid;
	};
	bool operator==(const unsigned int c) const{
		return pvoid == (void*)c;
	};
	bool operator!=(const ptr &p) const {
		return p.pvoid != pvoid;
	};
	bool operator!=(const unsigned int c) const{
		return pvoid != (void*)c;
	};

	void add( unsigned int c ) {
		pvoid = (char*)pvoid + c;
	}
	
	void sub( unsigned int c ) {
		pvoid = (char*)pvoid + c;
	}
		
	uint32 to_int() const {
		return (uint32)pvoid;
	};
	
	void *to_pvoid() const {
		return pvoid;
	};
	
	bool can_read( size_t nbytes ) const {
		return !IsBadReadPtr( pvoid, nbytes );
	};
	
	bool can_read() const {
		return can_read(1);
	};
	
	// XXX: These two refer to the underlying memory pages.
	// if set_read_only( False ) is called
	// the pointer will be writeable, but this 
	// will still return false
	bool can_write( size_t nbytes ) const {
		return !never_write && !IsBadWritePtr( pvoid, nbytes );
	};

	bool can_write() const {
		return can_write(1);
	};

	bool is_read_only() const {
		if ( !can_read(1) ) {
		     return true;
		}
		return !( can_write(1) || auto_write );
	};
	
	void set_read_only( bool b ) {
		if ( never_write || !can_read(1) ) {
		     throw ACCESS_ERROR_STR;
		     return;
		}
		auto_write = !b;		
	};

	// Not really intended for use from python.
	// Still, could be handy for something.
	// One such thing might be guard pages...
	int set_protection( int protection, size_t nbytes ) const {
		bool ret;
		DWORD old;
		
		if ( !can_read( nbytes ) ) {
		     throw ACCESS_ERROR_STR;
		}
		ret = VirtualProtect( pvoid, nbytes, protection, &old);
		if ( !ret ) {
		     throw PROTECTION_ERROR_STR;
		}
		return old;	
	};
	
	uint8 read_byte() {
		if ( !can_read( sizeof(char) ) ) {
		     throw ACCESS_ERROR_STR;
		}
		return *(uint8*)pvoid;
	};

	char read_char() {
		if ( !can_read( sizeof(char) ) ) {
		     throw ACCESS_ERROR_STR;
		}
		return *(char*)pvoid;
	};
	
	uint16 read_short() {
		if ( !can_read( sizeof(short int) ) ) {
		     throw ACCESS_ERROR_STR;
		}
		return *(uint16*)pvoid;	
	};
	
	uint32 read_int() {
		if ( !can_read( sizeof(int) ) ) {
		     throw ACCESS_ERROR_STR;
		}
		return *(uint32*)pvoid;
	};
	
	float read_float() {
		if ( !can_read( sizeof(float) ) ) {
		     throw ACCESS_ERROR_STR;
		}
		return *(float*)pvoid;
	};
	
	double read_double() {
		if ( !can_read( sizeof(double) ) ) {
		     throw ACCESS_ERROR_STR;
		}
		return *(double*)pvoid;
	};
	
	void write_byte( uint8 c ) {
		DWORD old_protect = 0;
		if ( !can_write( sizeof( uint8 ) ) ) {
		     if ( !auto_write ) {
				throw ACCESS_ERROR_STR;
			 } else {
				old_protect = set_protection( PAGE_EXECUTE_READWRITE, sizeof( uint8 ) );
				if ( !old_protect ) return;
			 }
		}
		*(uint8 *)pvoid = c;
		if (old_protect) set_protection( old_protect, sizeof( uint8 ) );
	};

	void write_char( char c ) {
		DWORD old_protect = 0;
		if ( !can_write( sizeof( char ) ) ) {
		     if ( !auto_write ) {
				throw ACCESS_ERROR_STR;
			 } else {
				old_protect = set_protection( PAGE_EXECUTE_READWRITE, sizeof( char ) );
				if ( !old_protect ) return;
			 }
		}
		*(char *)pvoid = c;
		if (old_protect) set_protection( old_protect, sizeof( char ) );
	};

	
	void write_short( uint16 s ) {
		DWORD old_protect = 0;
		if ( !can_write( sizeof( uint16 ) ) ) {
		     if ( !auto_write ) {
				throw ACCESS_ERROR_STR;
			 } else {
				old_protect = set_protection( PAGE_EXECUTE_READWRITE, sizeof( uint16 ) );
				if ( !old_protect ) return;
			 }
		}
		*(uint16 *)pvoid = s;
		if (old_protect) set_protection( old_protect, sizeof( uint16 ) );
	};

	void write_int( uint32 i ) {
		DWORD old_protect = 0;
		if ( !can_write( sizeof( uint32 ) ) ) {
		     if ( !auto_write ) {
				throw ACCESS_ERROR_STR;
			 } else {
				old_protect = set_protection( PAGE_EXECUTE_READWRITE, sizeof( uint32 ) );
				if ( !old_protect ) return;
			 }
		}
		*(uint32 *)pvoid = i;
		if (old_protect) set_protection( old_protect, sizeof( uint32 ) );
	};
	
	void write_float( float f ) {
		DWORD old_protect = 0;
		if ( !can_write( sizeof( float ) ) ) {
		     if ( !auto_write ) {
				throw ACCESS_ERROR_STR;
			 } else {
				old_protect = set_protection( PAGE_EXECUTE_READWRITE, sizeof( float ) );
				if ( !old_protect ) return;
			 }
		}
		*(float *)pvoid = f;
		if (old_protect) set_protection( old_protect, sizeof( float ) );
	};
	
	void write_double( double d ) {
		DWORD old_protect = 0;
		if ( !can_write( sizeof( double ) ) ) {
		     if ( !auto_write ) {
				throw ACCESS_ERROR_STR;
			 } else {
				old_protect = set_protection( PAGE_EXECUTE_READWRITE, sizeof( double ) );
				if ( !old_protect ) return;
			 }
		}
		*(double *)pvoid = d;
		if (old_protect) set_protection( old_protect, sizeof( double ) );
	};

	// These use typemaps specified at the beginning of this file.
	
	size_t read_bytes( void *rbuffer, size_t len ) {
		if ( !can_read( len ) ) {
		     throw ACCESS_ERROR_STR;
		}
		memmove( rbuffer, pvoid, len );
		return len;
	};
	
	void write_bytes( void *wbuffer, size_t len ) {
		DWORD old_protect = 0;
		if ( !can_write( len ) ) {
		     if ( !auto_write ) {
				throw ACCESS_ERROR_STR;
			 } else {
				old_protect = set_protection( PAGE_EXECUTE_READWRITE, len );
				if ( !old_protect ) return;
			 }
		}
		memmove( pvoid, wbuffer, len );
		if (old_protect) set_protection( old_protect, len );
	};

	size_t read_strz( void *rbuffer, size_t len ) {
		int offset;
		if ( !can_read( len ) ) {
		     throw ACCESS_ERROR_STR;
		}
		offset = find_byte( 0, len );
		if ( offset < 0 ) {
		     return 0;
		}
		memmove( rbuffer, pvoid, offset );
		return offset;
	};

	size_t read_unistrz( wchar_t *urbuffer, size_t len ) {
		int offset;
		if ( !can_read( len ) ) {
		     throw ACCESS_ERROR_STR;
		}
		offset = find_short( 0, len / sizeof( wchar_t ) );
		if ( offset < 0 ) {
		     return 0;
		}		
		memmove( (void *)urbuffer, pvoid, offset * sizeof( wchar_t ) );
		return offset;
	};

	int find_byte( uint8 b, int distance ) {
		byte *bptr = (byte *)pvoid;
		int i = 0;
		try {
			for (i = 0; i <= distance && bptr[i] != b; i++);
		} catch (...) {
		     throw ACCESS_ERROR_STR;
		}
		if ( i <= distance ) return i;
		else {
			throw NOTFOUND_ERROR_STR;
		}     
	}

	int find_short( uint16 b, int distance ) {
		uint16 *bptr = (uint16 *)pvoid;
		int i = 0;
		try {
			for (i = 0; i < distance && bptr[i] != b; i++);
		} catch (...) {
		     throw ACCESS_ERROR_STR;
		}
		if ( i < distance ) return i;
		else {
			throw NOTFOUND_ERROR_STR;
		}     
	}

	// Hack to make SWIGed conversion operators work right
	// with a protected member
	friend uint32 ptr___int__(ptr *self);
	friend char* ptr___str__(ptr *self);
	
protected:
	void *pvoid;
	bool auto_write;
	bool never_write;
};
%}

// Back to Default exception handling
%exception;

%extend ptr {
	char *__str__() {
		static char tmp[16];
		sprintf(tmp,"0x%x", (int)self->pvoid );
		return tmp;
	}
	uint32 __int__() {
		return (unsigned int)self->pvoid;
	}
};

// This typemap redefines void pointer arguments to be ptr objects.
// XXX: extend it to accept a _real_ void* as well?
%typemap(in) (void *) {
	ptr *p;
	if ((SWIG_ConvertPtr($input,(void **) &p, $descriptor(ptr *), SWIG_POINTER_EXCEPTION)) == -1) {
        PyErr_SetString(PyExc_ValueError, "Expecting a ptr object");
		return NULL;
	}
	$1 = p->to_pvoid();
}

// This typemap redefines void * as a return value to return a 
// python ptr object instead. XXX object is owned by python (arg3)
// so this shouldn't leak (right?)
%typemap(out) (void *) {
	ptr *p = new ptr( $1 );
	$result = SWIG_NewPointerObj( (void *)p, $descriptor(ptr *), TRUE );
}

%rename(LoadLibrary) LoadLibraryPy;
%rename(GetProcAddress) GetProcAddressPy;

%feature("director") splice_callback;

////
// INCLUDE MAIN HEADER
////
%include "adder.h"

%registers_pseudomember( eflags, 32 )
%registers_pseudomember( edi, 32 )
%registers_pseudomember( esi, 32 )
%registers_pseudomember( ebp, 32 )
%registers_pseudomember( esp, 32 )
%registers_pseudomember( ebx, 32 )
%registers_pseudomember( edx, 32 )
%registers_pseudomember( ecx, 32 )
%registers_pseudomember( eax, 32 )
%registers_pseudomember( flags, 16 )
%registers_pseudomember( di, 16 )
%registers_pseudomember( si, 16 )
%registers_pseudomember( bp, 16 )
%registers_pseudomember( sp, 16 )
%registers_pseudomember( bx, 16 )
%registers_pseudomember( dx, 16 )
%registers_pseudomember( cx, 16 )
%registers_pseudomember( ax, 16 )
%registers_pseudomember( bl, 8 )
%registers_pseudomember( bh, 8 )
%registers_pseudomember( dl, 8 )
%registers_pseudomember( dh, 8 )
%registers_pseudomember( cl, 8 )
%registers_pseudomember( ch, 8 )
%registers_pseudomember( al, 8 )
%registers_pseudomember( ah, 8 )

// So we can print registers objects
%extend registers {
   char *__str__() {
   // XXX: This function is not thread safe!
       static char tmp[1024];
       unsigned short ah = self->r8.ah;
       unsigned short al = self->r8.al;
       unsigned short bh = self->r8.bh;
       unsigned short bl = self->r8.bl;
       unsigned short ch = self->r8.ch;
       unsigned short cl = self->r8.cl;
       unsigned short dh = self->r8.dh;
       unsigned short dl = self->r8.dl;
              
       sprintf(tmp,"ia32 registers:\n\teax = 0x%x\n\tebx = 0x%x\n\tecx = 0x%x\n\tedx = 0x%x\n"
					"\tesi = 0x%x\n\tedi = 0x%x\n\tesp = 0x%x\n\tebp = 0x%x\n\teflags = 0x%x\n"
					"\tax = 0x%hx\n\tbx = 0x%hx\n\tcx = 0x%hx\n\tdx = 0x%hx\n\tsi = 0x%hx\n"
					"\tdi = 0x%hx\n\tsp = 0x%hx\n\tbp = 0x%hx\n\tflags = 0x%hx\n\tah = 0x%hx\n"
					"\tal = 0x%hx\n\tbh = 0x%hx\n\tbl = 0x%hx\n\tch = 0x%hx\n\tcl = 0x%hx\n"
					"\tdh = 0x%hx\n\tdl = 0x%hx\n",
		 self->r32.eax, self->r32.ebx, self->r32.ecx, self->r32.edx, self->r32.esi, self->r32.edi,
		 self->r32.esp, self->r32.ebp, self->r32.eflags,
		 self->r16.ax, self->r16.bx, self->r16.cx, self->r16.dx, self->r16.si, self->r16.di, 
		 self->r16.sp, self->r16.bp, self->r16.flags,
		 ah, al, bh, bl, ch, cl, dh, dl 
       );
       return tmp;
   }
};


// SWIG has problems with static const members
// this is a bit of a hack to get around them
// (they're ifdef'd to not be const for swig, and
// making them %immutable prevents SWIG from generating
// mutators)
// Defining the consts inside the class seemed to work 
// better with VC++ 7, but doesn't compile under VC++ 6


%constant_pseudomember( x86_instruction, C_ERROR, unsigned int) 
%constant_pseudomember( x86_instruction, C_ADDR1, unsigned int)
%constant_pseudomember( x86_instruction, C_ADDR2, unsigned int)
%constant_pseudomember( x86_instruction, C_ADDR4, unsigned int)
%constant_pseudomember( x86_instruction, C_LOCK, unsigned int)
%constant_pseudomember( x86_instruction, C_67, unsigned int)
%constant_pseudomember( x86_instruction, C_66, unsigned int) 
%constant_pseudomember( x86_instruction, C_REP, unsigned int) 
%constant_pseudomember( x86_instruction, C_SEG, unsigned int) 
%constant_pseudomember( x86_instruction, C_ANYPREFIX, unsigned int) 
%constant_pseudomember( x86_instruction, C_DATA1, unsigned int) 
%constant_pseudomember( x86_instruction, C_DATA2, unsigned int) 
%constant_pseudomember( x86_instruction, C_DATA4, unsigned int) 
%constant_pseudomember( x86_instruction, C_SIB, unsigned int) 
%constant_pseudomember( x86_instruction, C_ADDR67, unsigned int) 
%constant_pseudomember( x86_instruction, C_DATA66, unsigned int) 
%constant_pseudomember( x86_instruction, C_MODRM, unsigned int) 
%constant_pseudomember( x86_instruction, C_BAD, unsigned int) 
%constant_pseudomember( x86_instruction, C_OPCODE2, unsigned int) 
%constant_pseudomember( x86_instruction, C_REL, unsigned int) 
%constant_pseudomember( x86_instruction, C_STOP, unsigned int) 


 /* Operand and instruction types */
/*                   Permissions: */
%constant_pseudomember( x86_instruction,  C_OP_R         ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_W         ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_X         ,unsigned int) 
/*                   Types: */
%constant_pseudomember( x86_instruction,  C_OP_UNK       ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_REG       ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_IMM       ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_REL       ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_ADDR      ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_EXPR      ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_PTR       ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_OFF       ,unsigned int) 
/*                   Modifiers: */
%constant_pseudomember( x86_instruction,  C_OP_SIGNED    ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_STRING    ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_CONST     ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_EXTRASEG  ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_CODESEG   ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_STACKSEG  ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_DATASEG   ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_DATA1SEG  ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_DATA2SEG  ,unsigned int) 
/*                   Size: */
%constant_pseudomember( x86_instruction,  C_OP_BYTE      ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_HWORD     ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_WORD      ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_DWORD     ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_QWORD     ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_SREAL     ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_DREAL     ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_XREAL     ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_BCD       ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_SIMD      ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_FPENV     ,unsigned int) 

/* operand masks */
%constant_pseudomember( x86_instruction,  C_OP_PERM_MASK ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_TYPE_MASK ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_MOD_MASK  ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_SEG_MASK  ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_SIZE_MASK ,unsigned int) 

%constant_pseudomember( x86_instruction,  C_OP_REG_MASK    ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_OP_REGTBL_MASK ,unsigned int) 

/* instruction types [groups] */
%constant_pseudomember( x86_instruction,  C_INS_EXEC		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_ARITH		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_LOGIC		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_STACK		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_COND		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_LOAD		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_ARRAY		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_BIT		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_FLAG		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_FPU		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_TRAPS		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_SYSTEM		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_OTHER		,unsigned int) 

/* C_INS_EXEC group */
%constant_pseudomember( x86_instruction,  C_INS_BRANCH		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_BRANCHCC	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_CALL		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_CALLCC		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_RET		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_LOOP		,unsigned int) 

/* C_INS_ARITH group */
%constant_pseudomember( x86_instruction,  C_INS_ADD 		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_SUB		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_MUL		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_DIV		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_INC		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_DEC		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_SHL		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_SHR		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_ROL		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_ROR		,unsigned int) 

/* C_INS_LOGIC group */
%constant_pseudomember( x86_instruction,  C_INS_AND		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_OR			,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_XOR		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_NOT		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_NEG		,unsigned int) 

/* C_INS_STACK group */
%constant_pseudomember( x86_instruction,  C_INS_PUSH		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_POP		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_PUSHREGS	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_POPREGS	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_PUSHFLAGS	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_POPFLAGS	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_ENTER		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_LEAVE		,unsigned int) 

/* C_INS_COND group */
%constant_pseudomember( x86_instruction,  C_INS_TEST		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_CMP		,unsigned int) 

/* C_INS_LOAD group */
%constant_pseudomember( x86_instruction,  C_INS_MOV		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_MOVCC		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_XCHG		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_XCHGCC		,unsigned int) 

/* C_INS_ARRAY group */
%constant_pseudomember( x86_instruction,  C_INS_STRCMP		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_STRLOAD	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_STRMOV		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_STRSTOR	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_XLAT		,unsigned int) 

/* C_INS_BIT group */
%constant_pseudomember( x86_instruction,  C_INS_BITTEST	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_BITSET		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_BITCLR		,unsigned int) 

/* C_INS_FLAG group */
%constant_pseudomember( x86_instruction,  C_INS_CLEARCF	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_CLEARZF	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_CLEAROF	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_CLEARDF	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_CLEARSF	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_CLEARPF	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_SETCF		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_SETZF		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_SETOF		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_SETDF		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_SETSF		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_SETPF		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_TOGCF		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_TOGZF		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_TOGOF		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_TOGDF		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_TOGSF		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_TOGPF		,unsigned int) 

/* C_INS_FPU */

/* C_INS_TRAP */
%constant_pseudomember( x86_instruction,  C_INS_TRAP		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_TRAPCC		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_TRET		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_BOUNDS		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_DEBUG		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_TRACE		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_INVALIDOP	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_OFLOW		,unsigned int) 

/* C_INS_SYSTEM */
%constant_pseudomember( x86_instruction,  C_INS_HALT		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_IN			,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_OUT		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_CPUID		,unsigned int) 

/* C_INS_OTHER */
%constant_pseudomember( x86_instruction,  C_INS_NOP		,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_BCDCONV	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_SZCONV		,unsigned int) 
 
   /* instruction size */
%constant_pseudomember( x86_instruction,  C_INS_BYTE      ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_WORD      ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_DWORD      ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_QWORD      ,unsigned int) 
   /* instruction modifiers */
%constant_pseudomember( x86_instruction,  C_INS_REPZ     ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_REPNZ    ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_LOCK     ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_DELAY    ,unsigned int) 

%constant_pseudomember( x86_instruction,  C_INS_TYPE_MASK	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_GROUP_MASK	,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_SIZE_MASK   ,unsigned int) 
%constant_pseudomember( x86_instruction,  C_INS_MOD_MASK    ,unsigned int) 

%extend x86_instruction {
   char *__str__() {
		static char tmp[256];
		return self->to_str(tmp, 256);
   }
};



%pythoncode {

import code

version = "Adder v0.3.2"

NULL = ptr(0x00000000)
        
def interact( readfunc=None, frame=None ):
	code.interact( version + "\n(C)2003 Oliver Lavery\n\ntype help() for help, or enter python commands\nType <Ctrl-Z> alone on a line to quit\n", readfunc, frame )
	
};