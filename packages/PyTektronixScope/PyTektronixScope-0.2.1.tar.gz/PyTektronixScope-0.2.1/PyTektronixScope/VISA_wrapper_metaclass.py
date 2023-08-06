#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module convert VISA command to methods


For example, from a command like "BEGin:End VALue" the programm
will generate methods get_begin_end, set_begin_end and a property
begin_end using those methods.
"""
import re
import numbers

class TestValue(object):
    """Class use to test the paramters 

        This class implement the test method the return either None (if the test failed) or
        a string to format the value
    """
    def test(self, value):
        if self.condition(value):
            return self.to_string(value)
        else:
            return None
    def to_string(self, value):
        return str(value)
    def condition(self, value):
        return False

class TestValueFromEnum(TestValue):
    def __init__(self, values, replacement=None):
        if replacement is None:
            replacement = enum_value._keys
        self.replacement = replacement
        self.values = values
    def to_string(self, value):
        if isinstance(value, type(self.values[0])):
            i = self.values._values.index(value)
            return self.replacement[i]
        else: 
            i = self.values._keys.index(value)
            return self.replacement[i]            
    def condition(self, value):
        return (value in self.values._values) or (value in self.values._keys)
    def __repr__(self):
        return 'from enum %s'%self.values._keys.__str__()
            

class TestValueFromType(TestValue):
    """ Test if a value is from a given type """
    def __init__(self, tpe):
        self.type = tpe
    def condition(self, value):
        return isinstance(value, self.type)
    def __repr__(self):
        return 'of type %s'%self.type.__name__

class TestValueFromRE(TestValue):
    """ Test a value using a regular expression """
    def __init__(self, re):
        self.re = re
    def condition(self, value):
        return re.match(value)
    def __repr__(self):
        return 'match %s'%self.re

class TestValueBoundNumber(TestValue):
    """ Test if a value is a number within bounds """
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum
    def condition(self, value):
        return isinstance(value, numbers.Number) and value>=self.minimum and value<=self.maximum 
    def __repr__(self):
        return 'is between %s and %s'%(self.minimum, self.maximum)

class TestValueFromValue(TestValue):
    """ Test if a value is equal to a given one """
    def __init__(self, val):
        self.val = val
    def condition(self, value):
        return value==self.val
    def __repr__(self):
        return 'equal to %s'%self.val

def _short_version(s): 
    """Returns the short version of a string

    _short_version('COUPling')=='COUP'
    """
    sl = s.lower()
    return ''.join([c for i,c in enumerate(s) if s[i]<>sl[i]])

class TestValueFromString(TestValue):
    """ Test a value by comparing to a string. If the string is 
        CAPsmall then test for capsmall and cap. This test 
        is not case sensitive """
    def __init__(self, val):
        self.initial_val = val
        self.val = val.lower()
        self.val_short = _short_version(val).lower()
    def condition(self, value):
        return str(value).lower()==self.val or str(value).lower()==self.val_short
    def __repr__(self):
        return 'equal to %s or equal to %s'%(self.initial_val, self.val_short)

def _convert_value_to_TestValue(val):
    if isinstance(val, TestValue):
        return val
    elif isinstance(val, type):
        return TestValueFromType(val)
    elif isinstance(val, type(re.compile('po'))):
        return TestValueFromRe(val)
    elif isinstance(val, str) or isinstance(val, unicode):
        return TestValueFromString(val)
    else:
        return TestValueFromValue(val)

def _convert_list_value_to_list_of_TestValue(lst):
    try:
        return map(_convert_value_to_TestValue, lst)
    except TypeError:
        return map(_convert_value_to_TestValue, [lst])

def _try_to_convert_to_number(value):
    """Try to convert a string to a number (int or float)"""
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

def _generic_get_command(cmd_name, out_conversion=None, doc=None):
    """ Create a method that will query the cmd_name 

        for example : _generic_get_command('CH1:IMPedance') will create the method 
        whose name is _get_ch1_impedance

        By default this function try also to convert the output of the request into an int or a float
        otherwise it uses the out_conversion function.
    """
    if out_conversion is None:
        out_conversion = _try_to_convert_to_number
    def get_val(self):
        cmd_nameb = self.get_cmd_name(cmd_name)
        value = self.ask('%s ?'%cmd_nameb)
        return out_conversion(value)
    get_val.__name__ = "_get_%s"%(cmd_name.replace(':','_').lower())
    get_val.__doc__ = get_val.__name__ if doc is None else doc
    return get_val

def _generic_set_command(cmd_name, list_value=None, default_value=None, doc=None):
    """ Create a method that will set the cmd_name 

        for example : _generic_set_command('CH1:IMPedance') will create the method 
        whose name is _set_ch1_impedance and takes one parameter

        Optional argument : 
                list_value : the list of possible values. The list can be direct value        
                        or type or regular expression. 
                default_value : the default value
    """
    if list_value is None:
        def set_val(self, value):
            cmd_nameb = self.get_cmd_name(cmd_name)
            self.write('%s %s'%(cmd_nameb, value))
    else:
        list_test_value = _convert_list_value_to_list_of_TestValue(list_value)
        def set_val(self, value=None):
            cmd_nameb = self.get_cmd_name(cmd_name)
            if value is None:
                value = default_value
            for test in list_test_value:
                a = test.test(value)
                if a is not None:
                    self.write('%s %s'%(cmd_nameb, a))
                    return None
                raise ValueError("Error in %s(). Set value is %s while it should be %s"\
                %('set_%s'%cmd_name.replace(':','_').lower(), value,  ' or '.join(map(str, list_test_value))) )
    set_val.__name__ = "_set_%s"%(cmd_name.replace(':','_').lower())
    set_val.__doc__ = set_val.__name__ if doc is None else doc
    return set_val


class GenericCommand(object):
    pass

class generic_get_command(GenericCommand):
    def __init__(self, cmd_name, out_conversion=None, doc=None):    
        self.doc = doc
        self.cmd_name = cmd_name
        self.get_cmd = _generic_get_command(cmd_name, out_conversion, doc=doc)
    def to_dict(self,name):
        return {name:property(self.get_cmd,doc=self.doc), self.get_cmd.__name__:self.get_cmd}

class generic_set_command(GenericCommand):
    def __init__(self, cmd_name, list_value=None, default_value=None, doc=None):
        self.doc = doc
        self.cmd_name = cmd_name
        self.set_cmd = _generic_set_command(cmd_name, list_value, default_value, doc=doc)
    def to_dict(self,name):
        return {name:property(lambda self:None,self.set_cmd,doc=self.doc), self.set_cmd.__name__:self.set_cmd}


class generic_get_set_command(GenericCommand):
    def __init__(self, cmd_name, list_value=None, default_value=None, out_conversion=None, doc=None):
        self.doc = doc
        self.cmd_name = cmd_name
        self.get_cmd = _generic_get_command(cmd_name, out_conversion, doc=doc)
        self.set_cmd = _generic_set_command(cmd_name, list_value, default_value, doc=doc)
    def to_dict(self,name):
        return {name:property(self.get_cmd,self.set_cmd,doc=self.doc), 
                    self.get_cmd.__name__:self.get_cmd,
                    self.set_cmd.__name__:self.set_cmd}


class InstrumentMetaclass(type):
    """ Meta class used to create property from GeneriCommand object



        For example : 
        class Test():
            __metaclass__ = InstrumentMetaclass
            # Create a a property attribute and the method get_attribute and set_attribute
            attribute = generic_get_set_command(....)         
    """
    def __new__(cls, name, bases, dct):
        attrs = dict((name, value) for name, value in dct.items() if isinstance(value, GenericCommand))

        out =  dict((name, value) for name, value in dct.items() if not name.startswith('__'))       
        out = dct
        for (name, value) in attrs.items():
            out.update(value.to_dict(name))

        final_object = type.__new__(cls, name, bases, out)

        return final_object



class InstrumentCommand(object):
    def get_cmd_name(self, cmd_name):
        return cmd_name

class Group(object):
    """ This class is used to group command


    For example, if we want to use the command scope.Acquisition.StartTime,
    the object returned by scope.Acquisition is an instance of Group

    In order to add a group to an instrument:
    1) Define the class of the group that herits from Group
    2) Add an instance of the defined class in the __init__ of the instrument
    """
    def __init__(self, parent):
        self.__parent = parent
    def write(self, s):
        return self.__parent.write(s)
    def ask(self, s):
        return self.__parent.ask(s)
    def get_cmd_name(self, cmd_name):
        return cmd_name

class IndexedGroup(Group):
    """ This class is used to group command with a parameter


    For example, if we want to use the command scope.Channels[1].Offset,
    the object returned by scope.Channels is an instance of IndexedGroup

    In order to add a group to an instrument:
    1) Define the class of the group that herits from IndexedGroup
    2) Specify the attribute var that defines the string to replace with the item number in the command
    3) Add an instance of the defined class in the __init__ of the instrument
    """
    def __init__(self, parent, item=0):
        Group.__init__(self, parent)
        self.__item=item
    def __getitem__(self, i):
        # out = IndexedGroup(self._parent,i)
        # return out        
        self._item = i
        return self
    def get_cmd_name(self, cmd_name):
        new_cmd = cmd_name.replace(self.var, str(self._item))
        return new_cmd



if __name__ == "__main__":
    class Generic(object):
        __metaclass__ = InstrumentMetaclass
        def write(self,s):
            print s
        def ask(self,s):
            print s
            return '45.4'
    class ChannelGroup(IndexedGroup):
        __metaclass__ = InstrumentMetaclass
        var = '<X>'
        testa = generic_get_set_command('CH<X>:TEST',[TestValueBoundNumber(-1,1)])

    class Test(Generic, InstrumentCommand):
        def __init__(self):
            self.channel = ChannelGroup(self)
        coucou_val = generic_get_set_command( 'COUCOU:VAL',["PIErre", "MATHilde", numbers.Number], default_value='Pierre', doc='This is a test method')
        coucou_set = generic_set_command( 'COUCOU:VAL',["PIErre", "MATHilde", numbers.Number], default_value='Pierre', doc='This is a test method')


    scope = Test()
#    class Test(Generic):
#        pass
#    _add_generic_get_set_command(Test, 'COUCOU:VAL',["PIErre", "MATHilde", numbers.Number], default_value='Pierre', doc='This is a test method')
