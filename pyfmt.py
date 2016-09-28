import pygments as p
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import IPython as ip
import IPython.core.magic as m

htmlFormatter = HtmlFormatter()

class LineSelection:
	def __init__(self, start, end):
		self.start = start
		self.end = end

	def select(self, lines):
		return lines[self.start:self.end]

	def __str__(self):
		return "Lines {}-{}".format(self.start+1, self.end)


class RegionSelection:
	def __init__(self, name):
		self.name = name

	def select(self, lines):
		selected = []
		in_region = False
		for line in lines:
			if line.startswith('#region'):
				rname = line[line.index(' ')+1:-1]
				if rname == self.name:
					in_region = True
			elif line.startswith('#endregion'):
				in_region = False
			elif in_region:
				selected.append(line)
		return selected

	def __str__(self):
		return "Region '{}'".format(self.name)



@m.register_line_magic
def pyfmt(line):
	"""
	reads peices of a given file and returns a syntax-
	highlighted, HTML version

	selection syntax:
		region: r<region-name>
		lines: l<start>:<end>

	usage:
		%pyfmt [<selection>[,...]] <file>
	"""

	# default state
	filename = line
	selections = [LineSelection(0, -1)]

	# read start/end if included
	split = line.split(' ')
	if len(split) > 1:
		filename = ' '.join(split[1:])

		# clear default
		selections = []

		# parse selection parameters
		selects = split[0].split(',')
		for sel in selects:
			if sel[0] == 'l':
				colon = sel.index(':')
				start = int(sel[1:colon])-1
				end = int(sel[colon+1:])
				selections.append(LineSelection(start, end))
			elif sel[0] == 'r':
				selections.append(RegionSelection(sel[1:]))

	# read the file
	lines = None
	with open(filename, 'r') as f:
		lines = f.readlines()

	# get requested input
	selected = []
	for selection in selections:
		if len(selections) > 1:
			selected.append('# {}:\n'.format(str(selection)))
		selected += selection.select(lines)

	# join selections
	src = ''.join(selected)

	# syntax highlight the code
	fmt = '<style type="text/css">{}</style>{}'
	html = fmt.format(
		htmlFormatter.get_style_defs('.highlight'),
		p.highlight(src, PythonLexer(), htmlFormatter)
	)

	# return an object to display
	return ip.display.HTML(html)
