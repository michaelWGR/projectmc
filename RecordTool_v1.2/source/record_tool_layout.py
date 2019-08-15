# -*- coding:utf-8 -*-

layout = {
#Mac操作系统的界面布局参数
    "Darwin":{
        "main_window": {
            "x": 325,
            "y": 100,
            "width": 755,
            "height": 480,
            "resizable": False
        },
        "task_frame": {
            "header_frame_height": 80,
            "header_frame_x": 0,
            "header_frame_y": 0,
            "header_frame_bg": "#222222",

            "task_name_label_padx": 25,

            "list_frame_x": 0,

            "task_id_label_text": "  任务ID:  |",
            "task_id_label_font": "微软雅黑 -15 bold",
            "task_id_label_fg": "white",
            "task_id_label_bg": "#222222",

            "task_name_label_text": "任务名称:",
            "task_name_label_font": "微软雅黑 -15 bold",
            "task_name_label_fg": "white",
            "task_name_label_bg": "#222222",

            "list_box_font": "微软雅黑 -15 bold",
            "list_box_bg": "#F5F5F5",
            "list_box_fg": "#337AB7"
        },
        "case_frame": {
            "nav_frame_height": 80,

            "list_frame_width": 350,

            "nav_frame_bg": "#222222",
            "nav_frame_x": 0,
            "nav_frame_y": 0,

            "left_frame_bg": "#DEDEDE",
            "left_frame_x": 0,

            "task_info_label_font": "微软雅黑 -12 bold",
            "task_info_label_fg": "white",
            "task_info_label_bg": "#222222",
            "task_info_label_x": 0,
            "task_info_label_y": 10,

            "case_info_label_font": "微软雅黑 -12 bold",
            "case_info_label_fg": "white",
            "case_info_label_bg": "#222222",
            "case_info_label_x": 0,
            "case_info_label_y": 45,

            "platform_frame_bg": "#222222",
            "platform_frame_x": 380,
            "platform_frame_y": 10,

            "phone_info_frame_bg": "#222222",
            "phone_info_frame_x": 380,
            "phone_info_frame_y":43,

            "platform_label_text": "平台:",
            "platform_label_font": "微软雅黑 -12 bold",
            "platform_label_fg": "white",
            "platform_label_bg": "#222222",
            
            "nav_phone_label_text": "机型:",
            "nav_phone_label_font": "微软雅黑 -12 bold",
            "nav_phone_label_fg": "white",
            "nav_phone_label_bg": "#222222",

            "phone_info_label_font": "微软雅黑 -12 bold",
            "phone_info_label_fg": "white",
            "phone_info_label_bg": "#222222",
            "phone_info_label_padx": 20,

            "platform_cbbox_width": 7,
            "platform_cbbox_padx": 20,

            "nav_back_btn_text": "<--返回任务列表",
            "nav_back_btn_width": 12,
            "nav_back_btn_x": 635,
            "nav_back_btn_y": 8,

            "open_dir_btn_text": "打开已上传文件目录",
            "open_dir_btn_width": 12,
            "open_dir_btn_x": 635,
            "open_dir_btn_y": 40,

            "upload_list_btn_text": "上传列表",
            "upload_list_btn_width":6,
            "upload_list_btn_x": 558,
            "upload_list_btn_y": 40,

            "mode_btn_x": 539,
            "mode_btn_y": 8,

            "list_box_width": 60,
            "list_box_height": 28,
            "list_box_font": "微软雅黑 -12 bold",
            "list_box_fg": "#337AB7",
            "list_box_bg": "#F5F5F5"
        },
        "app_frame":{
            "bg": "#DEDEDE",
            "app_btn_width": 10,
            "order_label_width": 3,

            "app_button_frame_padx": 6,
            "app_button_frame_pady": 15,
            "app_button_label_font": "微软雅黑 -9 bold",
            "app_button_label_bg": "#F0AD4E",
            "app_button_label_fg": "white"
        },
        "upload_frame":{
            "width": 200,

            "nav_frame_height": 25,
            "nav_frame_bg": "#222222",
            "nav_frame_x": 0,
            "nav_frame_y": 0,

            "list_frame_x": 0,

            "title_text": "待上传文件列表",
            "title_font": "微软雅黑 -12 bold",
            "title_fg": "white",
            "title_bg": "#222222",
            "title_ipadx": 40,

            "list_box_font": "微软雅黑 -12 bold",
            "list_box_bg": "#DEDEDE",
            "list_box_fg": "#337AB7"
        },
        "remake_dialog":{
            "x": 600,
            "y": 200,
            "width": 280,
            "height": 130,
            "resizable": False,

            "main_frame_bg": "#222222",
            "main_frame_height": 100,

            "label_text": "现处于补录模式！\n\n请输入补录视频的order：",
            "label_font": "微软雅黑 -15 bold",
            "label_fg": "white",
            "label_bg": "#222222",
            "label_x": 10,
            "label_y": 0,

            "entry_fg": "white",
            "entry_bg": "#222222",
            "entry_x": 10,
            "entry_y": 65,

            "confirm_btn_text": "确认",
            "confirm_btn_font": "微软雅黑 -12 bold",
            "confirm_btn_fg": "white",
            "confirm_btn_x": 10,
            "confirm_btn_y": 100,

            "cancle_btn_text": "取消",
            "cancle_btn_font": "微软雅黑 -12 bold",
            "cancle_btn_fg": "white",
            "cancle_btn_x": 70,
            "cancle_btn_y": 100
        }
    },


#Windows操作系统的界面布局参数
    "Windows":{
        "main_window": {
            "x": 550,
            "y": 200,
            "width": 755,
            "height": 480,
            "resizable": False
        },
        "task_frame": {
            "header_frame_height": 80,
            "header_frame_x": 0,
            "header_frame_y": 0,
            "header_frame_bg": "#222222",

            "task_name_label_padx": 25,

            "list_frame_x": 0,

            "task_id_label_text": "  任务ID:  |",
            "task_id_label_font": "微软雅黑 -15 bold",
            "task_id_label_fg": "white",
            "task_id_label_bg": "#222222",

            "task_name_label_text": "任务名称:",
            "task_name_label_font": "微软雅黑 -15 bold",
            "task_name_label_fg": "white",
            "task_name_label_bg": "#222222",

            "list_box_font": "微软雅黑 -15 bold",
            "list_box_bg": "#F5F5F5",
            "list_box_fg": "#337AB7"
        },
        "case_frame": {
            "nav_frame_height": 80,

            "list_frame_width": 350,

            "nav_frame_bg": "#222222",
            "nav_frame_x": 0,
            "nav_frame_y": 0,

            "left_frame_bg": "#DEDEDE",
            "left_frame_x": 0,

            "task_info_label_font": "微软雅黑 -12 bold",
            "task_info_label_fg": "white",
            "task_info_label_bg": "#222222",
            "task_info_label_x": 0,
            "task_info_label_y": 10,

            "case_info_label_font": "微软雅黑 -12 bold",
            "case_info_label_fg": "white",
            "case_info_label_bg": "#222222",
            "case_info_label_x": 0,
            "case_info_label_y": 45,

            "platform_frame_bg": "#222222",
            "platform_frame_x": 380,
            "platform_frame_y": 10,

            "phone_info_frame_bg": "#222222",
            "phone_info_frame_x": 380,
            "phone_info_frame_y":43,

            "platform_label_text": "平台:",
            "platform_label_font": "微软雅黑 -12 bold",
            "platform_label_fg": "white",
            "platform_label_bg": "#222222",

            "nav_phone_label_text": "机型:",
            "nav_phone_label_font": "微软雅黑 -12 bold",
            "nav_phone_label_fg": "white",
            "nav_phone_label_bg": "#222222",

            "phone_info_label_font": "微软雅黑 -12 bold",
            "phone_info_label_fg": "white",
            "phone_info_label_bg": "#222222",
            "phone_info_label_padx": 20,

            "platform_cbbox_width": 7,
            "platform_cbbox_padx": 20,

            "nav_back_btn_text": "<--返回任务列表",
            "nav_back_btn_width": 15,
            "nav_back_btn_x": 622,
            "nav_back_btn_y": 8,

            "open_dir_btn_text": "打开已上传文件目录",
            "open_dir_btn_width": 15,
            "open_dir_btn_x": 622,
            "open_dir_btn_y": 40,

            "upload_list_btn_text": "上传列表",
            "upload_list_btn_x": 545,
            "upload_list_btn_y": 40,
            "upload_list_btn_width": 8,

            "mode_btn_x": 521,
            "mode_btn_y": 8,

            "list_box_width": 60,
            "list_box_height": 28,
            "list_box_font": "微软雅黑 -12 bold",
            "list_box_fg": "#337AB7",
            "list_box_bg": "#F5F5F5"
        },
        "app_frame":{
            "bg": "#DEDEDE",
            "app_btn_width": 10,
            "order_label_width": 3,

            "app_button_frame_padx": 16,
            "app_button_frame_pady": 15,
            "app_button_label_font": "微软雅黑 -9 bold",
            "app_button_label_bg": "#F0AD4E",
            "app_button_label_fg": "white"
        },
        "upload_frame":{
            "width": 200,

            "nav_frame_height": 25,
            "nav_frame_bg": "#222222",
            "nav_frame_x": 0,
            "nav_frame_y": 0,

            "list_frame_x": 0,

            "title_text": "待上传文件列表",
            "title_font": "微软雅黑 -12 bold",
            "title_fg": "white",
            "title_bg": "#222222",
            "title_ipadx": 40,

            "list_box_font": "微软雅黑 -12 bold",
            "list_box_bg": "#DEDEDE",
            "list_box_fg": "#337AB7"
        },
        "remake_dialog":{
            "x": 820,
            "y": 285,
            "width": 280,
            "height": 130,
            "resizable": False,

            "main_frame_bg": "#222222",
            "main_frame_height": 100,

            "label_text": "现处于补录模式！\n\n请输入补录视频的order：",
            "label_font": "微软雅黑 -15 bold",
            "label_fg": "white",
            "label_bg": "#222222",
            "label_x": 10,
            "label_y": 0,

            "entry_fg": "white",
            "entry_bg": "#222222",
            "entry_x": 10,
            "entry_y": 65,

            "confirm_btn_text": "确认",
            "confirm_btn_font": "微软雅黑 -12 bold",
            "confirm_btn_fg": "black",
            "confirm_btn_x": 10,
            "confirm_btn_y": 100,

            "cancle_btn_text": "取消",
            "cancle_btn_font": "微软雅黑 -12 bold",
            "cancle_btn_fg": "black",
            "cancle_btn_x": 70,
            "cancle_btn_y": 100
        }
    }
}
