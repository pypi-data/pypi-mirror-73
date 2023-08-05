#
# remt - reMarkable tablet command-line tools
#
# Copyright (C) 2018-2020 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import cairo
import typing as tp
from collections import namedtuple

Page = namedtuple('Page', ['number'])
PageEnd = namedtuple('PageEnd', ['number'])

Layer = namedtuple('Layer', ['number'])
Stroke = namedtuple(
    'Stroke',
    ['number', 'pen', 'color', 'width', 'segments']
)
Segment = namedtuple(
    'Segment',
    ['number', 'x', 'y', 'speed', 'direction', 'width', 'pressure'],
)

class Color(tp.NamedTuple):
    red: float
    green: float
    blue: float
    alpha: float

class Style(tp.NamedTuple):
    tool_line: tp.Callable
    color: Color
    join: cairo.LineJoin
    cap: cairo.LineCap
    dash: tp.List[int] = []
    brush: tp.Optional[str] = None

Context = namedtuple(
    'Context',
    ['cr_surface', 'cr_ctx', 'pdf_doc', 'page_number']
)

# vim: sw=4:et:ai
