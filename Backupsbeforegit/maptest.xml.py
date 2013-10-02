# XML Parser/Data Access Object maptest.xml.py
"""AUTO-GENERATED Source file for maptest.xml.py"""
import xml.sax
import Queue
import Q2API.xml.base_xml

rewrite_name_list = ("name", "value", "attrs", "flatten_self", "flatten_self_safe_sql_attrs", "flatten_self_to_utf8", "children")

def process_attrs(attrs):
    """Process sax attribute data into local class namespaces"""
    if attrs.getLength() == 0:
        return {}
    tmp_dict = {}
    for name in attrs.getNames():
        tmp_dict[name] = attrs.getValue(name)
    return tmp_dict

def clean_node_name(node_name):
    clean_name = node_name.replace(":", "_").replace("-", "_").replace(".", "_")

    if clean_name in rewrite_name_list:
        clean_name = "_" + clean_name + "_"

    return clean_name

class desc_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'map', u'building', u'locked_door']
        Q2API.xml.base_xml.XMLNode.__init__(self, "desc", attrs, None, [])

class enemy_hp_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'map', u'building', u'enemy']
        Q2API.xml.base_xml.XMLNode.__init__(self, "enemy_hp", attrs, None, [])

class enemy_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'building']
        self.enemy_hp = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "enemy", attrs, None, [])

class event_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'building']
        Q2API.xml.base_xml.XMLNode.__init__(self, "event", attrs, None, [])

class item_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'building']
        Q2API.xml.base_xml.XMLNode.__init__(self, "item", attrs, None, [])

class locked_door_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'building']
        self.desc = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "locked_door", attrs, None, [])

class text_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'building']
        Q2API.xml.base_xml.XMLNode.__init__(self, "text", attrs, None, [])

class building_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 2
        self.path = [None, u'map']
        self.locked_door = []
        self.enemy = []
        self.text = []
        self.item = []
        self.event = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "building", attrs, None, [])

class map_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 1
        self.path = [None]
        self.building = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "map", attrs, None, [])

class NodeHandler(xml.sax.handler.ContentHandler):
    """SAX ContentHandler to map XML input class/object"""
    def __init__(self, return_q):     # overridden in subclass
        self.obj_depth = [None]
        self.return_q = return_q
        self.last_processed = None
        self.char_buffer = []
        xml.sax.handler.ContentHandler.__init__(self)   # superclass init

    def startElement(self, name, attrs): # creating the node along the path being tracked
        """Override base class ContentHandler method"""
        name = clean_node_name(name)
        p_attrs = process_attrs(attrs)

        if name == "":
            raise ValueError, "XML Node name cannot be empty"

        elif name == "building":
            self.obj_depth.append(building_q2class(p_attrs))

        elif name == "map":
            self.obj_depth.append(map_q2class(p_attrs))

        elif name == "locked_door":
            self.obj_depth.append(locked_door_q2class(p_attrs))

        elif name == "enemy":
            self.obj_depth.append(enemy_q2class(p_attrs))

        elif name == "text":
            self.obj_depth.append(text_q2class(p_attrs))

        elif name == "enemy_hp":
            self.obj_depth.append(enemy_hp_q2class(p_attrs))

        elif name == "item":
            self.obj_depth.append(item_q2class(p_attrs))

        elif name == "event":
            self.obj_depth.append(event_q2class(p_attrs))

        elif name == "desc":
            self.obj_depth.append(desc_q2class(p_attrs))

        self.char_buffer = []
        self.last_processed = "start"

    def endElement(self, name): # need to append the node that is closing in the right place
        """Override base class ContentHandler method"""
        name = clean_node_name(name)

        if (len(self.char_buffer) != 0) and (self.last_processed == "start"):
            self.obj_depth[-1].value = "".join(self.char_buffer)

        if name == "":
            raise ValueError, "XML Node name cannot be empty"

        elif name == "building":
            self.obj_depth[-2].building.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "map":
            # root node is not added to a parent; stays on the "stack" for the return_object
            self.char_buffer = []
            self.last_processed = "end"
            return

        elif name == "locked_door":
            self.obj_depth[-2].locked_door.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "enemy":
            self.obj_depth[-2].enemy.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "text":
            self.obj_depth[-2].text.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "enemy_hp":
            self.obj_depth[-2].enemy_hp.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "item":
            self.obj_depth[-2].item.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "event":
            self.obj_depth[-2].event.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "desc":
            self.obj_depth[-2].desc.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        self.last_processed = "end"


    def characters(self, in_chars):
        """Override base class ContentHandler method"""
        self.char_buffer.append(in_chars)

    def endDocument(self):
        """Override base class ContentHandler method"""
        self.return_q.put(self.obj_depth[-1])

def obj_wrapper(xml_stream):
    """Call the handler against the XML, then get the returned object and pass it back up"""
    try:
        return_q = Queue.Queue()
        xml.sax.parseString(xml_stream, NodeHandler(return_q))
        return (True, return_q.get())
    except Exception, e:
        return (False, (Exception, e))


