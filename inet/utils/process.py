import gipc


def fork(fn, *args, daemon=False):
    '''
    Creates a child process that runs the given function.
    @sig fork ::  (* -> _) -> * -> Bool -> _
    '''
    with gipc.pipe():
        gipc.start_process(target=fn, args=args, daemon=daemon)
