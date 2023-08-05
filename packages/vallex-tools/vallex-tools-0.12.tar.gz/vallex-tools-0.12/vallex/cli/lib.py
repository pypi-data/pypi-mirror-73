"""
    A library for creating cli interfaces





"""
import hashlib
import inspect
import logging
import os
import sys
import textwrap

from importlib import import_module
from pathlib import Path

from vallex.cli.completion import BASH_COMPLETION_SCRIPT
from vallex.config import Config
from vallex.term import get_terminal_size, FG, RED, STATUS, YELLOW

WHITE_FG = FG((255, 255, 255))


class CommandLineException(BaseException):
    def __init__(self, message, cmd):
        super().__init__(message)
        self._cmd = cmd

    def __str__(self):
        return "CLI Error" + " ("+self._cmd.name+"): "+super().__str__()


class TooManyArguments(CommandLineException):
    def __init__(self, cmd, arg, expected_args):
        super().__init__("Too many arguments (expected "+str(expected_args)+") for command "+cmd.name+". Offending argument: '"+arg+"'", cmd)
        self._arg = arg
        self._expected = expected_args


class NotEnoughArguments(CommandLineException):
    def __init__(self, cmd, got_args, expected_args):
        super().__init__("Not enough arguments. Got "+str(got_args)+" expected "+str(expected_args)+".", cmd)
        self._arg = got_args
        self._expected = expected_args


class UnknownOption(CommandLineException):
    def __init__(self, cmd, option):
        super().__init__("Unknown option '"+str(option)+"'", cmd)
        self._option = option


class MissingOptionValue(CommandLineException):
    def __init__(self, cmd, option):
        super().__init__("Option '"+str(option)+"' requires a value", cmd)
        self._option = option


class InvalidOptionValue(CommandLineException):
    def __init__(self, cmd, option, value, value_parser, message=None):
        if value_parser.__doc__:
            msg = "Option '"+str(option)+"' "+value_parser.__doc__+". '"+str(value)+"' given instead."
        else:
            msg = "Option '"+str(option)+"' got invalid value '"+str(value)+"'."

        if message:
            msg += '\nError details: '+message+')'
        super().__init__(msg, cmd)
        self._option = option
        self._value = value


class UnknownCommand(CommandLineException):
    def __init__(self, cmd, command):
        super().__init__("Unknown command '"+str(command)+"'", cmd)
        self._command = command


class Option:
    def __init__(self, cmd, long_form, short_form=None, help_text='', multiple=False, default=None):
        self._cmd = cmd
        self._short = short_form
        self._long = long_form
        self._help = help_text
        self._cmd._opts[self._long] = self
        self._multiple = multiple
        if self._short:
            self._cmd._opts[self._short] = self

    def parse(self, opt, argv):
        return 0


class ValueOption(Option):
    def __init__(self, _cmd, long_form, short_form=None, help_text='', multiple=False, default=None, multi=False, parser=None):
        super().__init__(_cmd, long_form, short_form, help_text, multiple)
        self._default = default
        self._specified = False
        self._value = None if not self._multiple else []
        self._parser = parser

    def parse(self, opt, argv):
        if argv and not argv[0].startswith('-'):
            if self._multiple:
                self._value.append(argv[0])
            else:
                self._value = argv[0]
            self._specified = True
        elif self._default:
            self._value = self._default if not self._multiple else [self._default]
        else:
            raise MissingOptionValue(self._cmd, opt)
        try:
            self.parse_value()
        except Exception as ex:
            raise InvalidOptionValue(self._cmd, opt, self._value, self.parse_value, message=str(ex))
        return 1

    def has_value(self):
        return self._specified or self._default is not None

    @property
    def value(self):
        # Provide defaults for options not specified on commandline
        if self._value is None or (self._multiple and not self._value) and self._default:
            self._value = self._default if not self._multiple else [self._default]
            try:
                self.parse_value()
            except:
                raise InvalidOptionValue(self._cmd, self._long, self._value, self.parse_value)
        return self._value

    def parse_value(self):
        if self._parser:
            if self._multiple:
                self._value = [self._parser(v) for v in self._value]
            else:
                self._value = self._parser(self._value)


class BoolOption(ValueOption):
    def parse(self, opt, argv):
        #  print("Parsing bool option", opt)
        self._value = True
        self._parsed = True
        self._specified = True
        return 0

    def has_value(self):
        return True

    @property
    def value(self):
        super().parse_value()
        # If not specified, defaults to false
        if not self._specified:
            return False
        return True


class IntOption(ValueOption):
    def parse_value(self):
        """expects an integer"""
        super().parse_value()
        self._value = int(self._value) if not self._multiple else [int(v) for v in self._value]


class StrOption(ValueOption):
    pass


_type2option_map = {
    int: IntOption,
    bool: BoolOption,
    str: StrOption,
}


class Command:
    def __init__(self, name='', parent=None):
        self.subcommands = {}
        self.main = self._unimplemented
        self._opts = {}
        self._args = []
        self.name = name
        self.parent = parent
        self._version = "version unspecified"
        self.config: Config = None

    def _unimplemented(self, *args, **kwargs):
        """Default main implementation, must be reimplemented using the @main_command decorator"""
        return self.help(*args, **kwargs)
        #raise CommandLineException("The command "+self.name+" is not implemented (try a subcommand?).", self)

    def get_command(self, path):
        if not path:
            return self
        if path[0] not in self.subcommands:
            self.subcommands[path[0]] = Command(path[0], parent=self)
            sub = self.subcommands[path[0]]
            self.subcommands[path[0]].sub_command('help')(sub.help)
            self.subcommands[path[0]].sub_command('--help')(sub.help)
        sub = self.subcommands[path[0]]
        return sub.get_command(path[1:])

    def parse_argument(self, arg):
        info = inspect.getargs(self.main.__code__)

        expected_num_args = len(info.args) - 1  # The mandatory options arg is provided by the runtime
        if info.args and info.args[0] == 'self':
            expected_num_args -= 1

        if info.varargs is None and len(self._args) >= expected_num_args:
            raise TooManyArguments(self, arg, expected_num_args)
        else:
            self._args.append(arg)

    def _check_args(self):
        info = inspect.getargspec(self.main)
        if info.defaults:
            default_len = len(info.defaults)
        else:
            default_len = 0
        expected_num_args = len(info.args) - default_len  # The mandatory options arg is provided by the runtime
        if info.args and info.args[0] == 'self':
            expected_num_args -= 1
        if len(self._args) < expected_num_args:
            #  print(info)
            raise NotEnoughArguments(self, len(self._args), expected_num_args)

    def parse(self, argv, global_opts: dict):
        self._argv = argv
        self._global_opts = global_opts
        pos = 0
        while pos < len(argv):
            #  print(pos, "Parsing argv item: '"+argv[pos]+"'...")
            arg = argv[pos]
            pos += 1
            if arg in self.subcommands:
                global_opts.update({o._long: o.value for o in set(self._opts.values()) if o.has_value()})
                return self.subcommands[arg].parse(argv[pos:], global_opts)
            elif arg.startswith('-'):
                opt = arg.lstrip('-')
                #  print("  Trying option: '"+opt+"'... (available", self._opts.keys(), ")")
                if opt not in self._opts:
                    if len(arg)-len(opt) == 1:
                        # Handle concatenated single letter short options (e.g. -vvv, -xvf, etc)
                        opts = list(opt)
                        for o in opts[:-1]:
                            if o not in self._opts:
                                raise UnknownOption(self, o)
                            else:
                                self._opts[o].parse(o, [])

                        # The last single letter option can have arguments
                        opt = opts[-1]
                        if opt not in self._opts:
                            raise UnknownOption(self, opt)
                        else:
                            pos += self._opts[o].parse(o, argv[pos:])
                    else:
                        raise UnknownOption(self, opt)
                else:
                    #  print("  Parsing option '"+opt+"' arguments from ", argv[pos:])
                    pos += self._opts[opt].parse(opt, argv[pos:])
            else:
                self.parse_argument(arg)
        self._check_args()
        global_opts.update({o._long: o.value for o in set(self._opts.values()) if o.has_value()})
        return self, self._args, global_opts

    def sub_command(self, name=None):
        def decorator(f):
            cmd_name = name or f.__name__

            info = inspect.getargs(f.__code__)
            if 'options' not in info.args:
                #  print(info, self)
                raise CommandLineException("Commands must mandatorily accept an 'options' argument. Offending command: '"+cmd_name+"'", cmd=self)

            sub_command = Command(cmd_name, self)
            sub_command.main = f
            sub_command.__doc__ = f.__doc__
            self.subcommands[cmd_name] = sub_command

            return sub_command

        return decorator

    def help(self, subcommand=None, options={}):
        """Prints basic help information. """
        term_w, term_h = get_terminal_size()
        indent_w = 4

        if subcommand:
            sub = self.subcommands.get(subcommand, None)
            if sub:
                sub.help()
                return
            else:
                STATUS.print("Unknown subcommand: ", FG(RED) | subcommand)
                STATUS.print()

        if not self.main == self._unimplemented:
            STATUS.print(textwrap.dedent(self.main.__doc__).strip())
            STATUS.print()
        elif self.__doc__:
            self.version()
            STATUS.print(textwrap.dedent(self.__doc__).strip())
            STATUS.print()
        else:
            root.version()
            STATUS.print(textwrap.dedent(root.__doc__).strip())
            STATUS.print()
            STATUS.print("Command:", FG(YELLOW) | self.name)
            STATUS.print()

        if self.subcommands:
            STATUS.print(FG(YELLOW) | "Available subcommands:")
            STATUS.print()
            cmd_list = [(name + ' '*indent_w, self.subcommands[name]) for name in sorted(self.subcommands.keys()) if name != '--help']
            max_cmd_len = max([len(name) for name, _ in cmd_list])
            help_text_len = max(term_w - indent_w - 10 - max_cmd_len, 10)
            for name, cmd in cmd_list:
                short_help_text = (cmd.__doc__.strip() or '').split('\n')[0]
                help_text = '\n'.join(textwrap.wrap(textwrap.dedent(short_help_text).strip(), help_text_len))
                help_text = textwrap.indent(help_text, ' '*(max_cmd_len+indent_w))
                STATUS.print(' '*indent_w, WHITE_FG | name, ' '*(max_cmd_len-len(name)), help_text.strip(), sep='')

        if self._opts:
            STATUS.print()
            STATUS.print(FG(YELLOW) | "Available options:")
            STATUS.print()
            option_list = [('--'+o._long + (', -'+o._short if o._short else '')+' '*indent_w, o._help) for o in sorted(set(self._opts.values()), key=lambda x: x._long)]
            max_opt_len = max(map(lambda x: len(x[0]), option_list))
            help_text_len = max(term_w - indent_w - 10 - max_opt_len, 10)
            for opt_text, opt_help in option_list:
                help_text = '\n'.join(textwrap.wrap(textwrap.dedent(opt_help).strip(), help_text_len))
                help_text = textwrap.indent(help_text, ' '*(max_opt_len+indent_w))
                STATUS.print(' '*indent_w, WHITE_FG | opt_text, ' '*(max_opt_len-len(opt_text)), help_text.strip(), sep='')

    def version(self, options={}):
        """Prints the program  version. """
        STATUS.print(WHITE_FG | self.name, FG(YELLOW) | self._version)

    def _get_command_tree(self):
        return {(self.name + '/' + cmd_name): cmd for cmd_name, cmd in self.subcommands.items()}

    def completion(self, options={}):
        """
        Generates a bash command completion script.

        To enable it systemwide, save its output to

            `/etc/bash_completion.d/{program}.bash-completion`

        or, alternatively, save the generated script somewhere
        else and source it in `~/.bash_profile` or `~/.bash_rc`.

        To enable it in your current session, run

            $ eval "$({program} completion)"`

        in your bash shell (note that this only effects the
        current bash session).
        """
        script_path = Path(os.getenv('_PY_VALLEX_PROGRAM_PATH', sys.argv[0]))
        script_hash = hashlib.sha256(str(script_path.absolute()).encode('utf-8')).hexdigest()[0:16]
        options = f"""command_options[{self.name}]='{' '.join(['--'+opt._long for opt in self._opts.values()])}'\n"""
        subcommands = f"""subcommands[{self.name}]='{' '.join([k for k in self.subcommands.keys() if not k.startswith('-')])}'\n"""
        for name, cmd in self._get_command_tree().items():
            if cmd.name.startswith('-'):
                continue
            subcommands += f"""subcommands[{name}]='{' '.join([k for k in cmd.subcommands.keys() if not k.startswith('-')])}'\n"""
            # command_options['{root_command}']="--config --help --load-lexicon -i --no-sort --output -o --output-format --post-pattern --pre-pattern --verbosity -v"
            options += f"""command_options[{name}]='{' '.join(['--'+opt._long for opt in cmd._opts.values()])}'\n"""
        print(BASH_COMPLETION_SCRIPT.format(
            root_command=self.name,
            script_path=str(script_path),
            program=script_path.name,
            abs_path_hash=script_hash,
            options=textwrap.indent(options, '    ').strip(),
            subcommands=textwrap.indent(subcommands, '    ').strip()
        )
        )
    completion.__doc__ = completion.__doc__.format(program=Path(os.getenv('_PY_VALLEX_PROGRAM_PATH', sys.argv[0])).name)  # type: ignore


def option(long_form, option_type, short_form=None, help='', default=None, parser=None, multiple=False):
    def decorator(cmd):
        if 'sphinx' in sys.modules:
            return cmd
        nonlocal long_form, option_type, short_form, help, default, parser
        if not long_form.startswith('--') or len(long_form) <= 2 or long_form[2] == '-':
            raise CommandLineException("Long form options must start with exactly '--'. Offending option: '"+long_form+"'", cmd=cmd)
        long_form = long_form.lstrip('-')
        if short_form:
            if not short_form.startswith('-') or len(short_form) <= 1 or short_form[1] == '-':
                raise CommandLineException("Short form options must start with exactly '-'. Offending option: '"+short_form+"'", cmd=cmd)
            short_form = short_form.lstrip('-')
        orig_type = option_type
        if not issubclass(option_type, Option):
            option_type = _type2option_map.get(option_type, None)
        if not option_type:
            raise CommandLineException("Option type must either derive from the 'cli.Option' class or must be one of the basic types (" +
                                       ','.join([k.__name__ for k in _type2option_map.keys()])+"). Offending option: '"+long_form+"' is of type: '"+str(orig_type)+"'", cmd=cmd)
        opt = option_type(cmd, long_form, short_form=short_form, help_text=help, default=default, parser=parser, multiple=multiple)
        return cmd
    return decorator


def main_command():
    def decorator(f):
        if 'sphinx' in sys.modules:
            return f
        frm = inspect.stack()[1]
        mod_name = frm[0].f_globals['__name__']
        command_path = mod_name[len(root._command_base)+1:].split('.')
        command = root.get_command(command_path)

        info = inspect.getargs(f.__code__)
        if 'options' not in info.args:
            raise CommandLineException("Commands must mandatorily accept an 'options' argument. Offending command: '"+command.name+"'", cmd=command)

        command.main = f
        command.__doc__ = command.__doc__ or f.__doc__

        return command
    return decorator


def sub_command(name=None):
    def decorator(f):
        if 'sphinx' in sys.modules:
            return f
        frm = inspect.stack()[1]
        mod_name = frm[0].f_globals['__name__']
        command_path = mod_name[len(root._command_base)+1:].split('.')

        parent_cmd = root.get_command(command_path)

        cmd_name = name or f.__name__

        info = inspect.getargs(f.__code__)
        if 'options' not in info.args:
            raise CommandLineException("Commands must mandatorily accept an 'options' argument. Offending command: '"+cmd_name+"'", cmd=parent_cmd)

        sub_command = Command(cmd_name, parent_cmd)
        sub_command.main = f
        parent_cmd.subcommands[cmd_name] = sub_command
        sub_command.__doc__ = f.__doc__

        return sub_command

    return decorator


root = Command()
root.sub_command()(root.help)
root.sub_command()(root.completion)
root.sub_command('--help')(root.help)
root.sub_command('--version')(root.version)


def load_commands(package, cmd=root, base=None):
    if base is None:
        c_path = []
    else:
        c_path = package.split('.')[len(base.split('.')):]
    cmd._command_base = package
    cmds = import_module(package)
    p = Path(cmds.__file__).parent
    for item in p.iterdir():
        if item.is_file and item.name.endswith('.py') and not item.name.startswith('__'):
            m = __import__(package, globals(), locals(), fromlist=[item.name[:-3]], level=0)
            imported_cmd = cmd.get_command(c_path+[item.name[:-3]])
            if not imported_cmd.__doc__ and m.__doc__:
                imported_cmd.__doc__ = m.__doc__
        elif item.is_dir() and not (item.name.startswith('__') or item.name.startswith('.')):
            load_commands(package+'.'+item.name, cmd)
            m = import_module(package+'.'+item.name)
            imported_cmd = cmd.get_command(c_path+[item.name])
            if not imported_cmd.__doc__ and m.__doc__:
                imported_cmd.__doc__ = m.__doc__


def choices_parser(choices):
    def parser(val):
        if val in choices:
            return val
        raise Exception("invalid choice")
    parser.__doc__ = 'Expecting one of '+','.join(choices)
    return parser


def main(argv):
    root.name = os.getenv('_PY_VALLEX_PROGRAM_NAME', Path(argv[0]).name)
    try:
        cmd, args, opts = root.parse(argv[1:], {})

        if not argv[1:] and root.default_cmd:
            # If there were no command line arguments and a
            # default command is provided, first call its
            # parse method to populate default option values
            # and then set the main method to its main method
            root.default_cmd.parse(argv[1:], opts)
            root.main = root.default_cmd.main

        return cmd.main(*args, options=opts)
    except CommandLineException as ex:
        print(ex)
        print()
        if ex._cmd:
            ex._cmd.help()
        else:
            root.help()
        return -1
