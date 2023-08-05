import os
import logging
from copy import deepcopy

from mcutk.debugger.base import DebuggerBase


class IDE(DebuggerBase):
    """IDE debugger: use IDE to flash application to board.

    """

    # supported ides
    TOOLS = [
        'iar',
        'mdk',
        'mcux'
    ]

    def __init__(self, ides, **kwargs):
        super(IDE, self).__init__("ide", '', **kwargs)
        if not isinstance(ides, list):
            raise TypeError('apps must be a list')
        self._ides = ides
        self.template_root = ''
        self._force_ide = None

    @property
    def is_ready(self):
        for ide in self._ides:
            if ide.is_ready is False:
                return False
        return True

    def set_force_ide(self, name):
        if name in self.TOOLS:
            self._force_ide = name

    def get_ide(self, name):
        convert_map = {
            'armgcc': 'mdk',
            'uv4': 'mdk'
        }
        name = convert_map.get(name, name)
        for app in self._ides:
            if app.name == name:
                return app

        raise ValueError('{} path is not exists or not set!'.format(name))

    def flash(self, debugfile, idename='mcux', target='flexspi_nor_debug', board=None, template_root=None, **kwargs):
        """Flash image to board by IDE.

        Arguments:
            debugfile - {str}: image path.
            idename - {str}: mcux, mdk, iar.
            target - {str}: project target name.
            board - {Board} overried board object.
            template_root - {str} path to root directory of template projects
        """
        if self._force_ide:
            idename = self._force_ide
            logging.info("mandatory debugger run with %s", idename)

        # force to use mcuxpresso to flash binary to board
        if debugfile.endswith('.bin'):
            idename = 'mcux'

        if template_root is None:
            template_root = self.template_root

        if board is None:
            board = self._board

        # assert template projects root
        if not os.path.exists(template_root):
            raise IOError("template project[%s] is not exists!"%template_root)

        app = self.get_ide(idename)
        idename = app.name
        # assert tool name
        if idename not in IDE.TOOLS:
            raise ValueError("IDE [{}] is unsupported for board programming!".format(app))

        prjdir = os.path.join(template_root, idename)
        # workaround to make sure the origin board object is not changed.
        board_m = deepcopy(board)
        if idename not in ['iar', 'mdk']:
            board_m.usbid = board_m.usbid.split(':')[-1]

        kwargs['gdbpath'] = self.gdbpath
        logging.info("IDE name: %s, Version: %s", idename, app.version)
        self._call_registered_callback("before-load")
        ret = app.programming(board_m, prjdir, target, debugfile, **kwargs)
        return ret

    def _erase_by_mcux(self, board, target):
        from mcutk.debugger.redlink import RedLink
        mcux = self.get_ide("mcux")
        prjdir = os.path.join(self.template_root, 'mcux')
        redlink = RedLink(mcux.path + '/ide', version=self.version)
        redlink.gdbpath = self.gdbpath
        redlink.template_root = prjdir
        self._board.usbid = self._board.usbid.split(':')[-1]
        redlink.set_board(self._board)
        return redlink.erase()

    def _erase_by_mdk(self, board, target, debugfile):
        mdk_ide = self.get_ide("mdk")
        prjdir = os.path.join(self.template_root, 'mdk')
        project = mdk_ide.Project.frompath(prjdir)
        # use flash target
        for tar in project.targets:
            if "flash" in tar or "flexspi_nor_debug" in tar:
                target = tar
                break

        mdk_ide.programming(board, prjdir, target, debugfile, action="erase")

    def erase(self, idename="mcux", target='debug', debugfile=None):
        """Erase flash by IDE.

        Arguments:
            idename - {str}: mcux or mdk.
            target - {str}: project target name.
            debugfile - {str}: path to debug file. must set when idename=mdk
        """
        # workaround to make sure the origin board object is not changed.
        board_m = deepcopy(self._board)
        board_m.usbid = board_m.usbid.split(':')[-1]
        if idename == "mdk":
            if not debugfile:
                raise ValueError("MDK erase must pass an exists debugfile")
            return self._erase_by_mdk(board_m, target, debugfile)
        else:
            return self._erase_by_mcux(board_m, target)


    def reset(self):
        pass
