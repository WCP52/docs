#!/usr/bin/env python3

# Gantt-chart rendering script
# Reads a YAML schedule description, parses it and outputs a chart.

# Chris Pavlina, 2015
# cpavlin1@binghamton.edu
# Public domain, or whatever license you like better. Just don't blame me if
# it's terrible.

import calendar
import yaml
import datetime
import dateutil.parser

def indent_str (s, numspaces):
    lines = s.split ('\n')
    return '\n'.join ((' ' * numspaces) + i for i in lines)

class ScheduleItem (object):
    def __init__ (self):
        raise NotImplementedError

    def get_name (self):
        """Return the descriptive name of the item"""
        raise NotImplementedError

    def get_id (self):
        """Return the identifier of the item"""
        raise NotImplementedError

    def get_start (self):
        """Return the start time of the item, as a `datetime` object"""
        raise NotImplementedError

    def get_end (self):
        """Return the end time of the item, as a `datetime` object"""
        raise NotImplementedError

    def get_progress (self):
        """Return the progress of the item, as a float out of 100"""
        raise NotImplementedError

    def resolve_dates (self, all_items):
        """Resolve all internally referenced dates. This function may need to
        be run multiple times to resolve all references; it returns the number
        of references resolved to permit stopping at zero.
        
        Should be passed a list containing all schedule items to allow
        resolution.
        """
        raise NotImplementedError

    def str_self (self):
        """Return a prettyprinted representation of self."""
        raise NotImplementedError

    def output_bars (self, outfile, options):
        """Output the ganttbars for this item."""
        raise NotImplementedError
        

class ScheduleParent (object):
    """This is a schedule item which is not a task in and of itself, but which
    contains other tasks."""

    def __init__ (self, tree):
        """Parse a ScheduleParent from its section of the YAML tree."""
        
        self.name = tree['name']
        if 'id' in tree:
            self.id_ = tree['id']
        else:
            self.id_ = self.name
        self.children = []
        for i in tree['items']:
            self.children.append(ParseScheduleItem(i))

        self.resolved = False

    def get_name (self):
        return self.name

    def get_id (self):
        return self.id_

    def get_start (self):
        return self.children[0].get_start ()

    def get_end (self):
        return self.children[-1].get_end ()

    def get_progress (self):
        # Add up childrens' progresses
        return sum (i.get_progress () for i in self.children) / (len (self.children))
    
    def resolve_dates (self, all_items):
        if self.resolved:
            return 0
        total_resolved = sum(i.resolve_dates(all_items) for i in self.children)
        if total_resolved == 0:
            self.resolved = True
        return total_resolved

    def str_self (self):
        s = self.name + '\n'
        # Get all children, then indent them
        children_strings = [i.str_self () for i in self.children]
        children_strings_indented = [indent_str (i, 4) for i in children_strings]
        for i in children_strings_indented:
            # Replace the first two spaces with ' -'
            i_dash = ' -' + i[2:]
            s += i_dash
        s += '\n'
        return s

    def outputbars (self, outfile, options):
        print (r"\ganttgroup[progress=%d]{%s}{%s}{%s}\\" % (
            self.get_progress (),
            self.name, self.get_start ().date ().isoformat (),
            self.get_end ().date ().isoformat ()), file=outfile)
        for i in self.children:
            i.outputbars (outfile, options)

class ScheduleTask (object):
    """This is a basic scheduled task."""

    def __init__ (self, tree):
        """Parse a ScheduleTask from its section of the YAML tree."""

        self.name = tree['name']
        if 'id' in tree:
            self.id_ = tree['id']
        else:
            self.id_ = self.name
        if 'start' in tree:
            self.start = str(tree['start'])
        else:
            self.start = 'after !preceding'

        if 'end' in tree:
            self.end = str(tree['end'])
        else:
            self.end = 'dur 0'

        if 'prog' in tree:
            self.progress = float (tree['prog'])
        else:
            self.progress = 0.0

        self.resolved = False
        
    def get_name (self):
        return self.name

    def get_id (self):
        return self.id_

    def get_start (self):
        return self.start_date

    def get_end (self):
        return self.end_date

    def get_progress (self):
        return self.progress

    def resolve_dates (self, all_items):
        # We must now resolve the date for the item. Allowed syntax:
        #  ISO8601. We detect this as anything starting with a digit. 
        #  after $item. Task begins the day after $item ends
        #  imm-after $item. Task begins the day $item ends
        #  
        # after and imm-after accept !preceding, which is the last task
        # mentioned. This is only valid if they are not the first item
        # in a list.
        #
        # end also accepts 'dur N', which is N days after start.

        if self.resolved:
            return 0

        if self.start[0].isdigit():
            self.start_date = dateutil.parser.parse (self.start)
        
        elif self.start.startswith ("after ") or self.start.startswith ("imm-after "):
            key, delim, value = self.start.partition (' ')
            if value == "!preceding":
                startafter = get_preceding (all_items, self)
            else:
                startafter = get_item (all_items, value)
            if startafter.resolved:
                if key == "after":
                    self.start_date = startafter.get_end () + datetime.timedelta (days = 1)
                else:
                    self.start_date = startafter.get_end ()
            else:
                return 1

        else:
            raise Exception ("Invalid start-date spec '%s'" % self.start)

        if self.end[0].isdigit ():
            self.end_date = dateutil.parser.parse (self.end)

        elif self.end.startswith ("dur "):
            end = self.end.split ()
            dur = int (end[1])
            self.end_date = self.start_date + datetime.timedelta (days = dur)

        else:
            raise Exception ("Invalid end-date spec '%s'" % self.end)

        self.resolved = True
        return 1

    def str_self (self):
        s = self.name + '\n'
        s += '  Start: '
        if self.resolved:
            s += str (self.start_date)
        else:
            s += '<not resolved>'
        s += '\n'
        s += '  End: '
        if self.resolved:
            s += str (self.end_date)
        else:
            s += '<not resolved>'
        s += '\n'
        return s

    def outputbars (self, outfile, options):

        # Individual tasks don't go in 'options'
        if 'simplified' in options:
            return

        start = self.get_start ().date ()
        end = self.get_end ().date ()
        is_milestone = (end-start).days < 1

        if is_milestone:
            print (r"\ganttmilestone[progress=%d]{%s}{%s}\\" % (
                self.progress, self.name, start))
        else:
            print (r"\ganttbar[progress=%d]{%s}{%s}{%s}\\" % (
                self.progress,
                self.name, self.get_start ().date ().isoformat (),
                self.get_end ().date ().isoformat ()), file=outfile)

def ParseScheduleItem (tree):
    if 'items' in tree:
        return ScheduleParent (tree)
    else:
        return ScheduleTask (tree)

def get_preceding (all_items, item, firstcall=True):
    # Go through all items, find the one that comes before 'item'
    item_at = 0
    for i in range (len (all_items)):
        i_item = all_items[i]
        if i_item is item:
            item_at = i
            break
        if hasattr (i_item, 'children'):
            try_to_find = get_preceding (i_item.children, item, firstcall=False)
            if try_to_find is not None:
                return try_to_find
    if item_at > 0:
        prec = all_items[item_at - 1]
        return prec
    else:
        if firstcall:
            raise Exception ("Could not find preceding item for '%s'" % item.get_name ())
        else:
            return None

def get_item (all_items, item, firstcall=True):
    # Go through all items, find one by ID
    for i in all_items:
        if i.get_id () == item:
            return i
        if hasattr (i, 'children'):
            try_to_find = get_item (i.children, item, firstcall=False)
            if try_to_find is not None:
                return try_to_find
    if firstcall:
        raise Exception ("Could not find named item '%s'" % item)
    else:
        return None

def get_date_span(items):
    # Return (earliest, latest)
    date_earliest = None
    date_latest = None
    for i in items:
        start = i.get_start ()
        end = i.get_end ()
        if date_earliest is None or start < date_earliest:
            date_earliest = start
        if date_latest is None or end > date_latest:
            date_latest = end
    return date_earliest, date_latest

def output_gantttitles(items, outfile=None):
    # Output the \gantttitle lines for pgfgantt document

    date_earliest, date_latest = get_date_span (items)
    # From date_earliest to date_latest, generate months
    y = date_earliest.year
    m = date_earliest.month
    y_end = date_latest.year
    m_end = date_latest.month

    months = []
    while True:
        months.append ((y, m))
        m += 1
        if (12*m + y) > (12*m_end + y_end):
            break
        if m > 12:
            m = 1
            y += 1

    # Output month lines
    for y, m in months:
        # Get length of month - this will correspond to width in the chart
        month_len = calendar.monthrange (y, m)[1]
        print ("\\gantttitle{%d--%02d}{%d}" % (y, m, month_len), file=outfile)
    print ("\\\\", file=outfile)

TEX_HEAD=r"""
\documentclass{article}
\usepackage[usenames,dvipsnames,svgnames]{xcolor}
\usepackage{pgfgantt}
\usepackage[letterpaper,margin=0.1in]{geometry}
\begin{document}
\pagenumbering{gobble}
\renewcommand*{\familydefault}{\sfdefault}
\begin{figure}[ftbp]
\begin{center}
\begin{ganttchart}[time slot format=isodate,
    x unit=2mm,
    y unit chart=5mm,
    bar height=0.3,
    vgrid, hgrid,
    bar/.append style={draw=none, fill=OliveGreen!75},
    bar incomplete/.append style={fill=Maroon}]"""

TEX_FOOT=r"""
\end{ganttchart}
\end{center}
\end{figure}
\end{document}
"""

def output_gantttex(items, options, outfile=None):

    # Get the number of days
    date_earliest, date_latest = get_date_span (items)

    # First, output header
    print (TEX_HEAD + "{%s}{%s}" % (date_earliest.date().isoformat(),
            date_latest.date().isoformat()), file=outfile)

    # Titles
    print (r"\gantttitlecalendar{year, month=name}\\", file=outfile)
    #output_gantttitles (items, options)

    for i in items:
        i.outputbars (outfile, options)

    # Output footer
    print (TEX_FOOT, file=outfile)

if __name__ == '__main__':
    import sys
    with open (sys.argv[1]) as f:
        tree = yaml.load (f)

    assert tree['magic'] == 'gantt'
    # print (tree['name'])


    items = []
    for i in tree['items']:
        items.append (ParseScheduleItem (i))

    fail_resolve = 0
    while fail_resolve < 3:
        num_resolved = 0
        for i in items:
            num_resolved += i.resolve_dates (items)
        if num_resolved:
            fail_resolve = 0
        else:
            fail_resolve += 1

    opts = []
    if "simplified" in sys.argv[2:]:
        opts.append ("simplified")

    output_gantttex (items, opts)
