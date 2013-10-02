# XML Parser/Data Access Object the_map.py
"""AUTO-GENERATED Source file for the_map.py"""
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

class event_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'building']
        Q2API.xml.base_xml.XMLNode.__init__(self, "event", attrs, None, [])

class exit_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'building']
        Q2API.xml.base_xml.XMLNode.__init__(self, "exit", attrs, None, [])

class item_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'player']
        Q2API.xml.base_xml.XMLNode.__init__(self, "item", attrs, None, [])

class monster_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'building']
        Q2API.xml.base_xml.XMLNode.__init__(self, "monster", attrs, None, [])

class monster_text_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'building']
        Q2API.xml.base_xml.XMLNode.__init__(self, "monster_text", attrs, None, [])

class room_name_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'building']
        Q2API.xml.base_xml.XMLNode.__init__(self, "room_name", attrs, None, [])

class text_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'intro']
        Q2API.xml.base_xml.XMLNode.__init__(self, "text", attrs, None, [])

class town_text_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'building']
        Q2API.xml.base_xml.XMLNode.__init__(self, "town_text", attrs, None, [])

class building_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 2
        self.path = [None, u'map']
        self.monster = []
        self.item = []
        self.monster_text = []
        self.text = []
        self.town_text = []
        self.room_name = []
        self.exit = []
        self.party = []
        self.event = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "building", attrs, None, [])

class intro_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 2
        self.path = [None, u'map']
        self.text = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "intro", attrs, None, [])

class party_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 2
        self.path = [None, u'map']
        Q2API.xml.base_xml.XMLNode.__init__(self, "party", attrs, None, [])

class player_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 2
        self.path = [None, u'map']
        self.item = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "player", attrs, None, [])

class map_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 1
        self.path = [None]
        self.building = []
        self.player = []
        self.intro = []
        self.party = []
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

        elif name == "monster":
            self.obj_depth.append(monster_q2class(p_attrs))

        elif name == "item":
            self.obj_depth.append(item_q2class(p_attrs))

        elif name == "monster_text":
            self.obj_depth.append(monster_text_q2class(p_attrs))

        elif name == "text":
            self.obj_depth.append(text_q2class(p_attrs))

        elif name == "town_text":
            self.obj_depth.append(town_text_q2class(p_attrs))

        elif name == "room_name":
            self.obj_depth.append(room_name_q2class(p_attrs))

        elif name == "player":
            self.obj_depth.append(player_q2class(p_attrs))

        elif name == "intro":
            self.obj_depth.append(intro_q2class(p_attrs))

        elif name == "exit":
            self.obj_depth.append(exit_q2class(p_attrs))

        elif name == "party":
            self.obj_depth.append(party_q2class(p_attrs))

        elif name == "event":
            self.obj_depth.append(event_q2class(p_attrs))

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

        elif name == "monster":
            self.obj_depth[-2].monster.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "item":
            self.obj_depth[-2].item.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "monster_text":
            self.obj_depth[-2].monster_text.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "text":
            self.obj_depth[-2].text.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "town_text":
            self.obj_depth[-2].town_text.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "room_name":
            self.obj_depth[-2].room_name.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "player":
            self.obj_depth[-2].player.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "intro":
            self.obj_depth[-2].intro.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "exit":
            self.obj_depth[-2].exit.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "party":
            self.obj_depth[-2].party.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "event":
            self.obj_depth[-2].event.append(self.obj_depth[-1]) #  make this object a child of the next object up...
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


