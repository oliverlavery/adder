# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.
import _adder
def _swig_setattr(self,class_type,name,value):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    self.__dict__[name] = value

def _swig_getattr(self,class_type,name):
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


try:
    from weakref import proxy as weakref_proxy
except:
    weakref_proxy = lambda x: x


cdata = _adder.cdata

memmove = _adder.memmove

ACCESS_ERROR_STR = _adder.ACCESS_ERROR_STR
PROTECTION_ERROR_STR = _adder.PROTECTION_ERROR_STR
NOTFOUND_ERROR_STR = _adder.NOTFOUND_ERROR_STR
class ptr(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ptr, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ptr, name)
    def __init__(self,*args):
        _swig_setattr(self, ptr, 'this', apply(_adder.new_ptr,args))
        _swig_setattr(self, ptr, 'thisown', 1)
    def __del__(self, destroy= _adder.delete_ptr):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __add__(*args): return apply(_adder.ptr___add__,args)
    def __sub__(*args): return apply(_adder.ptr___sub__,args)
    def __gt__(*args): return apply(_adder.ptr___gt__,args)
    def __ge__(*args): return apply(_adder.ptr___ge__,args)
    def __lt__(*args): return apply(_adder.ptr___lt__,args)
    def __le__(*args): return apply(_adder.ptr___le__,args)
    def __eq__(*args): return apply(_adder.ptr___eq__,args)
    def __ne__(*args): return apply(_adder.ptr___ne__,args)
    def add(*args): return apply(_adder.ptr_add,args)
    def sub(*args): return apply(_adder.ptr_sub,args)
    def to_int(*args): return apply(_adder.ptr_to_int,args)
    def to_pvoid(*args): return apply(_adder.ptr_to_pvoid,args)
    def can_read(*args): return apply(_adder.ptr_can_read,args)
    def can_write(*args): return apply(_adder.ptr_can_write,args)
    def is_read_only(*args): return apply(_adder.ptr_is_read_only,args)
    def set_read_only(*args): return apply(_adder.ptr_set_read_only,args)
    def set_protection(*args): return apply(_adder.ptr_set_protection,args)
    def read_byte(*args): return apply(_adder.ptr_read_byte,args)
    def read_char(*args): return apply(_adder.ptr_read_char,args)
    def read_short(*args): return apply(_adder.ptr_read_short,args)
    def read_int(*args): return apply(_adder.ptr_read_int,args)
    def read_float(*args): return apply(_adder.ptr_read_float,args)
    def read_double(*args): return apply(_adder.ptr_read_double,args)
    def write_byte(*args): return apply(_adder.ptr_write_byte,args)
    def write_char(*args): return apply(_adder.ptr_write_char,args)
    def write_short(*args): return apply(_adder.ptr_write_short,args)
    def write_int(*args): return apply(_adder.ptr_write_int,args)
    def write_float(*args): return apply(_adder.ptr_write_float,args)
    def write_double(*args): return apply(_adder.ptr_write_double,args)
    def read_bytes(*args): return apply(_adder.ptr_read_bytes,args)
    def write_bytes(*args): return apply(_adder.ptr_write_bytes,args)
    def read_strz(*args): return apply(_adder.ptr_read_strz,args)
    def read_unistrz(*args): return apply(_adder.ptr_read_unistrz,args)
    def find_byte(*args): return apply(_adder.ptr_find_byte,args)
    def find_short(*args): return apply(_adder.ptr_find_short,args)
    def __str__(*args): return apply(_adder.ptr___str__,args)
    def __int__(*args): return apply(_adder.ptr___int__,args)
    def __repr__(self):
        return "<C ptr instance at %s>" % (self.this,)

class ptrPtr(ptr):
    def __init__(self,this):
        _swig_setattr(self, ptr, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, ptr, 'thisown', 0)
        _swig_setattr(self, ptr,self.__class__,ptr)
_adder.ptr_swigregister(ptrPtr)

MAX_SPLICE_LENGTH = _adder.MAX_SPLICE_LENGTH
SPLICE_HEAP_MIN = _adder.SPLICE_HEAP_MIN
SPLICE_HEAP_MAX = _adder.SPLICE_HEAP_MAX
CreateConsole = _adder.CreateConsole

DestroyConsole = _adder.DestroyConsole

LoadLibrary = _adder.LoadLibrary

GetProcAddress = _adder.GetProcAddress

mark_thread = _adder.mark_thread

is_marked_thread = _adder.is_marked_thread

is_hosted_interpreter = _adder.is_hosted_interpreter

release_host_process = _adder.release_host_process

wait_for_shutdown = _adder.wait_for_shutdown

class registers32(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, registers32, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, registers32, name)
    __swig_setmethods__["eflags"] = _adder.registers32_eflags_set
    __swig_getmethods__["eflags"] = _adder.registers32_eflags_get
    if _newclass:eflags = property(_adder.registers32_eflags_get,_adder.registers32_eflags_set)
    __swig_setmethods__["edi"] = _adder.registers32_edi_set
    __swig_getmethods__["edi"] = _adder.registers32_edi_get
    if _newclass:edi = property(_adder.registers32_edi_get,_adder.registers32_edi_set)
    __swig_setmethods__["esi"] = _adder.registers32_esi_set
    __swig_getmethods__["esi"] = _adder.registers32_esi_get
    if _newclass:esi = property(_adder.registers32_esi_get,_adder.registers32_esi_set)
    __swig_setmethods__["ebp"] = _adder.registers32_ebp_set
    __swig_getmethods__["ebp"] = _adder.registers32_ebp_get
    if _newclass:ebp = property(_adder.registers32_ebp_get,_adder.registers32_ebp_set)
    __swig_setmethods__["esp"] = _adder.registers32_esp_set
    __swig_getmethods__["esp"] = _adder.registers32_esp_get
    if _newclass:esp = property(_adder.registers32_esp_get,_adder.registers32_esp_set)
    __swig_setmethods__["ebx"] = _adder.registers32_ebx_set
    __swig_getmethods__["ebx"] = _adder.registers32_ebx_get
    if _newclass:ebx = property(_adder.registers32_ebx_get,_adder.registers32_ebx_set)
    __swig_setmethods__["edx"] = _adder.registers32_edx_set
    __swig_getmethods__["edx"] = _adder.registers32_edx_get
    if _newclass:edx = property(_adder.registers32_edx_get,_adder.registers32_edx_set)
    __swig_setmethods__["ecx"] = _adder.registers32_ecx_set
    __swig_getmethods__["ecx"] = _adder.registers32_ecx_get
    if _newclass:ecx = property(_adder.registers32_ecx_get,_adder.registers32_ecx_set)
    __swig_setmethods__["eax"] = _adder.registers32_eax_set
    __swig_getmethods__["eax"] = _adder.registers32_eax_get
    if _newclass:eax = property(_adder.registers32_eax_get,_adder.registers32_eax_set)
    def __init__(self,*args):
        _swig_setattr(self, registers32, 'this', apply(_adder.new_registers32,args))
        _swig_setattr(self, registers32, 'thisown', 1)
    def __del__(self, destroy= _adder.delete_registers32):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C registers32 instance at %s>" % (self.this,)

class registers32Ptr(registers32):
    def __init__(self,this):
        _swig_setattr(self, registers32, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, registers32, 'thisown', 0)
        _swig_setattr(self, registers32,self.__class__,registers32)
_adder.registers32_swigregister(registers32Ptr)

class registers16(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, registers16, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, registers16, name)
    __swig_setmethods__["flags"] = _adder.registers16_flags_set
    __swig_getmethods__["flags"] = _adder.registers16_flags_get
    if _newclass:flags = property(_adder.registers16_flags_get,_adder.registers16_flags_set)
    __swig_setmethods__["flags_pad"] = _adder.registers16_flags_pad_set
    __swig_getmethods__["flags_pad"] = _adder.registers16_flags_pad_get
    if _newclass:flags_pad = property(_adder.registers16_flags_pad_get,_adder.registers16_flags_pad_set)
    __swig_setmethods__["di"] = _adder.registers16_di_set
    __swig_getmethods__["di"] = _adder.registers16_di_get
    if _newclass:di = property(_adder.registers16_di_get,_adder.registers16_di_set)
    __swig_setmethods__["di_pad"] = _adder.registers16_di_pad_set
    __swig_getmethods__["di_pad"] = _adder.registers16_di_pad_get
    if _newclass:di_pad = property(_adder.registers16_di_pad_get,_adder.registers16_di_pad_set)
    __swig_setmethods__["si"] = _adder.registers16_si_set
    __swig_getmethods__["si"] = _adder.registers16_si_get
    if _newclass:si = property(_adder.registers16_si_get,_adder.registers16_si_set)
    __swig_setmethods__["si_pad"] = _adder.registers16_si_pad_set
    __swig_getmethods__["si_pad"] = _adder.registers16_si_pad_get
    if _newclass:si_pad = property(_adder.registers16_si_pad_get,_adder.registers16_si_pad_set)
    __swig_setmethods__["bp"] = _adder.registers16_bp_set
    __swig_getmethods__["bp"] = _adder.registers16_bp_get
    if _newclass:bp = property(_adder.registers16_bp_get,_adder.registers16_bp_set)
    __swig_setmethods__["bp_pad"] = _adder.registers16_bp_pad_set
    __swig_getmethods__["bp_pad"] = _adder.registers16_bp_pad_get
    if _newclass:bp_pad = property(_adder.registers16_bp_pad_get,_adder.registers16_bp_pad_set)
    __swig_setmethods__["sp"] = _adder.registers16_sp_set
    __swig_getmethods__["sp"] = _adder.registers16_sp_get
    if _newclass:sp = property(_adder.registers16_sp_get,_adder.registers16_sp_set)
    __swig_setmethods__["sp_pad"] = _adder.registers16_sp_pad_set
    __swig_getmethods__["sp_pad"] = _adder.registers16_sp_pad_get
    if _newclass:sp_pad = property(_adder.registers16_sp_pad_get,_adder.registers16_sp_pad_set)
    __swig_setmethods__["bx"] = _adder.registers16_bx_set
    __swig_getmethods__["bx"] = _adder.registers16_bx_get
    if _newclass:bx = property(_adder.registers16_bx_get,_adder.registers16_bx_set)
    __swig_setmethods__["bx_pad"] = _adder.registers16_bx_pad_set
    __swig_getmethods__["bx_pad"] = _adder.registers16_bx_pad_get
    if _newclass:bx_pad = property(_adder.registers16_bx_pad_get,_adder.registers16_bx_pad_set)
    __swig_setmethods__["dx"] = _adder.registers16_dx_set
    __swig_getmethods__["dx"] = _adder.registers16_dx_get
    if _newclass:dx = property(_adder.registers16_dx_get,_adder.registers16_dx_set)
    __swig_setmethods__["dx_pad"] = _adder.registers16_dx_pad_set
    __swig_getmethods__["dx_pad"] = _adder.registers16_dx_pad_get
    if _newclass:dx_pad = property(_adder.registers16_dx_pad_get,_adder.registers16_dx_pad_set)
    __swig_setmethods__["cx"] = _adder.registers16_cx_set
    __swig_getmethods__["cx"] = _adder.registers16_cx_get
    if _newclass:cx = property(_adder.registers16_cx_get,_adder.registers16_cx_set)
    __swig_setmethods__["cx_pad"] = _adder.registers16_cx_pad_set
    __swig_getmethods__["cx_pad"] = _adder.registers16_cx_pad_get
    if _newclass:cx_pad = property(_adder.registers16_cx_pad_get,_adder.registers16_cx_pad_set)
    __swig_setmethods__["ax"] = _adder.registers16_ax_set
    __swig_getmethods__["ax"] = _adder.registers16_ax_get
    if _newclass:ax = property(_adder.registers16_ax_get,_adder.registers16_ax_set)
    __swig_setmethods__["ax_pad"] = _adder.registers16_ax_pad_set
    __swig_getmethods__["ax_pad"] = _adder.registers16_ax_pad_get
    if _newclass:ax_pad = property(_adder.registers16_ax_pad_get,_adder.registers16_ax_pad_set)
    def __init__(self,*args):
        _swig_setattr(self, registers16, 'this', apply(_adder.new_registers16,args))
        _swig_setattr(self, registers16, 'thisown', 1)
    def __del__(self, destroy= _adder.delete_registers16):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C registers16 instance at %s>" % (self.this,)

class registers16Ptr(registers16):
    def __init__(self,this):
        _swig_setattr(self, registers16, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, registers16, 'thisown', 0)
        _swig_setattr(self, registers16,self.__class__,registers16)
_adder.registers16_swigregister(registers16Ptr)

class registers8(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, registers8, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, registers8, name)
    __swig_setmethods__["_flags"] = _adder.registers8__flags_set
    __swig_getmethods__["_flags"] = _adder.registers8__flags_get
    if _newclass:_flags = property(_adder.registers8__flags_get,_adder.registers8__flags_set)
    __swig_setmethods__["_flags_pad"] = _adder.registers8__flags_pad_set
    __swig_getmethods__["_flags_pad"] = _adder.registers8__flags_pad_get
    if _newclass:_flags_pad = property(_adder.registers8__flags_pad_get,_adder.registers8__flags_pad_set)
    __swig_setmethods__["_di"] = _adder.registers8__di_set
    __swig_getmethods__["_di"] = _adder.registers8__di_get
    if _newclass:_di = property(_adder.registers8__di_get,_adder.registers8__di_set)
    __swig_setmethods__["_di_pad"] = _adder.registers8__di_pad_set
    __swig_getmethods__["_di_pad"] = _adder.registers8__di_pad_get
    if _newclass:_di_pad = property(_adder.registers8__di_pad_get,_adder.registers8__di_pad_set)
    __swig_setmethods__["_si"] = _adder.registers8__si_set
    __swig_getmethods__["_si"] = _adder.registers8__si_get
    if _newclass:_si = property(_adder.registers8__si_get,_adder.registers8__si_set)
    __swig_setmethods__["_si_pad"] = _adder.registers8__si_pad_set
    __swig_getmethods__["_si_pad"] = _adder.registers8__si_pad_get
    if _newclass:_si_pad = property(_adder.registers8__si_pad_get,_adder.registers8__si_pad_set)
    __swig_setmethods__["_bp"] = _adder.registers8__bp_set
    __swig_getmethods__["_bp"] = _adder.registers8__bp_get
    if _newclass:_bp = property(_adder.registers8__bp_get,_adder.registers8__bp_set)
    __swig_setmethods__["_bp_pad"] = _adder.registers8__bp_pad_set
    __swig_getmethods__["_bp_pad"] = _adder.registers8__bp_pad_get
    if _newclass:_bp_pad = property(_adder.registers8__bp_pad_get,_adder.registers8__bp_pad_set)
    __swig_setmethods__["_sp"] = _adder.registers8__sp_set
    __swig_getmethods__["_sp"] = _adder.registers8__sp_get
    if _newclass:_sp = property(_adder.registers8__sp_get,_adder.registers8__sp_set)
    __swig_setmethods__["_sp_pad"] = _adder.registers8__sp_pad_set
    __swig_getmethods__["_sp_pad"] = _adder.registers8__sp_pad_get
    if _newclass:_sp_pad = property(_adder.registers8__sp_pad_get,_adder.registers8__sp_pad_set)
    __swig_setmethods__["bl"] = _adder.registers8_bl_set
    __swig_getmethods__["bl"] = _adder.registers8_bl_get
    if _newclass:bl = property(_adder.registers8_bl_get,_adder.registers8_bl_set)
    __swig_setmethods__["bh"] = _adder.registers8_bh_set
    __swig_getmethods__["bh"] = _adder.registers8_bh_get
    if _newclass:bh = property(_adder.registers8_bh_get,_adder.registers8_bh_set)
    __swig_setmethods__["bx_pad"] = _adder.registers8_bx_pad_set
    __swig_getmethods__["bx_pad"] = _adder.registers8_bx_pad_get
    if _newclass:bx_pad = property(_adder.registers8_bx_pad_get,_adder.registers8_bx_pad_set)
    __swig_setmethods__["dl"] = _adder.registers8_dl_set
    __swig_getmethods__["dl"] = _adder.registers8_dl_get
    if _newclass:dl = property(_adder.registers8_dl_get,_adder.registers8_dl_set)
    __swig_setmethods__["dh"] = _adder.registers8_dh_set
    __swig_getmethods__["dh"] = _adder.registers8_dh_get
    if _newclass:dh = property(_adder.registers8_dh_get,_adder.registers8_dh_set)
    __swig_setmethods__["dx_pad"] = _adder.registers8_dx_pad_set
    __swig_getmethods__["dx_pad"] = _adder.registers8_dx_pad_get
    if _newclass:dx_pad = property(_adder.registers8_dx_pad_get,_adder.registers8_dx_pad_set)
    __swig_setmethods__["cl"] = _adder.registers8_cl_set
    __swig_getmethods__["cl"] = _adder.registers8_cl_get
    if _newclass:cl = property(_adder.registers8_cl_get,_adder.registers8_cl_set)
    __swig_setmethods__["ch"] = _adder.registers8_ch_set
    __swig_getmethods__["ch"] = _adder.registers8_ch_get
    if _newclass:ch = property(_adder.registers8_ch_get,_adder.registers8_ch_set)
    __swig_setmethods__["cx_pad"] = _adder.registers8_cx_pad_set
    __swig_getmethods__["cx_pad"] = _adder.registers8_cx_pad_get
    if _newclass:cx_pad = property(_adder.registers8_cx_pad_get,_adder.registers8_cx_pad_set)
    __swig_setmethods__["al"] = _adder.registers8_al_set
    __swig_getmethods__["al"] = _adder.registers8_al_get
    if _newclass:al = property(_adder.registers8_al_get,_adder.registers8_al_set)
    __swig_setmethods__["ah"] = _adder.registers8_ah_set
    __swig_getmethods__["ah"] = _adder.registers8_ah_get
    if _newclass:ah = property(_adder.registers8_ah_get,_adder.registers8_ah_set)
    __swig_setmethods__["ax_pad"] = _adder.registers8_ax_pad_set
    __swig_getmethods__["ax_pad"] = _adder.registers8_ax_pad_get
    if _newclass:ax_pad = property(_adder.registers8_ax_pad_get,_adder.registers8_ax_pad_set)
    def __init__(self,*args):
        _swig_setattr(self, registers8, 'this', apply(_adder.new_registers8,args))
        _swig_setattr(self, registers8, 'thisown', 1)
    def __del__(self, destroy= _adder.delete_registers8):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C registers8 instance at %s>" % (self.this,)

class registers8Ptr(registers8):
    def __init__(self,this):
        _swig_setattr(self, registers8, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, registers8, 'thisown', 0)
        _swig_setattr(self, registers8,self.__class__,registers8)
_adder.registers8_swigregister(registers8Ptr)

class registers(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, registers, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, registers, name)
    __swig_setmethods__["r32"] = _adder.registers_r32_set
    __swig_getmethods__["r32"] = _adder.registers_r32_get
    if _newclass:r32 = property(_adder.registers_r32_get,_adder.registers_r32_set)
    __swig_setmethods__["r16"] = _adder.registers_r16_set
    __swig_getmethods__["r16"] = _adder.registers_r16_get
    if _newclass:r16 = property(_adder.registers_r16_get,_adder.registers_r16_set)
    __swig_setmethods__["r8"] = _adder.registers_r8_set
    __swig_getmethods__["r8"] = _adder.registers_r8_get
    if _newclass:r8 = property(_adder.registers_r8_get,_adder.registers_r8_set)
    __swig_setmethods__["eflags"] = _adder.registers_eflags_set
    __swig_getmethods__["eflags"] = _adder.registers_eflags_get
    if _newclass:eflags = property(_adder.registers_eflags_get,_adder.registers_eflags_set)
    __swig_setmethods__["edi"] = _adder.registers_edi_set
    __swig_getmethods__["edi"] = _adder.registers_edi_get
    if _newclass:edi = property(_adder.registers_edi_get,_adder.registers_edi_set)
    __swig_setmethods__["esi"] = _adder.registers_esi_set
    __swig_getmethods__["esi"] = _adder.registers_esi_get
    if _newclass:esi = property(_adder.registers_esi_get,_adder.registers_esi_set)
    __swig_setmethods__["ebp"] = _adder.registers_ebp_set
    __swig_getmethods__["ebp"] = _adder.registers_ebp_get
    if _newclass:ebp = property(_adder.registers_ebp_get,_adder.registers_ebp_set)
    __swig_setmethods__["esp"] = _adder.registers_esp_set
    __swig_getmethods__["esp"] = _adder.registers_esp_get
    if _newclass:esp = property(_adder.registers_esp_get,_adder.registers_esp_set)
    __swig_setmethods__["ebx"] = _adder.registers_ebx_set
    __swig_getmethods__["ebx"] = _adder.registers_ebx_get
    if _newclass:ebx = property(_adder.registers_ebx_get,_adder.registers_ebx_set)
    __swig_setmethods__["edx"] = _adder.registers_edx_set
    __swig_getmethods__["edx"] = _adder.registers_edx_get
    if _newclass:edx = property(_adder.registers_edx_get,_adder.registers_edx_set)
    __swig_setmethods__["ecx"] = _adder.registers_ecx_set
    __swig_getmethods__["ecx"] = _adder.registers_ecx_get
    if _newclass:ecx = property(_adder.registers_ecx_get,_adder.registers_ecx_set)
    __swig_setmethods__["eax"] = _adder.registers_eax_set
    __swig_getmethods__["eax"] = _adder.registers_eax_get
    if _newclass:eax = property(_adder.registers_eax_get,_adder.registers_eax_set)
    __swig_setmethods__["flags"] = _adder.registers_flags_set
    __swig_getmethods__["flags"] = _adder.registers_flags_get
    if _newclass:flags = property(_adder.registers_flags_get,_adder.registers_flags_set)
    __swig_setmethods__["di"] = _adder.registers_di_set
    __swig_getmethods__["di"] = _adder.registers_di_get
    if _newclass:di = property(_adder.registers_di_get,_adder.registers_di_set)
    __swig_setmethods__["si"] = _adder.registers_si_set
    __swig_getmethods__["si"] = _adder.registers_si_get
    if _newclass:si = property(_adder.registers_si_get,_adder.registers_si_set)
    __swig_setmethods__["bp"] = _adder.registers_bp_set
    __swig_getmethods__["bp"] = _adder.registers_bp_get
    if _newclass:bp = property(_adder.registers_bp_get,_adder.registers_bp_set)
    __swig_setmethods__["sp"] = _adder.registers_sp_set
    __swig_getmethods__["sp"] = _adder.registers_sp_get
    if _newclass:sp = property(_adder.registers_sp_get,_adder.registers_sp_set)
    __swig_setmethods__["bx"] = _adder.registers_bx_set
    __swig_getmethods__["bx"] = _adder.registers_bx_get
    if _newclass:bx = property(_adder.registers_bx_get,_adder.registers_bx_set)
    __swig_setmethods__["dx"] = _adder.registers_dx_set
    __swig_getmethods__["dx"] = _adder.registers_dx_get
    if _newclass:dx = property(_adder.registers_dx_get,_adder.registers_dx_set)
    __swig_setmethods__["cx"] = _adder.registers_cx_set
    __swig_getmethods__["cx"] = _adder.registers_cx_get
    if _newclass:cx = property(_adder.registers_cx_get,_adder.registers_cx_set)
    __swig_setmethods__["ax"] = _adder.registers_ax_set
    __swig_getmethods__["ax"] = _adder.registers_ax_get
    if _newclass:ax = property(_adder.registers_ax_get,_adder.registers_ax_set)
    __swig_setmethods__["bl"] = _adder.registers_bl_set
    __swig_getmethods__["bl"] = _adder.registers_bl_get
    if _newclass:bl = property(_adder.registers_bl_get,_adder.registers_bl_set)
    __swig_setmethods__["bh"] = _adder.registers_bh_set
    __swig_getmethods__["bh"] = _adder.registers_bh_get
    if _newclass:bh = property(_adder.registers_bh_get,_adder.registers_bh_set)
    __swig_setmethods__["dl"] = _adder.registers_dl_set
    __swig_getmethods__["dl"] = _adder.registers_dl_get
    if _newclass:dl = property(_adder.registers_dl_get,_adder.registers_dl_set)
    __swig_setmethods__["dh"] = _adder.registers_dh_set
    __swig_getmethods__["dh"] = _adder.registers_dh_get
    if _newclass:dh = property(_adder.registers_dh_get,_adder.registers_dh_set)
    __swig_setmethods__["cl"] = _adder.registers_cl_set
    __swig_getmethods__["cl"] = _adder.registers_cl_get
    if _newclass:cl = property(_adder.registers_cl_get,_adder.registers_cl_set)
    __swig_setmethods__["ch"] = _adder.registers_ch_set
    __swig_getmethods__["ch"] = _adder.registers_ch_get
    if _newclass:ch = property(_adder.registers_ch_get,_adder.registers_ch_set)
    __swig_setmethods__["al"] = _adder.registers_al_set
    __swig_getmethods__["al"] = _adder.registers_al_get
    if _newclass:al = property(_adder.registers_al_get,_adder.registers_al_set)
    __swig_setmethods__["ah"] = _adder.registers_ah_set
    __swig_getmethods__["ah"] = _adder.registers_ah_get
    if _newclass:ah = property(_adder.registers_ah_get,_adder.registers_ah_set)
    def __str__(*args): return apply(_adder.registers___str__,args)
    def __init__(self,*args):
        _swig_setattr(self, registers, 'this', apply(_adder.new_registers,args))
        _swig_setattr(self, registers, 'thisown', 1)
    def __del__(self, destroy= _adder.delete_registers):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C registers instance at %s>" % (self.this,)

class registersPtr(registers):
    def __init__(self,this):
        _swig_setattr(self, registers, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, registers, 'thisown', 0)
        _swig_setattr(self, registers,self.__class__,registers)
_adder.registers_swigregister(registersPtr)

class splice_heap(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, splice_heap, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, splice_heap, name)
    def __init__(self,*args):
        _swig_setattr(self, splice_heap, 'this', apply(_adder.new_splice_heap,args))
        _swig_setattr(self, splice_heap, 'thisown', 1)
    def __del__(self, destroy= _adder.delete_splice_heap):
        try:
            if self.thisown: destroy(self)
        except: pass
    def alloc(*args): return apply(_adder.splice_heap_alloc,args)
    def free(*args): return apply(_adder.splice_heap_free,args)
    def __repr__(self):
        return "<C splice_heap instance at %s>" % (self.this,)

class splice_heapPtr(splice_heap):
    def __init__(self,this):
        _swig_setattr(self, splice_heap, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, splice_heap, 'thisown', 0)
        _swig_setattr(self, splice_heap,self.__class__,splice_heap)
_adder.splice_heap_swigregister(splice_heapPtr)

class raw_splice(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, raw_splice, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, raw_splice, name)
    def __init__(self,*args):
        _swig_setattr(self, raw_splice, 'this', apply(_adder.new_raw_splice,args))
        _swig_setattr(self, raw_splice, 'thisown', 1)
    def __del__(self, destroy= _adder.delete_raw_splice):
        try:
            if self.thisown: destroy(self)
        except: pass
    def install(*args): return apply(_adder.raw_splice_install,args)
    def uninstall(*args): return apply(_adder.raw_splice_uninstall,args)
    def is_installed(*args): return apply(_adder.raw_splice_is_installed,args)
    def set_address(*args): return apply(_adder.raw_splice_set_address,args)
    def get_address(*args): return apply(_adder.raw_splice_get_address,args)
    def get_pre_func(*args): return apply(_adder.raw_splice_get_pre_func,args)
    def set_pre_func(*args): return apply(_adder.raw_splice_set_pre_func,args)
    def get_post_func(*args): return apply(_adder.raw_splice_get_post_func,args)
    def set_post_func(*args): return apply(_adder.raw_splice_set_post_func,args)
    def __repr__(self):
        return "<C raw_splice instance at %s>" % (self.this,)

class raw_splicePtr(raw_splice):
    def __init__(self,this):
        _swig_setattr(self, raw_splice, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, raw_splice, 'thisown', 0)
        _swig_setattr(self, raw_splice,self.__class__,raw_splice)
_adder.raw_splice_swigregister(raw_splicePtr)

get_pre_trace = _adder.get_pre_trace

get_post_trace = _adder.get_post_trace

class splice_callback(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, splice_callback, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, splice_callback, name)
    def __init__(self,*args):
        if self.__class__ == splice_callback:
            args = (None,) + args
        else:
            args = (self,) + args
        _swig_setattr(self, splice_callback, 'this', apply(_adder.new_splice_callback,args))
        _swig_setattr(self, splice_callback, 'thisown', 1)
    def __del__(self, destroy= _adder.delete_splice_callback):
        try:
            if self.thisown: destroy(self)
        except: pass
    def run(*args): return apply(_adder.splice_callback_run,args)
    def __disown__(self):
        self.thisown = 0
        _adder.disown_splice_callback(self)
        return weakref_proxy(self)
    def __repr__(self):
        return "<C splice_callback instance at %s>" % (self.this,)

class splice_callbackPtr(splice_callback):
    def __init__(self,this):
        _swig_setattr(self, splice_callback, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, splice_callback, 'thisown', 0)
        _swig_setattr(self, splice_callback,self.__class__,splice_callback)
_adder.splice_callback_swigregister(splice_callbackPtr)

class splice(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, splice, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, splice, name)
    def __init__(self,*args):
        _swig_setattr(self, splice, 'this', apply(_adder.new_splice,args))
        _swig_setattr(self, splice, 'thisown', 1)
    def __del__(self, destroy= _adder.delete_splice):
        try:
            if self.thisown: destroy(self)
        except: pass
    def install(*args): return apply(_adder.splice_install,args)
    def uninstall(*args): return apply(_adder.splice_uninstall,args)
    def is_installed(*args): return apply(_adder.splice_is_installed,args)
    def set_address(*args): return apply(_adder.splice_set_address,args)
    def get_address(*args): return apply(_adder.splice_get_address,args)
    def set_pre_callback(*args): return apply(_adder.splice_set_pre_callback,args)
    def get_pre_callback(*args): return apply(_adder.splice_get_pre_callback,args)
    def del_pre_callback(*args): return apply(_adder.splice_del_pre_callback,args)
    def set_post_callback(*args): return apply(_adder.splice_set_post_callback,args)
    def get_post_callback(*args): return apply(_adder.splice_get_post_callback,args)
    def del_post_callback(*args): return apply(_adder.splice_del_post_callback,args)
    def dummy_call_pre(*args): return apply(_adder.splice_dummy_call_pre,args)
    def dummy_call_post(*args): return apply(_adder.splice_dummy_call_post,args)
    def __repr__(self):
        return "<C splice instance at %s>" % (self.this,)

class splicePtr(splice):
    def __init__(self,this):
        _swig_setattr(self, splice, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, splice, 'thisown', 0)
        _swig_setattr(self, splice,self.__class__,splice)
_adder.splice_swigregister(splicePtr)

x86_get_instruction = _adder.x86_get_instruction

x86_put_instruction = _adder.x86_put_instruction

class x86_instruction(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, x86_instruction, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, x86_instruction, name)
    def __init__(self,*args):
        _swig_setattr(self, x86_instruction, 'this', apply(_adder.new_x86_instruction,args))
        _swig_setattr(self, x86_instruction, 'thisown', 1)
    def disassemble(*args): return apply(_adder.x86_instruction_disassemble,args)
    def to_bytes(*args): return apply(_adder.x86_instruction_to_bytes,args)
    def write(*args): return apply(_adder.x86_instruction_write,args)
    def to_str(*args): return apply(_adder.x86_instruction_to_str,args)
    def is_valid(*args): return apply(_adder.x86_instruction_is_valid,args)
    def get_len(*args): return apply(_adder.x86_instruction_get_len,args)
    def get_flags(*args): return apply(_adder.x86_instruction_get_flags,args)
    def set_flags(*args): return apply(_adder.x86_instruction_set_flags,args)
    def get_addrsize(*args): return apply(_adder.x86_instruction_get_addrsize,args)
    def set_addrsize(*args): return apply(_adder.x86_instruction_set_addrsize,args)
    def get_datasize(*args): return apply(_adder.x86_instruction_get_datasize,args)
    def set_datasize(*args): return apply(_adder.x86_instruction_set_datasize,args)
    def get_rep(*args): return apply(_adder.x86_instruction_get_rep,args)
    def set_rep(*args): return apply(_adder.x86_instruction_set_rep,args)
    def get_seg(*args): return apply(_adder.x86_instruction_get_seg,args)
    def set_seg(*args): return apply(_adder.x86_instruction_set_seg,args)
    def get_opcode(*args): return apply(_adder.x86_instruction_get_opcode,args)
    def set_opcode(*args): return apply(_adder.x86_instruction_set_opcode,args)
    def get_opcode2(*args): return apply(_adder.x86_instruction_get_opcode2,args)
    def set_opcode2(*args): return apply(_adder.x86_instruction_set_opcode2,args)
    def get_modrm(*args): return apply(_adder.x86_instruction_get_modrm,args)
    def set_modrm(*args): return apply(_adder.x86_instruction_set_modrm,args)
    def get_sib(*args): return apply(_adder.x86_instruction_get_sib,args)
    def set_sib(*args): return apply(_adder.x86_instruction_set_sib,args)
    def get_addr_u8(*args): return apply(_adder.x86_instruction_get_addr_u8,args)
    def set_addr_u8(*args): return apply(_adder.x86_instruction_set_addr_u8,args)
    def get_addr_s8(*args): return apply(_adder.x86_instruction_get_addr_s8,args)
    def set_addr_s8(*args): return apply(_adder.x86_instruction_set_addr_s8,args)
    def get_addr_u16(*args): return apply(_adder.x86_instruction_get_addr_u16,args)
    def set_addr_u16(*args): return apply(_adder.x86_instruction_set_addr_u16,args)
    def get_addr_s16(*args): return apply(_adder.x86_instruction_get_addr_s16,args)
    def set_addr_s16(*args): return apply(_adder.x86_instruction_set_addr_s16,args)
    def get_addr_u32(*args): return apply(_adder.x86_instruction_get_addr_u32,args)
    def set_addr_u32(*args): return apply(_adder.x86_instruction_set_addr_u32,args)
    def get_addr_s32(*args): return apply(_adder.x86_instruction_get_addr_s32,args)
    def set_addr_s32(*args): return apply(_adder.x86_instruction_set_addr_s32,args)
    def get_data_u8(*args): return apply(_adder.x86_instruction_get_data_u8,args)
    def set_data_u8(*args): return apply(_adder.x86_instruction_set_data_u8,args)
    def get_data_s8(*args): return apply(_adder.x86_instruction_get_data_s8,args)
    def set_data_s8(*args): return apply(_adder.x86_instruction_set_data_s8,args)
    def get_data_u16(*args): return apply(_adder.x86_instruction_get_data_u16,args)
    def set_data_u16(*args): return apply(_adder.x86_instruction_set_data_u16,args)
    def get_data_s16(*args): return apply(_adder.x86_instruction_get_data_s16,args)
    def set_data_s16(*args): return apply(_adder.x86_instruction_set_data_s16,args)
    def get_data_u32(*args): return apply(_adder.x86_instruction_get_data_u32,args)
    def set_data_u32(*args): return apply(_adder.x86_instruction_set_data_u32,args)
    def get_data_s32(*args): return apply(_adder.x86_instruction_get_data_s32,args)
    def set_data_s32(*args): return apply(_adder.x86_instruction_set_data_s32,args)
    def get_mnemonic(*args): return apply(_adder.x86_instruction_get_mnemonic,args)
    def get_mnemonic_flags(*args): return apply(_adder.x86_instruction_get_mnemonic_flags,args)
    def get_dest(*args): return apply(_adder.x86_instruction_get_dest,args)
    def get_dest_flags(*args): return apply(_adder.x86_instruction_get_dest_flags,args)
    def get_src(*args): return apply(_adder.x86_instruction_get_src,args)
    def get_src_flags(*args): return apply(_adder.x86_instruction_get_src_flags,args)
    def get_aux(*args): return apply(_adder.x86_instruction_get_aux,args)
    def get_aux_flags(*args): return apply(_adder.x86_instruction_get_aux_flags,args)
    def get_size(*args): return apply(_adder.x86_instruction_get_size,args)
    __swig_getmethods__["C_ERROR"] = _adder.x86_instruction_C_ERROR_get
    if _newclass:C_ERROR = property(_adder.x86_instruction_C_ERROR_get)
    __swig_getmethods__["C_ADDR1"] = _adder.x86_instruction_C_ADDR1_get
    if _newclass:C_ADDR1 = property(_adder.x86_instruction_C_ADDR1_get)
    __swig_getmethods__["C_ADDR2"] = _adder.x86_instruction_C_ADDR2_get
    if _newclass:C_ADDR2 = property(_adder.x86_instruction_C_ADDR2_get)
    __swig_getmethods__["C_ADDR4"] = _adder.x86_instruction_C_ADDR4_get
    if _newclass:C_ADDR4 = property(_adder.x86_instruction_C_ADDR4_get)
    __swig_getmethods__["C_LOCK"] = _adder.x86_instruction_C_LOCK_get
    if _newclass:C_LOCK = property(_adder.x86_instruction_C_LOCK_get)
    __swig_getmethods__["C_67"] = _adder.x86_instruction_C_67_get
    if _newclass:C_67 = property(_adder.x86_instruction_C_67_get)
    __swig_getmethods__["C_66"] = _adder.x86_instruction_C_66_get
    if _newclass:C_66 = property(_adder.x86_instruction_C_66_get)
    __swig_getmethods__["C_REP"] = _adder.x86_instruction_C_REP_get
    if _newclass:C_REP = property(_adder.x86_instruction_C_REP_get)
    __swig_getmethods__["C_SEG"] = _adder.x86_instruction_C_SEG_get
    if _newclass:C_SEG = property(_adder.x86_instruction_C_SEG_get)
    __swig_getmethods__["C_ANYPREFIX"] = _adder.x86_instruction_C_ANYPREFIX_get
    if _newclass:C_ANYPREFIX = property(_adder.x86_instruction_C_ANYPREFIX_get)
    __swig_getmethods__["C_DATA1"] = _adder.x86_instruction_C_DATA1_get
    if _newclass:C_DATA1 = property(_adder.x86_instruction_C_DATA1_get)
    __swig_getmethods__["C_DATA2"] = _adder.x86_instruction_C_DATA2_get
    if _newclass:C_DATA2 = property(_adder.x86_instruction_C_DATA2_get)
    __swig_getmethods__["C_DATA4"] = _adder.x86_instruction_C_DATA4_get
    if _newclass:C_DATA4 = property(_adder.x86_instruction_C_DATA4_get)
    __swig_getmethods__["C_SIB"] = _adder.x86_instruction_C_SIB_get
    if _newclass:C_SIB = property(_adder.x86_instruction_C_SIB_get)
    __swig_getmethods__["C_ADDR67"] = _adder.x86_instruction_C_ADDR67_get
    if _newclass:C_ADDR67 = property(_adder.x86_instruction_C_ADDR67_get)
    __swig_getmethods__["C_DATA66"] = _adder.x86_instruction_C_DATA66_get
    if _newclass:C_DATA66 = property(_adder.x86_instruction_C_DATA66_get)
    __swig_getmethods__["C_MODRM"] = _adder.x86_instruction_C_MODRM_get
    if _newclass:C_MODRM = property(_adder.x86_instruction_C_MODRM_get)
    __swig_getmethods__["C_BAD"] = _adder.x86_instruction_C_BAD_get
    if _newclass:C_BAD = property(_adder.x86_instruction_C_BAD_get)
    __swig_getmethods__["C_OPCODE2"] = _adder.x86_instruction_C_OPCODE2_get
    if _newclass:C_OPCODE2 = property(_adder.x86_instruction_C_OPCODE2_get)
    __swig_getmethods__["C_REL"] = _adder.x86_instruction_C_REL_get
    if _newclass:C_REL = property(_adder.x86_instruction_C_REL_get)
    __swig_getmethods__["C_STOP"] = _adder.x86_instruction_C_STOP_get
    if _newclass:C_STOP = property(_adder.x86_instruction_C_STOP_get)
    __swig_getmethods__["C_OP_R"] = _adder.x86_instruction_C_OP_R_get
    if _newclass:C_OP_R = property(_adder.x86_instruction_C_OP_R_get)
    __swig_getmethods__["C_OP_W"] = _adder.x86_instruction_C_OP_W_get
    if _newclass:C_OP_W = property(_adder.x86_instruction_C_OP_W_get)
    __swig_getmethods__["C_OP_X"] = _adder.x86_instruction_C_OP_X_get
    if _newclass:C_OP_X = property(_adder.x86_instruction_C_OP_X_get)
    __swig_getmethods__["C_OP_UNK"] = _adder.x86_instruction_C_OP_UNK_get
    if _newclass:C_OP_UNK = property(_adder.x86_instruction_C_OP_UNK_get)
    __swig_getmethods__["C_OP_REG"] = _adder.x86_instruction_C_OP_REG_get
    if _newclass:C_OP_REG = property(_adder.x86_instruction_C_OP_REG_get)
    __swig_getmethods__["C_OP_IMM"] = _adder.x86_instruction_C_OP_IMM_get
    if _newclass:C_OP_IMM = property(_adder.x86_instruction_C_OP_IMM_get)
    __swig_getmethods__["C_OP_REL"] = _adder.x86_instruction_C_OP_REL_get
    if _newclass:C_OP_REL = property(_adder.x86_instruction_C_OP_REL_get)
    __swig_getmethods__["C_OP_ADDR"] = _adder.x86_instruction_C_OP_ADDR_get
    if _newclass:C_OP_ADDR = property(_adder.x86_instruction_C_OP_ADDR_get)
    __swig_getmethods__["C_OP_EXPR"] = _adder.x86_instruction_C_OP_EXPR_get
    if _newclass:C_OP_EXPR = property(_adder.x86_instruction_C_OP_EXPR_get)
    __swig_getmethods__["C_OP_PTR"] = _adder.x86_instruction_C_OP_PTR_get
    if _newclass:C_OP_PTR = property(_adder.x86_instruction_C_OP_PTR_get)
    __swig_getmethods__["C_OP_OFF"] = _adder.x86_instruction_C_OP_OFF_get
    if _newclass:C_OP_OFF = property(_adder.x86_instruction_C_OP_OFF_get)
    __swig_getmethods__["C_OP_SIGNED"] = _adder.x86_instruction_C_OP_SIGNED_get
    if _newclass:C_OP_SIGNED = property(_adder.x86_instruction_C_OP_SIGNED_get)
    __swig_getmethods__["C_OP_STRING"] = _adder.x86_instruction_C_OP_STRING_get
    if _newclass:C_OP_STRING = property(_adder.x86_instruction_C_OP_STRING_get)
    __swig_getmethods__["C_OP_CONST"] = _adder.x86_instruction_C_OP_CONST_get
    if _newclass:C_OP_CONST = property(_adder.x86_instruction_C_OP_CONST_get)
    __swig_getmethods__["C_OP_EXTRASEG"] = _adder.x86_instruction_C_OP_EXTRASEG_get
    if _newclass:C_OP_EXTRASEG = property(_adder.x86_instruction_C_OP_EXTRASEG_get)
    __swig_getmethods__["C_OP_CODESEG"] = _adder.x86_instruction_C_OP_CODESEG_get
    if _newclass:C_OP_CODESEG = property(_adder.x86_instruction_C_OP_CODESEG_get)
    __swig_getmethods__["C_OP_STACKSEG"] = _adder.x86_instruction_C_OP_STACKSEG_get
    if _newclass:C_OP_STACKSEG = property(_adder.x86_instruction_C_OP_STACKSEG_get)
    __swig_getmethods__["C_OP_DATASEG"] = _adder.x86_instruction_C_OP_DATASEG_get
    if _newclass:C_OP_DATASEG = property(_adder.x86_instruction_C_OP_DATASEG_get)
    __swig_getmethods__["C_OP_DATA1SEG"] = _adder.x86_instruction_C_OP_DATA1SEG_get
    if _newclass:C_OP_DATA1SEG = property(_adder.x86_instruction_C_OP_DATA1SEG_get)
    __swig_getmethods__["C_OP_DATA2SEG"] = _adder.x86_instruction_C_OP_DATA2SEG_get
    if _newclass:C_OP_DATA2SEG = property(_adder.x86_instruction_C_OP_DATA2SEG_get)
    __swig_getmethods__["C_OP_BYTE"] = _adder.x86_instruction_C_OP_BYTE_get
    if _newclass:C_OP_BYTE = property(_adder.x86_instruction_C_OP_BYTE_get)
    __swig_getmethods__["C_OP_HWORD"] = _adder.x86_instruction_C_OP_HWORD_get
    if _newclass:C_OP_HWORD = property(_adder.x86_instruction_C_OP_HWORD_get)
    __swig_getmethods__["C_OP_WORD"] = _adder.x86_instruction_C_OP_WORD_get
    if _newclass:C_OP_WORD = property(_adder.x86_instruction_C_OP_WORD_get)
    __swig_getmethods__["C_OP_DWORD"] = _adder.x86_instruction_C_OP_DWORD_get
    if _newclass:C_OP_DWORD = property(_adder.x86_instruction_C_OP_DWORD_get)
    __swig_getmethods__["C_OP_QWORD"] = _adder.x86_instruction_C_OP_QWORD_get
    if _newclass:C_OP_QWORD = property(_adder.x86_instruction_C_OP_QWORD_get)
    __swig_getmethods__["C_OP_SREAL"] = _adder.x86_instruction_C_OP_SREAL_get
    if _newclass:C_OP_SREAL = property(_adder.x86_instruction_C_OP_SREAL_get)
    __swig_getmethods__["C_OP_DREAL"] = _adder.x86_instruction_C_OP_DREAL_get
    if _newclass:C_OP_DREAL = property(_adder.x86_instruction_C_OP_DREAL_get)
    __swig_getmethods__["C_OP_XREAL"] = _adder.x86_instruction_C_OP_XREAL_get
    if _newclass:C_OP_XREAL = property(_adder.x86_instruction_C_OP_XREAL_get)
    __swig_getmethods__["C_OP_BCD"] = _adder.x86_instruction_C_OP_BCD_get
    if _newclass:C_OP_BCD = property(_adder.x86_instruction_C_OP_BCD_get)
    __swig_getmethods__["C_OP_SIMD"] = _adder.x86_instruction_C_OP_SIMD_get
    if _newclass:C_OP_SIMD = property(_adder.x86_instruction_C_OP_SIMD_get)
    __swig_getmethods__["C_OP_FPENV"] = _adder.x86_instruction_C_OP_FPENV_get
    if _newclass:C_OP_FPENV = property(_adder.x86_instruction_C_OP_FPENV_get)
    __swig_getmethods__["C_OP_PERM_MASK"] = _adder.x86_instruction_C_OP_PERM_MASK_get
    if _newclass:C_OP_PERM_MASK = property(_adder.x86_instruction_C_OP_PERM_MASK_get)
    __swig_getmethods__["C_OP_TYPE_MASK"] = _adder.x86_instruction_C_OP_TYPE_MASK_get
    if _newclass:C_OP_TYPE_MASK = property(_adder.x86_instruction_C_OP_TYPE_MASK_get)
    __swig_getmethods__["C_OP_MOD_MASK"] = _adder.x86_instruction_C_OP_MOD_MASK_get
    if _newclass:C_OP_MOD_MASK = property(_adder.x86_instruction_C_OP_MOD_MASK_get)
    __swig_getmethods__["C_OP_SEG_MASK"] = _adder.x86_instruction_C_OP_SEG_MASK_get
    if _newclass:C_OP_SEG_MASK = property(_adder.x86_instruction_C_OP_SEG_MASK_get)
    __swig_getmethods__["C_OP_SIZE_MASK"] = _adder.x86_instruction_C_OP_SIZE_MASK_get
    if _newclass:C_OP_SIZE_MASK = property(_adder.x86_instruction_C_OP_SIZE_MASK_get)
    __swig_getmethods__["C_OP_REG_MASK"] = _adder.x86_instruction_C_OP_REG_MASK_get
    if _newclass:C_OP_REG_MASK = property(_adder.x86_instruction_C_OP_REG_MASK_get)
    __swig_getmethods__["C_OP_REGTBL_MASK"] = _adder.x86_instruction_C_OP_REGTBL_MASK_get
    if _newclass:C_OP_REGTBL_MASK = property(_adder.x86_instruction_C_OP_REGTBL_MASK_get)
    __swig_getmethods__["C_INS_EXEC"] = _adder.x86_instruction_C_INS_EXEC_get
    if _newclass:C_INS_EXEC = property(_adder.x86_instruction_C_INS_EXEC_get)
    __swig_getmethods__["C_INS_ARITH"] = _adder.x86_instruction_C_INS_ARITH_get
    if _newclass:C_INS_ARITH = property(_adder.x86_instruction_C_INS_ARITH_get)
    __swig_getmethods__["C_INS_LOGIC"] = _adder.x86_instruction_C_INS_LOGIC_get
    if _newclass:C_INS_LOGIC = property(_adder.x86_instruction_C_INS_LOGIC_get)
    __swig_getmethods__["C_INS_STACK"] = _adder.x86_instruction_C_INS_STACK_get
    if _newclass:C_INS_STACK = property(_adder.x86_instruction_C_INS_STACK_get)
    __swig_getmethods__["C_INS_COND"] = _adder.x86_instruction_C_INS_COND_get
    if _newclass:C_INS_COND = property(_adder.x86_instruction_C_INS_COND_get)
    __swig_getmethods__["C_INS_LOAD"] = _adder.x86_instruction_C_INS_LOAD_get
    if _newclass:C_INS_LOAD = property(_adder.x86_instruction_C_INS_LOAD_get)
    __swig_getmethods__["C_INS_ARRAY"] = _adder.x86_instruction_C_INS_ARRAY_get
    if _newclass:C_INS_ARRAY = property(_adder.x86_instruction_C_INS_ARRAY_get)
    __swig_getmethods__["C_INS_BIT"] = _adder.x86_instruction_C_INS_BIT_get
    if _newclass:C_INS_BIT = property(_adder.x86_instruction_C_INS_BIT_get)
    __swig_getmethods__["C_INS_FLAG"] = _adder.x86_instruction_C_INS_FLAG_get
    if _newclass:C_INS_FLAG = property(_adder.x86_instruction_C_INS_FLAG_get)
    __swig_getmethods__["C_INS_FPU"] = _adder.x86_instruction_C_INS_FPU_get
    if _newclass:C_INS_FPU = property(_adder.x86_instruction_C_INS_FPU_get)
    __swig_getmethods__["C_INS_TRAPS"] = _adder.x86_instruction_C_INS_TRAPS_get
    if _newclass:C_INS_TRAPS = property(_adder.x86_instruction_C_INS_TRAPS_get)
    __swig_getmethods__["C_INS_SYSTEM"] = _adder.x86_instruction_C_INS_SYSTEM_get
    if _newclass:C_INS_SYSTEM = property(_adder.x86_instruction_C_INS_SYSTEM_get)
    __swig_getmethods__["C_INS_OTHER"] = _adder.x86_instruction_C_INS_OTHER_get
    if _newclass:C_INS_OTHER = property(_adder.x86_instruction_C_INS_OTHER_get)
    __swig_getmethods__["C_INS_BRANCH"] = _adder.x86_instruction_C_INS_BRANCH_get
    if _newclass:C_INS_BRANCH = property(_adder.x86_instruction_C_INS_BRANCH_get)
    __swig_getmethods__["C_INS_BRANCHCC"] = _adder.x86_instruction_C_INS_BRANCHCC_get
    if _newclass:C_INS_BRANCHCC = property(_adder.x86_instruction_C_INS_BRANCHCC_get)
    __swig_getmethods__["C_INS_CALL"] = _adder.x86_instruction_C_INS_CALL_get
    if _newclass:C_INS_CALL = property(_adder.x86_instruction_C_INS_CALL_get)
    __swig_getmethods__["C_INS_CALLCC"] = _adder.x86_instruction_C_INS_CALLCC_get
    if _newclass:C_INS_CALLCC = property(_adder.x86_instruction_C_INS_CALLCC_get)
    __swig_getmethods__["C_INS_RET"] = _adder.x86_instruction_C_INS_RET_get
    if _newclass:C_INS_RET = property(_adder.x86_instruction_C_INS_RET_get)
    __swig_getmethods__["C_INS_LOOP"] = _adder.x86_instruction_C_INS_LOOP_get
    if _newclass:C_INS_LOOP = property(_adder.x86_instruction_C_INS_LOOP_get)
    __swig_getmethods__["C_INS_ADD"] = _adder.x86_instruction_C_INS_ADD_get
    if _newclass:C_INS_ADD = property(_adder.x86_instruction_C_INS_ADD_get)
    __swig_getmethods__["C_INS_SUB"] = _adder.x86_instruction_C_INS_SUB_get
    if _newclass:C_INS_SUB = property(_adder.x86_instruction_C_INS_SUB_get)
    __swig_getmethods__["C_INS_MUL"] = _adder.x86_instruction_C_INS_MUL_get
    if _newclass:C_INS_MUL = property(_adder.x86_instruction_C_INS_MUL_get)
    __swig_getmethods__["C_INS_DIV"] = _adder.x86_instruction_C_INS_DIV_get
    if _newclass:C_INS_DIV = property(_adder.x86_instruction_C_INS_DIV_get)
    __swig_getmethods__["C_INS_INC"] = _adder.x86_instruction_C_INS_INC_get
    if _newclass:C_INS_INC = property(_adder.x86_instruction_C_INS_INC_get)
    __swig_getmethods__["C_INS_DEC"] = _adder.x86_instruction_C_INS_DEC_get
    if _newclass:C_INS_DEC = property(_adder.x86_instruction_C_INS_DEC_get)
    __swig_getmethods__["C_INS_SHL"] = _adder.x86_instruction_C_INS_SHL_get
    if _newclass:C_INS_SHL = property(_adder.x86_instruction_C_INS_SHL_get)
    __swig_getmethods__["C_INS_SHR"] = _adder.x86_instruction_C_INS_SHR_get
    if _newclass:C_INS_SHR = property(_adder.x86_instruction_C_INS_SHR_get)
    __swig_getmethods__["C_INS_ROL"] = _adder.x86_instruction_C_INS_ROL_get
    if _newclass:C_INS_ROL = property(_adder.x86_instruction_C_INS_ROL_get)
    __swig_getmethods__["C_INS_ROR"] = _adder.x86_instruction_C_INS_ROR_get
    if _newclass:C_INS_ROR = property(_adder.x86_instruction_C_INS_ROR_get)
    __swig_getmethods__["C_INS_AND"] = _adder.x86_instruction_C_INS_AND_get
    if _newclass:C_INS_AND = property(_adder.x86_instruction_C_INS_AND_get)
    __swig_getmethods__["C_INS_OR"] = _adder.x86_instruction_C_INS_OR_get
    if _newclass:C_INS_OR = property(_adder.x86_instruction_C_INS_OR_get)
    __swig_getmethods__["C_INS_XOR"] = _adder.x86_instruction_C_INS_XOR_get
    if _newclass:C_INS_XOR = property(_adder.x86_instruction_C_INS_XOR_get)
    __swig_getmethods__["C_INS_NOT"] = _adder.x86_instruction_C_INS_NOT_get
    if _newclass:C_INS_NOT = property(_adder.x86_instruction_C_INS_NOT_get)
    __swig_getmethods__["C_INS_NEG"] = _adder.x86_instruction_C_INS_NEG_get
    if _newclass:C_INS_NEG = property(_adder.x86_instruction_C_INS_NEG_get)
    __swig_getmethods__["C_INS_PUSH"] = _adder.x86_instruction_C_INS_PUSH_get
    if _newclass:C_INS_PUSH = property(_adder.x86_instruction_C_INS_PUSH_get)
    __swig_getmethods__["C_INS_POP"] = _adder.x86_instruction_C_INS_POP_get
    if _newclass:C_INS_POP = property(_adder.x86_instruction_C_INS_POP_get)
    __swig_getmethods__["C_INS_PUSHREGS"] = _adder.x86_instruction_C_INS_PUSHREGS_get
    if _newclass:C_INS_PUSHREGS = property(_adder.x86_instruction_C_INS_PUSHREGS_get)
    __swig_getmethods__["C_INS_POPREGS"] = _adder.x86_instruction_C_INS_POPREGS_get
    if _newclass:C_INS_POPREGS = property(_adder.x86_instruction_C_INS_POPREGS_get)
    __swig_getmethods__["C_INS_PUSHFLAGS"] = _adder.x86_instruction_C_INS_PUSHFLAGS_get
    if _newclass:C_INS_PUSHFLAGS = property(_adder.x86_instruction_C_INS_PUSHFLAGS_get)
    __swig_getmethods__["C_INS_POPFLAGS"] = _adder.x86_instruction_C_INS_POPFLAGS_get
    if _newclass:C_INS_POPFLAGS = property(_adder.x86_instruction_C_INS_POPFLAGS_get)
    __swig_getmethods__["C_INS_ENTER"] = _adder.x86_instruction_C_INS_ENTER_get
    if _newclass:C_INS_ENTER = property(_adder.x86_instruction_C_INS_ENTER_get)
    __swig_getmethods__["C_INS_LEAVE"] = _adder.x86_instruction_C_INS_LEAVE_get
    if _newclass:C_INS_LEAVE = property(_adder.x86_instruction_C_INS_LEAVE_get)
    __swig_getmethods__["C_INS_TEST"] = _adder.x86_instruction_C_INS_TEST_get
    if _newclass:C_INS_TEST = property(_adder.x86_instruction_C_INS_TEST_get)
    __swig_getmethods__["C_INS_CMP"] = _adder.x86_instruction_C_INS_CMP_get
    if _newclass:C_INS_CMP = property(_adder.x86_instruction_C_INS_CMP_get)
    __swig_getmethods__["C_INS_MOV"] = _adder.x86_instruction_C_INS_MOV_get
    if _newclass:C_INS_MOV = property(_adder.x86_instruction_C_INS_MOV_get)
    __swig_getmethods__["C_INS_MOVCC"] = _adder.x86_instruction_C_INS_MOVCC_get
    if _newclass:C_INS_MOVCC = property(_adder.x86_instruction_C_INS_MOVCC_get)
    __swig_getmethods__["C_INS_XCHG"] = _adder.x86_instruction_C_INS_XCHG_get
    if _newclass:C_INS_XCHG = property(_adder.x86_instruction_C_INS_XCHG_get)
    __swig_getmethods__["C_INS_XCHGCC"] = _adder.x86_instruction_C_INS_XCHGCC_get
    if _newclass:C_INS_XCHGCC = property(_adder.x86_instruction_C_INS_XCHGCC_get)
    __swig_getmethods__["C_INS_STRCMP"] = _adder.x86_instruction_C_INS_STRCMP_get
    if _newclass:C_INS_STRCMP = property(_adder.x86_instruction_C_INS_STRCMP_get)
    __swig_getmethods__["C_INS_STRLOAD"] = _adder.x86_instruction_C_INS_STRLOAD_get
    if _newclass:C_INS_STRLOAD = property(_adder.x86_instruction_C_INS_STRLOAD_get)
    __swig_getmethods__["C_INS_STRMOV"] = _adder.x86_instruction_C_INS_STRMOV_get
    if _newclass:C_INS_STRMOV = property(_adder.x86_instruction_C_INS_STRMOV_get)
    __swig_getmethods__["C_INS_STRSTOR"] = _adder.x86_instruction_C_INS_STRSTOR_get
    if _newclass:C_INS_STRSTOR = property(_adder.x86_instruction_C_INS_STRSTOR_get)
    __swig_getmethods__["C_INS_XLAT"] = _adder.x86_instruction_C_INS_XLAT_get
    if _newclass:C_INS_XLAT = property(_adder.x86_instruction_C_INS_XLAT_get)
    __swig_getmethods__["C_INS_BITTEST"] = _adder.x86_instruction_C_INS_BITTEST_get
    if _newclass:C_INS_BITTEST = property(_adder.x86_instruction_C_INS_BITTEST_get)
    __swig_getmethods__["C_INS_BITSET"] = _adder.x86_instruction_C_INS_BITSET_get
    if _newclass:C_INS_BITSET = property(_adder.x86_instruction_C_INS_BITSET_get)
    __swig_getmethods__["C_INS_BITCLR"] = _adder.x86_instruction_C_INS_BITCLR_get
    if _newclass:C_INS_BITCLR = property(_adder.x86_instruction_C_INS_BITCLR_get)
    __swig_getmethods__["C_INS_CLEARCF"] = _adder.x86_instruction_C_INS_CLEARCF_get
    if _newclass:C_INS_CLEARCF = property(_adder.x86_instruction_C_INS_CLEARCF_get)
    __swig_getmethods__["C_INS_CLEARZF"] = _adder.x86_instruction_C_INS_CLEARZF_get
    if _newclass:C_INS_CLEARZF = property(_adder.x86_instruction_C_INS_CLEARZF_get)
    __swig_getmethods__["C_INS_CLEAROF"] = _adder.x86_instruction_C_INS_CLEAROF_get
    if _newclass:C_INS_CLEAROF = property(_adder.x86_instruction_C_INS_CLEAROF_get)
    __swig_getmethods__["C_INS_CLEARDF"] = _adder.x86_instruction_C_INS_CLEARDF_get
    if _newclass:C_INS_CLEARDF = property(_adder.x86_instruction_C_INS_CLEARDF_get)
    __swig_getmethods__["C_INS_CLEARSF"] = _adder.x86_instruction_C_INS_CLEARSF_get
    if _newclass:C_INS_CLEARSF = property(_adder.x86_instruction_C_INS_CLEARSF_get)
    __swig_getmethods__["C_INS_CLEARPF"] = _adder.x86_instruction_C_INS_CLEARPF_get
    if _newclass:C_INS_CLEARPF = property(_adder.x86_instruction_C_INS_CLEARPF_get)
    __swig_getmethods__["C_INS_SETCF"] = _adder.x86_instruction_C_INS_SETCF_get
    if _newclass:C_INS_SETCF = property(_adder.x86_instruction_C_INS_SETCF_get)
    __swig_getmethods__["C_INS_SETZF"] = _adder.x86_instruction_C_INS_SETZF_get
    if _newclass:C_INS_SETZF = property(_adder.x86_instruction_C_INS_SETZF_get)
    __swig_getmethods__["C_INS_SETOF"] = _adder.x86_instruction_C_INS_SETOF_get
    if _newclass:C_INS_SETOF = property(_adder.x86_instruction_C_INS_SETOF_get)
    __swig_getmethods__["C_INS_SETDF"] = _adder.x86_instruction_C_INS_SETDF_get
    if _newclass:C_INS_SETDF = property(_adder.x86_instruction_C_INS_SETDF_get)
    __swig_getmethods__["C_INS_SETSF"] = _adder.x86_instruction_C_INS_SETSF_get
    if _newclass:C_INS_SETSF = property(_adder.x86_instruction_C_INS_SETSF_get)
    __swig_getmethods__["C_INS_SETPF"] = _adder.x86_instruction_C_INS_SETPF_get
    if _newclass:C_INS_SETPF = property(_adder.x86_instruction_C_INS_SETPF_get)
    __swig_getmethods__["C_INS_TOGCF"] = _adder.x86_instruction_C_INS_TOGCF_get
    if _newclass:C_INS_TOGCF = property(_adder.x86_instruction_C_INS_TOGCF_get)
    __swig_getmethods__["C_INS_TOGZF"] = _adder.x86_instruction_C_INS_TOGZF_get
    if _newclass:C_INS_TOGZF = property(_adder.x86_instruction_C_INS_TOGZF_get)
    __swig_getmethods__["C_INS_TOGOF"] = _adder.x86_instruction_C_INS_TOGOF_get
    if _newclass:C_INS_TOGOF = property(_adder.x86_instruction_C_INS_TOGOF_get)
    __swig_getmethods__["C_INS_TOGDF"] = _adder.x86_instruction_C_INS_TOGDF_get
    if _newclass:C_INS_TOGDF = property(_adder.x86_instruction_C_INS_TOGDF_get)
    __swig_getmethods__["C_INS_TOGSF"] = _adder.x86_instruction_C_INS_TOGSF_get
    if _newclass:C_INS_TOGSF = property(_adder.x86_instruction_C_INS_TOGSF_get)
    __swig_getmethods__["C_INS_TOGPF"] = _adder.x86_instruction_C_INS_TOGPF_get
    if _newclass:C_INS_TOGPF = property(_adder.x86_instruction_C_INS_TOGPF_get)
    __swig_getmethods__["C_INS_TRAP"] = _adder.x86_instruction_C_INS_TRAP_get
    if _newclass:C_INS_TRAP = property(_adder.x86_instruction_C_INS_TRAP_get)
    __swig_getmethods__["C_INS_TRAPCC"] = _adder.x86_instruction_C_INS_TRAPCC_get
    if _newclass:C_INS_TRAPCC = property(_adder.x86_instruction_C_INS_TRAPCC_get)
    __swig_getmethods__["C_INS_TRET"] = _adder.x86_instruction_C_INS_TRET_get
    if _newclass:C_INS_TRET = property(_adder.x86_instruction_C_INS_TRET_get)
    __swig_getmethods__["C_INS_BOUNDS"] = _adder.x86_instruction_C_INS_BOUNDS_get
    if _newclass:C_INS_BOUNDS = property(_adder.x86_instruction_C_INS_BOUNDS_get)
    __swig_getmethods__["C_INS_DEBUG"] = _adder.x86_instruction_C_INS_DEBUG_get
    if _newclass:C_INS_DEBUG = property(_adder.x86_instruction_C_INS_DEBUG_get)
    __swig_getmethods__["C_INS_TRACE"] = _adder.x86_instruction_C_INS_TRACE_get
    if _newclass:C_INS_TRACE = property(_adder.x86_instruction_C_INS_TRACE_get)
    __swig_getmethods__["C_INS_INVALIDOP"] = _adder.x86_instruction_C_INS_INVALIDOP_get
    if _newclass:C_INS_INVALIDOP = property(_adder.x86_instruction_C_INS_INVALIDOP_get)
    __swig_getmethods__["C_INS_OFLOW"] = _adder.x86_instruction_C_INS_OFLOW_get
    if _newclass:C_INS_OFLOW = property(_adder.x86_instruction_C_INS_OFLOW_get)
    __swig_getmethods__["C_INS_HALT"] = _adder.x86_instruction_C_INS_HALT_get
    if _newclass:C_INS_HALT = property(_adder.x86_instruction_C_INS_HALT_get)
    __swig_getmethods__["C_INS_IN"] = _adder.x86_instruction_C_INS_IN_get
    if _newclass:C_INS_IN = property(_adder.x86_instruction_C_INS_IN_get)
    __swig_getmethods__["C_INS_OUT"] = _adder.x86_instruction_C_INS_OUT_get
    if _newclass:C_INS_OUT = property(_adder.x86_instruction_C_INS_OUT_get)
    __swig_getmethods__["C_INS_CPUID"] = _adder.x86_instruction_C_INS_CPUID_get
    if _newclass:C_INS_CPUID = property(_adder.x86_instruction_C_INS_CPUID_get)
    __swig_getmethods__["C_INS_NOP"] = _adder.x86_instruction_C_INS_NOP_get
    if _newclass:C_INS_NOP = property(_adder.x86_instruction_C_INS_NOP_get)
    __swig_getmethods__["C_INS_BCDCONV"] = _adder.x86_instruction_C_INS_BCDCONV_get
    if _newclass:C_INS_BCDCONV = property(_adder.x86_instruction_C_INS_BCDCONV_get)
    __swig_getmethods__["C_INS_SZCONV"] = _adder.x86_instruction_C_INS_SZCONV_get
    if _newclass:C_INS_SZCONV = property(_adder.x86_instruction_C_INS_SZCONV_get)
    __swig_getmethods__["C_INS_BYTE"] = _adder.x86_instruction_C_INS_BYTE_get
    if _newclass:C_INS_BYTE = property(_adder.x86_instruction_C_INS_BYTE_get)
    __swig_getmethods__["C_INS_WORD"] = _adder.x86_instruction_C_INS_WORD_get
    if _newclass:C_INS_WORD = property(_adder.x86_instruction_C_INS_WORD_get)
    __swig_getmethods__["C_INS_DWORD"] = _adder.x86_instruction_C_INS_DWORD_get
    if _newclass:C_INS_DWORD = property(_adder.x86_instruction_C_INS_DWORD_get)
    __swig_getmethods__["C_INS_QWORD"] = _adder.x86_instruction_C_INS_QWORD_get
    if _newclass:C_INS_QWORD = property(_adder.x86_instruction_C_INS_QWORD_get)
    __swig_getmethods__["C_INS_REPZ"] = _adder.x86_instruction_C_INS_REPZ_get
    if _newclass:C_INS_REPZ = property(_adder.x86_instruction_C_INS_REPZ_get)
    __swig_getmethods__["C_INS_REPNZ"] = _adder.x86_instruction_C_INS_REPNZ_get
    if _newclass:C_INS_REPNZ = property(_adder.x86_instruction_C_INS_REPNZ_get)
    __swig_getmethods__["C_INS_LOCK"] = _adder.x86_instruction_C_INS_LOCK_get
    if _newclass:C_INS_LOCK = property(_adder.x86_instruction_C_INS_LOCK_get)
    __swig_getmethods__["C_INS_DELAY"] = _adder.x86_instruction_C_INS_DELAY_get
    if _newclass:C_INS_DELAY = property(_adder.x86_instruction_C_INS_DELAY_get)
    __swig_getmethods__["C_INS_TYPE_MASK"] = _adder.x86_instruction_C_INS_TYPE_MASK_get
    if _newclass:C_INS_TYPE_MASK = property(_adder.x86_instruction_C_INS_TYPE_MASK_get)
    __swig_getmethods__["C_INS_GROUP_MASK"] = _adder.x86_instruction_C_INS_GROUP_MASK_get
    if _newclass:C_INS_GROUP_MASK = property(_adder.x86_instruction_C_INS_GROUP_MASK_get)
    __swig_getmethods__["C_INS_SIZE_MASK"] = _adder.x86_instruction_C_INS_SIZE_MASK_get
    if _newclass:C_INS_SIZE_MASK = property(_adder.x86_instruction_C_INS_SIZE_MASK_get)
    __swig_getmethods__["C_INS_MOD_MASK"] = _adder.x86_instruction_C_INS_MOD_MASK_get
    if _newclass:C_INS_MOD_MASK = property(_adder.x86_instruction_C_INS_MOD_MASK_get)
    def __str__(*args): return apply(_adder.x86_instruction___str__,args)
    def __del__(self, destroy= _adder.delete_x86_instruction):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C x86_instruction instance at %s>" % (self.this,)

class x86_instructionPtr(x86_instruction):
    def __init__(self,this):
        _swig_setattr(self, x86_instruction, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, x86_instruction, 'thisown', 0)
        _swig_setattr(self, x86_instruction,self.__class__,x86_instruction)
_adder.x86_instruction_swigregister(x86_instructionPtr)

import code
version = "Adder v0.3.3"
NULL = ptr(0x00000000)
        
def interact( readfunc=None, frame=None ):
	code.interact( version + "\n(C)2004 Oliver Lavery\n\ntype help() for help, or enter python commands\nType <Ctrl-Z> alone on a line to quit\n", readfunc, frame )
	



