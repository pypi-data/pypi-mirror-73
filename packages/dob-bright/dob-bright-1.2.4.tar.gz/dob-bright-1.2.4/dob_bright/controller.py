# This file exists within 'dob-bright':
#
#   https://github.com/tallybark/dob-bright
#
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
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

"""The Controller."""

import inspect
import logging
import os
import sys

from gettext import gettext as _

from nark.control import NarkControl
from nark.helpers import logging as logging_helpers
from nark.items.fact import Fact

from . import __arg0name__
from . import help_newbs as help_strings
from .config.urable import ConfigUrable
from .termio.echoes import click_echo, highlight_value
from .termio.errors import dob_in_user_exit, dob_in_user_warning
from .termio.style import disable_colors, enable_colors

__all__ = (
    'Controller',
)


# ***
# *** [CONTROLLER] NarkControl Controller.
# ***

class Controller(NarkControl):
    """
    A custom controller that adds config handling on top of its regular functionality.
    """

    POST_PROCESSORS = []

    def __init__(self, config=None):
        super(Controller, self).__init__(config)
        self.configurable = None
        self.configfile_path = None
        self.config_keyvals = None
        self.arg0name = __arg0name__

    @property
    def now(self):
        return self.store.now

    def now_refresh(self):
        return self.store.now_refresh()

    @property
    def data_store_exists_at(self):
        return _(
            'Data store already exists at {}'
        ).format(self.config['db.path'])

    @property
    def data_store_url(self):
        return self.store.db_url

    @property
    def sqlite_db_path(self):
        if self.config['db.engine'] == 'sqlite':
            return self.config['db.path']
        else:
            # (lb): I don't super-like this. It's a weird side effect.
            #   And it's knowledgeable about the CLI command API. Meh.
            dob_in_user_exit(_(
                'Not a SQLite database. Try `{} store url`'
            ).format(self.arg0name))

    @property
    def is_germinated(self):
        if (
            (
                self.configurable.cfgfile_exists
                and self.configurable.cfgfile_sanity
            )
            and self.store_exists
        ):
            return True
        return False

    @property
    def store_exists(self):
        # Check either db.path is set, or all of db.host/port/name/user.
        if self.config['db.engine'] == 'sqlite':
            if self.config['db.path'] == ':memory:':
                return True
            return os.path.isfile(self.config['db.path'])
        else:
            # NOTE: db_url is an attribute of SQLAlchemyStore, not BaseStore.
            return bool(self.store.db_url)

    def standup_store(self, fact_cls=Fact):
        self.store.fact_cls = fact_cls
        return super(Controller, self).standup_store()

    def insist_germinated(self, fact_cls=Fact):
        """Assist user if config or database not present."""
        def _insist_germinated():
            if self.is_germinated:
                self.standup_store(fact_cls)
                return
            if not self.configurable.cfgfile_exists and not self.store_exists:
                help_newbie_onboard()
            else:
                berate_user_files_unwell()
            sys.exit(1)

        def help_newbie_onboard():
            message = help_strings.NEWBIE_HELP_ONBOARDING(self.ctx)
            click_echo(inspect.cleandoc(message), err=True)

        def berate_user_files_unwell():
            if not self.configurable.cfgfile_exists:
                oblige_user_create_config()
            if not self.configurable.cfgfile_sanity:
                oblige_user_repair_config()
            if not self.store_exists:
                oblige_user_create_store()

        def oblige_user_create_config():
            cfg_path = self.configurable.config_path
            message = help_strings.NEWBIE_HELP_CREATE_CONFIG(self.ctx, cfg_path)
            click_echo(inspect.cleandoc(message), err=True)

        def oblige_user_repair_config():
            cfg_path = self.configurable.config_path
            message = help_strings.NEWBIE_HELP_REPAIR_CONFIG(self.ctx, cfg_path)
            click_echo(inspect.cleandoc(message), err=True)

        def oblige_user_create_store():
            message = help_strings.NEWBIE_HELP_CREATE_STORE(
                self.ctx,
                db_path=self.config['db.path'],
                val_source=self.config.asobj.db.path.source,
            )
            click_echo(inspect.cleandoc(message), err=True)

        _insist_germinated()

    # ***

    def ensure_config(self, ctx, configfile_path=None, *keyvals):
        if self.configurable is not None:
            return
        # NOTE: This ctx.command.name == 'run', i.e., not the same context
        # passed to the Click command handlers. See: pass_context_wrap.
        self.ctx = ctx
        self.configfile_path = configfile_path
        self.config_keyvals = keyvals
        self.setup_config(configfile_path, *keyvals)
        self.wire_configience()

    def setup_config(self, configfile_path=None, *keyvals):
        self.configurable = self.setup_config_from_file_and_cli(
            configfile_path=configfile_path, *keyvals,
        )

    def setup_config_from_file_and_cli(self, configfile_path=None, *keyvals):
        configurable = ConfigUrable()
        configurable.load_config(configfile_path)
        configurable.inject_from_cli(*keyvals)
        return configurable

    def replay_config(self):
        # Called by ensure_plugged_in after loading plugin config.
        # NOTE: This'll re-print any errors messages from the first setup_config.
        #       Except that color will not have been set the first time, so errors
        #       before will be plain; and errors reprinted here will be colorful.
        self.setup_config(self.configfile_path, *self.config_keyvals)

    def create_config(self, force):
        self.configurable.create_config(force=force)
        self.wire_configience()

    def round_out_config(self):
        self.configurable.round_out_config()

    def write_config(self, skip_unset=False):
        self.configurable.write_config(skip_unset=skip_unset)

    def wire_configience(self, config_root=None):
        self.config = config_root or self.configurable.config_root
        self.capture_config_lib(self.config)
        self._adjust_log_level()

    def _adjust_log_level(self):
        # *cough*hack!*cough*”
        # Because invoke_without_command, we allow command-less invocations.
        #   For one such invocation -- dob -v -- tell the store not to log.
        # Also tell the store not to log if user did not specify anything,
        #   because we'll show the help/usage (which Click would normally
        #   handle if we had not tampered with invoke_without_command).
        if (
            (len(sys.argv) > 2)
            or (
                (len(sys.argv) == 2)
                and (sys.argv[1] not in ('-v', 'version'))
            )
        ):
            return
        # FIXME/EXPLAIN/2019-01-22: (lb): What about other 2 loggers?
        #   dev.cli_log_level
        #   dev.lib_log_level
        # (lb): Normally I'd prefer the []-lookup vs. attr., e.g., not:
        #   self.config.asobj.dev.sql_log_level.value_from_forced = 'WARNING'
        # because the self.config has non-key-val attributes (like
        # setdefault) so I think for clarity we should lookup via [].
        # Except the []-lookup returns the value, not the keyval object.
        # So here we have to use dotted attribute notation.
        self.config.asobj.dev.sql_log_level.value_from_forced = 'WARNING'

    # ***

    def create_data_store(self, force, fact_cls=Fact):
        skip_standup = self.check_sqlite_store_ready()
        if skip_standup:
            if force:
                self._reset_data_store()
                unlinked_db = True
            else:
                dob_in_user_exit(self.data_store_exists_at)
        self._standup_and_version_store(fact_cls)
        if unlinked_db:
            self._announce_recreated_store()

    def create_config_and_store(self, fact_cls=Fact):
        def _create_config_and_store():
            if not self.is_germinated:
                germinate_config_and_store()
            else:
                exit_already_germinated()

        def germinate_config_and_store():
            create_config_maybe()
            create_store_maybe()

        def create_config_maybe():
            cfg_path = self.configurable.config_path
            if not os.path.exists(cfg_path):
                self.create_config(force=False)
            else:
                click_echo(
                    _('Configuration already exists at {}').format(
                        highlight_value(cfg_path),
                    )
                )

        def create_store_maybe():
            # MEH: (lb): If the engine is not SQLite, this function cannot behave
            # like create_config_maybe, which tells the user if the things exists
            # already, because the storage class, SQLAlchemyStore, blindly calls
            # create_all (in create_storage_tables) without checking if db exists.
            skip_standup = self.check_sqlite_store_ready()
            if skip_standup:
                click_echo(self.data_store_exists_at)
            else:
                self._standup_and_version_store(fact_cls)

        def exit_already_germinated():
            dob_in_user_exit(_(
                'Dob is already setup. Run `{} details` for info.'
            ).format(self.arg0name))

        _create_config_and_store()

    def check_sqlite_store_ready(self):
        if self.config['db.engine'] != 'sqlite':
            return None
        db_path = self.config['db.path']
        if not os.path.isfile(db_path):
            return False
        return True

    def _reset_data_store(self):
        if self.config['db.engine'] != 'sqlite':
            # raise NotImplementedError
            dob_in_user_exit(_(
                'FIXME: Reset non-SQLite data store not supported (yet).'
            ))
        else:
            self.must_unlink_db_path(force=True)

    def must_unlink_db_path(self, *_args, force):
        db_path = self.config['db.path']
        if not os.path.exists(db_path):
            return
        if not os.path.isfile(db_path):
            dob_in_user_exit(_(
                'Data store exists but is not a file, so not overwriting {}'
            ).format(db_path))
        if not force:
            dob_in_user_exit(self.data_store_exists_at)
        os.unlink(db_path)

    def _announce_recreated_store(self):
        click_echo(
            _('Recreated data store at {}')
            .format(highlight_value(self.config['db.path']))
        )

    def _standup_and_version_store(self, fact_cls):
        created_fresh = self.standup_store(fact_cls)
        if created_fresh:
            verb = _('created')
        else:
            verb = _('already ready')
        click_echo(
            _('Dob database {verb} at {url}').format(
                verb=verb, url=highlight_value(self.store.db_url),
            )
        )

    @staticmethod
    def post_processor(func):
        Controller.POST_PROCESSORS.append(func)

    @staticmethod
    def _post_process(
        ctx,
        controller,
        fact_facts_or_true,
        show_plugin_error=None,
        carousel_active=False,
    ):
        # facts_or_true is one of:
        # - The saved/edited Fact;
        # - a list of Facts;
        # - or True, on upgrade-legacy.
        for handler in Controller.POST_PROCESSORS:
            handler(
                ctx,
                controller,
                fact_facts_or_true,
                show_plugin_error=show_plugin_error,
                carousel_active=carousel_active,
            )

    def post_process(
        self,
        controller,
        fact_facts_or_true,
        show_plugin_error=None,
        carousel_active=False,
    ):
        Controller._post_process(
            self.ctx,
            controller,
            fact_facts_or_true,
            show_plugin_error=show_plugin_error,
            carousel_active=carousel_active,
        )

    def setup_tty_color(self, use_color):
        if use_color is None:
            use_color = self.config['term.use_color']
        else:
            self.config['term.use_color'] = use_color
        if use_color:
            enable_colors()
        else:
            disable_colors()

    # ***

    def setup_logging(self, verbose=False, verboser=False):
        """Setup logging for the lib_logger as well as client specific logging."""
        self.client_logger = logging.getLogger('dob')
        loggers = self.get_loggers()
        for logger in loggers:
            logger.handlers = []
        # Clear existing Handlers, and set the level.
        # MAYBE: Allow user to specify different levels for different loggers.
        cli_log_level_name = self.config['dev.cli_log_level']
        cli_log_level, warn_name = logging_helpers.resolve_log_level(cli_log_level_name)
        # We can at least allow some simpler optioning from the command args.
        if verbose:
            cli_log_level = min(logging.INFO, cli_log_level)
        if verboser:
            cli_log_level = min(logging.DEBUG, cli_log_level)
        # 2019-01-25 (lb): I have not had any issues for past few weeks, but,
        #   just FYI in case you do, you might need to clear handlers on
        #   lib_logger and sql_logger, e.g.,:
        #        for logger in loggers:
        #            logger.handlers = []
        #            logger.setLevel(cli_log_level)
        self.client_logger.handlers = []
        self.client_logger.setLevel(cli_log_level)

        color = self.config['log.use_color']
        formatter = logging_helpers.formatter_basic(color=color)

        if self.config['log.use_console']:
            console_handler = logging.StreamHandler()
            logging_helpers.setup_handler(console_handler, formatter, *loggers)

        logfile = self.config['log.filepath']
        if logfile:
            file_handler = logging.FileHandler(logfile, encoding='utf-8')
            logging_helpers.setup_handler(file_handler, formatter, *loggers)

        if warn_name:
            self.client_logger.warning(
                'Unknown Client.cli_log_level specified: {}'
                .format(cli_log_level)
            )

    def get_loggers(self):
        loggers = [
            self.lib_logger,
            self.sql_logger,
            self.client_logger,
        ]
        return loggers

    def bulk_set_log_levels(self, log_level):
        for logger in self.get_loggers():
            logger.setLevel(log_level)

    def disable_logging(self):
        loggers = [
            self.lib_logger,
            self.sql_logger,
            self.client_logger,
        ]
        for logger in loggers:
            logger.handlers = []
            logger.setLevel(logging.NOTSET)

    # ***

    def affirm(self, condition):
        if condition:
            return
        self.client_logger.error(_('Something catastrophic happened!'))
        if not self.config['dev.catch_errors']:
            return
        import traceback
        traceback.print_stack()
        traceback.print_exc()
        self.pdb_set_trace()

    # ***

    def pdb_set_trace(self):
        import pdb
        self.pdb_break_enter()
        pdb.set_trace()
        self.pdb_break_leave()

    def pdb_break_enter(self):
        import subprocess
        # If the developer breaks into code from within the Carousel,
        # i.e., from within the Python Prompt Toolkit library, then
        # pdb terminal echo of stdin back to stdout is broken. You'll
        # see that pdb.stdin and pdb.stdout still match the sys.__stdin__
        # and sys.__stdout__, so that's not the issue -- it's that pdb
        # terminal is in *raw* mode. We can fix this by shelling to stty.
        proc = subprocess.Popen(['stty', '--save'], stdout=subprocess.PIPE)
        (stdout_data, stderr_data) = proc.communicate()
        self.stty_saved = stdout_data.strip()
        # Before breaking, twiddle the terminal away from PPT temporarily.
        subprocess.Popen(['stty', 'sane'])

    def pdb_break_leave(self):
        import subprocess
        # Aha! This is awesome! We can totally recover from an interactive
        # debug session! First, restore the terminal settings (which we
        # reset so the our keystrokes on stdin were echoed back to us)
        # so that sending keys to PPT works again.
        subprocess.Popen(['stty', self.stty_saved])
        # And then the caller, if self.carousel, will redraw the interface
        # (because it has the handle to the application).
        self.client_logger.debug(_("Get on with it!"))

    # ***

    def find_latest_fact(self, restrict=None):
        try:
            return self.facts.find_latest_fact(restrict=restrict)
        except Exception as err:
            # (lb): Unexpected! This could mean more than one ongoing Fact found!
            dob_in_user_warning(str(err))

    def find_oldest_fact(self):
        return self.facts.find_oldest_fact()

