# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/3/18 13:46

COMMENT_STRING = '/*'
LINE_ENDING = '\n'


def toggle_commenting(editor):
    # Check if the selections are valid
    selections = get_selections(editor)
    if selections is None:
        return
    # Merge overlapping selections
    while merge_test(selections):
        selections = merge_selections(selections)
    # Start the undo action that can undo all commenting at once
    editor.beginUndoAction()
    # Loop over selections and comment them
    for i, sel in enumerate(selections):
        if editor.text(sel[0]).lstrip().startswith(COMMENT_STRING):
            replace_text = set_commenting(editor, sel[0], sel[1], _uncomment)
        else:
            replace_text = set_commenting(editor, sel[0], sel[1], _comment)
    # Select back the previously selected regions
    editor.SendScintilla(editor.SCI_CLEARSELECTIONS)
    for i, sel in enumerate(selections):
        start_index = editor.positionFromLineIndex(sel[0], 0)
        # Check if ending line is the last line in the editor
        last_line = sel[1]
        if last_line == editor.lines() - 1:
            end_index = editor.positionFromLineIndex(
                sel[1], len(editor.text(last_line)))
        else:
            end_index = editor.positionFromLineIndex(
                sel[1], len(editor.text(last_line)) - 1)
        if i == 0:
            editor.SendScintilla(editor.SCI_SETSELECTION,
                                 start_index, end_index)
        else:
            editor.SendScintilla(editor.SCI_ADDSELECTION,
                                 start_index, end_index)

    # 空行注释，光标移动到/**/中间
    if replace_text == '/**/':
        pos = editor.getCursorPosition()
        editor.setCursorPosition(pos[0], pos[1] + 2)

    # Set the end of the undo action
    editor.endUndoAction()


def get_selections(editor):
    # Get the selection and store them in a list
    selections = []
    for i in range(editor.SendScintilla(editor.SCI_GETSELECTIONS)):
        selection = (
            editor.SendScintilla(editor.SCI_GETSELECTIONNSTART, i),
            editor.SendScintilla(editor.SCI_GETSELECTIONNEND, i)
        )
        # Add selection to list
        from_line, from_index = editor.lineIndexFromPosition(selection[0])
        to_line, to_index = editor.lineIndexFromPosition(selection[1])
        selections.append((from_line, to_line))
    selections.sort()
    # Return selection list
    return selections


def merge_test(selections):
    """
    Test if merging of selections is needed
    """
    for i in range(1, len(selections)):
        # Get the line numbers
        # previous_start_line = selections[i - 1][0]
        previous_end_line = selections[i - 1][1]
        current_start_line = selections[i][0]
        # current_end_line = selections[i][1]
        if previous_end_line == current_start_line:
            return True
    # Merging is not needed
    return False


def merge_selections(selections):
    """
    This function merges selections with overlapping lines
    """
    # Test if merging is required
    if len(selections) < 2:
        return selections
    merged_selections = []
    skip_flag = False
    for i in range(1, len(selections)):
        # Get the line numbers
        previous_start_line = selections[i - 1][0]
        previous_end_line = selections[i - 1][1]
        current_start_line = selections[i][0]
        current_end_line = selections[i][1]
        # Test for merge
        if previous_end_line == current_start_line and not skip_flag:
            merged_selections.append(
                (previous_start_line, current_end_line)
            )
            skip_flag = True
        else:
            if not skip_flag:
                merged_selections.append(
                    (previous_start_line, previous_end_line)
                )
            skip_flag = False
            # Add the last selection only if it was not merged
            if i == (len(selections) - 1):
                merged_selections.append(
                    (current_start_line, current_end_line)
                )
    # Return the merged selections
    return merged_selections


def set_commenting(editor, arg_from_line, arg_to_line, func):
    # Get the cursor information
    from_line = arg_from_line
    to_line = arg_to_line
    # Check if ending line is the last line in the editor
    last_line = to_line
    if last_line == editor.lines() - 1:
        to_index = len(editor.text(to_line))
    else:
        to_index = len(editor.text(to_line)) - 1
    # Set the selection from the beginning of the cursor line
    # to the end of the last selection line
    editor.setSelection(
        from_line, 0, to_line, to_index
    )
    # Get the selected text and split it into lines
    selected_text = editor.selectedText()
    selected_list = selected_text.split("\n")
    # Find the smallest indent level
    indent_levels = []
    for line in selected_list:
        indent_levels.append(len(line) - len(line.lstrip()))
    min_indent_level = min(indent_levels)
    # Add the commenting character to every line
    for i, line in enumerate(selected_list):
        selected_list[i] = func(line, min_indent_level)
    # Replace the whole selected text with the merged lines
    # containing the commenting characters
    replace_text = LINE_ENDING.join(selected_list)
    editor.replaceSelectedText(replace_text)
    return replace_text


def _comment(line, indent_level):
    return line[:indent_level] + COMMENT_STRING + line[indent_level:] + COMMENT_STRING[::-1]


def _uncomment(line, indent_level=None):
    if line.strip().startswith(COMMENT_STRING):
        return line.replace(COMMENT_STRING, "", ).replace(COMMENT_STRING[::-1], "", )
    else:
        return line
