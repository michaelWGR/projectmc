# -*- coding: utf-8 -*-

from pywinauto.application import Application
import pywinauto.application
import time
# from pywinauto import Desktop

# app = Application(backend='uia').start('notepad.exe')
#
# # dlg_spec = app.UntiledNotepad
# #
# # actionable_dlg = dlg_spec.wait('visible')
#
# dlg_spec = app.window(best_match=u'无标题 - 记事本')
# time.sleep(1)
# # note_win.minimize()
#
# # dlg_spec.print_control_identifiers()
#
# dlg_spec.menu_select(u'编辑(E) -> 替换(R)...')
# time.sleep(1)
#
# app.window(best_match=u'替换').print_control_identifiers()



app = pywinauto.application.Application().connect(path="explorer")
systray_icons = app.ShellTrayWnd.NotificationAreaToolbar
print systray_icons