# This file exists within 'dob-bright':
#
#   https://github.com/tallybark/dob-bright
#
# Copyright © 2019-2020 Landon Bouma. All rights reserved.
#
# This program is free software:  you can redistribute it  and/or  modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3  of the License,  or  (at your option)  any later version  (GPLv3+).
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY;  without even the implied warranty of MERCHANTABILITY or  FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU  General  Public  License  for  more  details.
#
# If you lost the GNU General Public License that ships with this software
# repository (read the 'LICENSE' file), see <http://www.gnu.org/licenses/>.

from gettext import gettext as _

import click_hotoffthehamster as click

from nark.helpers.format_text import format_value_truncate
from nark.helpers.objects import resolve_attr_or_method

from ..termio import dob_in_user_warning
from ..termio.style import stylize, verify_colors_attrs

__all__ = (
    'FactsDiff',
)


class FactsDiff(object):
    """"""
    def __init__(self, orig_fact, edit_fact, formatted=False):
        self.orig_fact = orig_fact
        self.edit_fact = edit_fact
        self.formatted = formatted
        self.include_newlines = False
        self.exclude_attrs = None

    def __str__(self):
        return 'FactsDiff:\n- orig: {}\n- edit: {}'.format(
            self.orig_fact.short, self.edit_fact.short,
        )

    # ***

    def friendly_diff(
        self,
        truncate=False,
        exclude=None,
        show_elapsed=False,
        show_midpoint=False,
        show_now=False,
    ):
        def _friendly_diff():
            self.include_newlines = True
            self.exclude_attrs = exclude

            result = '' if not self.formatted else []
            result = assemble_diff_attrs(result)

            self.include_newlines = False
            self.exclude_attrs = None

            if not self.formatted:
                result = result.rstrip()
            else:
                while (len(result) > 0) and (not result[-1][1].strip()):
                    result.pop()

            return result

        def assemble_diff_attrs(result):
            result += self.diff_line_assemble(
                None, self.time_humanize(show_now), 'interval',
            )
            if show_midpoint:
                result += self.diff_line_assemble(
                    None, self.time_midpoint(), 'midpoint',
                )
            if show_elapsed:
                self_val, other_val = self.diff_time_elapsed(show_now)
                result += self.diff_line_assemble(
                    self_val, other_val, 'duration',
                )
            result += self.diff_attrs('start_fmt_local', 'start')
            if not show_now:
                result += self.diff_attrs('end_fmt_local', 'end')
            else:
                result += self.diff_attrs('end_fmt_local_nowwed', 'end')
            if (not truncate) or self.orig_fact.pk or self.edit_fact.pk:
                result += self.diff_attrs('pk_str', 'id', beautify=self.beautify_pk)
            result += self.diff_attrs('deleted', 'deleted')
            # MAYBE?: (lb): Would we even want to show the split_from fact?
            #  result += self.diff_attrs('split_from', 'split_from')
            result += self.diff_attrs('activity_name', 'activity')
            result += self.diff_attrs('category_name', 'category')
            if not self.formatted:
                # For the command line, ANSI escape sequences.
                result += self.diff_attrs('oid_tags', 'tags', colorful=True)
            else:
                # For the interactive editor/Carousel, PTK style tuples.
                result += self.diff_attrs('tags_tuples', 'tags', colorful=True)
            result += self.diff_attrs('description', 'description', truncate=truncate)
            return result

        # ***

        return _friendly_diff()

    # ***

    def diff_attrs(
        self,
        prop,
        name=None,
        style_class='',
        truncate=False,
        beautify=None,
        mouse_handler=None,
        **kwargs
    ):
        if (self.exclude_attrs is not None) and (name in self.exclude_attrs):
            return ''
        self_val = resolve_attr_or_method(self.orig_fact, prop, **kwargs)
        other_val = ''
        if self.edit_fact is not None:
            other_val = resolve_attr_or_method(self.edit_fact, prop, **kwargs)
            if callable(other_val):
                other_val = other_val()
            self_val, other_val = self.diff_values_enhance(
                self_val,
                other_val,
                style_class=style_class,
                truncate=truncate,
                beautify=beautify,
                mouse_handler=mouse_handler,
            )
        elif truncate:
            self_val = self.format_value_truncate(self_val)
            self_val = self.format_prepare(
                self_val, style_class=style_class, mouse_handler=mouse_handler,
            )
            other_val = self.format_prepare(other_val, style_class=style_class)
        attr_diff = self.diff_line_assemble(self_val, other_val, name)
        return attr_diff

    def diff_line_assemble(self, self_val, other_val, name=None):
        prefix = self.diff_values_padded_prefix(name)
        if not self.formatted:
            return self.diff_line_inline_style(self_val, other_val, prefix)
        else:
            return self.diff_line_tuples_style(self_val, other_val, prefix)

    def diff_values_enhance(
        self,
        self_val,
        other_val,
        style_class='',
        truncate=False,
        beautify=None,
        mouse_handler=None,
    ):
        differ = False
        if self_val != other_val:
            differ = True
        if truncate:
            self_val = self.format_value_truncate(self_val)
            other_val = self.format_value_truncate(other_val)
        if beautify is not None:
            self_val, other_val = beautify(self_val, other_val)
            if self_val != other_val:
                differ = True
        if differ:
            self_val = self.format_edited_before(self_val, style_class)
            self_val, other_val = self.format_edited_after(
                self_val, other_val, style_class,
            )
        else:
            self_val = self.format_prepare(
                self_val, style_class=style_class, mouse_handler=mouse_handler,
            )
            other_val = self.format_prepare('', style_class=style_class)
        return (self_val, other_val)

    def format_prepare(self, some_val, style_class='', mouse_handler=None):
        if not self.formatted or not isinstance(some_val, str):
            # tags, e.g.,:
            #   [('fg: #C6C6C6 underline', '#'), ('fg: #D7FF87 underline', 'my-tag')]
            if (
                (mouse_handler is not None)
                and (isinstance(some_val, list))
                and (len(some_val) > 0)
                and (isinstance(some_val[0], tuple))
                and (len(some_val[0]) == 2)
            ):
                return [
                    (style_class + tup[0], tup[1], mouse_handler,) for tup in some_val
                ]
            return some_val
        if mouse_handler is None:
            return [(style_class, some_val)]
        return [(style_class, some_val, mouse_handler)]

    def format_value_truncate(self, val):
        # MAGIC_NUMBER: (lb): A third of the terminal (1 / 3.).
        # MAYBE/2019-02-15: Should have Carousel tells us width.
        term_width = click.get_terminal_size()[0]
        trunc_width = int(term_width * (1 / 3.))
        return format_value_truncate(val, trunc_width)

    # ***

    def diff_time_elapsed(self, show_now=False, style_class=''):
        self_val = self.time_elapsed(self.orig_fact, show_now)
        other_val = self.time_elapsed(self.edit_fact, show_now)
        if not self_val:
            # Make 'em the same, i.e., show no diff, no styling.
            self_val = other_val
        return self.diff_values_enhance(self_val, other_val, style_class=style_class)

    def time_elapsed(self, fact, show_now=False):
        # NOTE: start and/or end might be string; e.g., clock or rel. time.
        if (not fact.times_ok) and (not show_now):
            return None
        time_val = fact.format_delta(style='HHhMMm')
        return time_val

    def time_midpoint(self):
        return self.format_prepare(
            self.edit_fact.time_of_day_midpoint
        )

    def time_humanize(self, show_now=False):
        return self.format_prepare(
            self.edit_fact.time_of_day_humanize(show_now=show_now)
        )

    def beautify_pk(self, self_val, other_val):
        # (lb): NOTE: This is the only dirty_reasons usage in nark
        #               (most of its usage is in dob).
        # 'lsplit' and 'rsplit' are used by fix_times.resolve_overlapping.
        if 'lsplit' in self.edit_fact.dirty_reasons:
            other_val = 'New split fact, created before new fact'
        if 'rsplit' in self.edit_fact.dirty_reasons:
            other_val = 'New split fact, created after new fact'
        return (self_val, other_val)

    # ***

    FACTS_DIFF_STYLE = {}

    @classmethod
    def register_facts_diff_style(cls, facts_diff_style=None):
        """Registers a dictionary of style lists for FactsDiff methods.
        """
        for part, styles in facts_diff_style.items():
            if not part.endswith('-raw'):
                continue
            errs = ', '.join(verify_colors_attrs(*styles))
            if errs:
                emsg = _('Unknown colors or attrs for “{}”: {}').format(part, errs)
                dob_in_user_warning(emsg)
        # Nonetheless, can still use even if some/all unknown colors/attrs.
        cls.FACTS_DIFF_STYLE = facts_diff_style or {}

    @classmethod
    def fetch_style(cls, style_attr):
        try:
            return cls.FACTS_DIFF_STYLE[style_attr]
        except KeyError:
            if style_attr.endswith('-raw'):
                # Expect list of (color, *attrs) to pass to stylize()
                return []
            else:
                # Except ready-to-go PTK tuple style string.
                return ''

    # ***

    def format_edited_before(self, before_val, style_class):
        if not self.formatted:
            styles = FactsDiff.fetch_style('value-diff-old-raw')
            return styles and stylize(before_val, *styles) or before_val
        style = style_class
        style += FactsDiff.fetch_style('value-diff-old-ptk')
        before_parts = []
        if isinstance(before_val, str):
            before_parts += [(style, before_val)]
        elif before_val is not None:
            for tup in before_val:
                before_parts.append((style, tup[1]))
        return before_parts

    def format_edited_after(self, self_val, other_val, style_class):
        if not self.formatted:
            styles = FactsDiff.fetch_style('value-diff-new-raw')
            return '{} | was: '.format(
                styles and stylize(other_val, *styles) or other_val
            ), self_val
        style = style_class
        style += FactsDiff.fetch_style('value-diff-new-ptk')
        after_parts = []
        if isinstance(other_val, str):
            after_parts += [(style, other_val)]
        elif other_val is not None:
            for tup in other_val:
                after_parts.append((style, tup[1]))
        # (lb): Swap the order, for display purposes.
        #   (These formatting functions are so janky!)
        if self_val and self_val[0][1]:
            after_parts += [('italic', ' | was: ')]
        return after_parts, self_val

    # ***

    def diff_values_padded_prefix(self, name):
        if name is None:
            return ''
        prefix_prefix = '  '
        padded_prefix = '{}{:.<19} : '.format(prefix_prefix, name)
        return padded_prefix

    def diff_line_inline_style(self, self_val, other_val, prefix=''):
        format_inline = '{}{}{}'.format(prefix, self_val or '', other_val or '')
        format_inline += "\n" if self.include_newlines else ''
        return format_inline

    def diff_line_tuples_style(self, self_val, other_val, prefix='', style_class=''):
        format_tuples = []
        if prefix:
            format_tuples += [(style_class, prefix)]
        if self_val:
            format_tuples += self_val
        if other_val:
            format_tuples += other_val
        if self.include_newlines:
            format_tuples += [('', '\n')]
        return format_tuples

