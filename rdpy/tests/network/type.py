'''
@author: sylvain
'''
import unittest
import rdpy.network.type

class TypeCase(unittest.TestCase):
    '''
    represent test case for all classes and function
    present in rdpy.network.type
    '''
    def test_callable_value_const(self):
        '''
        test if callable value with const ctor doesn't change value
        '''
        c = rdpy.network.type.CallableValue(5)
        self.assertEqual(c.value, 5, "invalid callable const")
        
    def test_callable_value_lambda(self):
        '''
        test if callable value with lambda ctor return dynamic value
        '''
        c = rdpy.network.type.CallableValue(lambda:5)
        self.assertEqual(c.value, 5, "invalid callable lambda")
    
    def test_type_write_conditional_true(self):
        '''
        test when write is obligatory call write function
        '''
        class TestType(rdpy.network.type.Type):
            def __write__(self, s):
                raise Exception()
        s = rdpy.network.type.Stream()
        self.assertRaises(Exception, s.writeType, TestType(conditional = lambda:True))
    
    @unittest.expectedFailure
    def test_type_write_conditional_false(self):
        '''
        test when write doesn't needed, doesn't call write function
        '''
        class TestType(rdpy.network.type.Type):
            def __write__(self, s):
                raise Exception()
        s = rdpy.network.type.Stream()
        self.assertRaises(Exception, s.writeType, TestType(conditional = lambda:False))
        
    def test_type_read_conditional_true(self):
        '''
        test when read is obligatory call write function
        '''
        class TestType(rdpy.network.type.Type):
            def __read__(self, s):
                raise Exception()
        s = rdpy.network.type.Stream()
        self.assertRaises(Exception, s.readType, TestType(conditional = lambda:True))
    
    @unittest.expectedFailure
    def test_type_read_conditional_false(self):
        '''
        test when read doesn't needed, doesn't call read function
        '''
        class TestType(rdpy.network.type.Type):
            def __read__(self, s):
                raise Exception()
        s = rdpy.network.type.Stream()
        self.assertRaises(Exception, s.readType, TestType(conditional = lambda:False))
        
    
    def test_sizeof_conditional_true(self):
        '''
        test if sizeof of simple type is init value(4) when type is conditional true
        '''
        v = rdpy.network.type.SimpleType("I", 4, False, 0, conditional = lambda:True)
        self.assertEqual(rdpy.network.type.sizeof(v), 4, "invalid sizeof")
        
    def test_sizeof_conditional_false(self):
        '''
        test if sizeof of simple type is 0 when type is conditional false
        '''
        v = rdpy.network.type.SimpleType("I", 4, False, 0, conditional = lambda:False)
        self.assertEqual(rdpy.network.type.sizeof(v), 0, "invalid sizeof")
        
    def test_sizeof_list(self):
        '''
        test call sizeof on list of type
        '''
        v = [rdpy.network.type.UInt8(), rdpy.network.type.UInt16Le(), rdpy.network.type.UInt32Le()]
        self.assertEqual(rdpy.network.type.sizeof(v), 7, "invalid sizeof")
        
    def test_sizeof_list_conditional(self):
        '''
        test call sizeof on list of type with one type hidden
        '''
        v = [rdpy.network.type.UInt8(), rdpy.network.type.UInt16Le(conditional = lambda:False), rdpy.network.type.UInt32Le()]
        self.assertEqual(rdpy.network.type.sizeof(v), 5, "invalid sizeof")
        
    def test_sizeof_tuple(self):
        '''
        test call sizeof on tuple of type
        '''
        v = [rdpy.network.type.UInt8(), rdpy.network.type.UInt16Le(), rdpy.network.type.UInt32Le()]
        self.assertEqual(rdpy.network.type.sizeof(v), 7, "invalid sizeof")
        
    def test_sizeof_tuple_conditional(self):
        '''
        test call sizeof on tuple of type with one type hidden
        '''
        v = (rdpy.network.type.UInt8(), rdpy.network.type.UInt16Le(), rdpy.network.type.UInt32Le(conditional = lambda:False))
        self.assertEqual(rdpy.network.type.sizeof(v), 3, "invalid sizeof")
        
    def test_stream_write_uint8_type(self):
        '''
        test write uint8 in stream
        '''
        s = rdpy.network.type.Stream()
        s.writeType(rdpy.network.type.UInt8(1))
        self.assertEqual(''.join(s.buflist), '\x01', "invalid stream write")
        
    def test_stream_write_uint16Le_type(self):
        '''
        test write UInt16Le in stream
        '''
        s = rdpy.network.type.Stream()
        s.writeType(rdpy.network.type.UInt16Le(1))
        self.assertEqual(''.join(s.buflist), '\x01\x00', "invalid stream write")
    
    def test_stream_write_uint16Be_type(self):
        '''
        test write UInt16Be in stream
        '''
        s = rdpy.network.type.Stream()
        s.writeType(rdpy.network.type.UInt16Be(1))
        self.assertEqual(''.join(s.buflist), '\x00\x01', "invalid stream write")
        
    def test_stream_write_uint24Le_type(self):
        '''
        test write UInt24Le in stream
        '''
        s = rdpy.network.type.Stream()
        s.writeType(rdpy.network.type.UInt24Le(1))
        self.assertEqual(''.join(s.buflist), '\x01\x00\x00', "invalid stream write")
    
    def test_stream_write_uint24Be_type(self):
        '''
        test write uint24Be in stream
        '''
        s = rdpy.network.type.Stream()
        s.writeType(rdpy.network.type.UInt24Be(1))
        self.assertEqual(''.join(s.buflist), '\x00\x00\x01', "invalid stream write")
        
    def test_stream_write_uint32Le_type(self):
        '''
        test write UInt32Le in stream
        '''
        s = rdpy.network.type.Stream()
        s.writeType(rdpy.network.type.UInt32Le(1))
        self.assertEqual(''.join(s.buflist), '\x01\x00\x00\x00', "invalid stream write")
    
    def test_stream_write_uint32Be_type(self):
        '''
        test write UInt32Be in stream
        '''
        s = rdpy.network.type.Stream()
        s.writeType(rdpy.network.type.UInt32Be(1))
        self.assertEqual(''.join(s.buflist), '\x00\x00\x00\x01', "invalid stream write")
        
    def test_stream_read_uint8_type(self):
        '''
        test read UInt8 type from stream
        '''
        s = rdpy.network.type.Stream('\x01')
        t = rdpy.network.type.UInt8()
        s.readType(t)
        self.assertEqual(t.value, 1, "invalid stream read value")
        self.assertEqual(s.dataLen(), 0, "not read all stream")
        
    def test_stream_read_uint16Le_type(self):
        '''
        test read UInt16Le type from stream
        '''
        s = rdpy.network.type.Stream('\x01\x00')
        t = rdpy.network.type.UInt16Le()
        s.readType(t)
        self.assertEqual(t.value, 1, "invalid stream read value")
        self.assertEqual(s.dataLen(), 0, "not read all stream")
        
    def test_stream_read_uint16Be_type(self):
        '''
        test read UInt16Be type from stream
        '''
        s = rdpy.network.type.Stream('\x00\x01')
        t = rdpy.network.type.UInt16Be()
        s.readType(t)
        self.assertEqual(t.value, 1, "invalid stream read value")
        self.assertEqual(s.dataLen(), 0, "not read all stream")
        
    def test_stream_read_uint24Le_type(self):
        '''
        test read UInt24Le type from stream
        '''
        s = rdpy.network.type.Stream('\x01\x00\x00')
        t = rdpy.network.type.UInt24Le()
        s.readType(t)
        self.assertEqual(t.value, 1, "invalid stream read value")
        self.assertEqual(s.dataLen(), 0, "not read all stream")
        
    def test_stream_read_uint24Be_type(self):
        '''
        test read UInt24Be type from stream
        '''
        s = rdpy.network.type.Stream('\x00\x00\x01')
        t = rdpy.network.type.UInt24Be()
        s.readType(t)
        self.assertEqual(t.value, 1, "invalid stream read")
        self.assertEqual(s.dataLen(), 0, "not read all stream")
        
    def test_stream_read_uint32Le_type(self):
        '''
        test read UInt32Le type from stream
        '''
        s = rdpy.network.type.Stream('\x01\x00\x00\x00')
        t = rdpy.network.type.UInt32Le()
        s.readType(t)
        self.assertEqual(t.value, 1, "invalid stream read value")
        self.assertEqual(s.dataLen(), 0, "not read all stream")
        
    def test_stream_read_uint32Be_type(self):
        '''
        test read UInt32Be type from stream
        '''
        s = rdpy.network.type.Stream('\x00\x00\x00\x01')
        t = rdpy.network.type.UInt32Be()
        s.readType(t)
        self.assertEqual(t.value, 1, "invalid stream read")
        self.assertEqual(s.dataLen(), 0, "not read all stream")
        
    def test_stream_read_optional_singletype(self):
        '''
        test optional option in case of simple type reading
        '''
        #unsigned int case
        t = rdpy.network.type.SimpleType("I", 4, False, 0, optional = True)
        #empty stream
        s1 = rdpy.network.type.Stream()
        s1.readType(t)
        self.assertEqual(t.value, 0, "invalid stream read optional value")
        
    def test_stream_read_conditional_singletype_false(self):
        '''
        test conditional option in case of simple type reading and when condition is false (not read)
        '''
        #unsigned int case
        t = rdpy.network.type.SimpleType("I", 4, False, 0, conditional = lambda:False)
        s1 = rdpy.network.type.Stream("\x01\x00\x00\x00")
        s1.readType(t)
        self.assertEqual(t.value, 0, "invalid stream read conditional value")
        
    def test_stream_read_conditional_singletype_true(self):
        '''
        test conditional option in case of simple type reading and when condition is true (must be read)
        '''
        #unsigned int case
        t = rdpy.network.type.SimpleType("I", 4, False, 0, conditional = lambda:True)
        s1 = rdpy.network.type.Stream("\x01\x00\x00\x00")
        s1.readType(t)
        self.assertEqual(t.value, 1, "invalid stream read conditional value")
        
    def test_strem_read_rollback_constant_constraint(self):
        '''
        test if constant constraint fail, the reading stream is correctly rollback
        '''
        class TestComposite(rdpy.network.type.CompositeType):
            def __init__(self):
                rdpy.network.type.CompositeType.__init__(self)
                self.padding = rdpy.network.type.UInt32Le(0)
                self.constraint = rdpy.network.type.UInt32Le(1, constant = True)
                
        s = rdpy.network.type.Stream("\x00\x00\x00\x00\x00\x00\x00\x00")
        try:
            s.readType(TestComposite())
        except Exception:
            self.assertEqual(s.readLen(), 0, "invalid stream roll back operation")
            return
        self.assertTrue(False, "Constant constraint fail")
        
    def test_strem_read_rollback_constant_constraint_recurcive(self):
        '''
        test if constant constraint fail even in recurcive composite type, 
        the reading stream is correctly rollback
        '''
        class TestSubComposite(rdpy.network.type.CompositeType):
            def __init__(self):
                rdpy.network.type.CompositeType.__init__(self)
                self.padding = rdpy.network.type.UInt32Le(0)
                self.constraint = rdpy.network.type.UInt32Le(1, constant = True)
                
        class TestComposite(rdpy.network.type.CompositeType):
            def __init__(self):
                rdpy.network.type.CompositeType.__init__(self)
                self.padding = rdpy.network.type.UInt32Le(0)
                self.recurcive = TestSubComposite()
                
        s = rdpy.network.type.Stream("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        try:
            s.readType(TestComposite())
        except Exception:
            self.assertEqual(s.readLen(), 0, "invalid stream roll back operation")
            return
        self.assertTrue(False, "Constant constraint fail")
    
    def test_stream_read_rollback_not_enough_data(self):
        '''
        test if constant constraint fail even in recurcive composite type, 
        the reading stream is correctly rollback
        '''
        class TestSubComposite(rdpy.network.type.CompositeType):
            def __init__(self):
                rdpy.network.type.CompositeType.__init__(self)
                self.padding = rdpy.network.type.UInt32Le(0)
                self.constraint = rdpy.network.type.UInt32Le(1)
                
        class TestComposite(rdpy.network.type.CompositeType):
            def __init__(self):
                rdpy.network.type.CompositeType.__init__(self)
                self.padding = rdpy.network.type.UInt32Le(0)
                self.recurcive = TestSubComposite()
                
        s = rdpy.network.type.Stream("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        try:
            s.readType(TestComposite())
        except Exception:
            self.assertEqual(s.readLen(), 0, "invalid stream roll back operation")
            return
        self.assertTrue(False, "Constant constraint fail")
        
    def test_stream_composite_type_force_read_length_optional(self):
        '''
        test where type have readLen forced and have optional subtype which have
        length greater than last subtype of composite type
        '''
        class TestType(rdpy.network.type.CompositeType):
            def __init__(self, readLen = None):
                rdpy.network.type.CompositeType.__init__(self, readLen = readLen)
                self.t1 = rdpy.network.type.UInt32Le(0, optional = True)
                self.t2 = rdpy.network.type.UInt16Le(0, optional = True)
                
        s = rdpy.network.type.Stream("\x00\x00\x00\x00\x00\x00\x00")
        t = TestType(readLen = rdpy.network.type.UInt8(2))
        s.readType(t)
        self.assertTrue(not t.t1._is_readed and t.t2._is_readed, "Invalid optional reading when length is forced")