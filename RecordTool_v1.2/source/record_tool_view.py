# -*- coding:utf-8 -*-
from Tkinter import *
from functools import partial
from record_tool_presenter import *
from record_tool_util import *
from record_tool_layout import *
import ttk
import os
import platform


class AppFrame(Frame):


    def __init__(self, parent):
        app_frame_layout = layout[operate_system]["app_frame"]
        self.bg = app_frame_layout["bg"]
        Frame.__init__(self, parent, bg=self.bg)

        self.parent = parent
        self.x = self.parent.list_frame_width
        self.y = self.parent.nav_frame_height
        self.app_btn_width = app_frame_layout["app_btn_width"]
        self.order_label_width = app_frame_layout["order_label_width"]
        self.width = self.parent.width - self.parent.list_frame_width
        self.height = self.parent.height - self.parent.nav_frame_height

        self.app_button_frame_padx = app_frame_layout["app_button_frame_padx"]
        self.app_button_frame_pady = app_frame_layout["app_button_frame_pady"]
        self.app_button_label_font = app_frame_layout["app_button_label_font"]
        self.app_button_label_bg = app_frame_layout["app_button_label_bg"]
        self.app_button_label_fg = app_frame_layout["app_button_label_fg"]


    def hide(self):
        self.place_forget()
        self.__remove_children()
        self.is_showed = False


    def show(self, task_id, task_name, case_id, case_en_name, event=None):
        self.__remove_children()
        self.is_showed = True

        self.task_id = task_id
        self.task_name = task_name
        self.case_id = case_id
        self.case_en_name = case_en_name

        self.place(x=self.x, y=self.y, width=self.width, height=self.height)

        apps = AppPresenter.get_apps(task_id)
        if type(apps) is str:
            Label(self, text=apps, font='微软雅黑 -15 bold', fg='red', bg='#DEDEDE', justify=LEFT).place(x=0, y=0)
            return

        row_num = len(apps) / 2;
        col_num = 3;
        row_now = 0;
        col_now = 0;

        for app in apps:
            if row_now <= row_num and col_now <= col_num:
                order = StringVar()
                app_id = app[0][0]
                app_name = app[0][1]

                thread = Thread(target=self.__update_order,args=(order, self.task_id, self.case_id, app_id, 'android'))
                thread.setDaemon(True)
                thread.start()

                app_button_frame = Frame(self)
                app_button_frame.grid(row=row_now, column=col_now, padx=self.app_button_frame_padx, pady=self.app_button_frame_pady)

                label = Label(app_button_frame, width=self.order_label_width, textvariable=order, font=self.app_button_label_font,
                              bg=self.app_button_label_bg, fg=self.app_button_label_fg, justify=CENTER )
                label.pack(side=RIGHT, expand='yes', fill='both')

                btn_status = StringVar()
                btn_status.set('%s\n(开始录制)'%(app_name))
                ttk.Style().configure('AppNormal.TButton', font=('微软雅黑', 9,'bold'), justify=CENTER)
                ttk.Style().configure('AppRecording.TButton', foreground='red', font=('微软雅黑', 9, 'bold'), justify=CENTER)
                btn = ttk.Button(app_button_frame, width=self.app_btn_width, textvariable=btn_status, style='AppNormal.TButton', cursor='hand2')
                btn.pack(side=LEFT)
                btn.config(command=partial(self.__start_stop_record, btn, btn_status, app_id, app_name, 'android'))

                col_now += 1
                if col_now >= col_num:
                    row_now += 1
                    col_now = 0


    def __start_stop_record(self, btn, btn_status, app_id, app_name, platform):
        if (RecordPresenter.record_status==0):
            self.parent.disable_widgets(btn)

            if self.parent.mode=='Remake':
                remake_dialog = RemakeDialog()
                self.wait_window(remake_dialog)
                self.order = remake_dialog.value
                if self.order is None:
                    self.parent.enable_widgets(btn)
                    return
                if not RemakePresenter.check_remake_order(self.task_id, app_id, platform, self.case_id, self.order):
                    tkMessageBox.showwarning('Order错误', '您还未录制过这个视频，只能补录录过的视频！')
                    self.parent.enable_widgets(btn)
                    return
            else:
                self.order = ResultOrderPresenter.hold_order(self.task_id, self.case_id, platform, app_id)

            if RecordPresenter.record():
                btn_status.set('%s\n(停止录制)'%(app_name))
        elif (RecordPresenter.record_status==1):
            RecordPresenter.finish_record(app_id, app_name, platform, self.task_id, self.case_id, self.case_en_name, self.order)
            self.parent.enable_widgets(btn)
            btn_status.set('%s\n(开始录制)'%(app_name))


    def __update_order(self, order_str_var, task_id, case_id, app_id, platform):

        while(self.is_showed and self.case_id == case_id):

            order = ResultOrderPresenter.get_order(task_id, case_id, platform, app_id)

            order_str_var.set(order)

            time.sleep(2)


    def __remove_children(self):
        for item in self.children.items():
            item[1].destroy()


class CaseFrame(Frame):


    def __init__(self, parent=None):
        Frame.__init__(self, parent)

        case_frame_layout = layout[operate_system]["case_frame"]
        self.parent = parent
        self.width = self.parent.width
        self.height = self.parent.height
        self.nav_frame_height = case_frame_layout["nav_frame_height"]
        self.list_frame_width = case_frame_layout["list_frame_width"]
        self.is_shown = False

        self.mode = 'Normal'

        self.app_frame = AppFrame(self)

        self.nav_frame_bg = case_frame_layout["nav_frame_bg"]
        self.nav_frame_x = case_frame_layout["nav_frame_x"]
        self.nav_frame_y = case_frame_layout["nav_frame_y"]
        self.nav_frame = Frame(self, bg=self.nav_frame_bg)
        self.nav_frame.place(x=self.nav_frame_x, y=self.nav_frame_y, width=self.width, height=self.nav_frame_height)

        self.left_frame_bg = case_frame_layout["left_frame_bg"]
        self.left_frame_x = case_frame_layout["left_frame_x"]
        self.left_frame = Frame(self, bg=self.left_frame_bg)
        self.left_frame.place(x=self.left_frame_x, y=self.nav_frame_height, width=self.list_frame_width,
                              height=self.height - self.nav_frame_height)

        self.upload_frame = UploadFrame(self)

        self.task_info_label_val = StringVar()
        self.case_info_label_val = StringVar()
        self.phone_info_label_val = StringVar()

        self.task_info_label_font = case_frame_layout["task_info_label_font"]
        self.task_info_label_fg = case_frame_layout["task_info_label_fg"]
        self.task_info_label_bg = case_frame_layout["task_info_label_bg"]
        self.task_info_label_x = case_frame_layout["task_info_label_x"]
        self.task_info_label_y = case_frame_layout["task_info_label_y"]
        self.task_info_label = Label(self.nav_frame, textvariable=self.task_info_label_val, font=self.task_info_label_font,
                                     fg=self.task_info_label_fg, bg=self.task_info_label_bg, justify=LEFT)
        self.task_info_label.place(x=self.task_info_label_x, y=self.task_info_label_y)

        self.case_info_label_font = case_frame_layout["case_info_label_font"]
        self.case_info_label_fg = case_frame_layout["case_info_label_fg"]
        self.case_info_label_bg = case_frame_layout["case_info_label_bg"]
        self.case_info_label_x = case_frame_layout["case_info_label_x"]
        self.case_info_label_y = case_frame_layout["case_info_label_y"]
        self.case_info_label = Label(self.nav_frame, textvariable=self.case_info_label_val, font=self.case_info_label_font,
                                     fg=self.case_info_label_fg, bg=self.case_info_label_bg, justify=LEFT)
        self.case_info_label.place(x=self.case_info_label_x, y=self.case_info_label_y)


        self.platform_frame_bg = case_frame_layout["platform_frame_bg"]
        self.platform_frame_x = case_frame_layout["platform_frame_x"]
        self.platform_frame_y = case_frame_layout["platform_frame_y"]
        self.platform_frame = Frame(self.nav_frame, bg=self.platform_frame_bg)
        self.platform_frame.place(x=self.platform_frame_x, y=self.platform_frame_y)

        self.phone_info_frame_bg = case_frame_layout["phone_info_frame_bg"]
        self.phone_info_frame_x = case_frame_layout["phone_info_frame_x"]
        self.phone_info_frame_y = case_frame_layout["phone_info_frame_y"]
        self.phone_info_frame = Frame(self.nav_frame, bg=self.phone_info_frame_bg)
        self.phone_info_frame.place(x=self.phone_info_frame_x, y=self.phone_info_frame_y)

        self.platform_label_text = case_frame_layout["platform_label_text"]
        self.platform_label_font = case_frame_layout["platform_label_font"]
        self.platform_label_fg = case_frame_layout["platform_label_fg"]
        self.platform_label_bg = case_frame_layout["platform_label_bg"]
        self.platform_label = Label(self.platform_frame, text=self.platform_label_text, font=self.platform_label_font,
                                    fg=self.platform_label_fg, bg=self.platform_label_bg, justify=LEFT)
        self.platform_label.pack(side=LEFT)

        self.nav_phone_label_text = case_frame_layout["nav_phone_label_text"]
        self.nav_phone_label_font = case_frame_layout["nav_phone_label_font"]
        self.nav_phone_label_fg = case_frame_layout["nav_phone_label_fg"]
        self.nav_phone_label_bg = case_frame_layout["nav_phone_label_bg"]
        self.nav_phone_label = Label(self.phone_info_frame, text=self.nav_phone_label_text, font=self.nav_phone_label_font,
                                     fg=self.nav_phone_label_fg, bg=self.nav_phone_label_bg, justify=LEFT)
        self.nav_phone_label.pack(side=LEFT)

        self.phone_info_label_font = case_frame_layout["phone_info_label_font"]
        self.phone_info_label_fg = case_frame_layout["phone_info_label_fg"]
        self.phone_info_label_bg = case_frame_layout["phone_info_label_bg"]
        self.phone_info_label_padx = case_frame_layout["phone_info_label_padx"]
        self.phone_info_label = Label(self.phone_info_frame, textvariable=self.phone_info_label_val, font=self.phone_info_label_font,
                                      fg=self.phone_info_label_fg, bg=self.phone_info_label_bg, justify=LEFT)
        self.phone_info_label.pack(side=LEFT, padx=self.phone_info_label_padx)

        platforms = ['Android']
        self.platform_cbbox_width = case_frame_layout["platform_cbbox_width"]
        self.platform_cbbox_padx = case_frame_layout["platform_cbbox_padx"]
        self.platform_cbbox = ttk.Combobox(self.platform_frame, width=self.platform_cbbox_width)
        self.platform_cbbox['values'] = platforms
        self.platform_cbbox.current(0)
        self.platform_cbbox.pack(padx=self.platform_cbbox_padx)

        ttk.Style().configure('Nav.TButton', font=('微软雅黑', 10,'bold'), justify=CENTER)

        self.nav_back_btn_text = case_frame_layout["nav_back_btn_text"]
        self.nav_back_btn_width = case_frame_layout["nav_back_btn_width"]
        self.nav_back_btn_x = case_frame_layout["nav_back_btn_x"]
        self.nav_back_btn_y = case_frame_layout["nav_back_btn_y"]
        self.nav_back_btn = ttk.Button(self.nav_frame, width=self.nav_back_btn_width, text=self.nav_back_btn_text,
                                       style='Nav.TButton', command=self.parent.task_frame.show, cursor='hand2')
        self.nav_back_btn.place(x=self.nav_back_btn_x, y=self.nav_back_btn_y)

        self.open_dir_btn_text = case_frame_layout["open_dir_btn_text"]
        self.open_dir_btn_width = case_frame_layout["open_dir_btn_width"]
        self.open_dir_btn_x = case_frame_layout["open_dir_btn_x"]
        self.open_dir_btn_y = case_frame_layout["open_dir_btn_y"]
        self.open_dir_btn = ttk.Button(self.nav_frame, width=self.open_dir_btn_width, text=self.open_dir_btn_text,
                                       style='Nav.TButton', command=self.__open_dir, cursor='hand2')
        self.open_dir_btn.place(x=self.open_dir_btn_x, y=self.open_dir_btn_y)

        self.upload_list_btn_text = case_frame_layout["upload_list_btn_text"]
        self.upload_list_btn_x = case_frame_layout["upload_list_btn_x"]
        self.upload_list_btn_y = case_frame_layout["upload_list_btn_y"]
        self.upload_list_btn_width = case_frame_layout["upload_list_btn_width"]
        self.upload_list_btn = ttk.Button(self.nav_frame, text=self.upload_list_btn_text, style='Nav.TButton',
                                          command=self.__show_hide_upload_frame, cursor='hand2', width=self.upload_list_btn_width)
        self.upload_list_btn.place(x=self.upload_list_btn_x, y=self.upload_list_btn_y)

        self.mode_val = StringVar()
        self.mode_val.set('切至补录模式')
        self.mode_btn_x = case_frame_layout["mode_btn_x"]
        self.mode_btn_y = case_frame_layout["mode_btn_y"]
        self.mode_btn = ttk.Button(self.nav_frame, textvariable=self.mode_val, style='Nav.TButton',
                                          command=self.__switch_mode, cursor='hand2', state='normal')
        self.mode_btn.place(x=self.mode_btn_x, y=self.mode_btn_y)

        self.scroll_bar = Scrollbar(self.left_frame)
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.list_box_width = case_frame_layout["list_box_width"]
        self.list_box_hieght = case_frame_layout["list_box_height"]
        self.list_box_font = case_frame_layout["list_box_font"]
        self.list_box_fg = case_frame_layout["list_box_fg"]
        self.list_box_bg = case_frame_layout["list_box_bg"]
        self.list_box = Listbox(self.left_frame, width=self.list_box_width, height=self.list_box_hieght, font=self.list_box_font,
                                fg=self.list_box_fg, bg=self.list_box_bg, yscrollcommand=self.scroll_bar.set)
        self.bind_event(self.list_box, '<<ListboxSelect>>', self.__show_apps)
        self.list_box.pack(expand='yes', fill='both')
        self.scroll_bar.config(command=self.list_box.yview)


    def change_nav_color(self, color):
        self.nav_frame['bg'] = color
        self.phone_info_frame['bg'] = color
        self.platform_frame['bg'] = color
        self.case_info_label['bg'] = color
        self.task_info_label['bg'] = color
        self.case_info_label['bg'] = color
        self.nav_phone_label['bg'] = color
        self.platform_label['bg'] = color
        self.phone_info_label['bg'] = color


    def __switch_mode(self):
        if(self.mode=='Normal'):
            self.mode = 'Remake'
            self.change_nav_color('#EF3F3B')
            self.mode_val.set('切至正常模式')
            self.parent.title('用例窗口 v%s (补录模式)' %version)
        else:
            self.mode = 'Normal'
            self.change_nav_color('#222222')
            self.mode_val.set('切至补录模式')
            self.parent.title('用例窗口 v%s (正常模式)' %version)


    def bind_event(self, widget, event, func):
        widget.bind(event, func)

    def unbind_event(self, widget, event):
        widget.unbind(event)

    def __show_hide_upload_frame(self):
        if not self.upload_frame.is_shown:
            self.parent.width = self.parent.init_width + self.upload_frame.width
            self.parent.resize()
            self.upload_frame.show()


        else:
            self.parent.width = self.parent.init_width
            self.parent.resize()
            self.upload_frame.hide()


    def __update_case_list(self, cases):
        self.list_box.delete(0, self.list_box.size())

        for case in cases:
            self.list_box.insert(END, case[1])


    def __show_apps(self, event=None):
        cases = CasePresenter.cases
        if len(self.list_box.curselection()) > 0:
            case_id = cases[int(self.list_box.curselection()[0])][0]
            case_cn_name = cases[int(self.list_box.curselection()[0])][1]
            case_en_name = cases[int(self.list_box.curselection()[0])][11]
            self.case_info_label_val.set(u'用例:    %s' % (case_cn_name))
            self.app_frame.show(self.task_id, self.task_name, case_id, case_en_name)


    def hide(self):
        self.place_forget()
        self.app_frame.hide()
        self.upload_frame.hide()
        self.is_shown = False


    def __open_dir(self):
        path = os.path.join(data_dir, "uploaded_videos", "%s" %self.task_id)

        if not os.path.exists(path):
            os.makedirs(path)
        if "Darwin" in operate_system:
            os.system("open %s" %path)
        elif "Windows" in operate_system:
            os.system("explorer %s" %path)


    def __update_phone_info(self):
        while True:
            if not self.is_shown:
                break

            model = PhonePresenter.get_model()

            if '设备' in model:
                self.phone_info_label['fg'] = 'red'
            else:
                self.phone_info_label['fg'] = 'white'

            self.phone_info_label_val.set(model)

            time.sleep(1)


    def show(self, event=None):
        if self.mode=='Normal':
            self.parent.title('用例窗口 v%s (正常模式)' %version)
        else:
            self.parent.title('用例窗口 v%s (补录模式)' %version)
        self.parent.task_frame.place_forget()
        self.place(x=0, y=0, width=self.width, height=self.height)

        tasks = TaskPresenter.tasks
        self.task_id = tasks[int(self.parent.task_frame.list_box.curselection()[0])][0]
        self.task_name = tasks[int(self.parent.task_frame.list_box.curselection()[0])][1]
        cases = CasePresenter.get_cases(self.task_id)

        self.__update_case_list(cases)
        self.task_info_label_val.set('任务(ID:%s):    %s\n\n'%(self.task_id, self.task_name))
        self.case_info_label_val.set('')
        self.is_shown = True
        thread = threading.Thread(target=self.__update_phone_info)
        thread.setDaemon(True)
        thread.start()


    def disable_widgets(self,btn_click):
        self.unbind_event(self.list_box, '<<ListboxSelect>>')
        items = self.children.items()
        for item in items:
            if item[1] == self.app_frame:
                for child in item[1].children.items():
                    for app_btn in child[1].children.items():
                        if btn_click != app_btn[1]:
                            app_btn[1]['state'] = 'disabled'
                        else:
                            btn_click['style']='AppRecording.TButton'
            else:
                for child in item[1].children.items():
                    try:
                        child[1]['state'] = 'disabled'
                    except BaseException, e:
                        pass


    def enable_widgets(self, btn_click):
        self.bind_event(self.list_box, '<<ListboxSelect>>', self.__show_apps)
        items = self.children.items()
        btn_click['style'] = 'AppNormal.TButton'
        for item in items:
            if item[1] == self.app_frame:
                for child in item[1].children.items():
                    for app_widget in child[1].children.items():
                        app_widget[1]['state'] = 'normal'
            else:
                for child in item[1].children.items():
                    try:
                        child[1]['state'] = 'normal'
                    except BaseException, e:
                        pass


class TaskFrame(Frame):


    def __init__(self, parent):
        Frame.__init__(self, parent)
        task_frame_layout = layout[operate_system]["task_frame"]
        self.parent = parent
        self.width = self.parent.width
        self.height = self.parent.height
        self.header_frame_height = task_frame_layout["header_frame_height"]

        self.header_frame_bg = task_frame_layout["header_frame_bg"]
        self.header_frame_x = task_frame_layout["header_frame_x"]
        self.header_frame_y = task_frame_layout["header_frame_y"]
        self.header_frame = Frame(self, bg=self.header_frame_bg)
        self.header_frame.place(x=self.header_frame_x, y=self.header_frame_y, width=self.width,
                                height=self.header_frame_height)

        self.list_frame_x = task_frame_layout["list_frame_x"]
        self.list_frame = Frame(self)
        self.list_frame.place(x=self.list_frame_x, y=self.header_frame_height, width=self.width,
                              height=self.height - self.header_frame_height)

        self.task_id_label_text = task_frame_layout["task_id_label_text"]
        self.task_id_label_font =  task_frame_layout["task_id_label_font"]
        self.task_id_label_fg = task_frame_layout["task_id_label_fg"]
        self.task_id_label_bg = task_frame_layout["task_id_label_bg"]
        self.task_id_label = Label(self.header_frame, text=self.task_id_label_text,font=self.task_id_label_font,
                                   fg=self.task_id_label_fg, bg=self.task_id_label_bg, justify=LEFT)
        self.task_id_label.pack(side=LEFT)

        self.task_name_label_text = task_frame_layout["task_name_label_text"]
        self.task_name_label_font =  task_frame_layout["task_name_label_font"]
        self.task_name_label_fg = task_frame_layout["task_name_label_fg"]
        self.task_name_label_bg = task_frame_layout["task_name_label_bg"]
        self.task_name_label = Label(self.header_frame, text=self.task_name_label_text, font=self.task_name_label_font,
                                     fg=self.task_name_label_fg, bg=self.task_name_label_bg, justify=LEFT)
        self.task_name_label.pack(side=LEFT, padx=task_frame_layout["task_name_label_padx"])

        self.scroll_bar = Scrollbar(self.list_frame)
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.list_box_font = task_frame_layout["list_box_font"]
        self.list_box_bg = task_frame_layout["list_box_bg"]
        self.list_box_fg = task_frame_layout["list_box_fg"]
        self.list_box = Listbox(self.list_frame, yscrollcommand=self.scroll_bar.set, font=self.list_box_font,
                                bg=self.list_box_bg, fg=self.list_box_fg)
        self.list_box.pack(fill='both', expand='yes')
        self.scroll_bar.config(command=self.list_box.yview)

        self.__update_task_list()


    def bind_event(self, widget, event, func):
        widget.bind(event, func)


    def __update_task_list(self):
        tasks = TaskPresenter.get_tasks()

        for task in tasks:
            task_name = task[1]
            task_id = task[0]
            self.list_box.insert(END, '     %s     |     %s'%(task_id, task_name))


    def show(self):
        self.parent.title('任务窗口 v%s' %version)
        self.parent.case_frame.hide()
        self.parent.width = self.parent.init_width
        self.width = self.parent.width
        self.parent.resize()
        self.place(width=self.width, height=self.height)


class UploadFrame(Frame):


    def __init__(self,parent):
        Frame.__init__(self)

        upload_frame_layout = layout[operate_system]["upload_frame"]
        self.parent = parent
        self.is_shown = False
        self.width = upload_frame_layout["width"]
        self.height = self.parent.height

        self.nav_frame_height = upload_frame_layout["nav_frame_height"]
        self.nav_frame_bg = upload_frame_layout["nav_frame_bg"]
        self.nav_frame_x = upload_frame_layout["nav_frame_x"]
        self.nav_frame_y = upload_frame_layout["nav_frame_y"]
        self.nav_frame = Frame(self, bg=self.nav_frame_bg)
        self.nav_frame.place(x=self.nav_frame_x, y=self.nav_frame_y, width=self.width, height=self.nav_frame_height)

        self.list_frame_x = upload_frame_layout["list_frame_x"]
        self.list_frame = Frame(self)
        self.list_frame.place(x=self.list_frame_x, y=self.nav_frame_height, width=self.width,
                              height=self.height - self.nav_frame_height)

        self.title_text = upload_frame_layout["title_text"]
        self.title_font = upload_frame_layout["title_font"]
        self.title_fg = upload_frame_layout["title_fg"]
        self.title_bg = upload_frame_layout["title_bg"]
        self.title_ipadx = upload_frame_layout["title_ipadx"]
        self.title = Label(self.nav_frame, text=self.title_text, font=self.title_font, fg=self.title_fg,
                           bg=self.title_bg, justify=LEFT)
        self.title.pack(side=LEFT, ipadx=self.title_ipadx)

        self.scroll_bar = Scrollbar(self.list_frame)
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.list_box_font = upload_frame_layout["list_box_font"]
        self.list_box_bg = upload_frame_layout["list_box_bg"]
        self.list_box_fg = upload_frame_layout["list_box_fg"]
        self.list_box = Listbox(self.list_frame, yscrollcommand=self.scroll_bar.set, font=self.list_box_font,
                                bg=self.list_box_bg, fg=self.list_box_fg)
        self.list_box.pack(side=TOP, fill='both', expand='yes')
        self.list_box.bind('<Double-Button-1>', self.__open_file_dir)
        self.scroll_bar.config(command=self.list_box.yview)


    def __update_upload_list(self):
        try:
            while True:
                if not self.is_shown:
                    break
                if len(self.list_box.curselection()) > 0:
                    time.sleep(1)

                self.list_box.delete(0, self.list_box.size())
                self.items = UploadPresenter.get_items_to_be_uploaded()

                for item in self.items:
                    self.list_box.insert(END, os.path.basename(item))

                time.sleep(1)
        except BaseException,e:
            print e
            pass

    def __open_file_dir(self,event=None):
        if self.list_box.size() > 0:
            file = self.items[int(self.list_box.curselection()[0])]

            if os.path.exists(file):
                if "Darwin" in operate_system:
                    os.system("open %s" %os.path.dirname(file))
                elif "Windows" in operate_system:
                    os.system("explorer %s" %os.path.dirname(file))

    def show(self):
        self.is_shown = True
        self.place(width=self.width, height=self.height, x=self.parent.width, y=0)

        thread = threading.Thread(target=self.__update_upload_list)
        thread.setDaemon(True)
        thread.start()

    def hide(self):
        self.is_shown= False
        self.place_forget()


class MainWindow(Tk):

    def __init__(self):
        Tk.__init__(self)

        main_window_layout = layout[operate_system]["main_window"]

        self.init_width = main_window_layout["width"]
        self.init_height = main_window_layout["height"]
        self.width = self.init_width
        self.height = self.init_height
        self.x = main_window_layout["x"]
        self.y = main_window_layout["y"]

        self.geometry('%sx%s+%s+%s'%(self.width, self.height, self.x, self.y))
        self.resizable(main_window_layout["resizable"], main_window_layout["resizable"])

        self.task_frame = TaskFrame(self)
        self.case_frame = CaseFrame(self)

        self.task_frame.bind_event(self.task_frame.list_box, '<<ListboxSelect>>', self.case_frame.show)
        self.task_frame.show()


    def resize(self):
        self.geometry('%sx%s' % (self.width, self.height))


class RemakeDialog(Toplevel):


    def __init__(self):
        Toplevel.__init__(self)

        if 'Windows' in operate_system:
            self.wm_attributes('-topmost', 1)

        self.title('补录窗口 v%s' %version)

        remake_dialog_layout = layout[operate_system]["remake_dialog"]

        self.x = remake_dialog_layout["x"]
        self.y = remake_dialog_layout["y"]
        self.width = remake_dialog_layout["width"]
        self.height = remake_dialog_layout["height"]

        self.geometry('%sx%s+%s+%s' %(self.width, self.height, self.x, self.y))
        self.resizable(remake_dialog_layout["resizable"], remake_dialog_layout["resizable"])
        self.value = None

        self.main_frame_bg = remake_dialog_layout["main_frame_bg"]
        self.main_frame_height = remake_dialog_layout["main_frame_height"]
        self.main_frame = Frame(self, bg=self.main_frame_bg)
        self.main_frame.place(width=self.width, height=self.main_frame_height)

        self.label_text = remake_dialog_layout["label_text"]
        self.label_font = remake_dialog_layout["label_font"]
        self.label_fg = remake_dialog_layout["label_fg"]
        self.label_bg = remake_dialog_layout["label_bg"]
        self.label_x = remake_dialog_layout["label_x"]
        self.label_y = remake_dialog_layout["label_y"]
        self.label = Label(self.main_frame, text=self.label_text, font=self.label_font, fg=self.label_fg, bg=self.label_bg,
                           justify=LEFT)
        self.label.place(x=self.label_x, y=self.label_y)

        self.entry_fg = remake_dialog_layout["entry_fg"]
        self.entry_bg = remake_dialog_layout["entry_bg"]
        self.entry_x = remake_dialog_layout["entry_x"]
        self.entry_y = remake_dialog_layout["entry_y"]
        self.entry = Entry(self.main_frame, fg=self.entry_fg, bg=self.entry_bg)
        self.entry.place(x=self.entry_x, y=self.entry_y)

        self.confirm_btn_text = remake_dialog_layout["confirm_btn_text"]
        self.confirm_btn_font = remake_dialog_layout["confirm_btn_font"]
        self.confirm_btn_fg = remake_dialog_layout["confirm_btn_fg"]
        self.confirm_btn_x = remake_dialog_layout["confirm_btn_x"]
        self.confirm_btn_y = remake_dialog_layout["confirm_btn_y"]
        self.confirm_btn = Button(self, text=self.confirm_btn_text, font=self.confirm_btn_font, fg=self.confirm_btn_fg,
                                  command=self.confirm)
        self.confirm_btn.place(x=self.confirm_btn_x, y=self.confirm_btn_y)

        self.cancle_btn_text = remake_dialog_layout["cancle_btn_text"]
        self.cancle_btn_font = remake_dialog_layout["cancle_btn_font"]
        self.cancle_btn_fg = remake_dialog_layout["cancle_btn_fg"]
        self.cancle_btn_x = remake_dialog_layout["cancle_btn_x"]
        self.cancle_btn_y = remake_dialog_layout["cancle_btn_y"]
        self.cancle_btn = Button(self, text=self.cancle_btn_text, font=self.cancle_btn_font, fg=self.cancle_btn_fg,
                                 command=self.cancle)
        self.cancle_btn.place(x=self.cancle_btn_x, y=self.cancle_btn_y)


    def confirm(self):
        self.value = self.entry.get()

        try:
            if (int(self.value)<=0):
                tkMessageBox.showwarning('输入Order有误！', '请输入正确的Order值(order>0)')
                self.value = None
            else:
                self.value = int(self.value)
                self.destroy()
        except BaseException, e:
            tkMessageBox.showwarning('输入Order有误！', '请输入正确的Order值(order>0)')
            self.value = None


    def cancle(self):
        self.value = None
        self.destroy()



if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')

    version = VersionPresenter.get_version()
    if version is None:
        version = '[NULL]'
        VersionPresenter.set_version('[NULL]')

    UploadTool(Upload.get_items_to_be_uploaded, Upload.upload, is_daemon=True).start()

    window = MainWindow()
    try:
        window.mainloop()
    except BaseException, e:
        exit(0)
