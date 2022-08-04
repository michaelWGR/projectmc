package com.meelive.ingkee.mechanism.network;

/**
 * {
 *     "App": "https://servicelp.xinjuhn.com",
 *     "H5": "https://h5lp.xinjuhn.com",
 *     "ImageScale": "https://imagescale.xinjuhn.com",
 *     "Img2ik": "http://img.xinjuhn.com",
 *     "M4aik": "http://m4a.xinjuhn.com",
 *     "MaiDian": "http://maidian.xinjuhn.com",
 *     "Main": "https://zzaw.xinjuhn.com/",
 *     "Pay": "https://paylp.xinjuhn.com",
 *     "Serviceik": "https://servicelp.xinjuhn.com",
 *     "Serviceinfoik": "https://servicelp.xinjuhn.com",
 *     "TestApp": "https://testservicelp.xinjuhn.com",
 *     "TestH5": "https://testh5lp.xinjuhn.com",
 *     "TestPay": "https://testservicelp.xinjuhn.com",
 *     "Upload": "http://upload.xinjuhn.com",
 *     "Uploadlog": "http://uploadlog.xinjuhn.com",
 *     "Vocik": "http://vocik.xinjuhn.com"
 * }
 */
public class HttpHost {

    // -----------------------------------
    // App
    // -----------------------------------
    /**
     * 进房特效资源
     */
    public static final String COMMON_RESOURCE = "App/api/resource/common";

    /**
     * 座驾特效资源
     */
    public static final String COMMON_RESOURCE_VEHICLE = "App/api/vehicle/res";

    public static final String USER_LIVING = "App/api/user/living";

    public static final String USER_SEARCH = "App/api/user/search";//1002,

    public static final String ROOM_SEARCH = "App/api/room/search";//1002,

    public static final String USER_INFO = "App/api/user/info";//1003,

    public static final String USER_RELATION_FOLLOW = "App/api/user/relation/follow";//1004,

    public static final String USER_RELATION_UNFOLLOW = "App/api/user/relation/unfollow";//1005,

    public static final String USER_RELATION_FOLLOWINGS = "App/api/user/relation/followings";//1007,

    public static final String USER_RELATION_RELATION = "App/api/user/relation/relation";//1008,

    public static final String USER_FANS = "App/api/user/relation/fans";//1010,

    public static final String USER_RELATION_NUMRELATIONS = "App/api/user/relation/numrelations";//1011,

    public static final String LIVE_INFO = "App/api/live/info";//2001,

    public static final String LIVE_UPDATE_INFO = "App/api/live/update";//2002,

    public static final String LIVE_REPORT = "App/api/live/report";//2006,

    public static final String LIVE_USERS = "App/api/live/users";//2007,

    public static final String USER_UPDATE_INFO = "App/api/user/update_info";//1013,

    public static final String USER_NOTIFY_BLOCK = "App/notify/block";//1015,

    public static final String USER_NOTIFY_RECENT = "App/api/notify/recent";//1017,

    public static final String USER_NOTIFY_SWITCH = "App/notify/switch";//1018,

    public static final String USER_NOTIFY_STAT = "App/notify/stat";//1019

    public static final String USER_RELATION_MUTUAL = "App/api/user/relation/mutual";//1009,

    public static final String LIVE_SHARE_TIPS = "App/api/live/share_tips";

    public static final String GIFT_INFO = "App/api/base_giftwall/gift_wall";//7001,

    public static final String GIFT_RESOURCE = "App/api/resource/gift";//7002,

    public static final String RANK_RESOURCE = "App/api/resource/rank";//7003,

    public static final String USER_STATISTIC_INFO = "App/api/statistic/info";//1020,

    public static final String USER_RANK = "App/api/statistic/rank";//1021,

    public static final String USER_STATIATIC_CONTRIBUTION = "App/api/statistic/contribution";//1022,

    public static final String USER_STATISTIC_INOUT = "App/api/statistic/inout";//1023,

    public static final String ACCOMPAYN_SEARCH = "App/api/accompany/search";//5002,

    public static final String USER_UPDATE_PROFILE = "App/api/user/update_profile";//1024,

    public static final String MESSAGE_SEND_GIFT = "App/api/message/send_gift";//8063,


    public static final String VERIFIED_RESOURCE = "App/api/resource/verified";//7004,

    public static final String LIVE_INFOS = "App/api/live/infos";//2024,

    public static final String USER_BLACKSTAT = "App/api/user/blackstat";//1028,

    public static final String USER_BLACKLIST = "App/api/user/blacklist";//1027,

    public static final String USER_DELBLACK = "App/api/user/delblack";//1026,

    public static final String USER_BLACK = "App/api/user/black";//1025,

    public static final String USER_PHONE_LOGIN = "App/user/account/phone_login";//9005,

    public static final String USER_PHONE_CODE = "App/user/account/phone_code";//9006,

    public static final String MANAGER_ADD = "App/api/user/manager/add";//100001,

    public static final String SUPER_MANAGER_ADD = "App/api/user/super_manager/add";

    public static final String MANAGER_DEL = "App/api/user/manager/del";//100002,

    public static final String SUPER_MANAGER_DEL = "App/api/user/super_manager/del";

    public static final String MANAGER_LIST = "App/api/user/manager/list";//100002,

    public static final String SUPER_MANAGER_LIST = "App/api/user/super_manager/list";

    public static final String USER_PHONE_BIND = "App/user/account/phone_bind";//9006,

    public static final String USER_ACCOUNT_SECRET = "App/user/account/logins";//100007,

    public static final String QQ_LOGIN = "/user/account/logins";

    public static final String LIVE_LINK_KEEP = "App/api/live/link_keep";//2031,

    public static final String RECIVE_STAT = "App/api/recive/stat";//100020,

    public static final String RECIVE_SWITCH = "App/api/recive/statSwitch";//100021,

    public static final String LOG_NETWORK_CHECK = "App/api/daily/keepalive";//11005,

    public static final String LIVE_CITY_SEARCH = "App/api/live/citysearch";//110007,

    public static final String THEME_SEARCH = "App/api/live/themesearch";//110015,

    public static final String USER_ACCOUNT_TOKEN_V2 = "App/user/account/token_v2";//110011,

    public static final String SERVICEINFO_LAYOUT = "App/serviceinfo/layout";//7,

    public static final String USER_STATIATIC_HIDE = "App/api/statistic/hide";//110032,

    public static final String USER_ACCOUNT_CODE = "App/api/user/account/code_login"; //120044

    public static final String WE_CHAT_LOGIN = "/api/user/account/code_login";

    public static final String USER_FEED_NOTIFY = "App/api/v2/feed/notify";
    public static final String USER_FEED_NOTIFY_REPORT = "App/api/v2/feed/notify/report";
    public static final String BILL_BOARD_CARD = "App/api/bill_board/card";

    public static final String LIVE_REPORT_REASON = "App/api/report/reason";//举报理由

    public static final String USER_GIFTS_WALL = "App/api/resource/user_gifts";

    public static final String LIVE_UPLOAD_MUSIC = "App/api/live/upload_music";//上传伴奏音乐的选择、删除

    public static final String LIVE_GIFT_ICON = "App/api/resource/gift_icon"; // 礼物角标资源

    public static final String LIVER_RIGHTS_INFOS = "App/api/liver_growth/rights_infos"; // 粉丝分析列表入口t

    public static final String LIVE_HOST_LABEL = "App/api/live/hostlabel"; //获取是否髙颜值主播

    public static final String LIVE_ADDR_ALTERNATIVE = "App/api/addr/alternative"; //​ 获取视频播放地址,SDK在推拉流不理想的情况下或收到上层推送时调用此接口
    /**
     * json协议埋点上传
     */
    public static final String CLIENT_LOG_UPLOAD = "MaiDian/log/upload";

    public static final String USER_ACCOUNT_UNLOCK = "App/user/account/unlock";//用户自助解除拉黑


    public static final String PUBLIC_LIVE_LIVE_LIST = "App/api/public_live/live_list";

    public static final String CHARGE_GIFT_WALL_PAGE = "App/api/charge_support/gift_wall_charge_page/show"; // 礼物墙充值页

    public static final String CHANGE_LIVE = "App/api/live/change"; // 搜索页面推荐接口

    public static final String ROOM_RANK_LIST = "App/api/room/rank_list"; // 电台观众的的贡献榜

    public static final String ROOM_SCORE_LIST = "App/api/room/score_list"; // 电台连麦用户的的真爱值
    // 六人连麦相关
    public static final String LIVE_LINK_LIST = "App/api/live/link_list";
    public static final String ROOM_ANNOUNCEMENT = "App/api/live/room/announcement";// 获取房间公告
    //新私信接口
    public static final String MESSAGE_V2_LIST = "App/api/v2/message/list";
    public static final String MESSAGE_V2_SEND = "App/api/v2/message/send";
    public static final String MESSAGE_V2_FETCH = "App/api/v2/message/fetch";
    public static final String MESSAGE_V2_RECEIVE_RANGE = "App/api/v2/message/receive_range";
    public static final String MESSAGE_V2_RECEIVE_REMIND = "App/api/v2/message/receive_remind";
    public static final String MESSAGE_V2_SESSION_DEl_LIST = "App/api/v2/message/session/del_list";
    public static final String MESSAGE_V2_SESSION_DEl = "App/api/v2/message/session/del";
    public static final String MESSAGE_V2_UNREAD_CLEAN = "App/api/v2/message/unread/clean";
    public static final String MESSAGE_V2_UNREAD_CLEAN_LIST = "App/api/v2/message/unread/clean_list";
    public static final String MESSAGE_V2_USER_CONFIG = "App/api/v2/message/user_config";
    public static final String MESSAGE_V2_DEL = "App/api/v2/message/del";
    public static final String MESSAGE_V2_READ = "App/api/v2/message/read";
    public static final String MESSAGE_V2_MERGE_DATA = "App/api/v2/message/merge_data";
    public static final String MESSAGE_V2_TOP = "App/api/v2/message/set_top";

    public static final String BILL_BOARD_HIDE = "App/api/bill_board/hide";
    public static final String SOCIAL_LINKE_USERS = "App/api/social/link/users";
    public static final String GET_PREMIT_LIST = "App/api/resdient/get/perlist";
    public static final String SOCIAL_INVITE_USERS = "App/api/social/invite/users";

    /**
     * 表情包
     */
    public static final String EMOJI_WALL = "App/api/social/expression/list";

    /**
     * 个人礼物榜单
     */
    public static final String GIFT_USER_STATISTIC = "App/api/gift/user_statistic";

    //新大厅
    public static final String HALL_HOMEPAGE_FETCH_V2 = "App/api/link/fetch_v2";

    //首页历史
    public static final String HALL_HOMEPAGE_PAST_VIEW = "App/api/link/past_view";

    //首页head 推荐
    public static final String HALL_HOMEPAGE_ROOM_ALL = "App/api/link/room_all";

    //首页head banner
    public static final String ACTIVITY_BANNER_LIST = "App/api/activity/banner_list";

    /**
     * 创建房间
     */
    public static final String LIVE_CREATE = "App/api/live/create";

    /**
     * 是否在谁的房间
     */
    public static final String CURRENT_LIVE = "App/api/current/live";

    /**
     * 是否已经开播
     */
    public static final String LIVE_USER_PUBLISH = "App/api/live/user_publish";

    /**
     * 禁言列表
     */
    public static final String FORBID_LIST = "App/api/resident/forbid/list";
    /**
     * 保存身份信息
     **/
    public static final String TAXES_CERT_USER_INFO_SAVE = "App/api/cert/taxes-save";
    /**
     * 查询身份信息
     */
    public static final String TAXES_CERT_USER_INFO_DETAIL = "App/api/cert/taxes-get-detail";

    /**
     * 分享识别
     */
    public static final String SHARE_RECOGNITION = "App/api/live/share/recognition";

    /**
     * 进房策略
     */
    public static final String HALL_HOMEPAGE_GET_RECOMMEND = "App/api/link/get_recommend";
    public static final String FIRST_LOGIN_ROOM_RECOMMEND = "/api/link/get_recommend";

    /**
     * 打泡泡进房api
     */
    public static final String BUBBLE_ENTER = "App/api/bubble/enter";

    /**
     * 打泡泡购买锤子api
     */
    public static final String BUBBLE_BUY = "App/api/bubble/buy";

    /**
     * 打泡泡api
     */
    public static final String BUBBLE_BEAT = "App/api/bubble/beat";

    /**
     * 打泡泡奖品记录api
     */
    public static final String BUBBLE_REWARD = "App/api/bubble/reward_list";

    /**
     * 打泡泡榜单api
     */
    public static final String BUBBLE_RANK = "App/api/bubble/rank_list";

    /**
     * 打泡泡开关设置api
     */
    public static final String BUBBLE_SWITCH = "App/user/base/switch";

    /**
     * 打泡泡设置api
     */
    public static final String BUBBLE_HAMMER = "App/api/bubble/info";

    /**
     * 背包墙
     */
    public static final String BUBBLE_BAG = "App/api/bubble/bag";

    /**
     * 指定礼物tab及数据
     */
    public static final String SPECIAL_GIFT_TAB = "App/api/live_gift_tap/valid";

    public static final String BAG_ITEM_EQUIP = "BAG_ITEM_EQUIP";

    public static final String LOG_CONFIG = "MaiDian/bigdata/auto_upload_event";

    // 家长锁密码验证
    public static final String KID_LOCK_CHECK = "App/api/user/kid_lock/check";

    // 获取房间抽成比例
    public static final String SOCIAL_OWNER_DEVIDE_RATE = "App/api/link/social/owner_divide_rate";

    /**
     * 用户相册api
     */
    public static final String PROFILE_ALBUM_ADD_PIC = "App/api/user/profile/add_pic"; // 上传
    public static final String PROFILE_ALBUM_UPDATE_PIC = "App/api/user/profile/update_pic"; // 修改
    public static final String PROFILE_ALBUM_DEL_PIC = "App/api/user/profile/del_pic"; // 删除
    public static final String PROFILE_ALBUM_GET_PICS = "App/api/user/profile/get_pics"; // 获取

    // 版本升级
    public static final String CHECK_VERSION = "App/api/public/check_version";

    // 捞日志
    public static final String LOG_REPORT = "App/api/log/report";

    // 首页头条广播
    public static final String HALL_HOMEPAGE_RADIO = "App/api/hall/radio";
    public static final String HALL_HOMEPAGE_RADIO_RULE = "App/api/hall/radio_rule";

    // 首页全服榜单入口
    public static final String APPRANKALLTOP3 = "App/api/all/app_rank_top3";

    /**
     * 手机一键登录
     */
    public static final String USER_ACCOUNT_SHANYAN_LOGIN = "App/user/account/shanyan_login";

    public static final String FAST_PHONE_LOGIN = "/user/account/shanyan_login";

    /**
     * 手机一键绑定
     */
    public static final String USER_ACCOUNT_SHANYAN_BIND = "App/user/account/shanyan_bind";

    /**
     * 是否绑定手机号
     */
    public static final String USER_PHONE_IS_BIND = "App/user/account/phone_is_bind";

    /**
     * 拉取小纸条文案
     */
    public static final String NOTES_TEXT_LIST = "App/api/homepage/get_letter_tag_text_list";

    /**
     * 发布小纸条
     */
    public static final String PUBLISH_NOTES = "App/api/homepage/publish_letter";

    /**
     * 更新房间模式
     */
    public static final String SWITCH_MODE = "App/api/live/switchmode";

    /**
     * 获取交友模式的文案
     */
    public static final String BDCOPY_WRITING = "App/api/live/bdcopywriting";

    /**
     * 进入发布告白获取数据
     */
    public static final String CONFESSION_ENTER = "App/api/confession/enter";

    /**
     * 发布告白
     */
    public static final String CONFESSION_PUBLISH = "App/api/confession/publish";

    /**
     * 积分兑换
     */
    public static final String EXCHANGE_SCORE = "App/api/point/point_exchange";

    /**
     * 获取我的幸运值
     */
    public static final String MY_LUCK_POINT = "App/api/bubble/luck_point";

    /**
     * 幸运值兑换锄头
     */
    public static final String LUCK_POINT_EXCHANGE = "App/api/bubble/exchange";

    /**
     * 拉取小纸条分类
     */
    public static final String NOTES_TAG_LIST = "App/api/homepage/get_letter_tag_list";

    /**
     * 个人勋章榜单
     */
    public static final String MEDAL_USER_STATISTIC = "App/api/user/info/verify_list_new";

    /**
     * 获取我的页兑换栏开关
     */
    public static final String SWITCH_POINT_GIFT_EXCHANGE = "App/api/point/gift_exchange";
    /**
     * 获取礼物墙积分开关
     */
    public static final String SWITCH_POINT_GIFT_WALL = "App/api/point/gift_wall";
    /**
     * 获取可兑换的资源列表
     */
    public static final String EXCHANGE_RESOURCES = "App/api/point/exchange_resources";
    /**
     * 可邀请成为cp的好友列表
     */
    public static final String FRIEND_LIST_FOR_CP = "App/api/pattern/list";
    /**
     * 信物列表
     */
    public static final String GIFT_LIST_FOR_CP = "App/api/pattern/gift_list";
    /**
     * 发送cp邀请
     */
    public static final String SEND_CP_GIFT = "App/api/pattern/invite";
    /**
     * 查看cp信息
     */
    public static final String CP_INFO = "App/api/pattern/infos";
    /**
     * 查看所有的cp列表
     */
    public static final String CP_ALL_LIST = "App/api/pattern/all_list";
    /**
     * 解散cp
     */
    public static final String CP_DISMISS = "App/api/pattern/cancel";
    /**
     * 用户关系 - 私信 - 接受or拒绝邀请
     */
    public static final String MESSAGE_RELATIONSHIP_INVITE = "App/api/pattern/decide";

    /**
     * 用户关系 - 房间 - 陪伴模式 - 陪伴值定时上报
     */
    public static final String AUDIO_ACCOMPANY_VALUE_REPORT = "App/api/pattern/report";

    /**
     * 用户关系 - 房间 - 陪伴模式 - 获取陪伴值规则说明
     */
    public static final String AUDIO_ACCOMPANY_DECLARE = "App/api/pattern/desc";

    public static final String VEHICLE_LIST = "App/api/vehicle/list";
    public static final String VEHICLE_SELECT = "App/api/vehicle/select";

    public static final String GET_WELCOME_ENTER_ROOM_TEXT = "App/api/welcome/list";
    public static final String ADD_WELCOME_ENTER_ROOM_TEXT = "App/api/welcome/add";
    public static final String UPDATE_WELCOME_ENTER_ROOM_TEXT = "App/api/welcome/update";
    public static final String DELETE_WELCOME_ENTER_ROOM_TEXT = "App/api/welcome/del";

    // 表情墙入口可见状态
    public static final String SOCIAL_EXPRESSION_STATUS = "App/api/social/expression/status";

    /**
     * 首页换肤
     */
    public static final String GET_SKIN = "App/api/homepage/get_skin";
    /**
     * 编辑陪伴名称
     */
    public static final String EDIT_COMPANY_NAME = "App/api/pattern/invite_nick";
    /**
     * 陪伴名称敏感词校验
     */
    public static final String VERIFY_COMPANY_NAME = "App/api/pattern/check_rubbish_word";
    /**
     * 首页拉取互动tab的列表
     */
    public static final String GET_RECOMMEND_PERSONAL_ROOMS = "App/api/homepage/get_recommend_personal_room";

    // ------------- 用户贵族 ------------
    public static final String GET_USER_VIP_CONFIG = "App/api/user/vip/config";
    public static final String GET_USER_VIP_INFO = "App/api/user/vip/info";
    public static final String GET_USER_VIP_PAY_INFO = "App/api/user/vip/buy_info";
    public static final String GET_USER_VIP_BUY = "App/api/user/vip/buy";

    public static final String LIVE_TIPS = "App/api/live/tips";

    public static final String LIVE_SERVICEINFO = "App/serviceinfo/info";

    public static final String PUSH_REGISTER = "App/api/push/register";

    public static final String ROOM_OPER_GETROOMPSW = "App/room_oper_buz/RoomOperBuzService/GetRoomPsw";

    public static final String ROOM_OPER_JUDGEROOMPSW = "App/room_oper_buz/RoomOperBuzService/JudgeRoomPsw";

    public static final String GET_BG_LIST = "App/api/live/bg_list";

    public static final String COLLECT_GET_STATE = "App/api/room/collect/get_user_collect_state";

    public static final String COLLECT_GET_MY_COLLECTS = "App/api/room/collect/get_my_collects";

    public static final String COLLECT_PUSH_USER_NOTICE = "App/api/room/collect/push_user_notice";

    public static final String COLLECT_UPDATE_STATE = "App/api/room/collect/update_collect_state";

    public static final String KID_LOCK_VERIFY = "App/api/user/kid_lock/verify";

    public static final String SUPER_CHECK = "App/api/super/check";

    public static final String COLLECT_GET_RESIDUE = "App/api/room/collect/get_collect_residue";

    public static final String LINK_NOTIFY_RESIDUE = "App/api/user/relation/link_notify_residue";

    public static final String LINK_NOTIFY_JOIN = "App/api/user/relation/link_notify_join";

    public static final String LINK_NOTIFY_SWITCH = "App/api/user/relation/link_notify_switch";

    public static final String LINK_NOTIFY_LIST = "App/api/user/relation/link_notify_list";

    public static final String APP_SWITCH_CONFIG = "App/api/appconfig/get_raw";

    public static final String HALL_HOMEPAGE_NOTES = "App/api/homepage/get_letter_list";

    // 勋章编辑页，获取勋章分类列表
    public final static String VERIFY_LIST_NEW = "App/api/user/info/verify_list_new";

    // 勋章编辑页，按坑位设置勋章
    public final static String VERIFY_OPERATION = "App/api/user/info/verify_oper";

    // 头像框编辑页，获取用户头像框列表
    public final static String GET_USER_HEAD_FRAME = "App/api/user/verify/get_user_headframe";

    // 头像框编辑页，设置用户头像框
    public final static String SELECT_HEAD_FRAME = "App/api/user/info/head_frame_select";

    // linked me
    public final static String LINKED_ME_REPORT = "App/api/linkme/report";

    // 萌新策略
    public static final String NEWCOMER_INFO = "App/api/user/fresh/info";
    public static final String NEWCOMER_LIST = "App/api/user/fresh/fetch";
    public static final String NEWCOMER_PICK = "App/api/user/fresh/pick";
    public static final String NEWCOMER_TEXT_FETCH = "App/api/user/fresh/pick_text_fetch";
    public static final String NEWCOMER_TEXT_ADD = "App/api/user/fresh/pick_text_add";
    public static final String NEWCOMER_TEXT_MODIFY = "App/api/user/fresh/pick_text_modify";
    public static final String NEWCOMER_TEXT_DELETE = "App/api/user/fresh/pick_text_del";

    // 好友召回
    public static final String RECALL_USER_LIST = "App/api/user/recall/fetch_away_users";
    public static final String RECALL_USER = "App/api/user/recall/send";
    public static final String RECALL_USER_HISTORY_LIST = "App/api/user/recall/fetch_send_recall_history";
    public static final String RECALL_REWARD_INFO = "App/api/user/recall/fetch_recall_reward_info";
    public static final String RETURN_REWARD_INFO = "App/api/user/recall/fetch_return_reward_info";
    public static final String OBTAIN_RECALL = "App/api/user/recall/get_recall_reward";
    public static final String RECALL_RULE = "App/api/user/recall/get_rule";
    public static final String FETCH_RECALL_SUCCESS_USER = "App/api/user/recall/fetch_recall_success_users";

    // 敏感词
    public static final String CHECK_RUBBISH_WORD = "App/api/rubbish/client_check";

    // 用户榜单隐身开关
    public static final String SET_USER_RANK_HIDE_SWITCH = "App/api/user/vip/set_setup";
    public static final String GET_USER_RANK_HIDE_SWITCH = "App/api/user/vip/get_setup";

    // 收送陪伴礼物互相关注开关
    public static final String SET_USER_COMPANY_SWITCH = "App/api/pattern/set_setup";
    public static final String GET_USER_COMPANY_SWITCH = "App/api/pattern/get_setup";

    // 首页连麦互动
    public static final String GET_MATCH_PARTNER_DATA = "App/api/homepage/get_recommend_partner";

    // 用户专属礼物
    public static final String CHECK_EXCLUSIVE_GIFT = "App/api/gift/exclusive/undeliverable_gifts";
    // 3.4版本后专属礼物不再使用 CHECK_EXCLUSIVE_GIFT，改为使用GET_GIFT_TIP_CONFIG
    public static final String GET_GIFT_TIP_CONFIG = "App/api/gift/exclusive/special_gifts";

    // 技能卡
    public static final String GET_SKILL_CARD_CONFIG = "App/api/user/skill_card/get_official";
    public static final String GET_SKILL_CARD_USER = "App/api/user/skill_card/get_info";
    public static final String GET_ROOM_RECOMMEND_SKILL = "App/api/user/skill_card/chosen_partners";
    public static final String APPLY_SKILL_CARD = "App/api/user/skill_card/apply";
    public static final String POST_SKILL_CARD_ORDER_TOP = "App/api/user/skill_card/top";

    // 我的页 公会按钮开关
    public static final String SWITCH_MINE_HAVE_LIVE = "App/api/room/manage_situation/is_have_live";

    // 公会ID
    public static final String GET_USER_UNION_ID = "App/api/labor/person/get_bind_room_id";

    // 公聊气泡
    public static final String USER_CHAT_SKIN_LIST = "App/api/user/chat_skin/list";
    public static final String USER_CHAT_SKIN_SELECT = "App/api/user/chat_skin/select";

    // 动态个人主页
    public static final String GET_OFFICIAL_DYNAMIC_BG_LIST = "App/api/user/dynamic_homepage/official_resources";
    public static final String GET_MY_DYNAMIC_BG_LIST = "App/api/user/dynamic_homepage/list";
    public static final String POST_SELECT_MY_DYNAMIC_BG = "App/api/user/dynamic_homepage/select";
    public static final String GET_PERSONAL_DYNAMIC_BG = "App/api/user/dynamic_homepage/other";

    // 房间管理员标签
    public static final String GET_ROOM_ADMIN_TAGS = "App/api/room/role/pull_manager_tags";
    public static final String POST_ALTER_ROOM_ADMIN_TAGS = "App/api/room/role/alter_manager_tags";

    // 首充需求
    public static final String GET_USER_FIRST_CHARGE_REWARD = "App/api/user/first_pay/reward";
    public static final String GET_USER_FIRST_CHARGE_RULE = "App/api/user/first_pay/rule";
    public static final String GET_IS_FIRST_PAY = "App/api/user/first_pay/check";

    // 直播间PK
    public static final String GET_AUDIO_PK_CONFIG = "App/api/room/pk/config";
    public static final String GET_AUDIO_PK_DESCRIPTION = "App/api/room/pk/description";
    public static final String GET_AUDIO_PK_RANK_LIST = "App/api/room/pk/ranking";
    public static final String GET_AUDIO_PK_ADD_DURATION = "App/api/room/pk/add_duration";

    // 麦位离开状态
    public static final String GET_MIC_LEAVE_SWITCH = "/api/link/social/is_away";
    public static final String POST_MIC_LEAVE_SWITCH = "/api/link/social/set_away";

    // 红包雨
    public static final String GET_WELFARE_RAIN_CLICKABLE = "/api/room/welfare_rain/is_receive";
    public static final String POST_WELFARE_RAIN_RECEIVE = "/api/room/welfare_rain/receive";
    public static final String POST_WELFARE_RAIN_CLOSE = "/api/room/welfare_rain/close";

    // 房间贵宾用户
    public static final String POST_ROOM_VIP_SET_USER = "App/api/room/vip/set_user";
    public static final String POST_ROOM_VIP_REMOVE_USER = "App/api/room/vip/remove_user";

    public static final String GET_ROOM_VIP_CONFIG = "App/api/room/vip/fetch_config";
    public static final String GET_ROOM_VIP_FETCH_RULE = "App/api/room/vip/fetch_rule";
    public static final String GET_ROOM_VIP_FETCH_USERS = "App/api/room/vip/fetch_users";
    public static final String GET_ROOM_VIP_FETCH_PRIVILEGE = "App/api/room/vip/fetch_privilege";
    public static final String GET_ROOM_VIP_USER_INFO = "App/api/room/vip/get_user_info";

    public static final String GET_ROOM_VIP_SKIN_SWITCH = "App/api/room/vip/get_chat_skin_setup";
    public static final String POST_ROOM_VIP_SKIN_SWITCH = "App/api/room/vip/switch_chat_skin_setup";

    // 魅力等级
    public static final String CHARM_RANK_RESOURCE = "App/api/resource/rank_charm";

    // 房间误踢黑名单
    public static final String GET_ROOM_BLACK_KICK_LIST = "/api/room/kick/list";
    public static final String POST_REVOKE_ROOM_BLACK_KICK = "/api/room/kick/remove";
    public static final String GET_ROOM_BLACK_KICK_HISTORY = "/api/room/kick/history";
    public static final String GET_ROOM_FORBID_CHAT_LIST = "/api/room/forbid/list";
    public static final String GET_ROOM_FORBID_CHAT_HISTORY = "/api/room/forbid/history";


    // 免费货币签到
    public static final String GET_TASK_CENTER_IS_OPEN = "/api/busi/coin_task/is_open";
    public static final String GET_SIGN_IN_COIN_PAGE = "/api/busi/coin_task/sign_in_page";
    public static final String POST_COIN_TASK_SIGN_IN = "/api/busi/coin_task/sign_in";

    // 首页活动H5banner弹窗
    public static final String GET_CAMPAIGN_BANNER_LIST = "/api/hall/homepage/get_popup_list";

    // 房间许愿
    public static final String GET_ROOM_WISH_SWITCH = "/api/room/wish/check_permission";
    public static final String GET_ROOM_WISH_ENTER = "/api/room/wish/get_status";
    public static final String GET_ROOM_WISH_COMPLETE = "/api/room/wish/get_complete_setup";
    public static final String GET_GIFT_WISH_EDIT_SETUP = "/api/room/wish/get_setup";
    public static final String POST_GIFT_WISH_EDIT_SETUP = "/api/room/wish/setup";
    public static final String POST_GIFT_WISH_PUBLISH = "/api/room/wish/publish";
    public static final String POST_GIFT_WISH_OVER = "/api/room/wish/close";

    // 互动才艺
    public static final String POST_ACTIVE_INTERACT_TALENT = "/api/user/place_order/active_interaction";
    public static final String POST_PAY_INTERACT_TALENT = "/api/user/place_order/on_demand";
    public static final String GET_ACTIVE_INTERACT_TALENT = "/api/user/place_order/query_active_interaction";
    public static final String GET_CONFIG_INTERACT_TALENT = "/api/user/place_order/query_all_interaction";

    // -----------------------------------
    // ImageScale
    // -----------------------------------

    public static final String IMAGE_SCALE = "ImageScale/imageproxy2/dimgm/scaleImage?url=";


    // -----------------------------------
    // ImageUpload
    // -----------------------------------

    public static final String IMAGE_UPLOAD = "Upload/upload/image?";


    // -----------------------------------
    // Uploadlog
    // -----------------------------------

    public static final String UPLOAD_TOKEN = "Uploadlog/api/upload/token";

    // -----------------------------------
    // Img2ik
    // -----------------------------------

    public static final String IMAGE = "Img2ik/";//1005,

    // -----------------------------------
    // Serviceik
    // -----------------------------------

    public static final String APPCONFIG_GET_RAW = "Serviceik/api/appconfig/get_raw";//1011,

    public static final String LIVE_GET_MUSIC = "Serviceik/api/live/get_music";//获取伴奏音乐

    public static final String LINK_TIME_GETCONFIG = "Serviceik/time/getconfig";

    // -----------------------------------
    // Pay
    // -----------------------------------

    public static final String PAYMENT_INFO = "Pay/api/payment/info";//8000,

    public static final String PAYMENT_CREATE = "Pay/api/payment/create";//8001,

    public static final String PAYMENT_STATUS_NOTIFY = "Pay/api/payment/statusNotify";//8007,

    // -----------------------------------
    // HostKey
    // -----------------------------------
    /**
     * APP域名
     */
    public static final String App_HOST = "App";
    /**
     * H5域名
     */
    public static final String H5_HOST = "H5";

    /**
     * zego域名
     */
    public static final String ZEGO = "ZegoAudioDomain";
}
