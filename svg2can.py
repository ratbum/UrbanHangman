import xml.etree.ElementTree as ET

class SvgPathNode:
	
	def __init__(self, nodeType='M', x=0.0, y=0.0):
		self.nodeType = nodeType
		self.x = x
		self.y = y
		
	def __repr__(self):
		return 'SvgPathNode(type={}, x={}, y={})'.format(self.nodeType, self.x, self.y)
	
SvgPathNode.PATH_NODE_TYPES = ['M', 'L', 'H', 'V', 'C', 'S', 'Q', 'T', 'A', 'Z']

class SvgPath:
	def __init__(self, strPath=''):
		self.nodeList = []
		if strPath != None and len(strPath) > 0:
			pieces = strPath.split()
			self.add_nodes_from_string_pieces(pieces)
			
	
	def add_nodes_from_string_pieces(self, strNode, startPoint=0):
		nodeType = strNode[startPoint]
		if(not nodeType in SvgPathNode.PATH_NODE_TYPES):
			raise Exception('Invalid Path Node Type', 'Must be one of ' + str(SvgPathNode.PATH_NODE_TYPES))
			
		if (nodeType == 'Z'):
			self.nodeList.append(SvgPathNode(nodeType, None, None))
			return True
			
		if startPoint+2 > len(strNode):
			raise Exception('Must have coordinates', '')
		
		x = float(strNode[startPoint + 1])
		y = float(strNode[startPoint + 2])
		
		self.nodeList.append(SvgPathNode(nodeType, x, y))
		self.add_nodes_from_string_pieces(strNode, startPoint + 3)
			
	
	def add_node(self, node):
		if type(node) is SvgPathNode:
			self.nodeList.append(node)
		else:
			raise Exception('Invalid argument', 'node must be SvgPathNode')
			
	@property
	def nodes(self):
		return self.nodeList
			

class Svg2Can:
	
	def __init__(self):
		self.min_x = 0
		self.min_y = 0

	def clean_tag(self, tag):
		# Why is this here?
		return tag.replace('{http://www.w3.org/2000/svg}', '')
	
	def is_el_drawable(self, el):
		return self.clean_tag(el.tag) in Svg2Can.DRAWABLE_ELEMENTS
	
	def is_el_container(self, el):
		return self.clean_tag(el.tag) in Svg2Can.CONTAINER_ELEMENTS
	
	def draw_el(self, canvas, el):
		if (self.clean_tag(el.tag) == 'rect'):
			self.draw_rect(canvas, el)
		if (self.clean_tag(el.tag) == 'path'):
			self.draw_path(canvas, el)
		if (self.clean_tag(el.tag) == 'ellipse'):
			self.draw_ellipse(canvas, el)
	
	def draw_path(self, canvas, el):
		if (el.get('fill') == None):
			return

		path = SvgPath(el.get('d'))
		
		coordinates = []
		for node in path.nodes:
			if (node.nodeType == 'Z'):
				break
			coordinates.append(node.x - self.min_x)
			coordinates.append(node.y - self.min_y)
			
		fillColour = el.get('fill')
		
		canvas.create_polygon(coordinates, fill=fillColour)
		
	def draw_rect(self, canvas, el):
		if (el.get('fill') == None):
			return
		x1 = float(el.get('x')) - self.min_x
		y1 = float(el.get('y')) - self.min_y
		width = float(el.get('width'))
		height = float(el.get('height'))
		x2 = x1 + width
		y2 = y1 + height
		fillColour = el.get('fill')
		canvas.create_rectangle(x1, y1, x2, y2, fill=fillColour, width=el.get('stroke-width'))
		
	def draw_ellipse(self, canvas, el):
		if (el.get('fill') == None):
			return
		radius_x = float(el.get('rx'))
		radius_y = float(el.get('ry'))
			
		x1 = float(el.get('cx')) - self.min_x - radius_x
		y1 = float(el.get('cy')) - self.min_y - radius_y
		
		x2 = x1 + radius_x * 2
		y2 = y1 + radius_y * 2
		
		fillColour = el.get('fill')
		
		canvas.create_oval(x1, y1, x2, y2, fill=fillColour)
		
		
	def draw_children(self, canvas, el):
		for child in el:
			if self.is_el_drawable(child):
				self.draw_el(canvas, child)
			if self.is_el_container(child):
				self.draw_children(canvas, child)
				

	def draw_svg_from_file_on_canvas(self, canvas, svg_file_path):
		svg = ET.parse(svg_file_path)
		root = svg.getroot()
		self.min_x = float(root.get('viewBox').split()[0])
		self.min_y = float(root.get('viewBox').split()[1])
		self.draw_children(canvas, root)
	
	
	
Svg2Can.DRAWABLE_ELEMENTS = [
	'rect',
	'path',
	'ellipse'
	# This is incomplete; does what I need to for the time being 
]

Svg2Can.CONTAINER_ELEMENTS = [
	'a',
	'defs',
	'glyph',
	'g',
	'marker',
	'mask',
	'missing-glyph',
	'pattern',
	'svg',
	'switch',
	'symbol'
]
