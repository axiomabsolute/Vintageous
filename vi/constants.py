MODE_INSERT = 1
MODE_NORMAL = 1 << 1
MODE_VISUAL = 1 << 2
MODE_VISUAL_LINE = 1 << 3
# The mode you enter when giving i a count.
MODE_NORMAL_INSERT = 1 << 4
# Vintageous always runs actions based on selections, even in NORMAL mode. Some Vim commands,
# however, behave differently depending on whether the start mode was NORMAL or VISUAL. To
# differentiate within Vintageous too, we need to add a fake internal visual mode that won't
# interfere with the actual visual mode. _MODE_INTERNAL_VISUAL translates to what Vim understands
# as NORMAL mode operation.
#
# Note that for motions we still use plain NORMAL mode.
_MODE_INTERNAL_VISUAL = 1 << 5


DIGRAPH_ACTION = 1
DIGRAPH_MOTION = 2


digraphs = {
    ('vi_d', 'vi_d'): ('vi_dd', DIGRAPH_ACTION),
    ('vi_c', 'vi_c'): ('vi_cc', DIGRAPH_ACTION),
    ('vi_y', 'vi_y'): ('vi_yy', DIGRAPH_ACTION),
    ('vi_g_action', 'vi_g_big_u'): ('vi_g_big_u', DIGRAPH_ACTION),
    ('vi_g_action', 'vi_g_u'): ('vi_g_u', DIGRAPH_ACTION),

    ('vi_g_action', 'vi_gg'): ('vi_gg', DIGRAPH_MOTION),
    # XXX: I don't think the following is needed.
    ('vi_f_first_step', 'vi_set_user_input'): ('vi_f', DIGRAPH_MOTION),
}


# Actions that cannot run on their own --they require a qualifier.
INCOMPLETE_ACTIONS = ('vi_g_action',)


# TODO: This does not belong here.
def mode_to_str(mode):
    if mode == MODE_INSERT:
        return "INSERT"
    elif mode == MODE_NORMAL:
        return ""
    elif mode == MODE_VISUAL:
        return "VISUAL"
    elif mode == MODE_VISUAL_LINE:
        return "VISUAL LINE"
    elif mode == MODE_NORMAL_INSERT:
        return "INSERT"
    return "<unknown>"


# TODO: Move this to somewhere where it's easy to import from and use it for transformers.
def regions_transformer(view, f):
    """Applies ``f`` to every selection region in ``view`` and replaces the existing selections.
    """
    sels = list(view.sel())
    view.sel().clear()

    new_sels = []
    for s in sels:
        new_sels.append(f(view, s))

    for s in new_sels:
        view.sel().add(s)
