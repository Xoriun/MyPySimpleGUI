"""Copyright 2026 <Xoriun>"""


def mpsg_lines():
    with open('quick)tkinter.py', encoding='utf-8') as file:
        for line in file:
            yield line.strip()

types_to_typehint = {'no_buttons', 'non_blocking', 'quick', 'quick_message', 'no_titlebar', 'auto_close', 'error', 'cancel', 'ok', 'ok_cancel', 'yes_no'}

defs: dict[str, str] = {}
reading_def = False
popup_def = ''
docs: dict[str, str] = {}
reading_doc = False
popup_doc = ''
pops: dict[str, list[str]] = {}
reading_pops = False
for line in mpsg_lines():
    # beginning of new popup
    if line.startswith('def popup'):
        reading_def = True
        popup_type = line[10:line.find('(')]

    # reading which kwargs to pop
    if reading_pops:
        if line.startswith('kwargs.pop('):
            pops[popup_type].append(line.split("'")[1])
        else:
            reading_pops = False

    # reading doc lines of current popup
    if reading_doc:
        # check for last line of doc
        if line.count('"""') == 2 or ('"""' in line and popup_doc):
            reading_doc = False

        popup_doc += line
        popup_doc += '\n'

        # after last line, add def and doc to the dicts and reset
        if popup_doc and not reading_doc:
            if popup_type == '' or popup_type in types_to_typehint:
                defs[popup_type] = popup_def
                docs[popup_type] = popup_doc
                pops[popup_type] = []
                reading_pops = True

            popup_def = ''
            popup_doc = ''

    # reading def lines of current doc
    if reading_def:
        popup_def += line

        # end of def lines -> switch to reading docs
        if line.endswith('):'):
            reading_def = False
            reading_doc = True


defs = {
    popup_type: popup_def[popup_def.find('(')+1:].removeprefix('*args,').removesuffix(', **kwargs):').removesuffix('**kwargs):').replace(' ','').replace('None,None', 'None__COMMA__None')
    for popup_type, popup_def in defs.items()
}

popup_def_args: dict[str, dict[str, str]] = {}
popup_doc_args: dict[str, dict[str, str]] = {}
for popup_type in defs:
    popup_def_args[popup_type] = {}
    popup_doc_args[popup_type] = {'':''}
    if defs[popup_type]:
        for arg in defs[popup_type].split(','):
            kw, default = arg.split('=', maxsplit=1)
            popup_def_args[popup_type][kw] = default
    for line in docs[popup_type].split('\n'):
        line = line.replace('"""', '')
        if line.startswith(':'):
            if line.startswith(':return'):
                popup_doc_args[popup_type]['return'] = line
            elif line.startswith(':rtype'):
                popup_doc_args[popup_type]['return'] += '\n'
                popup_doc_args[popup_type]['return'] += line
            else:
                arg = line.split(':', maxsplit=2)[1].split(' ', maxsplit=1)[1]
                if arg in popup_doc_args[popup_type]:
                    popup_doc_args[popup_type][arg] += '\n'
                    popup_doc_args[popup_type][arg] += line
                else:
                    popup_doc_args[popup_type][arg] = line
        else:
            popup_doc_args[popup_type][''] += line



# creating the .pyi file
with open('MyPySimpleGUI.pyi', 'w') as pyi_file:
    for popup_type in types_to_typehint:
        # def and args
        pyi_file.write(f'def popup_{popup_type}(*args')
        for arg in popup_def_args['']:
            if arg in pops[popup_type]:
                continue

            if arg in popup_def_args[popup_type]:
                default = popup_def_args[popup_type][arg]
            else:
                default = popup_def_args[''][arg]

            pyi_file.write(f', {arg}={default.replace('__COMMA__', ', ')}')

        pyi_file.write('):\n')

        # doc
        pyi_file.write('    """\n')
        pyi_file.write(f'    {popup_doc_args[popup_type]['']}\n\n')
        for arg in popup_doc_args['']:
            if arg == '' or arg in pops[popup_type]:
                continue

            pyi_file.write(f'    {popup_doc_args[''][arg].replace('\n', '\n    ')}\n')

        pyi_file.write('    """  # noqa: PYI021\n\n')

