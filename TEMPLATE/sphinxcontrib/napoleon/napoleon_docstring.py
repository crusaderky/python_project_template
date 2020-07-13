# -*- coding: utf-8 -*-
"""
    sphinxcontrib.napoleon.docstring
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Classes for docstring parsing and formatting.
    :copyright: Copyright 2013-2018 by Rob Ruana, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import inspect
import re
from collections import Callable
from functools import partial

from six import string_types, u
from six.moves import range

from pockets import modify_iter, UnicodeMixin
from sphinxcontrib.napoleon._upstream import _

if False:
    # For type annotation
    from typing import Any, Dict, List, Tuple, Type, Union  # NOQA
    from sphinx.application import Sphinx  # NOQA
    from sphinx.config import Config as SphinxConfig  # NOQA


_directive_regex = re.compile(r'\.\. \S+::')
_google_section_regex = re.compile(r'^(\s|\w)+:\s*$')
_google_typed_arg_regex = re.compile(r'\s*(.+?)\s*\(\s*(.*[^\s]+)\s*\)')
_numpy_section_regex = re.compile(r'^[=\-`:\'"~^_*+#<>]{2,}\s*$')
_single_colon_regex = re.compile(r'(?<!:):(?!:)')
_xref_regex = re.compile(r'(:(?:[a-zA-Z0-9]+[\-_+:.])*[a-zA-Z0-9]+:`.+?`)')
_bullet_list_regex = re.compile(r'^(\*|\+|\-)(\s+\S|\s*$)')
_enumerated_list_regex = re.compile(
    r'^(?P<paren>\()?'
    r'(\d+|#|[ivxlcdm]+|[IVXLCDM]+|[a-zA-Z])'
    r'(?(paren)\)|\.)(\s+\S|\s*$)')


class NumpyDocstring(UnicodeMixin):
    """Convert NumPy style docstrings to reStructuredText.
    Parameters
    ----------
    docstring : :obj:`str` or :obj:`list` of :obj:`str`
        The docstring to parse, given either as a string or split into
        individual lines.
    config: :obj:`sphinxcontrib.napoleon.Config` or :obj:`sphinx.config.Config`
        The configuration settings to use. If not given, defaults to the
        config object on `app`; or if `app` is not given defaults to the
        a new :class:`sphinxcontrib.napoleon.Config` object.
    Other Parameters
    ----------------
    app : :class:`sphinx.application.Sphinx`, optional
        Application object representing the Sphinx process.
    what : :obj:`str`, optional
        A string specifying the type of the object to which the docstring
        belongs. Valid values: "module", "class", "exception", "function",
        "method", "attribute".
    name : :obj:`str`, optional
        The fully qualified name of the object.
    obj : module, class, exception, function, method, or attribute
        The object to which the docstring belongs.
    options : :class:`sphinx.ext.autodoc.Options`, optional
        The options given to the directive: an object with attributes
        inherited_members, undoc_members, show_inheritance and noindex that
        are True if the flag option of same name was given to the auto
        directive.
    Example
    -------
    >>> from sphinxcontrib.napoleon import Config
    >>> config = Config(napoleon_use_param=True, napoleon_use_rtype=True)
    >>> docstring = '''One line summary.
    ...
    ... Extended description.
    ...
    ... Parameters
    ... ----------
    ... arg1 : int
    ...     Description of `arg1`
    ... arg2 : str
    ...     Description of `arg2`
    ... Returns
    ... -------
    ... str
    ...     Description of return value.
    ... '''
    >>> print(NumpyDocstring(docstring, config))
    One line summary.
    <BLANKLINE>
    Extended description.
    <BLANKLINE>
    :param arg1: Description of `arg1`
    :type arg1: int
    :param arg2: Description of `arg2`
    :type arg2: str
    <BLANKLINE>
    :returns: Description of return value.
    :rtype: str
    <BLANKLINE>
    Methods
    -------
    __str__()
        Return the parsed docstring in reStructuredText format.
        Returns
        -------
        str
            UTF-8 encoded version of the docstring.
    __unicode__()
        Return the parsed docstring in reStructuredText format.
        Returns
        -------
        unicode
            Unicode version of the docstring.
    lines()
        Return the parsed lines of the docstring in reStructuredText format.
        Returns
        -------
        list(str)
            The lines of the docstring in a list.
    """
    def __init__(self, docstring, config=None, app=None, what='', name='',
                 obj=None, options=None):
        # type: (Union[unicode, List[unicode]], SphinxConfig, Sphinx, unicode, unicode, Any, Any) -> None  # NOQA
        self._directive_sections = ['.. index::']
        super(NumpyDocstring, self).__init__(docstring, config, app, what,
                                             name, obj, options)

    def _consume_field(self, parse_type=True, prefer_type=False):
        # type: (bool, bool) -> Tuple[unicode, unicode, List[unicode]]
        line = next(self._line_iter)
        if parse_type:
            _name, _, _type = self._partition_field_on_colon(line)
        else:
            _name, _type = line, ''
        _name, _type = _name.strip(), _type.strip()
        _name = self._escape_args_and_kwargs(_name)

        if prefer_type and not _type:
            _type, _name = _name, _type
        indent = self._get_indent(line) + 1
        _desc = self._dedent(self._consume_indented_block(indent))
        _desc = self.__class__(_desc, self._config).lines()
        return _name, _type, _desc

    def _consume_returns_section(self):
        # type: () -> List[Tuple[unicode, unicode, List[unicode]]]
        return self._consume_fields(prefer_type=True)

    def _consume_section_header(self):
        # type: () -> unicode
        section = next(self._line_iter)
        if not _directive_regex.match(section):
            # Consume the header underline
            next(self._line_iter)
        return section

    def _is_section_break(self):
        # type: () -> bool
        line1, line2 = self._line_iter.peek(2)
        return (not self._line_iter.has_next() or
                self._is_section_header() or
                ['', ''] == [line1, line2] or
                (self._is_in_section and
                    line1 and
                    not self._is_indented(line1, self._section_indent)))

    def _is_section_header(self):
        # type: () -> bool
        section, underline = self._line_iter.peek(2)
        section = section.lower()
        if section in self._sections and isinstance(underline, string_types):
            return bool(_numpy_section_regex.match(underline))  # type: ignore
        elif self._directive_sections:
            if _directive_regex.match(section):
                for directive_section in self._directive_sections:
                    if section.startswith(directive_section):
                        return True
        return False

    def _parse_see_also_section(self, section):
        # type: (unicode) -> List[unicode]
        lines = self._consume_to_next_section()
        try:
            return self._parse_numpydoc_see_also_section(lines)
        except ValueError:
            return self._format_admonition('seealso', lines)

    def _parse_numpydoc_see_also_section(self, content):
        # type: (List[unicode]) -> List[unicode]
        """
        Derived from the NumpyDoc implementation of _parse_see_also.
        See Also
        --------
        func_name : Descriptive text
            continued text
        another_func_name : Descriptive text
        func_name1, func_name2, :meth:`func_name`, func_name3
        """
        items = []

        def parse_item_name(text):
            # type: (unicode) -> Tuple[unicode, unicode]
            """Match ':role:`name`' or 'name'"""
            m = self._name_rgx.match(text)  # type: ignore
            if m:
                g = m.groups()
                if g[1] is None:
                    return g[3], None
                else:
                    return g[2], g[1]
            raise ValueError("%s is not a item name" % text)

        def push_item(name, rest):
            # type: (unicode, List[unicode]) -> None
            if not name:
                return
            name, role = parse_item_name(name)
            items.append((name, list(rest), role))
            del rest[:]

        current_func = None
        rest = []  # type: List[unicode]

        for line in content:
            if not line.strip():
                continue

            m = self._name_rgx.match(line)  # type: ignore
            if m and line[m.end():].strip().startswith(':'):
                push_item(current_func, rest)
                current_func, line = line[:m.end()], line[m.end():]
                rest = [line.split(':', 1)[1].strip()]
                if not rest[0]:
                    rest = []
            elif not line.startswith(' '):
                push_item(current_func, rest)
                current_func = None
                if ',' in line:
                    for func in line.split(','):
                        if func.strip():
                            push_item(func, [])
                elif line.strip():
                    current_func = line
            elif current_func is not None:
                rest.append(line.strip())
        push_item(current_func, rest)

        if not items:
            return []

        roles = {
            'method': 'meth',
            'meth': 'meth',
            'function': 'func',
            'func': 'func',
            'class': 'class',
            'exception': 'exc',
            'exc': 'exc',
            'object': 'obj',
            'obj': 'obj',
            'module': 'mod',
            'mod': 'mod',
            'data': 'data',
            'constant': 'const',
            'const': 'const',
            'attribute': 'attr',
            'attr': 'attr'
        }  # type: Dict[unicode, unicode]
        if self._what is None:
            func_role = 'obj'  # type: unicode
        else:
            func_role = roles.get(self._what, '')
        lines = []  # type: List[unicode]
        last_had_desc = True
        for func, desc, role in items:
            if role:
                link = ':%s:`%s`' % (role, func)
            elif func_role:
                link = ':%s:`%s`' % (func_role, func)
            else:
                link = "`%s`_" % func
            if desc or last_had_desc:
                lines += ['']
                lines += [link]
            else:
                lines[-1] += ", %s" % link
            if desc:
                lines += self._indent([' '.join(desc)])
                last_had_desc = True
            else:
                last_had_desc = False
        lines += ['']

        return self._format_admonition('seealso', lines)