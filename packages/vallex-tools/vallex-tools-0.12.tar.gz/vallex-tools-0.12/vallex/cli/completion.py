BASH_COMPLETION_SCRIPT = """
# Bash Completion script for {script_path}

_{program}_{abs_path_hash}_complete()
{{
    local parent_command words cur subcommands last_non_opt
    declare -A command_options
    declare -A subcommands

    COMPREPLY=()

    _get_comp_words_by_ref -n : cur words

    # Command options
    {options}

    # Command tree
    {subcommands}

    # Find the parent command (i.e. the cur sub command)
    parent_command='{root_command}'
    for arg in ${{words[@]:1}}; do
        if [[ $arg != -* ]]; then
            # Tests whether $parent_command.$arg is a valid command
            # by testing whether the key is set in command_options
            # see, e.g., https://stackoverflow.com/questions/13219634/easiest-way-to-check-for-an-index-or-a-key-in-an-array
#             echo "testing if $parent_command/$arg is a valid command"
            if [[ -v "command_options[$parent_command/$arg]" ]]; then
#                 echo "it is"
                parent_command="$parent_command/$arg"
            fi;
            last_non_opt=$arg
        fi
    done

    # If the words array ends with an empty string, i.e. cur
    # is empty, the previous for-cycle does not iterate over it
    # so we must explicitly set the last_non_opt to '' here
    if [ -z "$cur" ]; then
      last_non_opt="";
    fi;

    # completing for an option
    if [[ ${{cur}} == -* ]] ; then

        COMPREPLY=($(compgen -W "${{command_options[$parent_command]}}" -- ${{cur}}))
        __ltrim_colon_completions "$cur"

        return 0;

    # completing for a command
    elif [ "z${{cur}}" == "z$last_non_opt" ]; then
        COMPREPLY=($(compgen -W "${{subcommands[$parent_command]}}" -- ${{cur}}))
        __ltrim_colon_completions "$cur"
        return 0
    fi;
}}

complete -o default -F _{program}_{abs_path_hash}_complete {program}
complete -o default -F _{program}_{abs_path_hash}_complete ./{program}
complete -o default -F _{program}_{abs_path_hash}_complete {script_path}

"""
