import itertools
import inspect

from discord.ext.commands.formatter import HelpFormatter
from discord.ext.commands.formatter import GroupMixin, Command
from discord.ext.commands.errors import CommandError

# all copied from discord.ext.commands.formatter, with slight alteratios

class CustomHelp(HelpFormatter):
    def __init__(self, show_hidden=False, show_check_failure=False, width=80):
        self.width = width
        self.show_hidden = show_hidden
        self.show_check_failure = show_check_failure

    def has_subcommands(self):
        """bool : Specifies if the command has subcommands."""
        return isinstance(self.command, GroupMixin)

    def is_bot(self):
        """bool : Specifies if the command being formatted is the bot itself."""
        return self.command is self.context.bot

    def is_cog(self):
        """bool : Specifies if the command being formatted is actually a cog."""
        return not self.is_bot() and not isinstance(self.command, Command)

    def shorten(self, text):
        """Shortens text to fit into the :attr:`width`."""
        if len(text) > self.width:
            return text[:self.width - 3] + '...'
        return text

    @property
    def max_name_size(self):
        """int : Returns the largest name length of a command or if it has subcommands
        the largest subcommand name."""
        try:
            commands = self.command.commands if not self.is_cog() else self.context.bot.commands
            if commands:
                return max(map(lambda c: len(c.name), commands.values()))
            return 0
        except AttributeError:
            return len(self.command.name)

    @property
    def clean_prefix(self):
        """The cleaned up invoke prefix. i.e. mentions are ``@name`` instead of ``<@id>``."""
        user = self.context.bot.user
        # this breaks if the prefix mention is not the bot itself but I
        # consider this to be an *incredibly* strange use case. I'd rather go
        # for this common use case rather than waste performance for the
        # odd one.
        return self.context.prefix.replace(user.mention, '@' + user.name)

    def get_qualified_command_name(self):
        """Retrieves the fully qualified command name, i.e. the base command name
        required to execute it. This does not contain the command name itself.
        """
        entries = []
        command = self.command
        while command.parent is not None:
            command = command.parent
            entries.append(command.name)

        return ' '.join(reversed(entries))

    def get_command_signature(self):
        """Retrieves the signature portion of the help page."""
        result = []
        prefix = self.clean_prefix
        qualified = self.get_qualified_command_name()
        cmd = self.command
        if len(cmd.aliases) > 0:
            aliases = '|'.join(cmd.aliases)
            fmt = '{0}[{1.name}|{2}]'
            if qualified:
                fmt = '{0}{3} [{1.name}|{2}]'
            result.append(fmt.format(prefix, cmd, aliases, qualified))
        else:
            name = prefix + cmd.name if not qualified else prefix + qualified + ' ' + cmd.name
            result.append(name)

        params = cmd.clean_params
        if len(params) > 0:
            for name, param in params.items():
                if param.default is not param.empty:
                    # We don't want None or '' to trigger the [name=value] case and instead it should
                    # do [name] since [name=None] or [name=] are not exactly useful for the user.
                    should_print = param.default if isinstance(param.default, str) else param.default is not None
                    if should_print:
                        result.append('[{}={}]'.format(name, param.default))
                    else:
                        result.append('[{}]'.format(name))
                elif param.kind == param.VAR_POSITIONAL:
                    result.append('[{}...]'.format(name))
                else:
                    result.append('<{}>'.format(name))

        return ' '.join(result)

    def get_ending_note(self):
        command_name = self.context.invoked_with
        return "Type {0}{1} command for more info on a command.\n" \
               "You can also type {0}{1} category for more info on a category.".format(self.clean_prefix, command_name)

    def filter_command_list(self):
        """Returns a filtered list of commands based on the two attributes
        provided, :attr:`show_check_failure` and :attr:`show_hidden`. Also
        filters based on if :meth:`is_cog` is valid.
        Returns
        --------
        iterable
            An iterable with the filter being applied. The resulting value is
            a (key, value) tuple of the command name and the command itself.
        """
        def predicate(tuple):
            cmd = tuple[1]
            if self.is_cog():
                # filter commands that don't exist to this cog.
                if cmd.instance is not self.command:
                    return False

            if cmd.hidden and not self.show_hidden:
                return False

            if self.show_check_failure:
                # we don't wanna bother doing the checks if the user does not
                # care about them, so just return true.
                return True

            try:
                return cmd.can_run(self.context)
            except CommandError:
                return False

        iterator = self.command.commands.items() if not self.is_cog() else self.context.bot.commands.items()
        return filter(predicate, iterator)

    def _check_new_page(self):
        # be a little on the safe side
        # we're adding 1 extra newline per page
        if self._count + len(self._current_page) >= 1980:
            # add the page
            self._current_page.append('```')
            self._pages.append('\n'.join(self._current_page))
            self._current_page = ['```']
            self._count = 4
            return True
        return False

    def _add_subcommands_to_page(self, max_width, commands):
        for name, command in commands:
            if name in command.aliases:
                # skip aliases
                continue
            entry = '  {0:<{width}} {1}'.format(name, command.short_doc, width=max_width)
            shortened = self.shorten(entry)
            self._count += len(shortened)
            if self._check_new_page():
                self._count += len(shortened)
            self._current_page.append(shortened)

    def format_help_for(self, context, command_or_bot):
        """Formats the help page and handles the actual heavy lifting of how
        the help command looks like. To change the behaviour, override the
        :meth:`format` method.
        Parameters
        -----------
        context : :class:`Context`
            The context of the invoked help command.
        command_or_bot : :class:`Command` or :class:`Bot`
            The bot or command that we are getting the help of.
        Returns
        --------
        list
            A paginated output of the help command.
        """
        self.context = context
        self.command = command_or_bot
        return self.format()

    def format(self):
        """Handles the actual behaviour involved with formatting.
        To change the behaviour, this method should be overridden.
        Returns
        --------
        list
            A paginated output of the help command.
        """
        self._pages = []
        self._count = 4 # ``` + '\n'
        self._current_page = ['```']

        # we need a padding of ~80 or so

        description = self.command.description if not self.is_cog() else inspect.getdoc(self.command)

        if description:
            # <description> portion
            self._current_page.append(description)
            self._current_page.append('')
            self._count += len(description)

        if isinstance(self.command, Command):
            # <signature portion>
            signature = self.get_command_signature()
            self._count += 2 + len(signature) # '\n' sig '\n'
            self._current_page.append(signature)
            self._current_page.append('')

            # <long doc> section
            if self.command.help:
                self._count += 2 + len(self.command.help)
                self._current_page.append(self.command.help)
                self._current_page.append('')
                self._check_new_page()

            # end it here if it's just a regular command
            if not self.has_subcommands():
                self._current_page.append('```')
                self._pages.append('\n'.join(self._current_page))
                return self._pages


        max_width = self.max_name_size

        def category(tup):
            cog = tup[1].cog_name
            # we insert the zero width space there to give it approximate
            # last place sorting position.
            x = cog + ':' if cog is not None else '\u200bOther:'
            return "\n" + x

        if self.is_bot():
            data = sorted(self.filter_command_list(), key=category)
            for category, commands in itertools.groupby(data, key=category):
                # there simply is no prettier way of doing this.
                commands = list(commands)
                if len(commands) > 0:
                    self._current_page.append(category)
                    self._count += len(category)
                    self._check_new_page()

                self._add_subcommands_to_page(max_width, commands)
        else:
            self._current_page.append('Commands:')
            self._count += 1 + len(self._current_page[-1])
            self._add_subcommands_to_page(max_width, self.filter_command_list())

        # add the ending note
        self._current_page.append('')
        ending_note = self.get_ending_note()
        self._count += len(ending_note)
        self._check_new_page()
        self._current_page.append(ending_note)

        if len(self._current_page) > 1:
            self._current_page.append('```')
            self._pages.append('\n'.join(self._current_page))

        return self._pages
